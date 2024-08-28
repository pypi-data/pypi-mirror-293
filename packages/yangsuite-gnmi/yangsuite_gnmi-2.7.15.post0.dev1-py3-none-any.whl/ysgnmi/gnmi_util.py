import logging
import base64
import json
import re
import os
import traceback
import time
from xml.etree.ElementPath import xpath_tokenizer_re
from pprint import pformat
from google.protobuf import json_format
from six import string_types
from yang.connector import proto
from ysgnmi.device_plugin import GnmiNotification

log = logging.getLogger(__name__)


# Pattern to detect keys in an xpath
RE_FIND_KEYS = re.compile(r'\[.*?\]')


class GnmiMessageException(Exception):
    pass


class LeafListVal:
    """Class to set a leaf list value"""
    def __init__(self, val):
        self.llvalue = val

    @property
    def llvalue(self):
        return self._llvalue

    @llvalue.setter
    def llvalue(self, val):
        self._llvalue = val


class GnmiMessage:
    """Class to prepare and return gMNI messages"""

    def __init__(self, message_type, cfg):
        self.msg_type = message_type
        self.cfg = cfg

    @classmethod
    def run_set(self, device, payload, **kwargs):
        """Run gNMI set service.

        Args:
          device (ysgnmi.device_plugin.GnmiSession): Target device.
          user (str): YANG Suite username.
          payload (proto.gnmi_pb2.SetRequest): SetRequest.
          payload (str): JSON representing a SetRequest.
        """
        if isinstance(payload, proto.gnmi_pb2.SetRequest):
            gnmi_string = str(payload)
        else:
            try:
                payload = GnmiMessageConstructor.json_to_gnmi('set', payload)
                gnmi_string = str(payload)
            except Exception:
                log.error(traceback.format_exc())
                raise GnmiMessageException("Invalid payload\n{0}".format(
                    str(payload))
                )

        device.log.info('gNMI SET\n' + '=' * 8 + '\n{0}'.format(
            gnmi_string
        ))
        try:
            response = device.set(payload)
            device.log.info(
                'gNMI SET Response\n' + '=' * 17 + '\n{0}'.format(
                    str(response)
                )
            )
        except Exception as exc:
            log.error(traceback.format_exc())
            if hasattr(exc, 'details'):
                device.log.error('ERROR: {0}'.format(exc.details()))
            else:
                device.log.error(str(exc))

    @classmethod
    def run_get(self, device, payload):
        """Run gNMI get service.

        Args:
          device (ysgnmi.device_plugin.GnmiSession): Target device.
          user (str): YANG Suite username.
          payload (proto.gnmi_pb2.SetRequest): SetRequest.
          payload (str): JSON representing a SetRequest.
        """
        if isinstance(payload, proto.gnmi_pb2.GetRequest):
            gnmi_string = str(payload)
        else:
            try:
                payload = GnmiMessageConstructor.json_to_gnmi('get', payload)
                gnmi_string = str(payload)
            except Exception:
                log.error(traceback.format_exc())
                raise GnmiMessageException("Invalid payload\n{0}".format(
                    str(payload)
                ))

        device.log.info('gNMI GET\n' + '=' * 8 + '\n{0}'.format(
            gnmi_string
        ))
        try:
            response = device.get(payload)
            device.log.info(
                'gNMI GET Response\n' + '=' * 17 + '\n{0}'.format(
                    str(response)
                )
            )
            # Decoder works for JSON or base64 encoded JSON.
            json_dicts, opfields = self.decode_notification(response, {})
            log_json = False
            if json_dicts:
                for json_dict in json_dicts:
                    if len(str(json_dict)):
                        log_json = True
                        msg = 'JSON Decoded\n' + '=' * 12 + '\n' + json.dumps(
                            json_dict, indent=2
                        )
                        device.log.info(msg)
            if not log_json and opfields:
                # Only print opfields if encoding is PROTO
                msg = 'Xpath/Value\n' + '=' * 11 + '\n' + pformat(opfields)
                device.log.info(msg)

        except Exception as exc:
            log.error(traceback.format_exc())
            if hasattr(exc, 'details'):
                device.log.error('ERROR: {0}'.format(exc.details()))
            else:
                device.log.error(str(exc))

    @staticmethod
    def path_elem_to_xpath(path_elem, prefix='', namespace={}, opfields=[]):
        """Convert a Path structure to an Xpath."""
        elems = path_elem.get('elem', [])
        xpath = []
        for elem in elems:
            name = elem.get('name', '')
            if name:
                for mod in namespace.values():
                    name = name.replace(mod + ':', '')
                xpath.append(name)
            key = elem.get('key', '')
            if key:
                for name, value in key.items():
                    for mod in namespace.values():
                        value = str(value).replace(mod + ':', '')
                    opfields.append({
                        "datatype": 'key',
                        "value": value,
                        'xpath': prefix + '/' + '/'.join(xpath) + '/' + name
                    })
        return prefix + '/' + '/'.join(xpath)

    @staticmethod
    def decode_update(update, prefix=None, namespace={}, opfields=[]):
        """Convert Update to Xpath, value, and datatype."""
        pre_path = ''
        xpath = ''
        json_dict = {}

        if not isinstance(update, list):
            update = [update]

        if prefix is not None:
            pre_path = GnmiMessage.path_elem_to_xpath(
                prefix, pre_path, namespace, []
            )

        for upd in update:
            if 'path' in upd:
                xpath = GnmiMessage.path_elem_to_xpath(
                    upd['path'], pre_path, namespace, opfields
                )
            val = upd.get('val', {})
            if 'jsonIetfVal' in val:
                val = val.get('jsonIetfVal', '')
                if not val:
                    log.info('"val" has no content')
                    continue
                json_val = base64.b64decode(val).decode('utf-8')
                json_dict = json.loads(json_val, strict=False)
            elif 'jsonVal' in val:
                val = val.get('jsonVal', '')
                if not val:
                    log.info('"val" has no content')
                    continue
                json_val = base64.b64decode(val).decode('utf-8')
                json_dict = json.loads(json_val, strict=False)
            elif 'asciiVal' in val:
                val = val.get('asciiVal', '')
                if not val:
                    log.info('"asciiVal" has no content')
                    continue
                val = val.strip()
                opfields.append({
                    'datatype': 'ascii',
                    'value': val,
                })
            elif val:
                datatype = next(iter(val))
                value = val[datatype]
                if 'int' in datatype:
                    value = int(value)
                elif ('float' in datatype or
                      'decimal' in datatype or
                      'double' in datatype):
                    value = float(value)
                elif 'bytes' in datatype:
                    value = bytes(value)

                opfields.append({
                    'datatype': datatype.replace('Val', ''),
                    'value': value,
                    'xpath': xpath
                })
            else:
                log.info('Update has no value')

        return json_dict

    @staticmethod
    def decode_notification(response, namespace={}):
        """Convert JSON return to python dict for display or processing.

        Args:
          update (dict): Could also be a gNMI response.
          namespace (dict): Can be used if verifier is implemented.

        Returns:
          str
        """
        # Try to cover different return formats.
        opfields = []
        json_dicts = []
        log.info('Decoding notification')
        if isinstance(response, proto.gnmi_pb2.SubscribeResponse):
            notification = json_format.MessageToDict(response)
            if 'update' not in notification:
                raise GnmiMessageException('No update in SubscribeResponse')
            update = notification['update']
            prefix = update.get('prefix')
            json_dicts.append(GnmiMessage.decode_update(
                update['update'], prefix, namespace, opfields
            ))
        elif isinstance(response, proto.gnmi_pb2.GetResponse):
            get_resp = json_format.MessageToDict(response)
            if 'notification' not in get_resp:
                raise GnmiMessageException('No notification in GetResponse')
            notifications = get_resp['notification']
            for notification in notifications:
                if 'update' not in notification:
                    raise GnmiMessageException('No update in GetResponse')
                prefix = notification.get('prefix')
                json_dicts.append(GnmiMessage.decode_update(
                    notification['update'],
                    prefix,
                    namespace,
                    opfields
                ))

        return (json_dicts, opfields)

    @classmethod
    def iter_subscribe_request(self, payloads, delay=0, log=None):
        """Generator passed to Subscribe service to handle stream payloads.

        Args:
          payload (list): proto.gnmi_pb2.SubscribeRequest
        """
        for payload in payloads:
            if delay:
                time.sleep(delay)
                if log and payload.HasField('poll'):
                    log.info(
                        'gNMI SUBSCRIBE POLL\n' + '=' * 19 + '\n{0}'.format(
                            str(payload)
                        )
                    )
            yield payload

    @classmethod
    def run_subscribe(self, device, payload, request):
        """Run gNMI subscribe service.

        Args:
          device (ysgnmi.device_plugin.GnmiSession): Target device.
          user (str): YANG Suite username.
          payload (proto.gnmi_pb2.SetRequest): SetRequest.
          payload (str): JSON representing a SetRequest.
          request (dict): gNMI subscribe settings for thread.
        """
        if isinstance(payload, proto.gnmi_pb2.SubscribeRequest):
            gnmi_string = str(payload)
        else:
            try:
                payload = GnmiMessageConstructor.json_to_gnmi(
                    'subscribe', payload
                )
                gnmi_string = str(payload)
            except Exception:
                log.error(traceback.format_exc())
                raise GnmiMessageException("Invalid payload\n{0}".format(
                    str(payload)
                ))
        device.log.info('gNMI SUBSCRIBE\n' + '=' * 14 + '\n{0}'.format(
            gnmi_string
        ))
        try:
            payloads = [payload]
            delay = 0
            if request['request_mode'] == 'POLL':
                delay = 2
                payloads.append(
                    GnmiMessageConstructor.get_subscribe_poll()
                )

            def verify(data, returns={}):
                return data
            # TODO: add verify option for user?
            request['returns'] = {'empty': 'returns'}
            request['verifier'] = verify
            request['decode'] = self.decode_notification
            request['log'] = device.log

            response = device.subscribe(
                self.iter_subscribe_request(payloads, delay, device.log)
            )
            subscribe_thread = GnmiNotification(
                response,
                **request
            )
            subscribe_thread.log = device.log

            subscribe_thread.start()
            device.active_notifications[device] = subscribe_thread
        except Exception as exc:
            log.error(traceback.format_exc())
            if hasattr(exc, 'details'):
                device.log.error('ERROR: {0}'.format(exc.details()))
            else:
                device.log.error(str(exc))

    def get_modules(self, cfg):
        """Helper function for get_entries."""
        return cfg.get('modules', {})

    def get_entries(self, cfg):
        """Helper function for get_messages."""
        entries = []
        modules = self.get_modules(cfg)

        for mod in modules.keys():
            entries.append({
                'module': mod,
                'namespace_modules': modules[mod].get('namespace_modules'),
                'namespace_prefixes': modules[mod].get('namespace_prefixes'),
                'nodes': modules[mod]['configs']
            })
        return entries

    def get_messages(self):
        """Using request, instantiate GnmiMessageConstuctor class.

        Returns:
          list: GnmiMessageConstructor classes.
        """
        gmcs = []
        entries = self.get_entries(self.cfg)
        for entry in entries:
            gmc = GnmiMessageConstructor(self.msg_type, entry, **self.cfg)
            gmcs.append(gmc)
        return gmcs


class GnmiMessageConstructor:
    """Construct a single gNMI message based on request."""

    def __init__(self, message_type, entry, **cfg):
        self.request = entry
        self.cfg = cfg
        self.prefix = cfg.get('prefix')
        self.origin = cfg.get('origin')
        self.encoding = cfg.get('encoding', 'JSON_IETF').upper()
        self.get_type = cfg.get('get_type', 'ALL').upper()
        self.base64 = cfg.get('base64', False)
        self.nodes = None
        self.delete = []
        self.subscribe = []
        self.get = []
        self.json_val = {}
        self.msg_type = message_type
        self.xml_xpath_to_gnmi_xpath()
        self.nodes_to_dict()

    @property
    def origin(self):
        return self._origin

    @origin.setter
    def origin(self, value):
        if value == 'module' and 'modules' in self.cfg:
            self._origin = next(iter(self.cfg['modules']))
        else:
            self._origin = value

    @property
    def msg_type(self):
        return self._msg_type

    @msg_type.setter
    def msg_type(self, msg_type):
        self.payload = None
        self._msg_type = msg_type
        if msg_type == 'set':
            self.payload = proto.gnmi_pb2.SetRequest()
        elif msg_type == 'get':
            self.payload = proto.gnmi_pb2.GetRequest()
            self.payload.type = proto.gnmi_pb2.GetRequest.DataType.Value(
                self.get_type
            )
            self.payload.encoding = proto.gnmi_pb2.Encoding.Value(
                self.encoding
            )
        elif msg_type == 'subscribe':
            self.payload = proto.gnmi_pb2.SubscribeRequest()
        if msg_type != 'subscribe' and self.prefix:
            prefix_path = proto.gnmi_pb2.Path()
            prefix_path.origin = self.origin
            self.payload.prefix.CopyFrom(prefix_path)

    @classmethod
    def _upd_rpl(self, upd_rpl, base64_encode):
        updates = []
        for upd in upd_rpl:
            val = None
            if 'val' in upd:
                val = upd.pop('val', {})
            gnmi_update = json_format.ParseDict(
                upd,
                proto.gnmi_pb2.Update()
            )
            if val is not None:
                if 'jsonIetfVal' in val:
                    if base64_encode:
                        jval = bytes(
                            json.dumps(val['jsonIetfVal']), encoding='utf-8'
                        )
                        gnmi_update.val.json_ietf_val = base64.b64encode(jval)
                    else:
                        gnmi_update.val.json_ietf_val = json.dumps(
                            val['jsonIetfVal']
                        ).encode('utf-8')
                elif 'jsonVal' in val:
                    if base64_encode:
                        jval = bytes(
                            json.dumps(val['jsonVal']), encoding='utf-8'
                        )
                        gnmi_update.val.json_val = base64.b64encode(jval)
                    else:
                        gnmi_update.val.json_val = json.dumps(
                            val['jsonVal']
                        ).encode('utf-8')
            updates.append(gnmi_update)
        return updates

    @classmethod
    def json_to_gnmi(self, action, payload, **kwargs):
        """Given a JSON payload, convert it to a gNMI message.

        Expected JSON format is similar to a string __repr__ of the
        proto.gnmi_pb2 class with the exception of the "val" member.
        The "val" is passed in normal JSON format in the payload parameter
        but then gets converted to base64 encoding in the returned
        associated proto.gnmi_pb2 class.

        Args:
          action (str): set | get | subscribe.
          payload (str): Properly formated JSON string.
        Raises:
          GnmiMessageException
        Returns:
          gNMI proto.gnmi_pdb2 class
        """
        base64_encode = kwargs.get('base64', False)
        try:
            gnmi_dict = json.loads(payload)
        except Exception as exc:
            log.error(traceback.format_exc())
            raise GnmiMessageException('JSON parse failed: {0}'.format(
                str(exc)
            ))
        try:
            if action == 'set':
                updates = gnmi_dict.pop('update', [])
                replaces = gnmi_dict.pop('replace', [])
                gnmi_pld = json_format.ParseDict(
                    gnmi_dict,
                    proto.gnmi_pb2.SetRequest()
                )
                if updates:
                    gnmi_upd = self._upd_rpl(updates, base64_encode)
                    if gnmi_upd:
                        gnmi_pld.update.extend(gnmi_upd)
                if replaces:
                    gnmi_upd = self._upd_rpl(replaces, base64_encode)
                    if gnmi_upd:
                        gnmi_pld.replace.extend(gnmi_upd)
            elif action == 'get':
                gnmi_pld = json_format.Parse(
                    payload,
                    proto.gnmi_pb2.GetRequest()
                )
            elif action == 'subscribe':
                gnmi_pld = json_format.Parse(
                    payload,
                    proto.gnmi_pb2.SubscribeRequest()
                )
            return gnmi_pld
        except Exception as exc:
            log.error(traceback.format_exc())
            raise GnmiMessageException('Message parse failed: {}'.format(
                str(exc)
            ))

    @classmethod
    def spilt_value_namespaces(self, value: str) -> list:
        try:
            return value.split(':')
        except Exception:
            return []

    def _manage_paths(self, path_req, gnmi_req):
        # Get initial gnmi path for gnmi message
        short_xp = self.get_shortest_common_path(path_req)
        gnmi_path = self.parse_xpath_to_gnmi_path(
            short_xp, self.origin
        )

        ext_xpaths = []
        for n in path_req:
            xp = n['xpath']
            n['xpath'] = xp[len(short_xp):]
            ext_xpaths.append(n)
        # TODO: fix
        if self.prefix and ext_xpaths and False:
            self.payload.prefix.CopyFrom(gnmi_path)
            gnmi_req = []
            for n in ext_xpaths:
                update = proto.gnmi_pb2.Update()
                update.path.CopyFrom(
                    self.parse_xpath_to_gnmi_path(n['xpath'])
                )
                gnmi_req.append(update)
            self.json_val = {}
        else:
            gnmi_req.path.CopyFrom(gnmi_path)
            payload = self.get_payload(ext_xpaths)

        return payload

    def _gnmi_update_request(self, upd_req, gnmi_upd_req):
        # Construct an Update structure for a SetRequest gNMI message.
        json_val = self._manage_paths(upd_req, gnmi_upd_req)
        # Human readable for logs, by default it stores latest value
        # either update or replace
        if self.json_val:
            if not isinstance(self.json_val, list):
                self.json_val = [self.json_val]
            self.json_val.append(json_val)
        else:
            self.json_val = json_val
        if json_val:
            json_val = json.dumps(json_val).encode('utf-8')
            if self.base64:
                json_val = base64.b64encode(json_val)

            if self.encoding and self.encoding.lower() == 'json_ietf':
                gnmi_upd_req.val.json_ietf_val = json_val
            else:
                gnmi_upd_req.val.json_val = json_val
        return [gnmi_upd_req]

    def group_nodes(self, update):
        """ Group the nodes based on leaf/list/container level

        Args:
          nodes (list): dicts with xpath in gNMI format, nodetypes, values.
        """
        update_filter = []
        update_nodes = []
        list_or_cont = False
        parent_xp = ""
        # Group the nodes based on leaf/list/container level
        # Eg nodes: [leaf, leaf, leaf, list, leaf, leaf]
        # leaf level: [leaf], [leaf], [leaf] - Leaf level RPCs
        # will build sepeartely for each leaf node.
        # list level: [list, leaf, leaf]
        for node in update:
            if (node['xpath'].endswith("]") or
                node['nodetype'] == 'list' or
                    node['nodetype'] == 'container') and \
                        (not parent_xp or parent_xp not in node['xpath']):
                parent_xp = node['xpath']
                list_or_cont = True
                if update_filter:
                    update_nodes.append(update_filter)
                update_filter = []
                update_filter.append(node)
            else:
                update_filter.append(node)
                if not list_or_cont:
                    update_nodes.append(update_filter)
                    update_filter = []

        if update_filter:
            update_nodes.append(update_filter)

        return update_nodes

    def nodes_to_dict(self, nodes=None, origin=None):
        """Construct full gNMI request message to be sent through service.

        Args:
          nodes (list): dicts with xpath in gNMI format, nodetypes, values.
          origin (string): gNMI origin for message.
        """
        # TODO: classmethod?
        if not self.nodes:
            self.nodes = nodes
        if origin:
            self.origin = origin

        update = self.nodes.get('update', [])
        replace = self.nodes.get('replace', [])
        delete = self.nodes.get('delete', [])
        get = self.nodes.get('get', [])
        subscribes = self.nodes.get('subscribe', [])

        if update:
            gnmi_update = proto.gnmi_pb2.Update()
            update_nodes = self.group_nodes(update)
            # Send each group for payload building
            for node in update_nodes:
                self.update = self._gnmi_update_request(node, gnmi_update)
                self.payload.update.extend(self.update)

        if replace:
            gnmi_replace = proto.gnmi_pb2.Update()
            replace_nodes = self.group_nodes(replace)
            # Send each group for payload building.
            for node in replace_nodes:
                self.replace = self._gnmi_update_request(node, gnmi_replace)
                self.payload.replace.extend(self.replace)

        if delete:
            gnmi_delete_paths = []
            for xp in delete:
                gnmi_delete_paths.append(
                    self.parse_xpath_to_gnmi_path(xp, self.origin)
                )
            self.payload.delete.extend(gnmi_delete_paths)

        if get:
            if self.prefix and len(get) > 1:
                prefix = os.path.commonpath(get)
                if prefix and prefix != '/':
                    prefix_path = self.parse_xpath_to_gnmi_path(
                        prefix, self.origin
                    )
                    self.payload.prefix.CopyFrom(prefix_path)
                for xp in get:
                    self.payload.path.append(
                        self.parse_xpath_to_gnmi_path(
                            xp.replace(prefix, '')
                        )
                    )
            else:
                for xp in get:
                    self.payload.path.append(
                        self.parse_xpath_to_gnmi_path(xp, self.origin)
                    )

        if subscribes:
            # Create subscribe list.
            subscribe_list = proto.gnmi_pb2.SubscriptionList()
            subscribe_list.encoding = proto.gnmi_pb2.Encoding.Value(
                self.encoding
            )
            mode = self.cfg.get('request_mode')

            subscribe_list.mode = proto.gnmi_pb2.SubscriptionList.Mode.Value(
                mode
            )
            if self.prefix:
                # TODO: calculate prefix paths
                prefix_path = proto.gnmi_pb2.Path()
                prefix_path.origin = self.origin
                subscribe_list.prefix.CopyFrom(prefix_path)

            # Create subscriptions for the list.
            for subscribe in subscribes:
                subscription = proto.gnmi_pb2.Subscription()
                sub_mode = self.cfg.get('sub_mode')
                subscription.mode = proto.gnmi_pb2.SubscriptionMode.Value(
                    sub_mode
                )
                if sub_mode == 'SAMPLE':
                    subscription.sample_interval = self.cfg.get(
                        'sample_interval'
                    )
                gnmi_path = self.parse_xpath_to_gnmi_path(subscribe)
                if not self.prefix:
                    gnmi_path.origin = self.origin
                subscription.path.CopyFrom(gnmi_path)

                # Add the subscription to the list.
                subscribe_list.subscription.extend([subscription])

            # Add list to the subscribe request.
            self.payload.subscribe.CopyFrom(subscribe_list)

        return self.payload

    @classmethod
    def get_subscribe_poll(self):
        """POLL subscribe requires a message to start polling."""
        sub = proto.gnmi_pb2.SubscribeRequest()
        sub.poll.SetInParent()
        return sub

    def _trim_xpaths(self, xpaths, short_xp):
        # Helper function for get_shortest_common_path.
        for xpath in xpaths:
            if short_xp not in xpath:
                if short_xp.endswith(']'):
                    while short_xp.endswith(']'):
                        short_xp = short_xp[:short_xp.rfind('[')]
                    xp = short_xp[:short_xp.rfind('/')]
                else:
                    xp = short_xp[:short_xp.rfind('/')]
                short_xp = self._trim_xpaths(xpaths, xp)
        return short_xp

    def get_shortest_common_path(self, nodes):
        """Find the shortest common path in a collection of nodes.

        Args:
          nodes (list): dicts with xpath in gNMI format, nodetypes, values.

        Return:
          str
        """
        if len(nodes) == 1:
            return nodes[0]['xpath']
        xpaths = [n['xpath'] for n in nodes]
        short_xp = min(set(xpaths), key=len)
        short_xp = self._trim_xpaths(xpaths, short_xp)
        short_node = [n for n in nodes if n['xpath'] == short_xp]
        if short_node:
            if not short_node[0]['xpath'].endswith("]") and \
                    short_node[0]['nodetype'] not in ['list', 'container']:
                while short_xp.endswith(']'):
                    short_xp = short_xp[:short_xp.rfind('[')]
                short_xp = short_xp[:short_xp.rfind('/')]
        return short_xp

    def get_payload(self, update):
        """Construct dict that will be converted to json_val in Update.

        dict will be in format of json {}

        For all list having similar keys but different values,
        create a list of dictionaries.
        This will allow to store every key value in a single json_val

        Eg: xpath =  common_xpath/x-list[type="t1"]/val
                     common_xpath/x-list[type="t2"]/val

        json_val will be = "{"x-list": [{"type": "t1", "val": 10},
        {"type": "t2", "val": 10}]}"
        Args:
          update (list): dicts with xpath in gNMI format, nodetypes, values.

        Returns:
          dict
        """
        if len(update) == 1 and not update[0]['xpath']:
            return update[0]['value']
        json_val = {}
        processed_xp = []
        list_nodes = []
        for node in update:
            ind = 0
            xp = node['xpath']
            # in pyats code, if xpath ends with "]"
            # then appending "/" at the end
            if xp.endswith(']'):
                xp = xp + '/'
            if xp.endswith(']'):
                # list xpath; will be base xpath for other xpaths so skip it.
                continue
            if '[' in xp:
                # child node of list
                # get the name of the list node
                list_xpath = node['xpath']
                while '[' in list_xpath:
                    list_xpath = list_xpath[:list_xpath.rfind('[')]
                    if not list_xpath.endswith(']'):
                        list_node = list_xpath[list_xpath.rfind('/'):]
                        list_node = list_node.strip('/')
                        if list_node not in list_nodes:
                            list_nodes.append(list_node)
            if xp in processed_xp:
                # duplicate of path already processed.
                if node['nodetype'] != 'leaf-list':
                    continue
            jval = json_val
            collect_key = False
            key_elem = None
            tokenized = xpath_tokenizer_re.findall(xp)
            if len(tokenized) == 0:
                continue
            for i, seg in enumerate(tokenized, 1):
                token, elem = seg
                if token in ['/', '=']:
                    continue
                if not token and not collect_key and elem:
                    if len(tokenized) == i:
                        # If a node has only one element
                        if len(jval) == 0:
                            if node.get('nodetype', '') == 'leaf-list':
                                if jval.get(elem) is None:
                                    jval[elem] = [LeafListVal(node['value'][0])]
                                else:
                                    jval[elem].append(LeafListVal(node['value'][0]))
                            else:
                                jval[elem] = node['value']
                        else:
                            # Check if jval is pointing to a list
                            # or dict to assign values
                            if isinstance(jval, list):
                                if node.get('nodetype', '') == 'leaf-list':
                                    if jval[ind].get(elem) is None:
                                        jval[ind][elem] = [LeafListVal(node['value'][0])]
                                    else:
                                        jval[ind][elem].append(LeafListVal(node['value'][0]))
                                else:
                                    jval[ind][elem] = node['value']
                            else:
                                if node.get('nodetype', '') == 'leaf-list':
                                    if jval.get(elem) is None:
                                        jval[elem] = [LeafListVal(node['value'][0])]
                                    else:
                                        jval[elem].append(LeafListVal(node['value'][0]))
                                else:
                                    jval[elem] = node['value']
                    else:
                        # Create a new list of dictionary /
                        # new key in dictionary if elem is not present
                        if elem not in jval:
                            if isinstance(jval, list):
                                if (elem not in jval[ind]):
                                    if (len(jval) == 0 or {} in jval):
                                        ind = 0
                                    jval[ind][elem] = []
                                    jval[ind][elem].append({})
                            else:
                                jval[elem] = []
                                ind = 0
                                jval[elem].append({})

                        # For every interation point jval to
                        # the last list created.
                        if isinstance(jval, list):
                            if jval[ind][elem] == "":
                                jval[ind][elem] = []
                                jval[ind][elem].append({})
                            jval = jval[ind][elem]
                            ind = 0
                        else:
                            jval = jval[elem]
                    continue
                if token == '[':
                    # key is up next
                    collect_key = True
                    continue
                if token == ']':
                    collect_key = False
                    continue
                if key_elem is not None and token:
                    # Store key_elem only if it is not equal
                    # to prevous key_elem for the same list.
                    if key_elem in jval[ind]:
                        index = 0
                        f = 0
                        for j in jval:
                            if j[key_elem] == token.strip('"'):
                                f = 1
                                break
                            index = index+1
                        if f == 0:
                            ind = len(jval)
                            jval.append({})
                            jval[ind][key_elem] = token.strip('"')
                        else:
                            ind = index
                    else:
                        jval[ind][key_elem] = token.strip('"')
                    key_elem = None
                    continue
                if collect_key and elem:
                    # check if key value is an integer
                    # or a float value
                    try:
                        int(elem)
                        if isinstance(jval, list):
                            jval[ind][key_elem] = int(elem)
                        else:
                            jval[key_elem] = int(elem)
                    except ValueError:
                        try:
                            float(elem)
                            if isinstance(jval, list):
                                jval[ind][key_elem] = float(elem)
                            else:
                                jval[key_elem] = float(elem)
                        except ValueError:
                            key_elem = elem
                    continue
            processed_xp.append(xp)

        self.format_json_val(json_val)
        self.format_list_nodes(json_val, list_nodes)
        return json_val

    def format_json_val(self, json_val):
        # Convert List of Dictionaries with only 1 one element to Dictionary
        if not isinstance(json_val, dict):
            return
        for j in json_val:
            if isinstance(json_val[j], list) and len(json_val[j]) == 1:
                if isinstance(json_val[j][0], LeafListVal):
                    # leaflist value need to enclosed within brackets
                    # extract the value from Leaflistval object
                    json_val[j][0] = json_val[j][0].llvalue
                    self.format_json_val(json_val[j])
                else:
                    json_val[j] = json_val[j][0]
                    self.format_json_val(json_val[j])
            else:
                if isinstance(json_val[j], list):
                    for ind, i in enumerate(json_val[j]):
                        if isinstance(i, LeafListVal):
                            json_val[j][ind] = i.llvalue
                            self.format_json_val(i.llvalue)
                        else:
                            self.format_json_val(i)

    def format_list_nodes(self, json_val, list_nodes):
        # Enclose list entries within square brackets.
        if not isinstance(json_val, dict):
            if isinstance(json_val, list):
                for i in json_val:
                    self.format_list_nodes(i, list_nodes)
            else:
                return
        for j in json_val:
            if j in list_nodes:
                json_val[j] = [json_val[j]]
            if isinstance(j, dict) or isinstance(json_val, list):
                return
            self.format_list_nodes(json_val[j], list_nodes)

    def _trim_nodes(self, nodes):
        # Prune list nodes if already in other nodes xpath
        if nodes:
            xps = [n['xpath'] for n in nodes]
            long_xp = max(xps, key=len)
        for i in range(len(nodes)):
            if nodes[i]['xpath'] == long_xp:
                continue
            if nodes[i]['xpath'] in long_xp:
                nodes.remove(nodes[i])
                return self._trim_nodes(nodes)
        return nodes

    def _value_to_datatype(self, datatype, value):
        if datatype == 'empty' or datatype is None:
            value = None
        elif datatype == 'boolean':
            if isinstance(value, string_types):
                if value.lower() == 'true':
                    value = True
                elif value.lower() == 'false':
                    value = False
        elif datatype.startswith('int') or \
                datatype.startswith('uint'):
            if value:
                try:
                    value = int(value)
                except ValueError:
                    # default datatype to string
                    datatype = 'string'
        elif datatype in ('decimal64', 'float', 'double'):
            if value:
                try:
                    value = float(value)
                except ValueError:
                    # default datatype to string
                    datatype = 'string'
        return (value, datatype)

    def _adjust_value_to_datatype(self, node):
        datatype = node.get('datatype')
        value = node.get('value')
        if value is None:
            return None

        if datatype == 'union':
            values = []
            members = node.get('members', {})
            if members:
                for member in members:
                    values.append(
                        self._value_to_datatype(
                            member['datatype'],
                            value
                        )
                    )
                for val_dt in values:
                    val, dt = val_dt
                    if not isinstance(val, string_types):
                        value = val
                        datatype = dt
                        break
            else:
                value, datatype = self._value_to_datatype(
                    datatype,
                    value
                )
        else:
            value, datatype = self._value_to_datatype(
                datatype,
                value
            )
        if node.get('nodetype', '') == 'leaf-list':
            value = [value]

        node['datatype'] = datatype
        return value

    def _get_leafref_datatypes(self):
        # fill in leafref's referred-to datatypes
        for node in self.request.get('nodes'):
            if node.get('referred_to'):
                ref_path = node.get('referred_to', {}).get('leafref_path')
                for n in self.request.get('nodes'):
                    if ref_path == n['xpath']:
                        # found my leafref node so copy datatype over
                        n['datatype'] = node['datatype']
                        break

    def xml_xpath_to_gnmi_xpath(self):
        """Convert XML Path Language 1.0 Xpath to gNMI Xpath.

        Input modeled after YANG/NETCONF Xpaths.
        References:
        * https://www.w3.org/TR/1999/REC-xpath-19991116/#location-paths
        * https://www.w3.org/TR/1999/REC-xpath-19991116/#path-abbrev
        * https://tools.ietf.org/html/rfc6020#section-6.4
        * https://tools.ietf.org/html/rfc6020#section-9.13
        * https://tools.ietf.org/html/rfc6241

        Returns:
          (tuple): namespace_modules, message dict
        """
        message = {
            "update": [],
            "replace": [],
            "delete": [],
            "get": [],
            "subscribe": []
        }
        if "nodes" not in self.request:
            # TODO: raw rpc?
            return message

        # find any referred-to datatypes
        self._get_leafref_datatypes()

        if not self.request.get('namespace_modules'):
            log.warning("No prefix-to-module mapping in request")
            namespace = {}
            module = ''
            namespace_prefixes = self.request.get("namespace_prefixes", {})
            for prefix, nspace in namespace_prefixes.items():
                if "/Cisco-IOS-" in nspace:
                    module = nspace[nspace.rfind("/") + 1:]
                elif "/cisco-nx" in nspace:  # NXOS lowercases namespace
                    module = "Cisco-NX-OS-device"
                elif "/openconfig.net" in nspace:
                    module = "openconfig-"
                    module += nspace[nspace.rfind("/") + 1:]
                elif "urn:ietf:params:xml:ns:yang:" in nspace:
                    module = nspace.replace("urn:ietf:params:xml:ns:yang:", "")
                if module:
                    namespace[prefix] = module
            self.request['namespace_modules'] = namespace

        nodes = self.request.get("nodes", [])
        if self.msg_type == 'set':
            # removes node if edit-op is not assigned for key node.
            # if user tries to update multiple keynodes
            # then this will not work so added default operation in js
            # Prune key nodes without edit-op assigned.
            nodes = [n for n in nodes if not (
                n['xpath'].endswith(']') and
                not n.get('edit-op')
            )]
        if self.msg_type in ['get', 'subscribe'] and len(nodes) > 1:
            # Prune nodes with xpaths already in other node's xpath.
            nodes = self._trim_nodes(nodes)

        module = self.request.get('module')
        self.namespace_modules = self.request.get("namespace_modules", {})
        parent_edit_op = None
        for node in nodes:
            if "xpath" not in node:
                log.error("Xpath is not in message")
            else:
                xpath = node["xpath"]
                edit_op = node.get("edit-op", "")
                if xpath.endswith("]"):
                    nodetype = "list"
                else:
                    nodetype = node.get("nodetype", "")

                if nodetype in ['list', 'container']:
                    parent_edit_op = edit_op

                value = self._adjust_value_to_datatype(node)
                if xpath.startswith('/'):
                    xp = xpath.split('/')[1:]
                else:
                    node['xpath'] = '/' + xpath
                    xp = xpath.split('/')

                if not module:
                    # First segment of xpath has prefix of module.
                    if ':' in xp[0]:
                        pfx = xp[0].split(':')[0]
                        module = self.namespace_modules[pfx]
                    else:
                        module = ''
                    if self.encoding is None:
                        # Should be in format so this is an older test
                        log.warning("No encoding in request.")
                        if 'Cisco-IOS-XE' in module or \
                                'Cisco-IOS-XR' in module:
                            self.encoding = 'JSON_IETF'
                        elif 'openconfig' in module:
                            self.encoding = 'JSON'
                    if self.origin is None:
                        # Should be in format so this is an older test
                        if 'Cisco-IOS-XE' in module:
                            self.origin = 'rfc7951'
                        elif 'Cisco-IOS-XR' in module:
                            self.origin = module
                        elif 'openconfig' in module:
                            # For XR this could be module name
                            self.origin = 'openconfig'

                value_namespaces = self.spilt_value_namespaces(value)
                # For info about namespaces handling refer to
                # https://datatracker.ietf.org/doc/html/rfc7951#page-5
                for pfx, mod in self.namespace_modules.items():
                    if isinstance(value, string_types) and pfx in value_namespaces:
                        if mod != module:
                            value = value.replace(pfx + ":", mod + ':')
                    elif isinstance(value, list):
                        for ind, i in enumerate(value):
                            list_value_namespaces = self.spilt_value_namespaces(i)
                            if (pfx in list_value_namespaces) and (mod != module):
                                value[ind] = value[ind].replace(pfx + ":", mod + ":")
                    # rfc7951 origin requires entire module name in path.
                    # Module as origin requires entire module name in path.
                    for i, seg in enumerate(xp):
                        if pfx not in xpath:
                            continue
                        if i == 0 and self.origin == 'rfc7951':
                            # Only needed for first path elem.
                            seg = seg.replace(pfx + ":", module + ':')
                            xp[i] = seg
                            continue
                        if mod != module and self.origin == 'rfc7951':
                            # From another module so this is required.
                            seg = seg.replace(pfx + ":", mod + ':')
                        else:
                            seg = seg.replace(pfx + ':', '')
                        xp[i] = seg

                    if not xpath.endswith(']'):
                        node['name'] = xp[-1:][0]
                    else:
                        node['name'] = ''
                    node['xpath'] = '/'.join(xp)

                node['value'] = value

                if self.msg_type == 'set':
                    if not edit_op:
                        if parent_edit_op:
                            edit_op = parent_edit_op
                        else:
                            edit_op = 'update'

                    if edit_op in ["update", "replace"]:
                        if edit_op == "replace":
                            message["replace"] += [node]
                        elif edit_op == "update":
                            message["update"] += [node]
                    elif edit_op == "delete":
                        message["delete"].append(node['xpath'])

                elif self.msg_type in ['get', 'subscribe']:
                    if not message[self.msg_type]:
                        message[self.msg_type] = [node['xpath']]
                    elif node['xpath'] not in message[self.msg_type]:
                        message[self.msg_type].append(node['xpath'])
                else:
                    log.error('gNMI message type "{0}" is invalid.'.format(
                        str(self.msg_type)
                    ))
        self.nodes = message

    @classmethod
    def parse_xpath_to_gnmi_path(cls, xpath, origin=None):
        """Parses an XPath to proto.gnmi_pb2.Path.

        Effectively wraps the std XML XPath tokenizer and traverses
        the identified groups. Parsing robustness needs to be validated.
        Probably best to formalize as a state machine sometime.
        TODO: Formalize tokenizer traversal via state machine.
        """
        if not isinstance(xpath, string_types):
            raise Exception("xpath must be a string!")
        path = proto.gnmi_pb2.Path()
        if origin:
            if not isinstance(origin, string_types):
                raise Exception("origin must be a string!")
            path.origin = origin
        curr_elem = proto.gnmi_pb2.PathElem()
        in_filter = False
        just_filtered = False
        curr_key = None
        # TODO: Lazy
        xpath = xpath.strip("/")
        xpath_elements = xpath_tokenizer_re.findall(xpath)
        path_elems = []
        for element in xpath_elements:
            # stripped initial /, so this indicates a completed element
            if element[0] == "/":
                if not curr_elem.name:
                    # Trying to append to path without a name.
                    raise Exception(
                        "Current PathElem has no name! Invalid XPath?"
                    )
                path_elems.append(curr_elem)
                curr_elem = proto.gnmi_pb2.PathElem()
                continue
            # We are entering a filter
            elif element[0] == "[":
                in_filter = True
                continue
            # We are exiting a filter
            elif element[0] == "]":
                in_filter = False
                continue
            # If we're not in a filter then we're a PathElem name
            elif not in_filter:
                curr_elem.name = element[1]
            # Skip blank spaces
            elif not any([element[0], element[1]]):
                continue
            # If we're in the filter and just completed a filter expr,
            # "and" as a junction should just be ignored.
            elif in_filter and just_filtered and element[1] == "and":
                just_filtered = False
                continue
            # Otherwise we're in a filter and this term is a key name
            elif curr_key is None:
                curr_key = element[1]
                continue
            # Otherwise we're an operator or the key value
            elif curr_key is not None:
                if element[0] in [">", "<"]:
                    raise Exception("Only = supported as filter operand!")
                if element[0] == "=":
                    continue
                else:
                    # We have a full key here, put it in the map
                    if curr_key in curr_elem.key.keys():
                        raise Exception("Key already in key map!")
                    if element[0]:
                        curr_elem.key[curr_key] = element[0].strip("'\"")
                    else:
                        curr_elem.key[curr_key] = element[1].strip("'\'")
                    curr_key = None
                    just_filtered = True
        # Keys/filters in general should be totally cleaned up at this point.
        if curr_key:
            raise Exception("Hanging key filter! Incomplete XPath?")
        # If we have a dangling element that hasn't been completed due to no
        # / element then let's just append the final element.
        if curr_elem:
            path_elems.append(curr_elem)
            curr_elem = None
        if any([curr_elem, curr_key, in_filter]):
            raise Exception("Unfinished elements in XPath parsing!")

        path.elem.extend(path_elems)
        return path
