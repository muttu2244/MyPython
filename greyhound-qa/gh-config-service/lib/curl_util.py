#!/usr/bin/python26
import subprocess
import pycurl
import simplejson as json
import StringIO
import time,os
from constants import constants
def sendRequest(url, data = None, headers = None, cred=''):
	
	ch = pycurl.Curl()
	ch.setopt(pycurl.URL, url)
	ch.setopt(pycurl.TIMEOUT, 300)
	ch.setopt(pycurl.SSL_VERIFYPEER, 0)
	ch.setopt(pycurl.SSL_VERIFYHOST, 0)
	header = ["Expect:", "Connection: Keep-Alive", "Content-Type: application/json"]
	if headers:
		header += headers
	ch.setopt(pycurl.HTTPHEADER, header)
	if data:
		ch.setopt(pycurl.POST, 1)
		postbody = json_encode(data)
		ch.setopt(pycurl.POSTFIELDS, postbody)
	
	if cred:
		ch.setopt(pycurl.USERPWD, cred)

	buf = StringIO.StringIO()
	ch.setopt(pycurl.WRITEFUNCTION, buf.write)	
	try:
		ch.perform()
	except Exception:
		return False, constants.HTTP_FAILED 
	err = ch.getinfo(pycurl.HTTP_CODE)
	output = buf.getvalue()
	buf.close()
	ch.close()
	if err == 500:
		return False, constants.ERROR_INTERNAL
	if err == 200:
		return json_decode(output)
	return False, constants.HTTP_ERROR.format(err)
	

def json_encode(data):
	return json.dumps(data)

def json_decode(data):
	try:
		ret = json.loads(data)
	except Exception:
		#ret = "Cant decode data"
		#TODO Logging of the error message
		return False, constants.DECODE_FAILED
	return True, ret

def runJobAndWait(cmd=None, wait=30):
	#command = "sudo php -d hidef.data_path=no /opt/zynga/overmind/client/bin/overmindClient.php OVERMIND_CONFIG=greyhound >> /var/log/overmind/greyhound.log  2>&1 &"
	#if cmd:
		#command = cmd
	#p = subprocess.Popen(command, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)
	#while True:
		#ret = p.poll()
		#if ret is not None:
			#break
	#os.system(command)
	time.sleep(wait)
	

if __name__ == "__main__":
	output = sendRequest("http://ghqacluster-staging-web-2.zc1.zynga.com/srv/get")
	print output
	
