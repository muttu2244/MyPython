#! /usr/bin/env python2.6

import base64
import hashlib
import sys
import hmac
import socket
import base64
import struct

from time import time as now

def main(gid, zid, expire_in):
  #SECRET = 'c998c9a1be742384644e2c2d2648353f5de75cf3'
  SECRET = 'c58b3bc0c1b0f3ca8e13b388fedc6c73aa36b330' 
  expire = int(expire_in)  
  secret = SECRET[::-1]

  expire_time = int(now() + expire)
  authbits = 8
  authbits_str = base64.encodestring(struct.pack("I", socket.htonl(authbits)))
  token = str(gid) + ":" + str(zid) + "." + str(expire_time) + "." + authbits_str.strip()
  sig = base64.encodestring(hmac.new(secret, msg=token, digestmod=hashlib.sha256).digest()).strip()
  print token + "|" + sig
  return token + "|" + sig

if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2], sys.argv[3])

