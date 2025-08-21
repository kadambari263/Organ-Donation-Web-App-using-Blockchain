import hashlib
import json

blockchain_storage = []  # For demo only. In production, use a persistent system.

def save_to_blockchain(data):
    data_string = json.dumps(data, sort_keys=True).encode()
    block_hash = hashlib.sha256(data_string).hexdigest()
    blockchain_storage.append({"data": data, "hash": block_hash})
    print("Saved to blockchain with hash:", block_hash)
    return block_hash

def verify_on_blockchain(data):
    data_string = json.dumps(data, sort_keys=True).encode()
    check_hash = hashlib.sha256(data_string).hexdigest()
    return any(block["hash"] == check_hash for block in blockchain_storage)
