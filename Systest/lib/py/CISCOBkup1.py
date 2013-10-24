#!/usr/bin/python2.4

import sys, os
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

import pexpect
import time
import misc
import sys
import re
import glob
import calendar
from stat import *
from Host import *
from logging import getLogger
log = getLogger()
from StokeTest import test_case
from helpers import compare2ipv4

#newline, then systemname[context]#"
#enable_prompt_regex = "[\r\n]*\S+\[\S+\](-STANDBY)*#"
enable_prompt_regex = "[\r\n]*\w+>"
#enable_prompt_regex = "almatti>"
#terminal_prompt_regex = "[\r\n]*\S+\([terminal]\S*\)?"
terminal_prompt_regex = "[\r\n]Configuring from terminal, memory, or network [terminal]?"
#config_prompt_regex = "[\r\n]*\S+\(config\S*\)#"
config_prompt_regex = "[\r\n]*\S+-\d+-\S+\(config\S*\)#"
yesno_prompt_regex = ".*[\r\n.]*\(\[*yes\]*/\[*no\]*\)\s*$"
login_prompt_regex = ".*[\r\n]+Username: $"
password_prompt_regex = ".*[\r\n]+Password: $"
#shell_prompt_regex = "[\r\n]+\S+\W+\-\S+\W+\S+\W+\-\W+\S+#"
#shell_prompt_regex = "[\r\n]*\S+-\d+-\S+.*#"
shell_prompt_regex = "[\r\n]*\S+#"
#shell_prompt_regex = "[\r\n].*#"
#shell_prompt_regex = "[\r\n]+\S+-\S+#"
#shell_prompt_regex = "[\r\n]+\S+\W+\-\S+\W+#"
cisco_enable_prompt_regex = "[\r\n]+qa-6500-1>$"

(EXEC_PROMPT, CONFIG_PROMPT) = range(2)

class CISCO:
    def __init__(self,host):
        self.ses = None
        self.username = None
        self.password = None
        self.version = None
        self.name = None
        self.nfs = True
        self.slot = 0
    
    def telnet(self, host, username="stoke", password="stoke"):
        """Connect to cisco via telnet, username defaults to "cisco",
        password defaults to "cisco"
        """
        self.username = username
        self.password = password
        self.ses = pexpect.spawn("telnet -E -8 " + host)
        try:
            self.ses.expect(login_prompt_regex)
            self.login()
        except pexpect.TIMEOUT:
            misc.testerror("Problem connecting in cisco_telnet()")
            return False
        self.ses.delaybeforesend = 0
        self.init_vars(host)
        return True

    def login(self):
        try:
            self.flush_child()
            self.ses.sendline()
            self.ses.sendline()
            self.ses.sendline()
            self.ses.sendline()
            self.ses.expect(login_prompt_regex)
            self.ses.sendline(self.username)
            self.ses.expect("Password:")
            self.ses.sendline(self.password)
            self.ses.sendline("end")
            self.ses.expect(enable_prompt_regex)
        except pexpect.TIMEOUT:
            misc.TestError("Problem logging in")

    def console(self, host, username="stoke", password="cisco"):
        """Connect to host via telnet to console (terminal server expected),
        username defaults to "cisco",
        password defaults to "cisco"
        """
        self.username = username
        self.password = password
        self.ses = pexpect.spawn("telnet -E -8 " + host)
        try:
            while True:
                time.sleep(1)
                self.flush_child()
                self.ses.sendline()
                index = self.ses.expect(["Enter your option :", "sername:", config_prompt_regex, enable_prompt_regex, shell_prompt_regex])
                  
                if index == 0:
                    self.ses.send("1")
                    print "WARNING, someone else is using console on %s" % host
                    self.flush_child()
                    continue
                if index == 1:
                    self.login()
                    continue
                if index == 2:
                    self.ses.sendline("enable")
                    self.ses.expect("Password:")
                    self.ses.sendline(self.password)			
                    #self.ses.sendline("cisco")
                    continue
                if index == 3:
                    self.ses.sendline("enable")
                    self.ses.expect("Password:")
                    self.ses.sendline(self.password)
                    #self.ses.sendline("cisco")
                    break
                if index == 4:
                    self.ses.sendline("end")
                    break
        except pexpect.TIMEOUT:
            misc.testerror("Problem connecting in cisco_console()")
#           print "child.before: %s" % self.ses.before
            return False
        self.ses.delaybeforesend = 0
        self.init_vars(host)
        return True

    def init_vars(self,hostname):
	self.cmd("terminal length 512")
	self.cmd("terminal width 512")
	self.cmd("configure term")
	self.cmd("no logging console")
	self.cmd("end")
#        hostreg = re.compile("(.*)-mc
#        self.name = blahblahblah
        
        
        
    def cmd(self,command, timeout=200):
        """Routine to send an EXEC command to a CISCO

        Returns output of command as a string."""
        #self.get_to_exec()
	log.cmd(command)
        retstr = ""
        try:
            self.flush_child()
            self.ses.sendline(command)
            self.ses.expect(re.escape(command)) #clean this out of output buffer
            while True:
                which = self.ses.expect([enable_prompt_regex, yesno_prompt_regex, config_prompt_regex,
                                         login_prompt_regex, shell_prompt_regex,terminal_prompt_regex], timeout=timeout)
                if which == 1:
                    self.ses.sendline("yes")
                    retstr += self.ses.before + self.ses.match.group(0)
		    #print "in yesNo"
                if which == 5:
                    self.ses.sendline("terminal")
		    #print "in termPrompt"
                    break
                if which == 3: #cli context blown away, back at login
                    raise misc.TestError("CLI knocked back to login prompt")
		    #print "in loginPrompt"
                else:
		    #print "in break"
		    #print self.ses.before
                    break
            retstr += self.ses.before
        except pexpect.TIMEOUT:
            print "Timeout in cisco.cmd for command %s\n" % command
            raise misc.TestError("pexpect timeout")
	#print retstr
        return retstr

    def clear_log(self,timeout=20):
        self.ses.sendline("clear log")
        self.ses.expect("\[confirm\]",timeout=timeout)
        self.ses.send("\n")

    def config_from_string(self, data):
        """Reads the commands from a string and configures the SSX with them."""
        cmds = []
	cmds.append("config t")
        for line in data.splitlines():
            cmd = line.strip()
            cmds.append(cmd)
	cmds.append("end")
        for entry in cmds:
            self.cmd(entry.strip())

    def configure_ipv4_interface(self,ip_addr="1.1.1.1 255.255.255.0",intf="5/10",vrf=None):
	ip1 = ip_addr.split()[0]
        self.cmd("config t")
	self.cmd("interface gigabit %s"%intf)
	self.cmd("no ip address")
        self.cmd("end")
	ip_op = self.cmd("show ip interface brief | inc %s\.%s\.%s"%(ip1.split('.')[0],ip1.split('.')[1],ip1.split('.')[2]))
	for i in range(len(ip_op.splitlines())-1):
		cmp_op = compare2ipv4(ip1,ip_op.splitlines()[i+1].split()[1],index=3)
		if cmp_op == 0:
			log.error("Some one configured with same IP, please use some other IP")
			return 1
	self.cmd("config t")
	self.cmd("interface gigabit %s"%intf)
	self.cmd("no shutdown")
	self.cmd("no switchport")
	#print vrf
	if vrf != None:
		self.cmd("ip vrf forwarding %s" % vrf)
		#print "I am in vrf"
	self.cmd("ip address %s"%ip_addr)
	self.cmd("end")
	return 0

    def configure_ipv4_vlan_interface(self,ip_addr="1.1.1.1 255.255.255.0",intf="5/10",vlan=1,vrf=None):
	ip1 = ip_addr.split()[0]
        self.cmd("config t")
	self.cmd("interface gigabit %s"%intf)
	self.cmd("no ip address")
        self.cmd("exit")
	self.cmd("interface vlan %s"%vlan)
	self.cmd("no ip address")
	self.cmd("end")
	
	ip_op = self.cmd("show ip interface brief | inc %s\.%s\.%s"%(ip1.split('.')[0],ip1.split('.')[1],ip1.split('.')[2]))
	for i in range(len(ip_op.splitlines())-1):
		cmp_op = compare2ipv4(ip1,ip_op.splitlines()[i+1].split()[1],index=3)
		if cmp_op == 0:
			log.error("Some one configured with same IP, please use some other IP")
			return 1
	self.cmd("config t")
	self.cmd("interface vlan %s"%vlan)
	self.cmd("no shutdown")
        if vrf != None:
                self.cmd("ip vrf forwarding %s" % vrf)
	self.cmd("ip address %s"%ip_addr)
	self.cmd("exit")
	self.cmd("interface gigabit %s"%intf)
	self.cmd("no shutdown")
	self.cmd("switchport")
	self.cmd("switchport access vlan %s"%vlan)
	self.cmd("switchport trunk encapsulation dot1q")
	self.cmd("switchport trunk allowed vlan %s"%vlan)
	self.cmd("switchport mode trunk")
	self.cmd("end")
	return 0

    def configure_only_vlan_interface(self,ip_addr="1.1.1.1 255.255.255.0",vlan=1):
        ip1 = ip_addr.split()[0]
        self.cmd("config t")
        self.cmd("interface vlan %s"%vlan)
        self.cmd("no ip address")
        self.cmd("end")

        ip_op = self.cmd("show ip interface brief | inc %s\.%s\.%s"%(ip1.split('.')[0],ip1.split('.')[1],ip1.split('.')[2]))
        for i in range(len(ip_op.splitlines())-1):
                cmp_op = compare2ipv4(ip1,ip_op.splitlines()[i+1].split()[1],index=3)
                if cmp_op == 0:
                        log.error("Some one configured with same IP, please use some other IP for the VLAN: %s"%vlan)
                        return 1

        self.cmd("config t")
        self.cmd("interface vlan %s"%vlan)
        self.cmd("no shutdown")
        self.cmd("ip address %s"%ip_addr)
        self.cmd("end")
	return 0

    def configure_multi_vlan_interface(self,ips="1.1.1.1 255.255.255.0,3.1.1.1 255.255.255.0",vlans="1,2",intf="5/10"):
	VlanList = vlans.split(',')
	vlans_op=""
	for StripIndex in range(len(VlanList)):
		VlanList[StripIndex]=VlanList[StripIndex].strip()
		if StripIndex == len(VlanList) - 1:
			break
		vlans_op ="%s%s,"%(vlans_op,VlanList[StripIndex])

	vlans_op="%s%s"%(vlans_op,VlanList[len(VlanList)-1])
	IpList = ips.split(',')
	if len(VlanList) != len(IpList):
		log.error("Number of IPs are not equal to number of Vlans")
		return 1
	#ip1 = ip_addr.split()[0]
        self.cmd("config t")
	self.cmd("interface gigabit %s"%intf)
	self.cmd("no ip address")
        self.cmd("end")
	for VlanIndex in range(len(VlanList)):
		vlan_op = self.configure_only_vlan_interface(ip_addr=IpList[VlanIndex],vlan=VlanList[VlanIndex])
		if vlan_op == 1:
			return 1
	self.clear_interface_config(intf)
	self.cmd("config t")
	self.cmd("interface gigabit %s"%intf)
	self.cmd("switchport")
	self.cmd("switchport trunk encapsulation dot1q")
	self.cmd("switchport trunk allowed vlan %s"%vlans_op)
	self.cmd("switchport mode trunk")
        self.cmd("end")
        return 0

    def clear_interface_config(self,intf="5/22"):
	conf = self.cmd("show running interface gigabit %s"%intf)
	#print conf
	conf=conf.split('!')
	conf=conf[1].strip('\n')
	conf_str = conf.splitlines()
	self.cmd("conf t")
	self.cmd("interface gigabit %s"% intf )
	lnth = len(conf_str)
	for noIndex in range(len(conf_str)-3):
		#if ("no" or "end") in conf_str[lnth-(noIndex+2)].split()[0]:
		if ( ("no" in conf_str[lnth-(noIndex+2)]) or ("end" in conf_str[lnth-(noIndex+2)]) ):
			continue
		self.cmd("no %s"%conf_str[lnth-(noIndex+2)])
	self.cmd("end")
	return 0
	
    def clear_interface_counters(self,intf):
        self.ses.sendline("clear counters gigabitEthernet %s"%intf)
        self.ses.expect("\[confirm\]",10)
        self.ses.send("\n")

    def verify_interface_counters(self,intf,inPktCnt,outPktCnt):
	""" API to verify the interface counters
	    usage: verify_interface_counters(self.cisco,intf="0/2",inPktCnt=5,outPktCnt=5)
	    returns 0, if counters macthes
	    returns 1 on failure
	"""

	inFlag = outFlag = 0
	cntOp = self.cmd("show interfaces gigabitEthernet %s counters | begin InUcastPkts"%intf)
	inCnt = cntOp.splitlines()[2].split()[2]
	outCnt = cntOp.splitlines()[-1].split()[2]

	if ((int(inCnt) == int(inPktCnt)) and (int(outCnt) == int(outPktCnt))):
		return 0
	return 1

    def chk_ip_route_detail(self,route="",admin="",proto="",metric="",next_hop=""):
        passed=[]
        failed=[]

	if not route:
		log.error("Route is compulsary argument")
		failed.append("No Route")

        rt_op = self.cmd("show ip route %s"%route)
        log.output("output of the command: show ip route %s\n%s"%(route,rt_op))
        if "Subnet not in table" in rt_op:
                log.error("Error while getting info for route: %s"%route)
                failed.append("Wrong input")
        if admin:
                log.info("Verifying the Admin Distance")
                op = re.search("\s+distance\s+(\d+)",rt_op,re.IGNORECASE)
                if not op:
                        log.error("Test Failed: Cannot find Admin distance")
                        failed.append("Admin:%s"%admin)
                else:
                        op = op.group(1)
                        admin = admin.strip()
                        if int(op) != int(admin):
                                log.error("Test Failed: Admin distance is not %s"%admin)
                                failed.append("Admin:%s"%admin)
                        else:
                                log.output("Test Passed: Admin distance is %s"%op)
                                passed.append("Admin:%s"%op)

        if proto:
                log.info("Verifying the Protocol")
                op = re.search("\s+Known\s+via\s+\"(.*)\"",rt_op,re.IGNORECASE)
                if not op:
                        log.error("Test Failed: Cannot find Protocal")
                        failed.append("Protocol:%s"%proto)
                else:
                        op = op.group(1)
                        proto=proto.strip()
                        if proto.lower() not in op.lower():
                                log.error("Test Failed: Protocol is not %s"%proto)
                                failed.append("Protocol:%s"%proto)
                        else:
                                log.output("Test Passed: Protocol is  %s"%op)
                                passed.append("Protocol:%s"%op)

        if metric:
                log.info("Verifying the Metric")
                op = re.search("\s+metric\s+(\d+)",rt_op,re.IGNORECASE)
                if not op:
                        log.error("Test Failed: Cannot find Metric")
                        failed.append("Metric:%s"%metric)
                else:
                        op = op.group(1)
                        if int(op) != int(metric):
                                log.error("Test Failed: Metric is not %s"%metric)
                                failed.append("Metric:%s"%metric)
                        else:
                                log.output("Test Passed: Metric is %s"%op)
                                passed.append("Metric:%s"%op)

        if next_hop:
                log.info("Verifying the Next hop")
                op = re.search("\s+\*\s+([0-9.]+),",rt_op,re.IGNORECASE)
                if not op:
                        log.error("Test Failed: Cannot find nexthop")
                        failed.append("Nexthop:%s"%next_hop)
                else:
                        op = op.group(1)
                        next_hop = next_hop.strip()
                        if op != next_hop:
                                log.error("Test Failed: Nexthop is not %s"%next_hop)
                                failed.append("Nexthop:%s"%next_hop)
                        else:
                                log.output("Test Passed: Nexthop is %s"%op)
                                passed.append("Nexthop:%s"%op)

	return passed,failed

    def get_ip_arp(self, ipaddr):
        self.get_to_exec()
        #Internet  92.1.1.2               32   0012.7300.0900  ARPA   Vlan570
        regexp = re.compile("(?P<Protocol>\S+)\s+(?P<Address>\S+)\s+(?P<Age>\S+)\s+(?P<macAddr>\S+)\s+(?P<Type>\S+)\s+(?P<Interface>\S+)")
        output = self.cmd("show ip arp %s" % ipaddr)
        retdict = {}
        for line in output.splitlines():
            m = regexp.match(line)
            if m :
                mydict = m.groupdict()
                retdict.update(mydict)
        return retdict


    def cfg(self, command):
        """Routine to send a config command to a CISCO

        Returns either EXEC_PROMPT or CONFIG_PROMPT, the prompt
        the last command left the cli at."""

        self.get_to_config()
        try:
            self.flush_child()
            self.ses.sendline(command)
            which = self.ses.expect([enable_prompt_regex, yesno_prompt_regex, config_prompt_regex,
                                         login_prompt_regex, shell_prompt_regex,terminal_prompt_regex])
            if which == 0:
                return EXEC_PROMPT
            if which == 2:
                return CONFIG_PROMPT
            if which == 2:
                raise misc.TestError("CLI knocked back to login prompt")
        except pexpect.TIMEOUT:
            misc.testerror("Timeout waiting for prompt after configuring: \n\t%s" % command)

        

    def get_to_exec(self):
        """Ensures cli in exec mode, issuing "end" if in conf mode"""
        self.flush_child()
        self.ses.sendline()
        which = self.ses.expect([enable_prompt_regex, yesno_prompt_regex, config_prompt_regex,
                                         login_prompt_regex, shell_prompt_regex,terminal_prompt_regex])
        if which == 1:
            self.sendline("end")
        if which == 2:
            self.sendline("end")
            
    def get_to_config(self):
        """Ensures cli in global config mode, issuing "conf" if in exec mode"""
        print "in get_to_config"
        self.flush_child()
        self.ses.sendline()
        which = self.ses.expect([enable_prompt_regex, yesno_prompt_regex, config_prompt_regex,
                                         login_prompt_regex, shell_prompt_regex,terminal_prompt_regex])
        if which == 0:
            self.cmd("configure ter")
        if which == 4:
            self.cmd("configure ter")


    def cfg_from_str(self, astr):
        """Load configuration from a multiline string"""
        was_exec = False
        self.get_to_config()
        astr = misc.eat_blank_lines(astr)
        astr = misc.eat_leading_whitespace(astr)
        lines = astr.splitlines()
        for i in range(len(lines)):
            whatprompt = self.cfg(lines[i])
            #if whatprompt != CONFIG_PROMPT and i != len(lines) - 1:
            #if  i != len(lines) - 1:
               # misc.testerror("Config load failed, config line returned wrong prompt")
        if was_exec:
            self.cfg("end")


	
    '''
    def close(self):
        """This properly handles the closing down of a session with a host."""
        self.ses.close()
        log.debug("Closing down the session to host %s." % self.host)
   
    def shell_cmd(self,command, timeout=20):
        """Routine to send a SHELL command to a CISCO
        Returns output of command as a string."""
        self.get_to_shell()
        retstr = ""
        try:
            self.flush_child()
            self.ses.sendline(command)
            self.ses.expect(re.escape(command)) #clean this out of output buffer
            while True:
                which = self.ses.expect([enable_prompt_regex, yesno_prompt_regex, config_prompt_regex,
                                         login_prompt_regex, shell_prompt_regex,terminal_prompt_regex], timeout=timeout)
                if which < 3: #shell blown away, back at Stoke prompt
                    raise misc.TestError("shell lost unexpectedly.")
                else:
                    break
            retstr += self.ses.before
        except pexpect.TIMEOUT:
            print "Timeout in ssx.cmd for command %s\n" % command
            raise misc.TestError("pexpect timeout")
        return retstr

    def isup(self):
        try:
            self.flush_child()
            self.ses.sendline()
            which = self.ses.expect([enable_prompt_regex, yesno_prompt_regex, config_prompt_regex,
                                     login_prompt_regex])
            if which == 1:
                self.ses.sendline()
                self.ses.sendline()
            elif which == 3:
                self.login()
            return True
        except pexpect.TIMEOUT:
            return False
    

    #Success rate is 0.00 percent (0/5) 100.0% packet loss
    def ping(self, dest, size=64, repeat=5):
        #Success rate is 0.00 percent (0/5) 100.0% packet loss
        pingreg = re.compile("Success rate is [\d\.]+ percent \((\d+)/(\d+)\).*$")
        self.get_to_exec()
        output = self.cmd("ping %s size %s repeat %s" % (dest, size, repeat))
        received = sent = 0
        for line in output.splitlines():
            m = pingreg.match(line)
            if m:
                received, sent = m.groups()
        if received == sent and received != 0:
            return True
        return False
    '''
    def flush_child(self):
        misc.flush_child(self.ses)

    def sendline(self, *args, **kwargs):
        return self.ses.sendline(*args, **kwargs)

    def expect(self, *args, **kwargs):
        return self.ses.expect(*args, **kwargs)

    def send(self, *args, **kwargs):
        return self.ses.send(*args, **kwargs)
    '''
    def get_port_macaddr(self, port):
        port_state = self.get_port_state(port)
        if not port_state:
            return False
        mac_address = port_state["macaddr"]
        return mac_address

    def get_proc_mem(self):
        retval = {}
        show_proc_mem_reg = re.compile("""^(?P<proc_name>\S+)
                                           \s+\d+\s+\S+\s+\S+\s+\S+\s+\S+\s+
                                           (?P<stack>\S+)\s+
                                           (?P<heap>\S+)\s+
                                           (?P<share>\S+)
                                           """, re.VERBOSE)
        self.get_to_exec()
        for slot in ["0", "1", "2", "3", "4"]:
            tmp = {}
            output = self.cmd("show process mem slot " + slot)
            if output:
                for line in output.splitlines():
                    m = show_proc_mem_reg.match(line)
                    if m:
                        tmp[m.groupdict()['proc_name']] = m.groupdict()
            retval[slot] = tmp
        if retval:
            return retval
        raise misc.TestError("Couldnt parse show proc mem output")

    def get_slot_proc_mem(self, slot):
        memory = self.get_proc_mem()
        return memory[slot]

    def get_memory(self):
        retval = {}
        show_memory_reg = re.compile("""^\s+(?P<slot>\d+)\s+
                                            (?P<type>\S+)\s+
                                            (?P<total>\S+)\s+
                                            (?P<used>\S+)\s+
                                            (?P<available>\S+)
                                            """, re.VERBOSE)
        self.get_to_exec()
        output = self.cmd("show memory")        
        for line in output.splitlines():
            m = show_memory_reg.match(line)
            if m:
                slot_mem = m.groupdict()
                retval[slot_mem['slot']] = slot_mem
        if retval:
            return retval
        raise misc.TestError("Couldnt parse show memory output")
    
    def get_slot_memory(self, slot):
        memory = self.get_memory()
        return memory[slot]
                
    def get_port_state(self, port):
        retval = {}
	if self.version[0] == "buckeye" or self.version[0] == "2.1B1":
            #3/0   Admin Up     Up            1000 Full   SFP       00:12:73:00:08:20
	    show_port_output_reg = re.compile("""^(?P<slotport>\d+/\d+)\s+
						  Admin\s+
						  (?P<admin_state>\w+)\s+
						  (?P<link_state>\w+)\s+
						  (?P<speed>\w+)\s+
						  (?P<duplex>\w+)\s+
						  (?P<connector>\w+)\s+
						  (?P<macaddr>\S+)
						  """, re.VERBOSE)
	else:
	    #2/0   Eth  Up     Up    1000 Full   SFP       Copper 00:12:73:00:06:90
	    show_port_output_reg = re.compile("""^(?P<slotport>\d+/\d+)\s+
						  (?P<type>\w+)\s+
						  (?P<admin_state>\w+)\s+
						  (?P<link_state>\w+)\s+
						  (?P<speed>\w+)\s+
						  (?P<duplex>\w+)\s+
						  (?P<connector>\w+)\s+
						  (?P<medium>\w+)\s+
						  (?P<macaddr>\S+)
						  """, re.VERBOSE)
        self.get_to_exec()
        output = self.cmd("show port %s" % port)
        for line in output.splitlines():
            m = show_port_output_reg.match(line)
            if m:
                return m.groupdict()
        raise misc.TestError("Couldnt parse show port output for port %s" % port)

    def port_link_up(self, port):
        """Returns True if port is link up in show port output"""
        port_state = self.get_port_state(port)
        link_state = port_state["link_state"]
        if link_state == "Up":
            return True
        else:
            return False

    def port_admin_up(self, port):
        """Returns True if port is admin up in show port output"""
        port_state = self.get_port_state(port)
        admin_state = port_state["admin_state"]
        if admin_state == "Up":
            return True
        else:
            return False

    def get_ip_intf(self, intf):
        """Returns a dict of attributes from "show ip int" output, with a list
        for the ccts bound list"""
        #Name: joe                              IP address: 2.2.2.1/24
        #State: Down                            mtu: 1500
        #Arp: On                                Arp timeout: 3600
        #Arp refresh: Off                       Ignore DF: Off
        #Icmp unreachables: Off                 Mask reply: Off
        #Default source: No                     Description: 
        #Type: Classic                          Index: 0x80000010
        #Bind/session count: 0                  Session default: No
        #Bound to: None    
        regexps_list = ["Name: (?P<name>[\w-]+)",                        "IP address: (?P<ipaddr>[\d\./]+)",
                        "State: (?P<state>\w+)",                         "mtu: (?P<mtu>\d+)",
                        "Arp: (?P<arp>\w+)",                             "Arp timeout: (?P<arp_timeout>\d+)",
                        "Arp refresh: (?P<arp_refresh>\w+)",             "Ignore DF: (?P<ignore_df>\w+)",
                        "Icmp unreachables: (?P<icmp_unreachables>\w+)", "Mask reply: (?P<mask_reply>\w+)",
                        "Default source: (?P<default_source>\w+)",       "Description: (?P<description>.*$)",
                        "Type: (?P<type>\w+)",                           "Index: (?P<index>\w+)",
                        "Bind/session count: (?P<count>\d+)",            "Session default: (?P<session_default>\w+)",
                        "Bound to: (?P<bound_to>.*$)"]
        regexps = map(re.compile, regexps_list)
        self.get_to_exec()
        output = self.cmd("show ip interface %s" % intf)
        retdict = {}
        bind_ccts_str = ""
        in_bound_ccts = False
        for line in output.splitlines():
            if not in_bound_ccts:
                for reg in regexps:
                    m = reg.match(line)
                    if m :
                        mydict = m.groupdict()
                        if "bound_to" in mydict.keys():
                            in_bound_ccts = True
                            bind_ccts_str += mydict["bound_to"]
                        else:
                            retdict.update(mydict)
            else:
                bind_ccts_str += line
        #fix up bind ccts here
        cct_reg = re.compile("(cct \S+)")
        cct_list = cct_reg.findall(bind_ccts_str)
        retdict["bound_to"] = cct_list
        return retdict

    def intf_up(self, intf):
        """Return True is intf is up"""
        intf_state = self.get_ip_intf(intf)
        if intf_state["state"] == "Up":
            return True
        else:
            return False

    def wait4intf(self, intf, maxtime=5, wait_interval=1):
        """wait for v4 interface to come up
        maxtime defaults to 5 seconds,
        wait_interval defaults to 1 seconds"""
        maxtries = maxtime / wait_interval
        while True:
            if self.intf_up(intf):
                break
            time.sleep(wait_interval)
            maxtries -= 1
            if not maxtries:
                misc.testerror("Interface %s did not come up in %d seconds." % (intf, maxtime))

    def wait4v6intf(self, intf, maxtime=5, wait_interval=1):
        """wait for v4 interface to come up
        maxtime defaults to 5 seconds,
        wait_interval defaults to 1 seconds"""
        maxtries = maxtime / wait_interval
        while True:
            if self.v6intf_up(intf):
                break
            time.sleep(wait_interval)
            maxtries -= 1
            if not maxtries:
                misc.testerror("Interface %s did not come up in %d seconds." % (intf, maxtime))

    ### This is crude, need parsing out complete 'show ipv6 interface' output
    def v6intf_up(self, intf):
        upreg = re.compile(".*[\r\n]+Up.*", re.DOTALL)
        tentative_reg = re.compile(".*\[Tentative\].*", re.DOTALL)
        self.get_to_exec()
        output = self.cmd("show ipv6 interface %s" % intf)
        m = upreg.search(output)
        if m:
            #wait for intf to not have 'tentative'addr
            m2 = tentative_reg.search(output)
            if m2:
                return False
            return True
        else:
            return False
        
    def get_ip_route(self, route):
        """Parse show ip route <whatever> output, return dict of items"""
        #Routing entry for 1.1.1.0/24
        #  Known via "static", best route, distance 1, metric 0, tag 0
        #    Learnt from 172.10.1.1 (active nexthop), interface isp
        ip_route_reg = re.compile("""Routing\ entry\ for
                                     \ (?P<entry>[\d\.]+/\d+).*
                                     Known\ via\ "(?P<type>\w+)"
                                     .*distance\ (?P<distance>\d+)
                                     .*metric\ (?P<metric>\d+)
                                     .*tag\ (?P<tag>\d+).*""", re.VERBOSE | re.DOTALL)
        self.get_to_exec() 
        output = self.cmd("show ip route %s" % route)
        m = ip_route_reg.search(output)
        if m:
            return m.groupdict()
        else:
            return False

    def check_ip_route(self, route):
        """Check if a route shows up via show ip route <whatever>
        just return True or False"""
        ip_route = self.get_ip_route(route)
        if not ip_route:
            return False
        else:
            return True

    def get_ipv6_nd(self, neighbor):
	#Address:                       2::2
	#Circuit Handle:                3/0/7d0
	#Hardware Address:              00:12:73:00:07:f1
	#State:                         Reachable
	#Age:                           24s
	#Interface:                     joev6
	#Queued-packets:                0
	#Neighbor-Solicitation Count:   1
	regexps_list = ["Address:\s+(?P<addr>\W+)",
			"Circuit Handle:\s+(?P<cct_handle>\S+)",
			"Hardware Address:\s+(?P<hwaddr>\S+)",
			"State:\s+(?P<state>\S+)",
			"Age:\s+(?P<age>\S+)",
			"Interface:\s+(?P<intf>\S+)",
			"Queued-packets:\s+(?P<queued>\S+)",
			"Neighbor-Solicitation Count:\s+(?P<ns_count>\S+)"]
        regexps = map(re.compile, regexps_list)
        self.get_to_exec()
        output = self.cmd("show ipv6 neighbor %s" % neighbor)
        retdict = {}
        for line in output.splitlines():
	    for reg in regexps:
		m = reg.match(line)
		if m :
		    mydict = m.groupdict()
		    retdict.update(mydict)
	return retdict

    def check_ipv6_nd(self, neighbor):
	ipv6_nd = self.get_ipv6_nd(neighbor)
	if ipv6_nd:
	    return True
	else:
	    return False

    def wait4nd(self, neighbor, maxtime=5, wait_interval=1):
        """wait for v6 neighbor discovery
        maxtime defaults to 5 seconds,
        wait_interval defaults to 1 seconds"""
        maxtries = maxtime / wait_interval
        while True:
            if self.check_ipv6_nd(neighbor):
                break
            time.sleep(wait_interval)
            maxtries -= 1
            if not maxtries:
                misc.testerror("Neighbor discovery for %s did not happen within %d seconds." % (neighbor, maxtime))

    def get_ip_arp(self, ipaddr):
	self.get_to_exec()
	#172.10.1.1        2/2/1          00:12:73:00:06:93    resolved             3592
	regexp = re.compile("(?P<addr>\S+)\s+(?P<cct>\S+)\s+(?P<macaddr>\S+)\s+(?P<state>\S+)\s+(?P<age>\S+)")
        output = self.cmd("show ip arp %s" % ipaddr)
        retdict = {}
        for line in output.splitlines():
	    m = regexp.match(line)
	    if m :
		mydict = m.groupdict()
		retdict.update(mydict)
	return retdict

    def check_ip_arp(self, ipaddr):
	ip_arp = self.get_ip_arp(ipaddr)
	if ip_arp:
	    return True
	else:
	    return False

    def wait4arp(self, ipaddr, maxtime=5, wait_interval=1):
        """wait for v4 arp
        maxtime defaults to 5 seconds,
        wait_interval defaults to 1 seconds"""
        maxtries = maxtime / wait_interval
        while True:
            if self.check_ip_arp(ipaddr):
                break
            time.sleep(wait_interval)
            maxtries -= 1
            if not maxtries:
                misc.testerror("Arp for %s did not come happen within %d seconds." % (ipaddr, maxtime))
	'''



class CISCOConsole(CISCO):
    def __init__(self, host):
    #def __init__(self, host, username="cisco", password="cisco"):
        CISCO.__init__(self)
        self.console(host)
class CISCOTelnet(CISCO):
    def __init__(self, host, username="cisco", password="cisco"):
        CISCO.__init__(self)
        self.telnet(host, username=username, password=password)


if __name__ == "__main__":
    print "testing...\n"
    s = CISCOConsole("qa-cisco2811-1-con")
    print "1\n"
    s.cmd("configure")
    print "2\n"
    s.cfg("system hostname 6506")
    print "3\n"
    s.cfg("end")
