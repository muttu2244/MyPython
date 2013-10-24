#!/usr/bin/env python2.5
import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from CISCO import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger

class test_cisco_clear(test_case):
	myLog = getLogger()
	def setUp(self):
		self.cisco = CISCO("c4900m-15-con")
		self.cisco.console("c4900m-15-con")
	def tearDown(self):
		self.myLog.output("Cisco clearing done")
	def test_cisco_clear(self):
		cisco_intf = ("1/1","1/2","1/3","1/4","1/5","1/6","2/7","2/8","2/9","2/5","2/6","2/1","2/2","2/3","2/4","2/10","2/11","2/12","2/13","2/14","2/15","2/16","2/17","2/18","2/19","2/20") #populate the list with all the cisco interfaces connected to both SSX, ixia machine and all linux machines in use.
		for interf in cisco_intf:
			self.cisco.clear_interface_config(intf=interf)
			self.cisco.cmd("config t")
			self.cisco.cmd("interface gigabitEthernet %s"%interf)
		 	#self.cisco.cmd("switchport")
			#self.cisco.cmd("mtu 9000")
			self.cisco.cmd("no shutdown")
			self.cisco.cmd("no keepalive")
			self.cisco.cmd("no cdp enable")
			self.cisco.cmd("end")	
		
		self.cisco.cmd("config t")
		self.cisco.cmd("no monitor session all")
		self.cisco.cmd("no spanning-tree vlan 1-4094")
		self.cisco.cmd("end")

if __name__ == '__main__':
        filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_cisco_clear)
        test_runner(stream = sys.stdout).run(suite)

