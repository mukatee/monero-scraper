__author__ = 'teemu kanstren'

from . import rpc
import json
from typing import List

#details about the output address for tx_out
class OutDetails:
    #blockchain height for this output
    height = None
    #public key of the output (?)
    key_hex = None
    #mask - a hex string but not sure yet what it is for
    mask_hex = None
    #this seems to be 0 in later transactions in the chain, earlier have to check..
    tx_id = None
    #is the transaction unlocked or not? i think it means the unlock time has passed and can be spent
    unlocked = None

    def __init__(self, height, key_hex, mask_hex, tx_id, unlocked):
        self.height = height
        self.key_hex = key_hex
        self.mask_hex = mask_hex
        self.tx_id = tx_id
        self.unlocked = unlocked

#details about a tx_in for a transaction
class TxIn:
    #amount of funds in tx_in. seems to be 0 later in the chain. have to check when it changed to 0.
    amount = None
    #offsets of keys to tx_out that this refers to. first offset is absolute, following are added on top of that. so [123,5] would mean [123, 128]
    key_offsets:List[int] = []
    #not sure what this is, have to check
    key_image = None
    #list of OutDetail objects. these describe the target receiver addresses etc
    out_details: List[OutDetails] = []

    def __init__(self, amount, key_offsets, key_image, out_details):
        self.amount = amount
        self.key_offsets = key_offsets
        self.key_image = key_image
        self.out_details = out_details

#describes a tx_out. just the basic values
class TxOut:
    #amount in spent tx. seems to be 0 in later parts of the blockchain
    amount = None
    #the hash of the receiver target key
    target_key = None

    def __init__(self, amount, target_key):
        self.amount = amount
        self.target_key = target_key

#the transaction itself, containing the txins, txouts, and the rest of the details
class Transaction:
    #not sure what they mean, at this time the value seems to be 2
    version = None
    #hash of the transaction itself, not sure of details
    hash_hex = None
    #transaction fee for the miners? need to check how this goes with the txouts, is this put into one of them
    #this is available in the memory pool but not in the chain, which is why suspecting txout
    fee = None
    #height where this was included in block. sometimes called confirmations (chain length - block height = depth = confirmations)
    block_height = None
    #how much  time until this transaction can be spent (as tx_out)
    unlock_time = None
    #when was this transaction first seen
    receive_time = None
    #list of associated tx_ins for this transaction (existing tx_outs)
    tx_ins: List[TxIn] = []
    #list of tx_outs to generate from this transaction
    tx_outs: List[TxOut] = []

    def __init__(self, version, hash_hex, fee, unlock_time, receive_time):
        self.version = version
        self.hash_hex = hash_hex
        self.fee = fee
        self.unlock_time = unlock_time
        self.receive_time = receive_time

def from_json(tx_data, block_height):
    tx = json.loads(tx_data)
    # transaction version, havent found the version table yet
    version = tx["version"]
    unlock_time = tx["unlock_time"]  # the time when output is spendable
    hash_hex = ""#tx["hash"]
    fee = 0
    receive_time = None
    if "receive_time" in tx:
        receive_time = tx("receive_time")
    t = Transaction(version, hash_hex, fee, unlock_time, receive_time)
    t.block_height = block_height
    inputs = tx["vin"]
    for inp in inputs:
        if "gen" in inp:
            #a coinbase tx input. generating coins. appears to have no other info, and will have only one txout for miner
            amount = -1
            key_offsets = -1
            key_image = ""
            out_detail_objs = None
            tx_in = TxIn(amount, key_offsets, key_image, out_detail_objs)
            t.tx_ins.append(tx_in)
            continue
        # key is actually list of output key id's that are included as tx_ins in the transaction
        key = inp["key"]
        key_offsets = key["key_offsets"]
        key_image = key["k_image"]
        amount = key["amount"]
        key_offsets_cum = [key_offsets[0]]
        for key in key_offsets[1:]:
            key_offsets_cum.append(key + key_offsets_cum[-1])
        out_params = []
        for key in key_offsets_cum:
            # the api for get_outs requires amount and index. earlier in the chain amount is there, later not.
            out_params.append({"amount": amount, "index": key})
        out_details = rpc.raw_request('/get_outs', {"outputs": out_params})
        out_detail_objs = []
        # credits is not mentioned in daemon api docs
        credits = out_details["credits"]
        # if obtained in bootstrap mode, labeled as untrusted (daemon api docs...)
        untrusted = out_details["untrusted"]
        # top hash is not mentioned in daemon api docs
        top_hash = out_details["top_hash"]
        for out in out_details["outs"]:
            # output keys are receiver stealth address public keys
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

    return t
