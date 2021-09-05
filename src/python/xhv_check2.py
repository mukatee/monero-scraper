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
rows = []
keys = set()
count = 0
for x in range(800000, top_height):
    print(f"checking block {x}")
    block = daemon.get_block(height=x)  # 882877 882883
    row = {"height": x}
    for tx_out in block.miner_tx.tx_outs:
        row[tx_out.tx_type] = tx_out.amount
        keys.add(tx_out.tx_type)
    rows.append(row)
    count += 1
#    if count > 100:
#        break

keys = list(keys)
keys.sort(reverse=True)
#        file.write(f"{x},{len(block.miner_tx.tx_outs)}\n")
with open("numbers.csv", "w") as file:
    header_str = "height"
    for key in keys:
        header_str += f"{key}"
    file.write(header_str + "\n")

    for row in rows:
        row_str = f"{row['height']}"
        for key in keys:
            value = ""
            if key in row:
                value = row[key]
            if len(row_str) > 0:
                row_str += ", "
            row_str += f"{value}"
        file.write(row_str+"\n")


