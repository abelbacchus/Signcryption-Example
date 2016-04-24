#!/usr/bin/python
import sys
from binascii import hexlify
import pyelliptic
import json


ecc = pyelliptic.ECC(curve='secp521r1')
pubkey = hexlify(ecc.get_pubkey())
obj = {'pubkey':pubkey}

with open ('./values/pubkey.json', 'w') as file:
  json.dump(obj, file)
file.close()

privkey = hexlify(ecc.get_privkey())
obj = {'privkey':privkey}
with open ('privkey.json', 'w') as file:
  json.dump(obj, file)
file.close()
