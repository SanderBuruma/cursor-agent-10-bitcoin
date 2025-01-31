import hashlib
from mnemonic import Mnemonic
from bitcoin import *
import os

# Initialize mnemonic generator
mnemo = Mnemonic('english')

# Try to read words from phrase.txt, generate new ones if file doesn't exist
if os.path.exists('phrase.txt'):
    with open('phrase.txt', 'r') as f:
        words = f.read().strip()
else:
    words = mnemo.generate(128)

# Generate seed
seed = mnemo.to_seed(words)

# Generate private key
priv = hashlib.sha256(seed).hexdigest()

# Generate public key and address
pub = privtopub(priv)
addr = pubtoaddr(pub)

print(f'Mnemonic: {words}')
print(f'Private key: {priv}')
print(f'Public key: {pub}')
print(f'Address: {addr}')
