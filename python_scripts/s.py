#!/usr/bin/python
#import required libraries
import sys
from binascii import unhexlify
from binascii import hexlify
import pyelliptic
import requests
import json

url = "http://"
#Message to be sent
message = sys.argv [1]

#Determines Host to communicate with
with open ('config.json', 'r') as file:
	data = json.load (file)
	url += data["receiverHost"]+":"+str(data["port"])
	file.close()


myPrivkey =""
myPubkey = ""
myCurve = "secp521r1"
with open ('privkey.json', 'r') as file:
  data = json.load (file)
  myPrivkey = unhexlify (data["privkey"])
file.close()

with open ('./values/pubkey.json', 'r') as file:
  data = json.load (file)
  myPubkey = unhexlify (data["pubkey"])
file.close()

ecc = pyelliptic.ECC(privkey=myPrivkey, pubkey=myPubkey ,curve='secp521r1')

#Get Receiver public key

r = requests.get(url+"/values/pubkey.json")
receiverPubkey = unhexlify (r.json()["pubkey"])

#Generate Shared key
sharedKey = ecc.get_ecdh_key (receiverPubkey)

#Sign Message
signature = ecc.sign (message)

#Encrypt Message
# Symmetric encryption
iv = pyelliptic.Cipher.gen_IV('aes-256-cfb')
ctx = pyelliptic.Cipher(sharedKey, iv, 1, ciphername='aes-256-cfb')
ciphertext = ctx.update(message)
ciphertext += ctx.final()

print "Shared Key: ", hexlify (sharedKey)

#Send Signature, Ciphertext and Public Key
payload = {"ciphertext": ciphertext, "signature": signature, "pubkey": hexlify(ecc.get_pubkey())}
r = requests.post (url+"/receive", data=payload)
print r.text

