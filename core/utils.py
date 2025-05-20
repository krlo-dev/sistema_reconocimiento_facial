import pickle

def encode_to_bytes(encoding):
    return pickle.dumps(encoding)

def decode_from_bytes(blob):
    return pickle.loads(blob)
