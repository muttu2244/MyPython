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
'''
def check_tunnel_state(self,tunnel = "tunnel1",attempt="5") :
        """Checks For Tunnel Up State"""
        i=1
        count  = "1"
        output = self.cmd("show tunnel | grep %s | grep up | count" %tunnel)
        while i < int(attempt) and count not in output :
                time.sleep(5)
                output = self.cmd("show tunnel | grep %s | grep up | count" %tunnel)
                i = i + 1

        if count not in output :
                return False
        else :
                return True
'''
def check_tunnel_state(self,count="1",attempt="5") :
        """Checks For Tunnel Up State"""
        i=1
        output = self.cmd("show tunnel | grep up | count")
        while i < int(attempt) and count not in output :
                time.sleep(5)
                output = self.cmd("show tunnel | grep up | count")
                i = i + 1

        if count not in output :
                return False
        else :
                return True

def check_tunnel_counters(self,tunnel1="tunnel1", tunnel2="tunnel2", sent_pkts="5") :
	"""Check Tunnel Counters for Incoming and Outgoing Packets"""
	tun_count1=self.cmd("show tunnel counters | grep %s"%tunnel1)
	tun_count2=self.cmd("show tunnel counters | grep %s"%tunnel2)

	if tun_count1 and tun_count2 :
		tun_break=tun_count1.split()
		actual_in1 = tun_break[2]
		actual_out1 = tun_break[3]
	
        	tun_break=tun_count2.split()
	        actual_in2 = tun_break[2]
        	actual_out2 = tun_break[3]
		
	
		if actual_in1 == actual_out2 == sent_pkts and actual_out1 == actual_in2 == sent_pkts :
			return True
		else :
			return False
	else :
		return False

def check_tunnel_counters_return(self,tunnel1="tunnel1", tunnel2="tunnel2", sent_pkts="5",ret_pkts="5") : 
        """Check Tunnel Counters for Incoming and Outgoing Packets"""
        tun_count1=self.cmd("show tunnel counters | grep %s"%tunnel1)
        tun_count2=self.cmd("show tunnel counters | grep %s"%tunnel2)

        if tun_count1 and tun_count2 :
                tun_break=tun_count1.split()
                actual_in1 = tun_break[2]
                actual_out1 = tun_break[3]

                tun_break=tun_count2.split()
                actual_in2 = tun_break[2]
                actual_out2 =tun_break[3]


                if actual_in1 == actual_out2 == sent_pkts and actual_out1 == actual_in2 == ret_pkts :
                        return True
                else :
                        return False
        else :
                return False


def reload_card(self, port="2/0") :
	""" Reloads card based on port issued by command"""
	card=port.split('/')
	card=card[0]
	self.cmd("reload card %s"%card)
	return True


def scp_thru_tunnel(self, file_path="/xpm/largefile.cfg", source="17.1.1.1",username="regress", password="gleep7",dest_path="/xpm/") :
	""" Sends large file from Network1 to Network2 thru tunnel using SCP"""
	self.ses.sendline("sudo scp %s@%s:%s %s" %(username,source,file_path,dest_path))
        log.debug("Sending File Thru Tunnel Using SCP")
        #if not self.ses.expect("(yes/no)?"):
	#	self.ses.sendline("yes")
        if not self.ses.expect("assword:"):
                self.ses.sendline(password)
		return True
	return False
def sftp_thru_tunnel(self, file_path="/xpm/largefile.cfg", source="17.1.1.1",username="regress", password="gleep7",dest_path="/xpm/") :
	""" Sends large file from Network1 to Network2 thru tunnel using SFTP"""
        self.ses.sendline("sudo sftp %s@%s:%s %s" %(username,source,file_path,dest_path))
        log.debug("Sending File Thru Tunnel Using SFTP")
        #if not self.ses.expect("(yes/no)?"):
	#	rint "break1"
        #       self.ses.sendline("yes")
        if not self.ses.expect("assword:"):
		#print "break2"
                self.ses.sendline(password)
		time.sleep(5)
                return True
        return False

def tftp_thru_tunnel(self, filename="largefile.cfg", source="17.1.1.1") :
        """ Sends large file from Network1 to Network2 thru tunnel using TFTP"""
        self.ses.sendline("sudo tftp %s -c get %s" %(source,filename))
        log.debug("Sending File Thru Tunnel Using TFTP")
	time.sleep(5)
	return True

def check_tunnel_counters_bytes_gte(self,tunnel1="tunnel1", tunnel2="tunnel2", sent_bytes="5",ret_bytes="5") :
        """Check Tunnel Counters for Incoming and Outgoing Packets"""
        tun_count1=self.cmd("show tunnel counters | grep %s"%tunnel1)
        tun_count2=self.cmd("show tunnel counters | grep %s"%tunnel2)

        if tun_count1 and tun_count2 :
                tun_break=tun_count1.split()
                actual_in1 = tun_break[4]
                actual_out1 = tun_break[5]

                tun_break=tun_count2.split()
                actual_in2 = tun_break[4]
                actual_out2 = tun_break[5]


                if actual_in1 >= sent_bytes and actual_out2 >= sent_bytes and actual_out1 >= ret_bytes and actual_in2 >= ret_bytes :
                        return True
                else :
                        return False
        else :
                return False


def check_single_tunnel_counters_bytes_gte(self,tunnel="tunnel1",  sent_bytes="5",ret_bytes="5") :
        """Check Tunnel Counters for Incoming and Outgoing Packets"""
        tun_count=self.cmd("show tunnel counters | grep %s"%tunnel)

        if tun_count :
                tun_break=tun_count.split()
                actual_in = tun_break[4]
                actual_out = tun_break[5]

                if actual_in >= sent_bytes and actual_out >= ret_bytes :
                        return True
                else :
                        return False
        else :
                return False

def check_single_tunnel_counters_return(self,tunnel="tunnel1", sent_pkts="5", ret_pkts="5") :
        """Check Tunnel Counters for Incoming and Outgoing Packets"""
        tun_count=self.cmd("show tunnel counters | grep %s"%tunnel)

        if tun_count :
                tun_break=tun_count.split()
                actual_in = tun_break[2]
                actual_out = tun_break[3]

                if actual_in == sent_pkts and actual_out == ret_pkts :
                        return True
                else :
                        return False
        else :
                return False

def verify_ike_session_counters(self, count="100") :
	""" Checks Ike-session counters for Active Sessions """
	ike_details=self.cmd("show ike-session counters | grep -i \"Active Sessions\"")
	
	ike_line=ike_details.split()
	ike_active = ike_line[2]
	
	if int(ike_active) >= int(count) :
		return True
	return False


def check_ike_session_brief(self, count="100") :
        """ Checks Ike-session counters for Active Sessions """
        ike_details=self.cmd("show ike-session brief | grep Y | count")
	
	ike_line=ike_details.split()
	ike_count=ike_line[1]
	ike_count = int(ike_count) - 1
        if ike_count == int(count) :
                return True
        return False

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

	
### Ashu's additions starts here
def check_tun_flap_status(self,tunname) :
        """ This API should take a tunnel name as input and then shall return true or false
        based on output returned. It would return true if tunnel if flapped and false in other case
        """
        #print tunname
        out = self.cmd("show tunnel name %s | grep -i flapped"%tunname)
        if out:
                return True
        else:
                return False

def check_8k_tun_flap_status(self) :
        """
        This API shall check flap status for 8k tunnels and returns list of all
        flapped tunnels.
        """
        tmp = []
        out = self.cmd("show tunnel | grep lan")
        out = out.splitlines()
        for i in range(1,len(out)):
                tname = out[i].split(' ')[0]
                #print tname
                #time.sleep(5)
                status = check_tun_flap_status(self,tname)
                if status:
                        log.info("%s flapped"%tname)
                        tmp.append(tname)
                else:
                        #print i
                        continue
        if (len(tmp) >0) :
                log.info("Following tunnels flapped")
                for i in range(0,len(tmp)) :
                        log.info(tmp[i])
        else :
                log.info("No tunnels were flapped")
### Ashu's Additions Ends here



