import base64
import hashlib
import sys
import hmac
import socket
import base64
import struct

from time import time as now

def main(gid, zid, expire_in):
  #SECRET = 'c58b3bc0c1b0f3ca8e13b388fedc6c73aa36b330'
  SECRET = '10c6072f24599bf286350f635f8640a26d0f2457'
  expire = int(expire_in)  

  expire_time = int(now() + expire)
  print now()
  print expire
  authbits = 0
  authbits_str = base64.encodestring(struct.pack("I", socket.htonl(authbits)))
  #token = str(gid) + ":" + str(zid) + "." + str(expire_time) + "." + authbits_str.strip()
  token = str(gid) + ":" + str(zid) + "." + str(expire_time) + "." + authbits_str.strip()
  sig = base64.encodestring(hmac.new(SECRET, msg=token, digestmod=hashlib.sha256).digest()).strip()
  print token + "|" + sig
  return token + "|" + sig

if __name__ == '__main__':
  main(sys.argv[1], sys.argv[2], sys.argv[3])

