__author__ = 'teemu kanstren'

from havenprotocol import jsonapi, rpc
from codeprofile import profiler
import logging

logging.basicConfig(filename='xhv_scraper.log',
                    format='%(asctime)s - %(name)s - %(message)s',
                    filemode='w',
                    level=logging.WARNING)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

stream = logging.StreamHandler()
stream.setLevel(logging.DEBUG)
streamformat = logging.Formatter("%(asctime)s:%(levelname)s:%(message)s")
stream.setFormatter(streamformat)
logger.addHandler(stream)
#
#rpc.init(_host="nodes.hashvault.pro")
rpc.init(_host="localhost", _port=17750)
daemon = jsonapi
info = daemon.info()
logger.info(info)
logger.info(f"current deamon height: {daemon.get_height()}")
mtx = daemon.get_transactions(["7d48e1189e2f4013bbe1f217d48baf909e1bad681a94d136c7a6ce3ae44f8236"])

profiler.collect_raw = False
block_idx = 882877
block = daemon.get_block(height=882877)
block_used = daemon.get_block(height=882939)
top_height = daemon.get_height()
for x in range(882877, top_height):
    #print(f"checking block {x}")
    block = daemon.get_block(height=x)  # 882877 882883
    for tx in block.txs:
        for tx_in in tx.tx_ins:
            for out_detail in tx_in.out_details:
#                bad_block = 882877
                bad_block = 883040
                tx_hash1 = "5042dab28ef8999a4185327689e1875ac8fa9f67a7dd55923f35d00abfb67324"
#                tx_hash1 = "3b8e80a279000d3d32826010b665e2c78aaf25d1744c49cac8a5da154d293875"
#                if out_detail.key_hex == "3b8e80a279000d3d32826010b665e2c78aaf25d1744c49cac8a5da154d293875":
                if out_detail.key_hex == tx_hash1:
                    print(f"block {bad_block} txout ({tx_hash1}) found as input in block {x}.{tx.idx}: {tx.hash_hex}")
#                if out_detail.key_hex == "7dec1f53dd30416458926bd35e9c1fff98d0ac86fc185a8fedfad546ff7d4546":
                tx_hash2 = "fa35c8851e5182e3b3dbc8a86730915fc6ef1266bb5296111aa3a94c290deb26"
#                tx_hash2 = "7dec1f53dd30416458926bd35e9c1fff98d0ac86fc185a8fedfad546ff7d4546"
                if out_detail.key_hex == tx_hash2:
                    print(f"block {bad_block} txout ({tx_hash2}) found as input in block {x}.{tx.idx}: {tx.hash_hex}")
#                    print(f"FAIL2: {tx}")
        #print(tx)

mempool = daemon.mempool()
print(mempool)
#882877
#3b8e80a279000d3d32826010b665e2c78aaf25d1744c49cac8a5da154d293875
#7dec1f53dd30416458926bd35e9c1fff98d0ac86fc185a8fedfad546ff7d4546

#883040
#5042dab28ef8999a4185327689e1875ac8fa9f67a7dd55923f35d00abfb67324
#fa35c8851e5182e3b3dbc8a86730915fc6ef1266bb5296111aa3a94c290deb26
