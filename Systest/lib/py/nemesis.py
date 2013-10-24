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


def send_udp_nemesis(self, src="17.1.1.1", dst="18.1.1.1", send_pkts="5", dev="eth2", src_port="500", dst_port="500") :
	output = self.cmd("whereis nemesis")
	if "/usr/local/bin/" not in output :
		return False
	else :
		count=0
		while count < int(send_pkts) :
			self.cmd("sudo /usr/local/bin/nemesis udp -D %s -S %s -x %s -y %s -d %s"%(dst,src,src_port,dst_port,dev))
			count = count + 1
		return True

	
def send_igmp_nemesis(self, src="17.1.1.1", dst="18.1.1.1", send_pkts="5", dev="eth2") :
	output = self.cmd("whereis nemesis")
        if "/usr/local/bin/" not in output :
                return False
        else :
                count=0
                while count < int(send_pkts) :
                        self.cmd("sudo /usr/local/bin/nemesis igmp -D %s -S %s -d %s"%(dst,src,dev))
                        count = count + 1
                return True

def send_tcp_nemesis(self, src="17.1.1.1", dst="18.1.1.1", send_pkts="5", dev="eth2") :
        output = self.cmd("whereis nemesis")
        if "/usr/local/bin/" not in output :
                return False
        else :
                count=0
                while count < int(send_pkts) :
                        self.cmd("sudo /usr/local/bin/nemesis tcp -D %s -S %s -d %s"%(dst,src,dev))
                        count = count + 1
                return True


def send_icmp_nemesis(self, src="17.1.1.1", dst="18.1.1.1", send_pkts="5", dev="eth2") :
        output = self.cmd("whereis nemesis")
        if "/usr/local/bin/" not in output :
                return False
        else :
                count=0
                while count < int(send_pkts) :
                        self.cmd("sudo /usr/local/bin/nemesis icmp -D %s -S %s -d %s"%(dst,src,dev))
                        count = count + 1
                return True

