import os
import pickle

def load_data(file_name):
    file_path = os.path.join(os.path.dirname(__file__), 'data', file_name)
    with open(file_path, 'rb') as f:
        return pickle.load(f)

KMAP = load_data('kmap.pkl')
ALOHA_MAP = load_data('aloha_map.pkl')

DECODE_KMAP = {v: k for k, v in KMAP.items()}
DECODE_ALOHA_MAP = {v: k for k, v in ALOHA_MAP.items()}

def check_invalid(mesaage):
    for char in mesaage:
        if char not in KMAP:
            return True
    return False

def encode_one(message):
    encoded_message = ""
    for char in message:
        if char in KMAP:
            encoded_message += KMAP[char]
        else:
            continue
    return encoded_message.strip()

def encode_two(message):
    encoded_message = ""

    for char in message:
        if char in ALOHA_MAP:
            encoded_message += ALOHA_MAP[char]
        else:
            encoded_message += char

    return encoded_message.strip()

def encode_three(message):
    encoded_message = ""
    counter = 1

    for i in range(0, len(message) - 1):
        if message[i] == message[i + 1]:
            counter += 1
        else:
            if counter == 1:
                encoded_message += message[i]
            else:
                encoded_message += str(counter) + message[i]
            counter = 1

    if counter == 1:
        encoded_message += message[-1]
    else:
        encoded_message += str(counter) + message[-1]

    return encoded_message.strip()

def hasher(message):
    encoded_message = ""

    for char in message:
        if char in ALOHA_MAP:
            encoded_message += ALOHA_MAP[char]
        else:
            encoded_message += char

    hashText = encoded_message
    hash_length=32

    if len(hashText) < hash_length:
        hashText += (hash_length - len(hashText)) * '#'
    elif len(hashText) > hash_length:
        hashText = hashText[:hash_length]

    transformed = [0] * hash_length
    for i in range(len(hashText)):
        transformed[i % hash_length] ^= ord(hashText[i])

    for i in range(hash_length):
        transformed[i] = (transformed[i] + i) % 256

    fixed_length_hash = ''.join([format(x, '02x') for x in transformed])

    
    fixed_length_hash = fixed_length_hash[:32]
    return fixed_length_hash

def decode_one(message):
    decoded_message = ""
    for i in range(0, len(message), 4):
        decoded_message += DECODE_KMAP[message[i:i + 4]]

    return decoded_message.strip()

def decode_two(message):
    decoded_message = ""

    for char in message:
        if char in DECODE_ALOHA_MAP:
            decoded_message += DECODE_ALOHA_MAP[char]
        else:
            decoded_message += char

    return decoded_message.strip()

def decode_three(message):
    decoded_message = ""
    i = 0

    while i < len(message):
        if message[i].isdigit():
            decoded_message += int(message[i]) * message[i + 1]
            i += 2
        else:
            decoded_message += message[i]
            i += 1

    return decoded_message.strip()

def encode(message):
    if(not check_invalid(message)):
       enmsone = encode_one(message)
       enmstwo = encode_two(enmsone)
       enmsthree = encode_three(enmstwo)
       return enmsthree

def hash(message):
    if(not check_invalid(message)):
       enmsone = encode_one(message)
       enmstwo = encode_two(enmsone)
       enmsthree = encode_three(enmstwo)
       hashstr = hasher(enmsthree)
       return hashstr
    
def compare(message,hash):
    if(not check_invalid(message)):
        enmsone = encode_one(message)
        enmstwo = encode_two(enmsone)
        enmsthree = encode_three(enmstwo)
        hashstr = hasher(enmsthree)
       
        if(hashstr == hash):
            return True
        else:
            return False     

def decode(message):
    if(not check_invalid(message)):
        print("Decoding")
        
        Dec3 = decode_three(message)
        Dec2 = decode_two(Dec3)
        Dec1 = decode_one(Dec2)
        return Dec1

    else:
        return "Invalid message"
