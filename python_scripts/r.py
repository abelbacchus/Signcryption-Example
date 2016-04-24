#!/usr/bin/python
#import required libraries
import sys
from binascii import unhexlify,  hexlify
import struct
import pyelliptic
import requests
import json

url = "http://"
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
#Generate Elliptic Curve
ecc = pyelliptic.ECC(privkey=myPrivkey, pubkey=myPubkey ,curve='secp521r1')
#Get Receiver public key
r = requests.get(url+"/values/pubkey.json")
senderPubkey = unhexlify (r.json()["pubkey"])


#Generate Shared key
sharedKey = hexlify (ecc.get_ecdh_key (senderPubkey))
print "Shared Key: ", sharedKey

#Get arguments

ciphertext = unhexlify (sys.argv [1])
signature = unhexlify (sys.argv [2])
iv = sys.argv [3]

#print "Signature: ", hexlify (signature)
#decrypt Message
ctx = pyelliptic.Cipher("secretkey", iv, 1, ciphername='aes-256-cfb')
message = ctx.ciphering (ciphertext)
print "Decrypted Message: ", message
print "Signature Verified", pyelliptic.ECC(pubkey=senderPubkey, curve=myCurve).verify (signature, message)

