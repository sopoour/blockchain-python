import hashlib as hl
import json

def hash_string_256(string):
    return hl.sha3_256(string).hexdigest()

def hash_block(block):
    #OLD: Simple non-secure hashing of a block = append all key values into one string:
    # Previously, for loop to create a hashed_block
    # hashed_block = ''
    # for key in last_block:
    #     value = last_block[key]
    #     hashed_block = hashed_block + str(value)

    # use list comprehension for that instead of a separate for loop:
    # hashed_block = str([last_block[key] for key in last_block]) --> Problem: you get the brackets of list also stringified "["['', 0, []]", 1, [{'sender': 'Sophia', 'recipient': 'Anna', 'amount': 5.6}]]"
    # Better: use join method to add a character ("-") together with the list where the last_block[key] must be a string
    # return "-".join([str(block[key]) for key in block])

    #when using classes and objects, we need to first convert the object to a dict in order to be hashable:
    hashable_block = block.__dict__.copy()

    #the above conversion doesn't convert every other element in the block (nesting), meaning that if the block has an attribute like transaction, that holds another list of elements, it is not converted to a dict
    #therefore we need to manipulate that dict block (that's why we use copy())
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    #NEW: using proper unique hashing
    #sha256: algorithm that creates a 64 character hash and will ensure that the same input always leads to the same hash in order to recalculate and compare the hash in the verify_chain function properly
    #json.dump: since the block is a dictionary but sha256 needs a string we use json.dumps in order to stringify it by converting it to a JSON formated String
    #encode: to then really encode the block to UTF8 which can be read by sha256
    #hexdigest: the returned hash is actually not a string but a bite hash so we need to convert it to a normal string with hexdigest
    #sort_keys: ensures that even though the order of the dictionary might change, it always leads to the same string by first sorting it 
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())