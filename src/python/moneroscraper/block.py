__author__ = 'teemu kanstren'

from .transaction import Transaction
from typing import Dict, List

#following fields seem to be from "json" field copied into block_header:
#- major_version
#- minor_version
#- timestamp
#- prev_id/prev_hash
#- nonce

class Block:
    #-- from rpc msg header --
    block_size = 0
    block_weight = 0
    cumulative_difficulty = 0
    cumulative_difficulty_top64 = 0
    difficulty = 0
    difficulty_top64 = 0
#    depth...
    hash = ""
    height = 0
    long_term_weight = 0
    miner_tx_hash = ""
    major_version = 0
    minor_version = 0
    nonce = 0
    num_txes = 0
    #same as prev_id?
    prev_hash = ""
    timestamp = 0
    reward = 0
    wide_cumulative_difficulty = ""
    wide_difficulty = ""
    blockhashing_blob = ""

    #-- from rpc msg "top level"
    credits = 0
    status = ""
    top_hash = ""
    untrusted = ""
    miner_tx: Transaction = None
    txs: List[Transaction] = None
    miner_tx_hash_list: List[str] = None
    tx_hashes: List[str] = None

    def __init__(self, rpc_dict: Dict):
        header = rpc_dict["block_header"]
        self.height = header["height"]
        self.block_size = header["block_size"]
        self.block_weight = header["block_weight"]
        self.cumulative_difficulty = header["cumulative_difficulty"]
        self.cumulative_difficulty_top64 = header["cumulative_difficulty_top64"]
        self.difficulty = header["difficulty"]
        self.difficulty_top64 = header["difficulty_top64"]
        self.hash = header["hash"]
        self.long_term_weight = header["long_term_weight"]
        self.miner_tx_hash = rpc_dict["miner_tx_hash"]
        self.major_version = header["major_version"]
        self.nonce = header["nonce"]
        self.num_txes = header["num_txes"]
        self.prev_hash = header["prev_hash"]
        self.reward = header["reward"]
        self.timestamp = header["timestamp"]
        self.wide_cumulative_difficulty = header["wide_cumulative_difficulty"]
        self.wide_difficulty = header["wide_difficulty"]
        self.credits = rpc_dict["credits"]
        self.status = rpc_dict["status"]
        self.top_hash = rpc_dict["top_hash"]
        self.untrusted = rpc_dict["untrusted"]
        self.miner_tx_hash_list = [header["miner_tx_hash"]]
        if len(self.miner_tx_hash_list) > 1:
            #TODO: use logger
            print(f"!!! height={self.height}, miner tx list is larger than 1: {self.miner_tx_hash_list}")
        self.tx_hashes = rpc_dict["tx_hashes"]
        #the blockhashing blob is there only if you run a specially patched daemon. made on for myself to check the merkle calculations
        if "blockhashing_blob" in rpc_dict:
            self.blockhashing_blob = rpc_dict["blockhashing_blob"]
        pass
