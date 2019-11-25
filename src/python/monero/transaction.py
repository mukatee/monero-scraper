__author__ = 'teemu kanstren'

class OutDetails:
    height = None
    key_hex = None
    mask_hex = None
    tx_id = None
    unlocked = None

    def __init__(self, height, key_hex, mask_hex, tx_id, unlocked):
        self.height = height
        self.key_hex = key_hex
        self.mask_hex = mask_hex
        self.tx_id = tx_id
        self.unlocked = unlocked

class TxIn:
    amount = None
    key_offsets = []
    key_image = None
    out_details = []

    def __init__(self, amount, key_offsets, key_image, out_details):
        self.amount = amount
        self.key_offsets = key_offsets
        self.key_image = key_image
        self.out_details = out_details

class TxOut:
    amount = None
    target_key = None

    def __init__(self, amount, target_key):
        self.amount = amount
        self.target_key = target_key

class Transaction:
    version = None
    hash_hex = None
    fee = None
    #height where this was included in block. sometimes called confirmations
    block_height = None
    unlock_time = None
    tx_ins = []
    tx_outs = []

    def __init__(self, version, hash_hex, fee, unlock_time):
        self.version = version
        self.hash_hex = hash_hex
        self.fee = fee
        self.unlock_time = unlock_time