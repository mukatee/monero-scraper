__author__ = 'teemu kanstren'

from datetime import datetime
from monero import rpc
from monero.transaction import Transaction, TxIn, TxOut, OutDetails
from decimal import Decimal
import json

PICONERO = Decimal('0.000000000001')

def from_atomic(amount):
    """Convert atomic integer of piconero to Monero decimal."""
    return (Decimal(amount) * PICONERO).quantize(PICONERO)

def info():
    info = rpc.raw_jsonrpc_request('get_info')
    return info


def get_block(hash = None, height = None):
    if hash is not None:
        res = rpc.raw_jsonrpc_request('get_block', {'hash': hash})
    else:
        res = rpc.raw_jsonrpc_request('get_block', {'height': height})
    return res

#https://monero.stackexchange.com/questions/3958/what-is-the-format-of-a-block-in-the-monero-blockchain
#https://monero.stackexchange.com/questions/7576/rpc-method-to-translate-key-offsets
#https://monero.stackexchange.com/questions/2136/understanding-the-structure-of-a-monero-transaction/2150#2150
def get_transactions(tx_hashes):
    # need decode_as_json to get actual vin and a vout values for transaction inputs and outputs
    transactions = rpc.raw_request('/get_transactions', {'txs_hashes': tx_hashes, "decode_as_json": True})
    tx_dicts = [json.loads(tx) for tx in transactions["txs_as_json"]]
    idx = 0
    for tx in tx_dicts:
        version = tx["version"]
        unlock_time = tx["unlock_time"] #the time when output is spendable
        inputs = tx["vin"]
        hash_hex = tx_hashes[idx]
        #TODO: is fee somewhere in the txouts?
        fee = 0
        t = Transaction(version, hash_hex, fee, unlock_time)
        #pop "gen" first
        for inp in inputs:
            key = inp["key"]
            key_offsets = key["key_offsets"]
            key_image = key["k_image"]
            amount = key["amount"]
            key_offsets_cum = [key_offsets[0]]
            for key in key_offsets[1:]:
                key_offsets_cum.append(key+key_offsets_cum[-1])
            out_params = []
            for key in key_offsets_cum:
                out_params.append({"amount": amount, "index": key})
            out_details = rpc.raw_request('/get_outs', {"outputs": out_params})
            out_detail_objs = []
            credits = out_details["credits"]
            untrusted = out_details["untrusted"]
            top_hash = out_details["top_hash"]
            for out in out_details["outs"]:
                out_obj = OutDetails(out["height"], out["key"], out["mask"], out["txid"], out["unlocked"])
                out_detail_objs.append(out_obj)
#            out_details = rpc.raw_request('/get_outs', {"outputs": [{'amount': amount, "index": key_offsets_cum}]})
            tx_in = TxIn(amount, key_offsets, key_image, out_detail_objs)
            t.tx_ins.append(tx_in)

        outputs = tx["vout"]
        for out in outputs:
            amount = out["amount"]
            target_key = out["target"]["key"]
            tx_out = TxOut(amount, target_key)
            t.tx_outs.append(tx_out)
        idx += 1

    return tx_dicts


def mempool():
    res = rpc.raw_request('/get_transaction_pool', {})
    txs = []
    for tx in res.get('transactions', []):
        txs.append(Transaction(
            hash_hex = tx['id_hash'],
            fee = from_atomic(tx['fee']),
            timestamp = datetime.utcfromtimestamp(tx['receive_time']),
            confirmations = 0))
    return txs


def headers(start_height, end_height = None):
    end_height = end_height or start_height
    res = rpc.raw_jsonrpc_request('get_block_headers_range', {
        'start_height': start_height,
        'end_height': end_height})
    if res['status'] == 'OK':
        return res['headers']
    raise Exception()
