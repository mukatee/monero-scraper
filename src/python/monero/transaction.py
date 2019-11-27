__author__ = 'teemu kanstren'

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
    key_offsets = []
    #not sure what this is, have to check
    key_image = None
    #list of OutDetail objects. these describe the target receiver addresses etc
    out_details = []

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
    #hash of the transaction itself, "id" if nothing else (key?)
    hash_hex = None
    #transaction fee for the miners? need to check how this goes with the txouts, is this put into one of them
    fee = None
    #height where this was included in block. sometimes called confirmations
    block_height = None
    #how much  time until this transaction can be spent (as tx_out)
    unlock_time = None
    #list of associated tx_ins for this transaction (existing tx_outs)
    tx_ins = []
    #list of tx_outs to generate from this transaction
    tx_outs = []

    def __init__(self, version, hash_hex, fee, unlock_time):
        self.version = version
        self.hash_hex = hash_hex
        self.fee = fee
        self.unlock_time = unlock_time