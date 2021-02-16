from Crypto.Hash import keccak
import hashlib
import math
from monero import jsonapi, rpc

#assuming you run a local daemon. any remote should work too.
rpc.init(_host="localhost")
daemon = jsonapi
#merkle tree root is hash_blob itself, since block 1 only has 1 tx, the coinbase
hash_blob = daemon.get_coinbase_hash(1)
print(hash_blob)

#tree_hash: https://github.com/monero-project/monero/blob/8286f07b265d16a87b3fe3bb53e8d7bf37b5265a/src/crypto/tree-hash.c
#cn_fast_hash: https://github.com/monero-project/monero/blob/8286f07b265d16a87b3fe3bb53e8d7bf37b5265a/src/crypto/hash.c

def keccak_this(data_to_hash):
    k = keccak.new(digest_bits=256)
    hash_bin = bytes.fromhex(data_to_hash)
    k.update(hash_bin)
    return k.hexdigest()

def hash_pair(array, start):
    item1 = array[start]
    item2 = ''
    #if item1 is last element, just hash it alone. else take next hash for concatenation
    if start + 1 < len(array):
        item2 = array[start + 1]
    merged = item1 + item2
    merge_hash = keccak_this(merged)
    return merge_hash


def merkletree_naive(input_hashes):
    print(f"hashing: {input_hashes}")
    new_hashes = []

    for x in range(0, len(input_hashes), 2):
        new_hash = hash_pair(input_hashes, x)
        new_hashes.append(new_hash)

    if len(new_hashes) > 1:
        return merkletree_naive(new_hashes)
    return new_hashes[0]

#find the first x for 2^x that is larger than n
def find_nearest_pow(n):
    pow = 1
    powed = math.pow(2, pow)
    while powed < n:
        pow += 1
        powed = math.pow(2, pow)
    #this should now be the power of 2 that gives maximum value that is still less than n
    return pow - 1 #math.pow(2, pow - 1)

#this is the XMR merkle tree build function in python. i guess same also for cryptonote
def merkletree_xmr(input_hashes):
    print(f"hashing: {input_hashes}")
    hashes = input_hashes.copy()
    n_inputs = len(input_hashes)
    if n_inputs == 1:
        #arrived at root, return it
        return input_hashes[0]
    if n_inputs == 2:
        return hash_pair(input_hashes, 0)
    pow = find_nearest_pow(n_inputs)
    powed = math.pow(2, pow)
    #
    start_idx = int(2*powed) - n_inputs
    count = 0
    # if you read the medium article, start_idx is the first index of iteration 1
    for x in range(start_idx, n_inputs, 2):
        hashes[x-count] = hash_pair(input_hashes, x)
        count += 1
    # iteration 1 above should always make the range a power of 2 (2^x), thus divisible by 2
    # see the medium article for more details
    while (pow > 1):
        pow -= 1
        #powed should always be whole number here since powed is a factor of 2 from above
        powed = int(math.pow(2, pow))
        count = 0
        for x in range(0, powed*2, 2):
            hashes[x - count] = hash_pair(hashes, x)
            count += 1
    return hash_pair(hashes, 0)


b = daemon.get_block(height=1407480)
"""
i,j,count,cnt
starting tree hashstarting tree hash
9,9,23,16
11,10,23,16
13,11,23,16
15,12,23,16
17,13,23,16
19,14,23,16
21,15,23,16
2: 0,0,23,8
2: 2,1,23,8
2: 4,2,23,8
2: 6,3,23,8
2: 8,4,23,8
2: 10,5,23,8
2: 12,6,23,8
2: 14,7,23,8
2: 0,0,23,4
2: 2,1,23,4
2: 4,2,23,4
2: 6,3,23,4
2: 0,0,23,2
2: 2,1,23,2

20c0034a87f005f0000000b0c6034a87f00a0b7143a87f00
"""
all_hashes = []
all_hashes.append(b.miner_tx_hash)
all_hashes.extend(b.tx_hashes)
print(f"hashes={len(all_hashes)}")
merkle_root = merkletree_xmr(all_hashes)
print(merkle_root)
