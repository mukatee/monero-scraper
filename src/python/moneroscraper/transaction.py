__author__ = 'teemu kanstren'

from . import rpc
import json
from typing import List

#details about the output address for tx_out
class OutDetails:
    #blockchain height for this output
    height:int = None
    #public key of the output (?)
    key_hex:str = None
    #mask - a hex string but not sure yet what it is for
    mask_hex:str = None
    #this seems to be 0 in later transactions in the chain, earlier have to check..
    tx_id:int = None
    #is the transaction unlocked or not? i think it means the unlock time has passed and can be spent
    unlocked:bool = None

    def __init__(self, height, key_hex, mask_hex, tx_id, unlocked):
        self.height = height
        self.key_hex = key_hex
        self.mask_hex = mask_hex
        self.tx_id = tx_id
        self.unlocked = unlocked

    def __str__(self):
        return f"height={self.height},keyhex={self.key_hex},maskhex={self.mask_hex},txid={self.tx_id},unlocked={self.unlocked}"

    __repr__ = __str__

#details about a tx_in for a transaction
class TxIn:
    txin_id:int = None
    #amount of funds in tx_in. seems to be 0 later in the chain. have to check when it changed to 0.
    amount = None
    #offsets of keys to tx_out that this refers to. first offset is absolute, following are added on top of that. so [123,5] would mean [123, 128]
    key_offsets:List[int] = []
    #not sure what this is, have to check
    key_image = None
    #list of OutDetail objects. these describe the target receiver addresses etc
    out_details: List[OutDetails] = []
    #is this a coinbase txin?
    coinbase: bool = False

    def __init__(self, amount, key_offsets, key_image, out_details, coinbase = False):
        self.txin_id = None
        self.amount = amount
        self.key_offsets = key_offsets
        self.key_image = key_image
        self.out_details = out_details
        self.coinbase = coinbase

    def __str__(self):
        return f"txin_id={self.txin_id},amount={self.amount},keyoffs={len(self.key_offsets)},keyimg={self.key_image},out_details={len(self.out_details)},cb={self.coinbase}"

    __repr__ = __str__

#describes a tx_out. just the basic values
class TxOut:
    #amount in spent tx. seems to be 0 in later parts of the blockchain
    amount = None
    #the hash of the receiver target key
    target_key = None
    #in moneroscraper this is just xmr all the time, in xhv it can be different such as xhv, offshore, xasset, ...
    tx_type = None
    #in xhv you can produce different types of outputs
    asset_type = None

    def __init__(self, amount, target_key, tx_type, asset_type=None):
        self.amount = amount
        self.target_key = target_key
        self.tx_type = tx_type
        self.asset_type = asset_type

    def __str__(self):
        return f"amount={self.amount},tgtkey={self.target_key},tx_type={self.tx_type},asset_type={self.asset_type}"

    __repr__ = __str__

#the transaction itself, containing the txins, txouts, and the rest of the details
class Transaction:
    tx_id = None
    #the numerical index in block tx list
    idx: int = None
    #not sure what they mean, at this time the value seems to be 2
    version = None
    #hash of the transaction itself, not sure of details
    hash_hex: str = None
    #transaction fee for the miners? need to check how this goes with the txouts, is this put into one of them
    #this is available in the memory pool but not in the chain, which is why suspecting txout
    fee: int = None
    #height where this was included in block. sometimes called confirmations (chain length - block height = depth = confirmations)
    block_height: int = None
    #how much  time until this transaction can be spent (as tx_out)
    unlock_time: int = None
    #when was this transaction first seen
    receive_time: int = None
    #list of associated tx_ins for this transaction (existing tx_outs)
    tx_ins: List[TxIn] = None
    #list of tx_outs to generate from this transaction
    tx_outs: List[TxOut] = None
    #extra data, i guess it could be anything you want to embed in it, although some coins such as XHV user it for actual protocol purposes
    tx_extra: str = None
    #XHV: amount of XHV/xUSD burnt
    amount_burnt: int = None
    #XHV: amount of XHV/xUSD minted
    amount_minted: int = None

    def __init__(self, version, hash_hex, fee, unlock_time, receive_time, tx_extra):
        self.tx_id = None
        self.version = version
        self.hash_hex = hash_hex
        self.fee = fee
        self.block_height = None
        self.unlock_time = unlock_time
        self.receive_time = receive_time
        #these are needed to overwrite the lists or they will be class-level variables. ugh
        self.tx_ins = []
        self.tx_outs = []
        self.tx_extra = "".join(["%0.2X" % num for num in tx_extra])

    def __str__(self):
        return f"txid={self.tx_id},v={self.version},fee={self.fee},height={self.block_height},unlocktime={self.unlock_time},receivetime={self.receive_time},txins={len(self.tx_ins)},txouts={len(self.tx_outs)}"

    __repr__ = __str__

def from_json(tx_data, block_height, tx_hash, tx_idx, coin_type):
    if coin_type == 'xmr':
        return from_json_xmr(tx_data, block_height, tx_hash, tx_idx)
    elif coin_type == 'xhv':
        return from_json_xhv(tx_data, block_height, tx_hash, tx_idx)
    else:
        raise NotImplementedError(f'Unknown coin type given: {coin_type}')

def from_json_xmr(tx_data, block_height, tx_hash, tx_idx):
    coin_type = 'xmr'
    tx = json.loads(tx_data)
    # transaction version, havent found the version table yet
    version = tx["version"]
    unlock_time = tx["unlock_time"]  # the time when output is spendable
    hash_hex = tx_hash#tx["hash"]
    tx_extra = tx["extra"]
    fee = 0
    receive_time = None
    if "receive_time" in tx:
        receive_time = tx("receive_time")
    t = Transaction(version, hash_hex, fee, unlock_time, receive_time, tx_extra)
    t.idx = tx_idx
    t.block_height = block_height
    inputs = tx["vin"]
    for inp in inputs:
        if "gen" in inp:
            #a coinbase tx input. generating coins. appears to have no other info, and will have only one txout for miner (in monero)
            amount = 0
            key_offsets = []
            key_image = ""
            out_detail_objs = []
            tx_in = TxIn(amount, key_offsets, key_image, out_detail_objs, True)
            t.tx_ins.append(tx_in)
            continue
        # key is actually list of output key id's that are included as tx_ins in the transaction
        if "key" in inp:
            key = inp["key"]
        else:
            raise NotImplementedError(f"unknown input type: {inp}")
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
        target = out["target"]
        if "key" in target:
            target_key = target["key"]
            tx_out = TxOut(amount, target_key, coin_type)
            t.tx_outs.append(tx_out)
        else:
            raise NotImplementedError(f"Unknown tx type: {tx}")

    return t

def from_json_xhv(tx_data, block_height, tx_hash, tx_idx):
    tx = json.loads(tx_data)
    # transaction version, havent found the version table yet
    version = tx["version"]
    unlock_time = tx["unlock_time"]  # the time when output is spendable
    hash_hex = tx_hash#tx["hash"]
    tx_extra = tx["extra"]
    fee = 0
    receive_time = None
    if "receive_time" in tx:
        receive_time = tx("receive_time")
    t = Transaction(version, hash_hex, fee, unlock_time, receive_time, tx_extra)
    t.idx = tx_idx
    t.block_height = block_height
    if "amount_burnt" in tx:
        t.amount_burnt = tx["amount_burnt"]
        t.amount_minted = tx["amount_minted"]
    else:
        t.amount_burnt = 0
        t.amount_minted = 0
    inputs = tx["vin"]
    for inp in inputs:
        if "gen" in inp:
            #a coinbase tx input. generating coins. appears to have no other info, and will have only one txout for miner (in monero)
            amount = 0
            key_offsets = []
            key_image = ""
            out_detail_objs = []
            tx_in = TxIn(amount, key_offsets, key_image, out_detail_objs, True)
            t.tx_ins.append(tx_in)
            continue
        # key is actually list of output key id's that are included as tx_ins in the transaction
        if "key" in inp:
            key = inp["key"]
        elif "offshore" in inp:
            key = inp["offshore"]
        elif "onshore" in inp:
            key = inp["onshore"]
        elif "xasset" in inp:
            key = inp["xasset"]
        else:
            raise NotImplementedError(f"unknown asset type: {inp}")
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
        target = out["target"]
        if "key" in target:
            target_key = target["key"]
            tx_out = TxOut(amount, target_key, "XHV")
            t.tx_outs.append(tx_out)
        elif "offshore" in target:
            target_key = target["offshore"]
            tx_out = TxOut(amount, target_key, "offshore", "xUSD")
            t.tx_outs.append(tx_out)
        elif "xasset" in target:
            target_xasset = target["xasset"]
            tx_out = TxOut(amount, target_xasset["key"], "xasset", target_xasset["asset_type"])
            t.tx_outs.append(tx_out)
        else:
            raise NotImplementedError(f"Unknown tx type: {tx}")

    return t

#TODO: needs to add coin_burned, coin_minted to table