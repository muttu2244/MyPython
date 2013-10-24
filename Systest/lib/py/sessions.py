#!/usr/bin/python2.5

### Import the system libraries we need.
import sys, os, re, time

### path.
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)
from logging import getLogger
# grab the root logger.
log = getLogger()

def check_phase1_policy(self, remote_ip="17.1.2.1", encr="AES128", hash="SHA-1", dh="2", prf="SHA-1"):
        """Checks Ike-session details for policy configuration"""
	output=self.cmd("show ike-session detail remote %s | grep \"IKE-SA sec policy             :\""%remote_ip)
	if encr not in output :
		return False
	if hash not in output :
		return False
	if "D-H group %s"%(dh) not in output :
		return False

	output=self.cmd("show ike-session detail remote %s | grep \"IKE-SA PRF                    :\""%remote_ip)
	if prf not in output :
		return False
	return True

def check_phase2_policy(self, remote_ip="17.1.2.1", encr="AES128", hash="SHA-1"):
	"""Checks Ike-session details for policy configuration"""
	output=self.cmd("show ike-session detail remote %s | grep \"Child-SA sec policy           :\""%remote_ip)
        if encr not in output :
                return False
        if hash not in output :
                return False
	return True


