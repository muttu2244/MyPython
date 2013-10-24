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

DESCRIPTION: Do IMC/XGLC failover in different combinations and kill restartable/nonrestartbale process on GLC and restartable on IMC
TEST MATRIX: 4.6B2_HA-IMC.xls
TEST CASE  : HA
TOPOLOGY   : GLC-R Setup 

HOW TO RUN : python2.5 HA.py
AUTHOR     : rajshekar@stoke.com
REVIEWER   : 

"""

################ PLEASE CHANGE BELOW VARIABLES.
################ PLEASE RUN THIS SCRIPT AFTER TUNNELS UP ON DUT 
#########################################################################################
#  At 
#  Please change below variables on line number #113 ....... in this file
#  Max_Iterations = 10
#  Max_Tun_Slot2=4094 #If there are no tunnels then give this value as 0
#  Max_Tun_Slot3=4094 #If there are no tunnels then give this value as 0
#########################################################################################
print "\n\n\n\n BEFORE RUNNING SCRIPT MAKE SURE TUNNELS ARE ACTIVE ON DUT\n\n"
print "\n\n\n\n FOR STOPPING SCRIPT EXECUTE 'CTRL+C'\n\n\n"
import sys, os, commands,re
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
import sys, os
#from subprocess import Popen, PIPE, call
from os.path import normpath
import logging
from string import strip
from optparse import OptionParser

### local libs
from helpers import timestamp


#Import config and topo files
from config import *

## Threading the processes
from threading import Thread
global fail
#Get the ip adress of server where you are running the script.
usage1 = "python HA.py -s macau -m 1 "
parser = frameworkOptionParser(usage1)
parser.add_option("-s", action="store", type="str",default = "None", dest="ssxdetails",help="SSX name(management only). For ex : macau ")
parser.add_option("-m", action="store", type="int",default = "10", dest="Max_Iterations",help="loop for repeating HA. For Ex1 : 5 Ex2:1")

(options, args) = parser.parse_args()
sysname = options.ssxdetails
Max_Iterations = options.Max_Iterations
ssx= {'ip_addr':'%s' %sysname,'username':'joe@local','password':'joe123','name':'%s'%sysname}

class test_HA(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session
	self.myLog.info(__doc__)
        self.Resp = SSX(ssx['ip_addr'])

	#Initiate the telnet session
	self.Resp.telnet()
        
	# Load minimum configuration 
        self.Resp.load_min_config(ssx["name"])
	
        #Clear config and health stats
        self.Resp.clear_health_stats()
	self.Resp.wait4cards()
	
    def tearDown(self):

        # Close the telnet sessions
	self.Resp.close()

    def test_HA(self):
        count=self.Resp.cmd("sh ike-session 2 counters | grep \"Active Sessions\"",timeout = 120)
        if count :
           count_regex=re.search("Active Sessions:\s+(\d+)", count, re.I)
        if count_regex:
           count=int(count_regex.group(1))
        haimc_var['max_tuns_slot2'] = count
        count=self.Resp.cmd("sh ike-session 3 counters | grep \"Active Sessions\"",timeout = 120)
        if count :
           count_regex=re.search("Active Sessions:\s+(\d+)", count, re.I)
        if count_regex:
           count=int(count_regex.group(1))
        haimc_var['max_tuns_slot3'] = count

        Card_Reset = 0
        Card_Restart = 0
        IMC_Switch = 0
        Proc_Restarts = 0
        Proc_Exits    = 0
        Core_Files    = 0
        Crit_logs     = 0
        
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
		
        # Verify the IMC0 is Active
        cardSta = self.Resp.cmd('show card 0 | grep  "Running\(Active\)"')
        if len(cardSta) == 0 :
           self.myLog.info("\n\n###### SSX has IMC0 standby so do imc-switchover \n")
           self.Resp.imc_switchover_mgmt("system imc-switchover")
           IMC_Switch = IMC_Switch + 1
           Card_Reset = Card_Reset + 1
           self.Resp.wait4cards()         
        
        #===============================
        #VERIFICATION  STEPS
        #===============================
        fail = 0
        def ver_tun_up() :
               fail = 0
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
                        fail =1
                        self.fail("Could not able to establish %s tunnels in a proper time"%(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))

                itr += 1
               return fail
        ver_tun_up()
        self.Resp.wait4cards()

        #==========================================================================
        # Below test will do XGLC failover,IMC switchover,XGLC switchback,IMC switchover
        #==========================================================================
        cardIndexList = [2,3]
        iterations = Max_Iterations
        self.myLog.info("\n\n######## Below test will do XGLC failover,IMC switchover,XGLC switchback,IMC switchover ####### \n\n")
        while iterations :
          for cardIndex in cardIndexList :
            #===================   Reload the card and verify the tunnels are up
            self.myLog.info("\n\n######## Reload the %snd card and verify the %stunnels \n"%(cardIndex,int(haimc_var['max_tuns_slot2'])))
            self.Resp.cmd("reload card %s"%cardIndex)
            time.sleep(60)
            Card_Reset = Card_Reset + 1

            #===================  Verify tunnels
            self.myLog.info("\n\n######## Verify GLC%s-switchover should not have any impact on tunnels ##### \n"%cardIndex)
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            if cntOp != True :
               self.fail("Few tunnels gone down after GLC%s-Switchover but switchover should not have any impact on tunnels and tunnels are not swithced to Standby card"%cardIndex)
               self.myLog.info("\n\n##### Verified GLC%s-switchover not effected on tunnels and all Tunnels %s are UP \n"%(cardIndex,(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2']))))

            #================== Do imc-switchover
            self.myLog.info("\n\n######## Do IMC-switchover ##### \n")
            self.Resp.imc_switchover_mgmt("system imc-switchover")
            IMC_Switch = IMC_Switch + 1
            Card_Reset = Card_Reset + 1

            #================= Verify the all tunnels are up
            self.myLog.info("\n\n######## Verify IMC-switchover should not have any impact on tunnels ##### \n")
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            if cntOp != True :
               self.fail("Few tunnels gone down after IMC-Switchover but IMC-switchover should not have any impact on tunnels")
               self.myLog.info("\n\n##### Verified IMC-switchover not effected on tunnels and all Tunnels %s are UP \n"%(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            self.Resp.wait4cards()

            #================ Do GLC Switchback
            self.myLog.info("\n\n######## Do GLC Switchback ##### \n")
            self.Resp.cmd("system glc-switchback")
            Card_Restart = Card_Restart + 1
            time.sleep(60)

            #================ Verify tunnels
            self.myLog.info("\n\n######## Verify tunnels swithced back to Home slot ##### \n")
            self.myLog.info("ike-session counters info: %s"%self.Resp.cmd("show ike-session counters"))
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            self.failIf(cntOp == False , "%snd card tunnels are not swithced back to Home slot"%cardIndex)

            #================== Do imc-switchover
            self.myLog.info("\n\n######## Do IMC-switchover ##### \n")
            self.Resp.imc_switchover_mgmt("system imc-switchover")
            IMC_Switch = IMC_Switch + 1
            Card_Reset = Card_Reset + 1

            #================= Verify the all tunnels are up
            self.myLog.info("\n\n######## Verify IMC-switchover should not have any impact on tunnels ##### \n")
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            if cntOp != True :
               self.fail("Few tunnels gone down after IMC-Switchover but IMC-switchover should not have any impact on tunnels")
               self.myLog.info("\n\n##### Verified IMC-switchover not effected on tunnels and all Tunnels %s are UP \n"%(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            self.Resp.wait4cards()

          iterations = iterations - 1

        #==========================================================================
        # Below test will do IMC switchover,IMC switchback,XGLC failover,XGLC switchback
        #==========================================================================
        cardIndexList = [2,3]
        iterations = Max_Iterations
        self.myLog.info("\n\n######## Below test will do IMC switchover,IMC switchback,XGLC failover,XGLC switchback ####### \n\n")
        while iterations :
          for cardIndex in cardIndexList :

            #================== Do imc-switchover
            self.myLog.info("\n\n######## Do IMC-switchover ##### \n")
            self.Resp.imc_switchover_mgmt("system imc-switchover")
            IMC_Switch = IMC_Switch + 1
            Card_Reset = Card_Reset + 1
               
            #================= Verify the all tunnels are up
            self.myLog.info("\n\n######## Verify IMC-switchover should not have any impact on tunnels ##### \n")
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            if cntOp != True :
               self.fail("Few tunnels gone down after IMC-Switchover but IMC-switchover should not have any impact on tunnels")
               self.myLog.info("\n\n##### Verified IMC-switchover not effected on tunnels and all Tunnels %s are UP \n"%(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            self.Resp.wait4cards()

            #================== Do imc-switchover
            self.myLog.info("\n\n######## Do IMC-switchover ##### \n")
            self.Resp.imc_switchover_mgmt("system imc-switchover")
            IMC_Switch = IMC_Switch + 1
            Card_Reset = Card_Reset + 1

            #================= Verify the all tunnels are up
            self.myLog.info("\n\n######## Verify IMC-switchover should not have any impact on tunnels ##### \n")
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            if cntOp != True :
               self.fail("Few tunnels gone down after IMC-Switchover but IMC-switchover should not have any impact on tunnels")
               self.myLog.info("\n\n##### Verified IMC-switchover not effected on tunnels and all Tunnels %s are UP \n"%(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            self.Resp.wait4cards()

            #===================   Reload the card and verify the tunnels are up
            self.myLog.info("\n\n######## Reload the %snd card and verify the %stunnels \n"%(cardIndex,int(haimc_var['max_tuns_slot2'])))
            self.Resp.cmd("reload card %s"%cardIndex)
            time.sleep(10)
            Card_Reset = Card_Reset + 1
            time.sleep(60)

            #===================  Verify tunnels
            self.myLog.info("\n\n######## Verify GLC%s-switchover should not have any impact on tunnels ##### \n"%cardIndex)
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            if cntOp != True :
               self.fail("Few tunnels gone down after GLC%s-Switchover but switchover should not have any impact on tunnels and tunnels are not swithced to Standby card"%cardIndex)
               self.myLog.info("\n\n##### Verified GLC%s-switchover not effected on tunnels and all Tunnels %s are UP \n"%(cardIndex,(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2']))))


            #================ Do GLC Switchback
            self.myLog.info("\n\n######## Do GLC Switchback ##### \n")
            self.Resp.cmd("system glc-switchback")
            Card_Restart = Card_Restart + 1
            time.sleep(60)

            #================ Verify tunnels
            self.myLog.info("\n\n######## Verify tunnels swithced back to Home slot ##### \n")
            self.myLog.info("ike-session counters info: %s"%self.Resp.cmd("show ike-session counters"))
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            self.failIf(cntOp == False , "%snd card tunnels are not swithced back to Home slot"%cardIndex)

          iterations = iterations - 1
        #==========================================================================
        # Below test will do XGLC failover,XGLC switchback,IMC switchover,IMC switchback,
        #==========================================================================
        cardIndexList = [2,3]
        iterations = Max_Iterations 
        self.myLog.info("\n\n######## Below test will do XGLC failover,XGLC switchback,IMC switchover,IMC switchback ####### \n\n")
        while iterations :
          for cardIndex in cardIndexList :

            #===================   Reload the card and verify the tunnels are up
            self.myLog.info("\n\n######## Reload the %snd card and verify the %stunnels \n"%(cardIndex,int(haimc_var['max_tuns_slot2'])))
            self.Resp.cmd("reload card %s"%cardIndex)
            time.sleep(60)
            Card_Reset = Card_Reset + 1

            #===================  Verify tunnels
            self.myLog.info("\n\n######## Verify GLC%s-switchover should not have any impact on tunnels ##### \n"%cardIndex)
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            if cntOp != True :
               self.fail("Few tunnels gone down after GLC%s-Switchover but switchover should not have any impact on tunnels and tunnels are not swithced to Standby card"%cardIndex)
               self.myLog.info("\n\n##### Verified GLC%s-switchover not effected on tunnels and all Tunnels %s are UP \n"%(cardIndex,(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2']))))


            #================ Do GLC Switchback
            self.myLog.info("\n\n######## Do GLC Switchback ##### \n")
            self.Resp.cmd("system glc-switchback")
            Card_Restart = Card_Restart + 1
            time.sleep(60)

            #================ Verify tunnels
            self.myLog.info("\n\n######## Verify tunnels swithced back to Home slot ##### \n")
            self.myLog.info("ike-session counters info: %s"%self.Resp.cmd("show ike-session counters"))
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            self.failIf(cntOp == False , "%snd card tunnels are not swithced back to Home slot"%cardIndex)

            #================== Do imc-switchover
            self.myLog.info("\n\n######## Do IMC-switchover ##### \n")
            self.Resp.imc_switchover_mgmt("system imc-switchover")
            IMC_Switch = IMC_Switch + 1
            Card_Reset = Card_Reset + 1

            #================= Verify the all tunnels are up
            self.myLog.info("\n\n######## Verify IMC-switchover should not have any impact on tunnels ##### \n")
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            if cntOp != True :
               self.fail("Few tunnels gone down after IMC-Switchover but IMC-switchover should not have any impact on tunnels")
               self.myLog.info("\n\n##### Verified IMC-switchover not effected on tunnels and all Tunnels %s are UP \n"%(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            self.Resp.wait4cards()

            #================== Do imc-switchover
            self.myLog.info("\n\n######## Do IMC-switchover ##### \n")
            self.Resp.imc_switchover_mgmt("system imc-switchover")
            IMC_Switch = IMC_Switch + 1
            Card_Reset = Card_Reset + 1

            #================= Verify the all tunnels are up
            self.myLog.info("\n\n######## Verify IMC-switchover should not have any impact on tunnels ##### \n")
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            if cntOp != True :
               self.fail("Few tunnels gone down after IMC-Switchover but IMC-switchover should not have any impact on tunnels")
               self.myLog.info("\n\n##### Verified IMC-switchover not effected on tunnels and all Tunnels %s are UP \n"%(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            self.Resp.wait4cards()

          iterations = iterations - 1

        #==========================================================================
        # Below test will do XGLC failover,IMC switchover,IMC switchback,XGLC switchback
        #==========================================================================
        cardIndexList = [2,3]
        iterations = Max_Iterations
        self.myLog.info("\n\n######## Below test will do XGLC failover,IMC switchover,IMC switchback,XGLC switchback ####### \n\n")
        while iterations :
          for cardIndex in cardIndexList :

            #===================   Reload the card and verify the tunnels are up
            self.myLog.info("\n\n######## Reload the %snd card and verify the %stunnels \n"%(cardIndex,int(haimc_var['max_tuns_slot2'])))
            self.Resp.cmd("reload card %s"%cardIndex)
            time.sleep(10)
            Card_Reset = Card_Reset + 1
            time.sleep(60)

            #===================  Verify tunnels
            self.myLog.info("\n\n######## Verify GLC%s-switchover should not have any impact on tunnels ##### \n"%cardIndex)
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            if cntOp != True :
               self.fail("Few tunnels gone down after GLC%s-Switchover but switchover should not have any impact on tunnels and tunnels are not swithced to Standby card"%cardIndex)
               self.myLog.info("\n\n##### Verified GLC%s-switchover not effected on tunnels and all Tunnels %s are UP \n"%(cardIndex,(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2']))))


            #================== Do imc-switchover
            self.myLog.info("\n\n######## Do IMC-switchover ##### \n")
            self.Resp.imc_switchover_mgmt("system imc-switchover")
            IMC_Switch = IMC_Switch + 1
            Card_Reset = Card_Reset + 1

            #================= Verify the all tunnels are up
            self.myLog.info("\n\n######## Verify IMC-switchover should not have any impact on tunnels ##### \n")
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            if cntOp != True :
               self.fail("Few tunnels gone down after IMC-Switchover but IMC-switchover should not have any impact on tunnels")
               self.myLog.info("\n\n##### Verified IMC-switchover not effected on tunnels and all Tunnels %s are UP \n"%(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            self.Resp.wait4cards()

            #================== Do imc-switchover
            self.myLog.info("\n\n######## Do IMC-switchover ##### \n")
            self.Resp.imc_switchover_mgmt("system imc-switchover")
            IMC_Switch = IMC_Switch + 1
            Card_Reset = Card_Reset + 1

            #================= Verify the all tunnels are up
            self.myLog.info("\n\n######## Verify IMC-switchover should not have any impact on tunnels ##### \n")
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            if cntOp != True :
               self.fail("Few tunnels gone down after IMC-Switchover but IMC-switchover should not have any impact on tunnels")
               self.myLog.info("\n\n##### Verified IMC-switchover not effected on tunnels and all Tunnels %s are UP \n"%(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            self.Resp.wait4cards()

            #================ Do GLC Switchback
            self.myLog.info("\n\n######## Do GLC Switchback ##### \n")
            self.Resp.cmd("system glc-switchback")
            Card_Restart = Card_Restart + 1
            time.sleep(60)

            #================ Verify tunnels
            self.myLog.info("\n\n######## Verify tunnels swithced back to Home slot ##### \n")
            self.myLog.info("ike-session counters info: %s"%self.Resp.cmd("show ike-session counters"))
            cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
            self.failIf(cntOp == False , "%snd card tunnels are not swithced back to Home slot"%cardIndex)

          iterations = iterations - 1

        #============== Below test will kill nonrestartable process kill on Active GLCs
        #======================== Verify SSX behaviour when nonrestartable process kill on GLC
        self.myLog.info("\n\n######## Below test will do nonrestartable process kill on Active GLCs  ####### \n\n")
        cardIndexList = ["2","3"]
        for cardIndex in cardIndexList :
            self.myLog.info("\n\n######## Verify SSX behaviour when nonrestartable process kill on GLC, which causes only core\n")
            glcNonRestartProcesses = haimc_var['kill_glc_non_rest_process'].split()
            glcNonRestartProcesses =             glcNonRestartProcesses[0]
            for glcNonRestartProcess in glcNonRestartProcesses :
              self.myLog.info("\n\n######## Kill the nonrestartable process %s on GLC, which causes card Dumping and tunnel switched to standby card"%glcNonRestartProcess)
              # Retrieve the process list
              process_list = show_process(self.Resp, "slot %s"%cardIndex)
              # Grab the PID out of the list by named process
              pid = process_list[glcNonRestartProcess]['pid']
              # Kill the process
              self.myLog.info("About to kill the process %s on GLC-%s. PID:%s" %(glcNonRestartProcess,cardIndex,pid))
              result = kill_pid(self.Resp, pid, cardIndex)
              if result:
                 self.myLog.error(result)
                 sys.exit(1)
              else:
                 self.myLog.info("Completed killing the process")
              Proc_Restarts = Proc_Restarts + 1
              Core_Files    = Core_Files + 1
              Proc_Exits    = Proc_Exits + 1
              Crit_logs     = Crit_logs + 3
              self.Resp.wait4cards()

              #================ Verify tunnels
              self.myLog.info("\n\n######## Verify tunnels go to standby after Kill the nonrestartable process %s on GLC##### \n"%glcnonrestartProcess)
              self.myLog.info("ike-session counters info: %s"%self.Resp.cmd("show ike-session counters"))
              out = ver_tun_up()
              if out != 0 :
                 self.myLog.info("\n\n#####tunnels are not swithced back after Kill the nonrestartable process %s on GLC"%glcnonrestartProcess)
                 self.fail("Could not able to establish %s tunnels in a proper time"%(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))

              cntOp = verify_ike_session_counters(self.Resp, count=(int(haimc_var['max_tuns_slot3'])+int(haimc_var['max_tuns_slot2'])))
              self.failIf(cntOp == False , "tunnels are not go to standby  after Kill the nonrestartable process %s on GLC"%glcnonrestartProcess)

        #============== Below test will kill restartable process kill on Active IMC
        #==================== Verify SSX behaviour when restartable process kill on IMC
        self.myLog.info("\n\n########killing restartable process on IMC ...\n")
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

        #============== Below test will kill restartable process kill on Active 
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
           IMC_Switch = IMC_Switch + 1
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

if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_HA)
        test_runner().run(suite)

