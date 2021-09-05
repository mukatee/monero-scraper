__author__ = 'teemu kanstren'

from . import rpc
from . import transaction, block
from decimal import Decimal
import json
from typing import List

PICONERO = Decimal('0.000000000001')

xmr_genesis_hash = '418015bb9ae982a1975da7d79277c2705727a56894ba0fb246adaabb1f4632e3'
xhv_genesis_hash = '4b49042122496cc7e94d392b29bd12ebbc92bcec98990470a30c1eb323b41ebb'
coin_type = None

def init():
    global coin_type
    genesis_block_hash = get_block_hash(height=0)
    if genesis_block_hash == xmr_genesis_hash:
        coin_type = 'xmr'
    elif genesis_block_hash == xhv_genesis_hash:
        coin_type = 'xhv'

def from_atomic(amount):
    """Convert atomic integer of piconero to Monero decimal."""
    return (Decimal(amount) * PICONERO).quantize(PICONERO)

def info():
    info = rpc.raw_jsonrpc_request('get_info')
    return info

#the height is the number of blocks. it seems the top block index is height - 1.
def get_height():
    res = rpc.raw_jsonrpc_request('get_block_count')
    return res["count"]

def get_block_hash(height: int = None) -> str:
    res = rpc.raw_jsonrpc_request('get_block', {'height': height})
    header = res["block_header"]
    return header["hash"]

def get_block(hash: str = None, height: int = None) -> block.Block:
    if hash is not None:
        res = rpc.raw_jsonrpc_request('get_block', {'hash': hash})
    else:
        res = rpc.raw_jsonrpc_request('get_block', {'height': height})
    objs = json.loads(res["json"])
    #merge the two dicts: https://stackoverflow.com/questions/38987/how-do-i-merge-two-dictionaries-in-a-single-expression
    #this pulls the contents of the "json" key up to top level on "res", and turns them into actual dict keys
    for k in objs:
        if k not in res["block_header"]:
            res[k] = objs[k]
#    res = {**res, **objs}
    my_block = block.Block(res)
    my_block.miner_tx = get_transactions(my_block.miner_tx_hash_list)[0]
    my_block.txs = get_transactions(my_block.tx_hashes)
    return my_block

#https://monero.stackexchange.com/questions/3958/what-is-the-format-of-a-block-in-the-monero-blockchain
#https://monero.stackexchange.com/questions/7576/rpc-method-to-translate-key-offsets
#https://monero.stackexchange.com/questions/2136/understanding-the-structure-of-a-monero-transaction/2150#2150
def get_transactions(tx_hashes: List) -> List:
    if len(tx_hashes) == 0:
        return []
    # need decode_as_json to get actual vin and a vout values for transaction inputs and outputs
    transactions = rpc.raw_request('/get_transactions', {'txs_hashes': tx_hashes, "decode_as_json": True})
    txs = []
    if "txs" in transactions:
        for idx, tx in enumerate(transactions["txs"]):
            block_height = tx["block_height"]
            txs.append(transaction.from_json(tx["as_json"], block_height, tx_hashes[idx], idx, coin_type))
    else:
        #TODO: use logger
        print(f"No TX found for hashes: {tx_hashes}")
    return txs

def mempool():
    res = rpc.raw_request('/get_transaction_pool', {})
    txs = []
    for tx in res.get('transactions', []):
        block_height = -1 #using -1 for transaction pool
        #fee = tx["fee"]
        #print(fee)
        txs.append(transaction.from_json(tx["tx_json"], block_height, coin_type))
    return txs

def headers(start_height, end_height = None):
    end_height = end_height or start_height
    res = rpc.raw_jsonrpc_request('get_block_headers_range', {
        'start_height': start_height,
        'end_height': end_height})
    if res['status'] == 'OK':
        return res['headers']
    raise Exception()

def get_block_hash_blob(height):
    res = rpc.raw_jsonrpc_request('get_block', {'height': height})
    return res["blob"]

def get_coinbase_hash(height):
    res = rpc.raw_jsonrpc_request('get_block', {'height': height})
    return res["block_header"]["miner_tx_hash"]

def get_block_template(height):
    return

def flush_bad_tx():
    rpc.raw_jsonrpc_request('flush_txpool')




