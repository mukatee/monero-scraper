__author__ = 'teemu kanstren'

from moneroscraper import jsonapi, rpc, logging_config
from src.python.moneroscraper.db import sql, create_tables
from codeprofile import profiler
import io

logger = logging_config.create_logger(__name__)

#rpc.init(_host="nodes.hashvault.pro")
rpc.init(_host="localhost", _port=17750)
jsonapi.init()
#rpc.init(_host="localhost")
daemon = jsonapi
info = daemon.info()
logger.info(info)
logger.info(f"current deamon height: {daemon.get_height()}")
#genesis_block = daemon.get_block(height=0)

mtx = daemon.get_transactions(["c6988cbd8eec02efdb6ce8e43e5c54c8af898dec8d331025248a066645a259dd"])
create_tables.main(jsonapi.coin_type)
cnx = create_tables.get_cnx()
db_height = sql.get_max_block(cnx)
if db_height[0] is None:
    #this is the case when the table is empty
    db_height = (0,)
print(f"table height: ${db_height}")

profiler.collect_raw = False
block = daemon.get_block(height=884280)
top_height = daemon.get_height()
coin_type = jsonapi.coin_type
for x in range(db_height[0] + 1, top_height):
#for x in range(800000, top_height):
    with profiler.profile("get block"):
        block = daemon.get_block(height=x)
    with profiler.profile("insert block"):
        sql.insert_block(cnx, block, coin_type)
    if x%500 == 0:
        logger.info(f"block height: {x}")
        hack_f = io.StringIO()
        profiler.print_run_stats(file=hack_f)
        stats_str = hack_f.getvalue()
        logger.info(stats_str)

#print(block)
#coinbase_tx_hash = block["block_header"]["miner_tx_hash"]
#print(coinbase_tx_hash)
#cb_transactions = daemon.get_transactions([coinbase_tx_hash])
#print(cb_transactions)
#print(block.txs)
mempool = daemon.mempool()
print(mempool)
top_height = daemon.get_height() - 1
block = daemon.get_block(height=top_height)
pass
