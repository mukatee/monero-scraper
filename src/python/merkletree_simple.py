from Crypto.Hash import keccak

#keccak is the winning hash function of SHA3 competition, and popular in many cryptocurrencies
def keccak_bytes(hash_bin):
    k = keccak.new(digest_bits=256)
    k.update(hash_bin)
    return k.hexdigest()

#hash_pair() returns array[start] if start points to last element. else keccak(array[start]+array[start+1])
#array parameter is a list of hashes in hexadecimal string format. return is a hash in same hex format.
def hash_pair(array, start):
    if array[start] == array[-1]: return array[start]
    merged_pair = "".join(array[start:start+2])
    merge_hash = keccak_bytes(bytes.fromhex(merged_pair))
    return merge_hash

def merkletree(input_hashes):
    #recursively hashes pair in input list, until there is only one left; the merkle root.
    print(f"hashing: {input_hashes}")
    new_hashes = []

    for x in range(0, len(input_hashes), 2):
        new_hash = hash_pair(input_hashes, x)
        new_hashes.append(new_hash)

    if len(new_hashes) > 1:
        return merkletree(new_hashes)
    #only comes here after there is only one hash left, which is the merkle root. return that.
    return new_hashes[0]

def concat_hash_only(leaf_nodes):
    input_str = "".join(leaf_nodes)
    return keccak_bytes(bytes(input_str, 'utf8'))

leaf_nodes = ["Data1", "Data2", "Data3", "Data4", "Data5"]
leaf_hashes = [keccak_bytes(bytes(leaf_data, 'utf8')) for leaf_data in leaf_nodes]
merkle_root = merkletree(leaf_hashes)
print(f"root: {merkle_root}")
print(f"hash concat only: {concat_hash_only(leaf_nodes)}")