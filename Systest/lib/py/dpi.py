#!/usr/bin/python2.5

### Import the system libraries we need.
import sys, os, re

### path.
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)
from logging import getLogger
# grab the root logger.
log = getLogger()



def compareMultiStr(self, str1, str2 ):
        """Compares two multiple strings and returns TRUE if matched"""
        inputConfig = str1
        outputConfig = str2

        expected = [item.strip() for item in inputConfig.split("\n")
                   if item != str()]
        actual = [item.strip() for item in outputConfig.split("\r\n")
                   if item != str()]
	if expected == actual:
		return True
	else:
		return False

def get_ses_counters_qos(self):
        lines= self.cmd("show session counters qos class-of-service")
        if lines and "ERROR:" not in lines:
              split_lines=lines.splitlines()[-1].split()
              rx_pkts=split_lines[3]
              tx_pkts=split_lines[4]
              return int(rx_pkts), int(tx_pkts)
        else:
           return False

