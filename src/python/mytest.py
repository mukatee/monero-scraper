__author__ = 'teemu kanstren'

import json
from monero import jsonapi, rpc
from db import sql, create_tables

rpc.init(_host="nodes.hashvault.pro")
#rpc.init(_host="localhost")
daemon = jsonapi
info = daemon.info()
print(info)
mtx = daemon.get_transactions(["c6988cbd8eec02efdb6ce8e43e5c54c8af898dec8d331025248a066645a259dd"])
#-1 throws
#block = daemon.get_block(height=1412880)
block = daemon.get_block(height=1412880)
print(block)
cnx = create_tables.get_cnx()
sql.insert_block(cnx, block)
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
