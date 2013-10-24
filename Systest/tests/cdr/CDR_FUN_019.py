#!/usr/bin/env python2.5

"""
##############################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#       
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#       
##############################################################################

DESCRIPTION:To Verify  CDR data gets uploaded to the servers with max upload profiles(3) bound to port other than the management port.
TEST PLAN: CDR Test plans
TEST CASES: CDR_FUN_019
        
TOPOLOGY DIAGRAM: 
        
          
          |---------------|        |----------------|
          |               |        |                |            
          |    LINUX      | ------ |      SSX       |                                                                 
          | 17.1.1.1/24   |e1   2/3| 17.1.1.2/16    |                               
          |---------------|        |----------------|
        
        
AUTHOR:  suhasini@primesoftsolutionsinc.com
        
REVIEWER: alok@primesoftsolutionsinc.com

"""


import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Frame-work libraries
from SSX import *
from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from cdr import *
from helpers import is_healthy
import re


#import configs file
from config import *
from topo import *
#import private libraries
from ike import *

from misc import *


class test_CDR_FUN_019(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session to the SSX box.
        self.ssx = SSX(ssx["ip_addr"])
	self.linux=Linux(xpress_vpn1['ip_addr'],xpress_vpn1['user_name'],xpress_vpn1['password'])
        self.ssx.telnet()
        self.linux.telnet()

        # Clear the SSX config
        self.ssx.clear_config()
        
	# wait for card to come up
        self.ssx.wait4cards()
        self.ssx.clear_health_stats()


    def tearDown(self):

        # Close the telnet session of SSX
        self.ssx.close()
	self.linux.close()

    def test_CDR_FUN_019(self):

	# Enable debug logs for iked
        self.ssx.cmd("debug module iked all")
        self.ssx.cmd("debug module aaad all")
        #changing context and clearing ip counters
        self.ssx.cmd("context %s" %(script_var['context_name']))
        #clearing sessions on ssx
        self.ssx.cmd("clear session all")

        #Clearing already existing files on the linux machine
        self.linux.cmd("su root")
        time.sleep(5)
        self.linux.cmd("su krao")
        time.sleep(5)
        self.linux.cmd("cd")
        time.sleep(5)
        self.linux.cmd("rm -rf *.asn1")
        self.linux.cmd("rm -rf *.xml")
        self.linux.cmd("rm -rf *.ttlv")
        self.linux.cmd("exit")
        self.linux.cmd("exit")

        self.linux.cmd("cd /tftpboot/")
        #self.linux.cmd("sudo rm *.*")
        self.linux.cmd("sudo rm -rf *.asn1")
        self.linux.cmd("sudo rm -rf *.xml")
        self.linux.cmd("sudo rm -rf *.ttlv")

        

	#configuring interface on linux machine
	self.linux.configure_ip_interface(p1_ssx_xpressvpn1[1], script_var['xpress_phy_iface1_ip_mask'])

	# Push xpress vpn config on linux
        self.linux.write_to_file(script_var['autoexec_config'],"autoexec.cfg","/xpm/")
        self.linux.write_to_file(script_var['add_iptakama'],"add_ip_takama","/xpm/")

        # Push SSX config
        self.ssx.config_from_string(script_var['cdr_common_config'])
    

         #Vgrouping the Topology 
        #vg_output1 = vgroup_new(topo2[:])
        #self.failUnless(vg_output1 == None,"vgroup FAILED")
 


        # Initiate IKE Session from Xpress VPN Client (takama)
        self.linux.cmd("cd")
        self.linux.cmd("cd /xpm")
        self.linux.cmd("sudo chmod 777 add_ip_takama")
        self.linux.cmd("sudo ./add_ip_takama")
        time.sleep(5)
         
        self.linux.cmd("sudo ./start_ike")
        time.sleep(5)
        op1 = self.ssx.configcmd("show session")
        self.ssx.configcmd("exit")
        self.failUnless("IPSEC" in op1,"Failed because there is no session of IPSEC")


        self.linux.cmd("!ping %s -I %s -w 2 -c 2" %(script_var['ses_loopip'],script_var['pool_ip']))
        self.linux.cmd("quit")


        self.myLog.info("\n\n")
        self.myLog.info("*" *50)
	self.myLog.info("Waiting for 60 seconds to get the files generated on the linux machine-%s ...... " % linux['ip_addr'])
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")
        
        time.sleep(60) 

        self.linux.cmd("ls -rth /tftpboot/ | grep \".ttlv\" ")	
        self.linux.cmd("ls -rth ~krao | grep \"cdr-1*\" ")
        
        self.linux.cmd("cd ~krao")
        linuxip_asn = self.linux.cmd("ls -rth | grep \".asn\" ")
        linuxip = self.linux.cmd("ls -rth | grep \".xml\" | tail -n 1 ")
        linuxip1 = linuxip.strip()
        self.myLog.output(linuxip1) 
        self.failUnless(linuxip1,"CDR data generation failed with disk-commit-interval as 1 min")
        self.myLog.output("CDR data generation passed with disk-commit-interval as 1 min")
        
        self.myLog.info("\n\n")
        self.myLog.info("*" *50)
        self.myLog.info("Checking of xml files which are generated on SSX-%s ...... " % ssx['ip_addr'])
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")

        mib = self.ssx.cmd("sh ses detail | grep \"Assigned Ip address\"")
        ssxAdd = compare_ip_ssx(self.ssx,mib)
        self.myLog.output(ssxAdd)
        
        mib = self.ssx.cmd("sh ses detail | grep -i \"Username: \"")
        ssxUser = compare_usr_ssx(self.ssx,mib)
        self.myLog.output(ssxUser)


        mib = self.ssx.cmd("sh ses detail | grep -i \"Qos policy:\"")
        ssxCos = compare_cos_ssx(self.ssx,mib)
        self.myLog.output(ssxCos)

        mib = self.ssx.cmd("sh ses detail | grep -i \"Qos policy:\"")
        ssxCosid = compare_cosId_ssx(self.ssx,mib)
        self.myLog.output(ssxCosid)

     
        self.myLog.info("\n\n")
        self.myLog.info("*" *50)
	self.myLog.info("Checking of xml files which are generated on Linux machine-%s ...... " % linux['ip_addr'])
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")


        mib = self.linux.cmd("cat %s | grep \"iPBinV4Address\"" % linuxip1) 
        linuxAdd = compare_ip_linux(self.linux,mib) 
        self.myLog.output(linuxAdd)
  
        mib = self.linux.cmd("cat %s | grep -i \"sessionUsername\" " %linuxip1)
        lixUser = compare_usr_linux(self.linux,mib)
        self.myLog.output(lixUser)

        mib = self.linux.cmd("cat %s | grep -i \"classOfServiceName\"" % linuxip1)
        linuxCos = compare_cos_linux(self.linux,mib)
        self.myLog.output(linuxCos)

        mib = self.linux.cmd("cat %s | grep -i \"classOfServiceId\"" % linuxip1)
        linuxCosid = compare_cosId_linux(self.linux,mib)
        self.myLog.output(linuxCosid)

        self.myLog.info("Comparing the data on SSX and Linux machines")



        if  linuxAdd in ssxAdd:
         self.myLog.output("The Session Ip %s on both SSX and Linux using XML files are equal" % ssxAdd)
        else:   
         self.myLog.output("The Session Ip's on both SSX and Linux using XML files are not equal")
 
        if  lixUser in ssxUser :
         self.myLog.output("The Usernames %s on both SSX and Linux using XML files are equal" % ssxUser)
        else:
         self.myLog.output("The Usernames on both SSX and Linux using XML files are not equal")

        if  linuxCos in ssxCos:
         self.myLog.output("The ClassOfServices %s on both SSX and Linux using XML files are equal" % ssxCos)
        else:
         self.myLog.output("The ClassOfServices on both SSX and Linux using XML files are not equal")

        if linuxCosid in ssxCosid:
         self.myLog.output("The ClassOfServiceID's %s on both SSX and Linux using XML files are equal" % ssxCosid)
        else:
         self.myLog.output("The ClassOfServiceID's on both SSX and Linux using XML files are not equal")



        self.myLog.info("\n\n")
        self.myLog.info("*" *50)
        self.myLog.info("Checking of ttlv files which are generated on SSX-%s ...... " % ssx['ip_addr'])
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")

 
        #Check for ttlv files using CDR dump tool
        self.linux.cmd("cd")
        self.linux.cmd("cd /tftpboot/")
        linuxtftp = self.linux.cmd("ls -rth | grep \".ttlv\" | tail -n 1")
        linuxtftp1 = linuxtftp.strip()
        linuxtftp2 = linuxtftp1.strip().strip()
        self.failUnless(linuxtftp2,"Files are not generated on the Linux machine")

        self.ssx.cmd("context cdr-1")
	res = self.ssx.ftppasswd("copy sftp://root@%s:/tftpboot/%s /hd/CDR_FUN_001.ttlv noconfirm" %(script_var['upload_server_mgmt_ip'],linuxtftp2))
        time.sleep(10)
        self.ssx.shellcmd("cd /hd")
        ttl1= self.ssx.shellcmd("cdrdump -f CDR_FUN_001.ttlv -r 0 | grep \"icmp_policy\" ")
        ttl2=re.search("\w+\=(.*)",ttl1)        
        if ttl2:
          ttl3=ttl2.group(1)
          self.myLog.info("Data in SSX by using CDR Dump tool is %s" %ttl3)
          self.failUnless(ttl3,"No Files found using CDR Dumptool")
        else:
          self.myLog.info("No files generated")

        self.myLog.info("\n\n")
        self.myLog.info("*" *50)
	self.myLog.info("Checking of ttlv files which are generated on Linux machine-%s ...... " % linux['ip_addr'])
        self.myLog.info("*" *50)
        self.myLog.info("\n\n")

         
        mib = self.ssx.cmd("sh ses detail | grep -i \"Qos policy:\"")
        ssxCos = compare_cos_ssx(self.ssx,mib)
        self.myLog.output(ssxCos)
        self.myLog.info("*" *50)         
        self.myLog.info("Comparing both the SSX and  Linux values")
        self.myLog.info("*" *50)         
        if ttl3 in ssxCos :
         self.myLog.output("Data on SSX and Linux machines are equal")
         self.failUnless(ttl3,"No Files found using CDR Dumptool")
        else:
         self.myLog.output("Data on SSX and Linux machines are not equal")

        # Checking SSX Health
        hs = self.ssx.get_health_stats()
        self.failUnless(is_healthy( hs), "Platform is not healthy")

	      	   
if __name__ == '__main__':
	if os.environ.has_key('TEST_LOG_DIR'):
        	os.mkdir(os.environ['TEST_LOG_DIR'])
        	os.chdir(os.environ['TEST_LOG_DIR'])
	filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_CDR_FUN_019)
        test_runner(stream=sys.stdout).run(suite)
