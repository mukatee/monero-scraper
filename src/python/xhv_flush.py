from havenprotocol import jsonapi, rpc
from codeprofile import profiler
import logging

rpc.init(_host="localhost", _port=17750)
daemon = jsonapi
daemon.flush_bad_tx()
