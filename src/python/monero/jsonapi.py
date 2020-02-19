__author__ = 'teemu kanstren'

from datetime import datetime
from monero import rpc
from monero.transaction import Transaction, TxIn, TxOut, OutDetails
from decimal import Decimal
import json
from . import transaction, block
from typing import List

PICONERO = Decimal('0.000000000001')

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
    return block.Block(res)

#https://monero.stackexchange.com/questions/3958/what-is-the-format-of-a-block-in-the-monero-blockchain
#https://monero.stackexchange.com/questions/7576/rpc-method-to-translate-key-offsets
#https://monero.stackexchange.com/questions/2136/understanding-the-structure-of-a-monero-transaction/2150#2150
def get_transactions(tx_hashes: List) -> List:
    if len(tx_hashes) == 0:
        return []
    #what is this?
#    tx_hashes.append("82388254268f9887db936d20db89929f721d9cad4a5b1a1795bf05b2a511224c")
    # need decode_as_json to get actual vin and a vout values for transaction inputs and outputs
    transactions = rpc.raw_request('/get_transactions', {'txs_hashes': tx_hashes, "decode_as_json": True})
    txs = []
    for tx in transactions["txs"]:
        block_height = tx["block_height"]
        txs.append(transaction.from_json(tx["as_json"], block_height))
    return txs

def mempool():
    res = rpc.raw_request('/get_transaction_pool', {})
    txs = []
    for tx in res.get('transactions', []):
        block_height = -1 #using -1 for transaction pool
        fee = tx["fee"]
        print(fee)
        txs.append(transaction.from_json(tx["tx_json"], block_height))
    return txs


def headers(start_height, end_height = None):
    end_height = end_height or start_height
    res = rpc.raw_jsonrpc_request('get_block_headers_range', {
        'start_height': start_height,
        'end_height': end_height})
    if res['status'] == 'OK':
        return res['headers']
    raise Exception()
