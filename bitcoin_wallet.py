import hashlib
from mnemonic import Mnemonic
from bitcoin import *
import os
from hashlib import pbkdf2_hmac
import base58

def privkey_to_wif(priv_hex):
    # Add version byte (0x80 for mainnet)
    extended_key = "80" + priv_hex
    # Add compression byte
    extended_key += "01"
    # Perform double SHA256
    first_sha256 = hashlib.sha256(bytes.fromhex(extended_key)).hexdigest()
    second_sha256 = hashlib.sha256(bytes.fromhex(first_sha256)).hexdigest()
    # Add checksum (first 4 bytes of double SHA256)
    final_key = extended_key + second_sha256[:8]
    # Encode in base58
    wif = base58.b58encode(bytes.fromhex(final_key)).decode('utf-8')
    return wif

# Initialize mnemonic generator
mnemo = Mnemonic('english')

# Try to read words from phrase.txt, generate new ones if file doesn't exist
if os.path.exists('phrase.txt'):
    with open('phrase.txt', 'r') as f:
        words = f.read().strip()
else:
    words = mnemo.generate(128)

# Convert mnemonic to seed using PBKDF2
password = words.encode('utf-8')
salt = b'mnemonic'  # BIP39 standard salt
seed = pbkdf2_hmac('sha512', password, salt, 2048)  # 2048 iterations per BIP39

# Generate private key
priv = hashlib.sha256(seed).hexdigest()

# Convert private key to WIF format
wif_priv = privkey_to_wif(priv)

# Generate public key and address
pub = privtopub(priv)
addr = pubtoaddr(pub)

print(f'Mnemonic: {words}')
print(f'Private key (hex): {priv}')
print(f'Private key (WIF): {wif_priv}')
print(f'Public key: {pub}')
print(f'Address: {addr}')
