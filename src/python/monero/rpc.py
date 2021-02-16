from datetime import datetime
import operator
import json
import logging
import requests

_log = logging.getLogger(__name__)

url = None
user = None
password = None
timeout = None
verify_ssl_certs = None

"""
:param protocol: `http` or `https`
:param host: host name or IP
:param port: port number
:param path: path for JSON RPC requests (should not be changed)
:param timeout: request timeout
:param verify_ssl_certs: verify SSL certificates when connecting
"""
def init(_protocol='http', _host='127.0.0.1', _port=18081, _path='/json_rpc',
        _user='', _password='', _timeout=30, _verify_ssl_certs=True):
    global url, user, password, timeout, verify_ssl_certs
    url = f'{_protocol}://{_host}:{_port}'
    _log.debug("JSONRPC daemon backend URL: {url}".format(url=url))
    user = _user
    password = _password
    timeout = _timeout
    verify_ssl_certs = _verify_ssl_certs


def raw_request(path, data):
    hdr = {'Content-Type': 'application/json'}
    _log.debug(u"Request: {path}\nData: {data}".format(
        path=path,
        data=json.dumps(data, indent=2, sort_keys=True)))
    rsp = requests.post(
        url + path, headers=hdr, data=json.dumps(data),
        timeout=timeout, verify=verify_ssl_certs)
    if rsp.status_code != 200:
        raise MoneroException(f"Invalid HTTP status {rsp.status_code} for path {path}.")
    result = rsp.json()
    _ppresult = json.dumps(result, indent=2, sort_keys=True)
    _log.debug(u"Result: \n{result}".format(result=_ppresult))
    return result

def raw_jsonrpc_request(method, params=None):
    global user, password
    hdr = {'Content-Type': 'application/json'}
    data = {'jsonrpc': '2.0', 'id': 0, 'method': method, 'params': params or {}}
    _log.debug(u"Method: {method}\nParams:\n{params}".format(
        method=method,
        params=json.dumps(params, indent=2, sort_keys=True)))
    auth = requests.auth.HTTPDigestAuth(user, password)
    rsp = requests.post(
        url + '/json_rpc', headers=hdr, data=json.dumps(data), auth=auth,
        timeout=timeout, verify=verify_ssl_certs)

    if rsp.status_code == 401:
        raise Unauthorized("401 Unauthorized. Invalid RPC user name or password.")
    elif rsp.status_code != 200:
        raise MoneroException(f"Invalid HTTP status {rsp.status_code} for method {method}.")
    import os
    wd = os.getcwd()
    with open("kkkk.json", "wb") as aa:
        print(wd)
        aa.write(rsp.content)
    result = rsp.json()
    _ppresult = json.dumps(result, indent=2, sort_keys=True)
    _log.debug(u"Result:\n{result}".format(result=_ppresult))

    if 'error' in result:
        err = result['error']
        _log.error(u"JSON RPC error:\n{result}".format(result=_ppresult))
        raise MoneroException(
            f"Method '{method}' failed with RPC Error of unknown code {err['code']}, "
            f"message: {err['message']}")
    return result['result']

class MoneroException(Exception):
    pass

class Unauthorized(MoneroException):
    pass


