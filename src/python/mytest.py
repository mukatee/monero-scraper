__author__ = 'teemu kanstren'

import json
from monero import jsonapi, rpc

rpc.init(_host="nodes.hashvault.pro")
#rpc.init(_host="localhost")
daemon = jsonapi
info = daemon.info()
print(info)
#-1 throws
#block = daemon.get_block(height=1412880)
block = daemon.get_block(height=1412880)
print(block)
#coinbase_tx_hash = block["block_header"]["miner_tx_hash"]
#print(coinbase_tx_hash)
#cb_transactions = daemon.get_transactions([coinbase_tx_hash])
#print(cb_transactions)
print(block.txs)
print(daemon.get_height())
mempool = daemon.mempool()
print(mempool)
top_height = daemon.get_height() - 1
block = daemon.get_block(height=top_height)
pass
