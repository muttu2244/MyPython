#!/usr/bin/env python2.5
"""
#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

DESCRIPTION: Create many tunnels on a GLC and produce coredump on restartable process
TEST MATRIX: 4.6B2_HA-IMC.xls
TEST CASE  : HA_FUN_04
TOPOLOGY   : GLC-R Setup 

HOW TO RUN : python2.5 HA_FUN_04.py
AUTHOR     : rajshekar@stoke.com
REVIEWER   : 

"""

import sys, os, commands
from string import *

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from SSX import SSX
from CISCO import *
from Linux import *
from ixia import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import *
from misc import *
from glcr import *
from lanlan import *

#Import config and topo files
from config import *
from topo import *
from cleanUpCisco import test_cleanUpCisco

## Threading the processes
from threading import Thread

class testIt(Thread):
   threadLog = getLogger()
   def __init__ (self,myHandle, file):
        Thread.__init__(self)
        self.ssxHandle = myHandle
	self.file = file
        self.status = -1

   def run(self):
        # Let me run the thread, so I no need to
        # wait till it loads the configuration.
        self.threadLog.info("Loading the bulk configuration for the file %s"%self.file)
        self.ssxHandle.cmd("load configuration %s"%self.file, timeout=30000)
        self.status = 1

class test_HA_FUN_04(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session
	self.myLog.info(__doc__)
        self.Ini = SSX(ssx_ini["ip_addr"])
        self.Resp = SSX(ssx_resp["ip_addr"])
        self.cisco = CISCO(cisco["ip_addr"])
        self.ixia = IXIA(ixia['ip_addr'])

	#Initiate the telnet session
	self.Ini.telnet()
	self.Resp.telnet()
	#self.cisco.console(cisco["ip_addr"])
	self.ixia.telnet()
        
	# Load minimum configuration 
        self.Ini.load_min_config(ssx_ini["hostname"])
        self.Resp.load_min_config(ssx_resp["hostname"])
        
        #Clear config and health stats
        self.Resp.clear_ports()
        self.Ini.clear_ports()
        self.Resp.clear_context_all()
        self.Ini.clear_context_all()
        self.Ini.clear_health_stats()
	self.Ini.wait4cards()
        self.Resp.clear_health_stats()
	self.Resp.wait4cards()
	
    def tearDown(self):

        # Close the telnet sessions
	self.Ini.close()
	self.Resp.close()
	self.ixia.cmd("ixLogout")
        self.ixia.cmd("cleanUp")
        self.ixia.close()

    def test_HA_FUN_04(self):
        Card_Reset = 0
        Card_Restart = 0
        #Get the script location
        getPath = sys.path[0]
        Proc_Restarts = 0
        Proc_Exits    = 0
        Core_Files    = 0
        Crit_logs     = 0

        #Get the ip adress of server where you are running the script.
        hostName = commands.getoutput("hostname")
        if "silicon" in hostName:
             scriptServer = "10.10.10.182"
        else:
             scriptServer = commands.getoutput("host %s"% hostName)
             scriptServer = scriptServer.split()[-1]

        self.myLog.output("\n**********starting the test**************\n")
        
        self.myLog.info("\n\n###### Verifying the SSX has DUAL IMC \n")
        out = self.Resp.verify_dual_imc()
        if out == 1 :
            self.myLog.info("\n\n###### SSX has only Single IMC but it should Have DUAL IMC \n")
            self.fail("SSX should be DUAL IMC for running this case but it has only one IMC")
            sys.exit()
                    
        self.myLog.info("Verifying the SSX, GLC-R enabled or not")
        op = verify_glcr_status(self.Resp)
        if op == 1:
                self.myLog.output("Device[Responder] is not configured for GLC Redundancy\nConfiguring the System for GLC-R, needs reboot\n")
                set_device_to_glcr(self.Resp)
		
        op = verify_glcr_status(self.Ini)
        if op == 1:
                self.myLog.output("Device[Initiator] is not configured for GLC Redundancy\nConfiguring the System for GLC-R, needs reboot\n")
                set_device_to_glcr(self.Ini)

        # Verify the IMC0 is Active
        cardSta = self.Resp.cmd('show card 0 | grep  "Running\(Active\)"')
        if len(cardSta) == 0 :
           self.myLog.info("\n\n###### SSX has IMC0 standby so do imc-switchover \n")
           self.Resp.imc_switchover_mgmt("system imc-switchover")
           Card_Reset = Card_Reset + 1
           self.Resp.wait4cards()
        
	
	#Config File names
	ConfigFilename = os.path.split(__file__)[1].replace('.py','')
	iniConfigFile = "%s_Ini.cfg"%ConfigFilename
	respConfigFile = "%s_Resp.cfg"%ConfigFilename
        
        # Generate the 8K configurations 
	self.myLog.info("\n\n###### Generating the 8K tunnels config")
        commands.getoutput("python2.5 %s/generateMe_tunnelsResp.py %s %s %s %s y %s %s > %s/%s"%(getPath,haimc_var['max_tuns_slot2'],haimc_var['Resp_context_name'], haimc_var['tunnel_intf_slot2_startIp'], haimc_var['lpbk_ip'], haimc_var['slot2_route_startIp'], haimc_var['dummy_intf_slot2_startIp'],getPath,respConfigFile))
        time.sleep(30)
        
        commands.getoutput("python2.5 %s/generateMe_tunnelsRespCard3.py %s %s %s %s y %s %s > %s/Card3%s"%(getPath,haimc_var['max_tuns_slot3'],haimc_var['Resp_context_name2'], haimc_var['tunnel_intf_slot3_startIp'], haimc_var['lpbk_ip1'], haimc_var['slot3_route_startIp'], haimc_var['dummy_intf_slot3_startIp'],getPath,respConfigFile))
        
        time.sleep(30)
	os.system("python2.5 %s/generateMe_tunnelsIni.py %s %s %s %s %s %s %s %s %s %s > %s/%s"%(getPath,haimc_var['max_tuns_slot2'],haimc_var['Ini_context_name'], haimc_var['dummy_intf_slot2_startIp'], haimc_var['tunnel_intf_slot2_startIp'], haimc_var['ini_cisco_slot2_ip/mask'], haimc_var['cisco_ini_slot2_ip'], topo.dummy_ports[0], haimc_var['port_ini_slot2'], haimc_var['ini_slot2_route_startIp'], haimc_var['lpbk_ip'], getPath,iniConfigFile))

	time.sleep(30)
        
	os.system("python2.5 %s/generateMe_tunnelsIniCard3.py %s %s %s %s %s %s %s %s %s %s > %s/Card3%s"%(getPath,haimc_var['max_tuns_slot3'],haimc_var['Ini_context_name2'], haimc_var['dummy_intf_slot3_startIp'], haimc_var['tunnel_intf_slot3_startIp'], haimc_var['ini_cisco_slot3_ip/mask'], haimc_var['cisco_ini_slot3_ip'], topo.dummy_ports[1], haimc_var['port_ini_slot3'], haimc_var['ini_slot3_route_startIp'], haimc_var['lpbk_ip1'], getPath,iniConfigFile))
        time.sleep(30)
        
	# Copy the generated files to SSX
	self.Resp.ftppasswd("copy sftp://regress@%s:%s/%s /hd/%s noconfirm"%(scriptServer,getPath,respConfigFile,respConfigFile))
	self.Resp.ftppasswd("copy sftp://regress@%s:%s/Card3%s /hd/Card3%s noconfirm"%(scriptServer,getPath,respConfigFile,respConfigFile))
	self.Ini.ftppasswd("copy sftp://regress@%s:%s/%s /hd/%s noconfirm"%(scriptServer,getPath,iniConfigFile,iniConfigFile))
	self.Ini.ftppasswd("copy sftp://regress@%s:%s/Card3%s /hd/Card3%s noconfirm"%(scriptServer,getPath,iniConfigFile,iniConfigFile))
        
	# Configure Cisco.
	self.myLog.info("\n\n###### Clear and Configure Cisco")
        
	os.system("python2.5 %s/cleanUpCisco.py"%getPath)
	os.system("python2.5 %s/setUpCisco.py y"%getPath)
        
	# Load the configuration for 2nd card.
        self.myLog.info("\n\n######## Load the configuration for 2nd card \n")
	loadResp = testIt(self.Resp, "/hd/%s"%respConfigFile)
	loadIni = testIt(self.Ini, "/hd/%s"%iniConfigFile)
	loadResp.start()
	loadIni.start()
	time.sleep(300)
	loadResp.join()
	loadIni.join()
        self.myLog.info("\n\n###### Successfully loaded the %s tunnel configuration for 2nd card"%haimc_var['max_tuns_slot2'])

	# Successfully loaded the tunnel configuration for 2nd card
	self.myLog.info("Loading the %s tunnels on 3rd card"%haimc_var['max_tuns_slot3'])
	loadResp = testIt(self.Resp, "/hd/Card3%s"%respConfigFile)
        loadIni = testIt(self.Ini, "/hd/Card3%s"%iniConfigFile)
        loadResp.start()
        loadIni.start()
        time.sleep(360)
        loadResp.join()
        loadIni.join()
        self.myLog.info("\n\n###### Successfully loaded the %s tunnel configuration for 3rd card"%haimc_var['max_tuns_slot3'])
        
        #===============================
        #VERIFICATION  STEPS
        #===============================

        #=====================   Verify all Tunnels came up
        self.myLog.info("\n\n######## Verify %s Tunnels Came UP :\n"%(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
	itr = 0
	# Verify the all tunnels are up
	while(1):
		cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
		if cntOp == True :
			break
		time.sleep(30)
		self.myLog.output("%s tunnels not yet established, waiting for some time "%(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
		if itr >= 100:
			self.fail("Could not able to establish %s tunnels in a proper time"%(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))

		itr += 1
        #==================== Verify SSX behaviour when restartable process kill on IMC 
        imcRestartProcesses=haimc_var['kill_imc_resta_process'].split()
        for imcRestartProcess in imcRestartProcesses :        
          self.myLog.info("\n\n########killing restartable process on IMC.Process should restart without reloading IMC card...\n")
          self.ssx.kill_process(imcRestartProcess,1,6)      
          Proc_Restarts = Proc_Restarts + 1
          Proc_Exits    = Proc_Exits + 1
          Core_Files    = Core_Files + 1
          Crit_logs     = Crit_logs + 3
          self.myLog.info("\n\n########Verify Process got Restarted ...\n")
          proc = self.ssx.cmd("show process")
          self.failIf("%s not in $s"%(imcRestartProcess,proc), "Restartable Process not got started after killing on IMC")

          #===================  Verify tunnels
          self.myLog.info("\n\n######## Killing restartable process %s should not have any impact on tunnels ##### \n"%imcRestartProcess)
          cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
          if cntOp != True :
            self.fail("Few tunnels gone down after Killing restartable process %s"%imcRestartProcess)
            self.myLog.info("\n\n##### Verified Killing restartable process %s not effected on tunnels and all Tunnels %s are UP \n"%(cardIndex,imcRestartProcess,(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2']))))

        #==================== Verify SSX behaviour when restartable process kill on XGLC
        cardIndexList = [2,3]
        for cardIndex in cardIndexList :
            self.myLog.info("\n\n######## Verify SSX behaviour when restartable process kill on GLC, Process will restart without card dumping\n")
            glcRestartProcesses = haimc_var['kill_glc_resta_process'] 
            for glcRestartProcess in glcRestartProcesses :
              self.myLog.info("\n\n######## Kill the restartable process %s on GLC, Process will restart without card dumping"%glcRestartProcess)
              # Retrieve the process list
              process_list = show_process(self.ssx, "slot %s"%cardIndex)
              # Grab the PID out of the list by named process
              pid = process_list['Iked']['pid']
              # Kill the process
              self.myLog.info("About to kill the process Iked on GLC-2. PID:%s" % pid)
              result = kill_pid(self.ssx, pid, 2)
              if result:
                 self.myLog.error(result)
                 sys.exit(1)
              else:
                 self.myLog.info("Completed killing the process")
              Core_Files    = Core_Files + 1
              Proc_Exits    = Proc_Exits + 1
              Crit_logs     = Crit_logs + 3    
              Proc_Restarts = Proc_Restarts + 1
              self.Resp.wait4cards()

              #================ Verify tunnels
              self.myLog.info("\n\n######## Verify tunnels on home slot after Kill the restartable process %s on GLC##### \n"%glcRestartProcess)
              self.myLog.info("ike-session counters info: %s"%self.Resp.cmd("show ike-session counters"))
              cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
              self.failIf(cntOp == False , "tunnels down after Kill the restartable process %s on GLC"%glcRestartProcess)
              
        # Verify the IMC0 is Active
        cardSta = self.Resp.cmd('show card 0 | grep  "Running\(Active\)"')
        if len(cardSta) == 0 :
           self.Resp.imc_switchover_mgmt("system imc-switchover")
           Card_Reset = Card_Reset + 1
           self.Resp.wait4cards()

        # Verify the GLCR status
        glcrOp = get_glcr_status(self.Resp)
        if int(glcrOp['standby']) != 4:
                self.Resp.cmd("system glc-switchback")
                Card_Restart = Card_Restart + 1
                time.sleep(10)
                self.Resp.wait4cards()

        # Checking SSX Health
        hs1 = self.Resp.get_health_stats()
        self.failUnless(is_healthy(hs1,Card_Reset=Card_Reset,Card_Restart=Card_Restart,Proc_Restarts=Proc_Restarts,Proc_Exits=Proc_Exits,Core_Files=Core_Files,Crit_logs=Crit_logs,IMC_Switch=IMC_Switch), "Platform is not healthy -Responder")
        hs2 = self.Ini.get_health_stats()
        self.failUnless(is_healthy( hs2), "Platform is not healthy at Initiator - Remote peer")


if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_HA_FUN_04)
        test_runner().run(suite)

