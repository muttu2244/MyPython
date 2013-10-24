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

DESCRIPTION: Bring down the directly connected cisco port and validate backup route takes over the traffic
TEST MATRIX:
TEST CASE  : SLA_MA_FUN_031
TOPOLOGY   : 

HOW TO RUN : python2.5 SLA_MA_FUN_031.py
AUTHOR     : rajshekar@stoke.com
REVIEWER   :

"""

import sys, os, time
from string import *

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from SSX import SSX
from CISCO import *
from Linux import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy, insert_char_to_string
from misc import *
from glcr import *
from lanlan import *
from tunnel import *
from jf import *
from ike import *

#Import config and topo files
from config_raja import *
from topo import *

class test_SLA_MA_FUN_031(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session
	self.myLog.info(__doc__)
        self.Ini = SSX(ssx2["ip_addr"])
        self.Resp = SSX(ssx1["ip_addr"])
        self.cisco = CISCO(cisco["ip_addr"])
        self.host1 = Linux(host1["ip_addr"])
        self.host2 = Linux(host2["ip_addr"])

	#Initiate the telnet session
	self.Ini.telnet()
	self.Resp.telnet()
	self.cisco.console(cisco["ip_addr"])
	self.host1.telnet()
	self.host2.telnet()
	
        #Clear config and health stats
        self.Ini.clear_config()
        self.Ini.clear_health_stats()
	self.Ini.wait4cards()
        self.Resp.clear_config()
        self.Resp.clear_health_stats()
	self.Resp.wait4cards()
	
    def tearDown(self):

        # Close the telnet sessions
	self.Ini.close()
	self.Resp.close()
	self.host1.close()
	self.host2.close()

    def test_SLA_MA_FUN_031(self):

	self.myLog.info("-" *70)
        startTime = time.ctime()
        self.myLog.info("\n ####  TEST STARTED #### \n")
        self.myLog.info("Test Start Time is -> %s"%startTime)
        self.myLog.info("-" *70)
	
        self.myLog.info("Verifying the SSX, GLC-R enabled or not")
        op = verify_glcr_status(self.Resp)
        if op == 1:
                self.myLog.output("Device[Responder] is not configured for GLC Redundancy\nConfiguring the System for GLC-R, needs reboot\n")
                set_device_to_glcr(self.Resp)
		
        #Lets verify the MTU of the sys
        self.myLog.info("Verifying the system MTU, if it not set to JF, set it")
	set_sys_mtu(self.Resp,"9500")
        self.Resp.wait4cards()
        time.sleep(5)

        #Lets verify the MTU of the system
        self.myLog.info("Verifying the system MTU at Initiator, if it not set to JF, set it")
	set_sys_mtu(self.Ini,"9500")
        self.Ini.wait4cards()
        time.sleep(5)
	
        #Push the config to SSX
        self.myLog.info("Configuring the Responder")
	self.Resp.config_from_string(psr_var['IKEv2_PSR_L2L_Resp'])
	self.myLog.info("Configuring the Initiator")
	self.Ini.config_from_string(psr_var['IKEv2_PSR_L2L_Ini'])
	
	#Configure the host
	self.myLog.info("Configure the host at Initiator")
	self.host1.configure_ip_interface(p_ssx2_host1[1],psr_var['linux_ini_ip/mask'])
	self.host1.add_route(psr_var['lin_cisco_route'],psr_var['ini_linux_ip'],p_ssx2_host1[1])
	#self.host1.add_route(psr_var['primary_trans_route'],psr_var['ini_linux_ip'],p_ssx2_host1[1])
	#self.host1.add_route(psr_var['secondary_trans_route'],psr_var['ini_linux_ip'],p_ssx2_host1[1])
	#self.host1.add_route(psr_var['primary_service_route'],psr_var['ini_linux_ip'],p_ssx2_host1[1])
	#self.host1.add_route(psr_var['secondary_service_route'],psr_var['ini_linux_ip'],p_ssx2_host1[1])


	#self.host2.configure_ip_interface(p_cisco_host2[1],psr_var['linux_service_ip/mask'])
	self.host2.configure_vlan_interface(p_cisco_host2[1],psr_var['linux_service_ip/mask'],psr_var['vlan3'])
        self.host2.cmd("sudo /sbin/route add -net %s gw %s"%(psr_var['ini_linux_route1'],psr_var['service_ip']))
	
	#Configure the Swicth
	self.myLog.info("Configuring the Cisco")
	self.myLog.info("Enable routing at Cisco")
	self.cisco.cmd("conf t")
	self.cisco.cmd("ip routing")
	self.cisco.cmd("end")
	self.myLog.info("cleanUp the required interfaces")
	self.cisco.clear_interface_config(intf=homePortDict['2/0'])
	self.cisco.clear_interface_config(intf=homePortDict['2/1'])
	self.cisco.clear_interface_config(intf=homePortDict['3/0'])
	self.cisco.clear_interface_config(intf=homePortDict['3/1'])
	self.cisco.clear_interface_config(intf=redPortDict['4/0'])
	self.cisco.clear_interface_config(intf=redPortDict['4/1'])
	self.cisco.clear_interface_config(intf=p_cisco_host2[0])
	self.cisco.clear_interface_config(intf=p_ssx2_cisco[1])
	
	self.myLog.info("Adding required vlans to database")
	self.cisco.cmd("conf t")
        self.cisco.cmd("no interface vlan  %s"%psr_var['vlan1'])
        self.cisco.cmd("no interface vlan  %s"%psr_var['vlan2'])
        self.cisco.cmd("no interface vlan  %s"%psr_var['vlan3'])
        self.cisco.cmd("no interface vlan  %s"%psr_var['vlan4'])
        self.cisco.cmd("no interface vlan  %s"%psr_var['vlan5'])
	self.cisco.cmd("end")
        self.cisco.cmd("vlan database")
        self.cisco.cmd("vlan %s"%psr_var['vlan1'])
        self.cisco.cmd("vlan %s"%psr_var['vlan2'])
        self.cisco.cmd("vlan %s"%psr_var['vlan3'])
        self.cisco.cmd("vlan %s"%psr_var['vlan4'])
        self.cisco.cmd("vlan %s"%psr_var['vlan5'])
	self.cisco.cmd("exit")

	#Configure the Cisco interfaces at transport side towards DUT
	self.cisco.cmd("conf t")
	self.cisco.cmd("interface gigabit %s"%p_cisco_host2[0])
        self.cisco.cmd("no ip address")
        self.cisco.cmd("no shutdown")
	self.cisco.cmd("switchport")
        self.cisco.cmd("switchport access vlan %s"%psr_var['vlan3'])
        self.cisco.cmd("switchport trunk encapsulation dot1q")
        self.cisco.cmd("switchport trunk allowed vlan %s"%psr_var['vlan3'])
        self.cisco.cmd("switchport mode trunk")
        self.cisco.cmd("exit")

	#Configuring VLAN interface towards Initiator end
	self.cisco.cmd("interface vlan %s"%psr_var['vlan5'])
        self.cisco.cmd("no ip address")
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("ip address %s"%psr_var['cisco_remote_ip/mask'])
	self.cisco.cmd("exit")

	#Cisco -> Ini
	self.cisco.cmd("interface giga %s"%psr_var['port_cisco_ini'])
        self.cisco.cmd("no ip address")
        self.cisco.cmd("no shutdown")
        self.cisco.cmd("switchport")
        self.cisco.cmd("switchport access vlan %s"%psr_var['vlan5'])
        self.cisco.cmd("switchport trunk encapsulation dot1q")
        self.cisco.cmd("switchport trunk allowed vlan %s"%psr_var['vlan5'])
        self.cisco.cmd("switchport mode trunk")
        self.cisco.cmd("exit")

	#Configuring the routes at Cisco
	self.myLog.info("Configuring the routes at Cisco")
	self.cisco.cmd("ip route %s %s"%(psr_var['cisco_remoteLpbk_route'],psr_var['remote_ip']))
	self.cisco.cmd("ip route %s %s"%(psr_var['route_remoteTun_ip'],psr_var['remote_ip']))
	self.cisco.cmd("ip route %s %s "%(psr_var['route_localTun_ip'],psr_var['local_primary_ip']))
	self.cisco.cmd("ip route %s %s 200 "%(psr_var['route_localTun_ip'],psr_var['local_secondary_ip']))
	self.cisco.cmd("ip route %s %s "%(psr_var['cisco_localLpbk_route'],psr_var['local_primary_ip']))
	self.cisco.cmd("ip route %s %s 200 "%(psr_var['cisco_localLpbk_route'],psr_var['local_secondary_ip']))
	self.cisco.cmd("ip route %s %s "%(psr_var['cisco_service_route'],psr_var['local_primary_ip']))
	self.cisco.cmd("ip route %s %s 200 "%(psr_var['cisco_service_route'],psr_var['local_secondary_ip']))
	self.cisco.cmd("end")
	
	#Moving to context
	self.Ini.cmd("context %s"%psr_var['context_name'])
	self.Resp.cmd("context %s"%psr_var['context_name1'])

	#Clear system counters
	self.Resp.clear_health_stats()

	#Clear fast-path counters
	self.Resp.cmd("clear fast-path counters") 

	#Clear debug logs
	self.Resp.cmd("clear log debug")
	self.Resp.cmd("no debug all")

	#Enable debug logs for iked , aaad and iplc
	self.Resp.cmd("debug module iked all")
	self.Resp.cmd("debug module aaad all")
	#self.Resp.cmd("debug module iplc all")

	# Make directory to save failed port combibnations log
	self.Resp.cmd("mkdir /hd/psr")
	pingSizeList = ("512", "1372", "1400")
	lastRedPort = ""
	cycle = 1
	prev_logical_slot = "100"
	# Load session home configuration.
	self.myLog.info("Loading the session home and tunnel configuration")
	self.Resp.config_from_string(psr_var['session_home_config'] %prev_logical_slot)
	self.Resp.config_from_string(psr_var['IKEv2_PSR_L2L_Resp_TUNNEL'])
	'''
	def sortedDictKeys(adict):
    		items = adict.items()
    		items.sort()
    		return [key for key, value in items]

	homePortList = sortedDictKeys(homePortDict)
	servPortList = sortedDictKeys(servPortDict)
	redPortList = sortedDictKeys(redPortDict)
	'''
	homePortList = ["2/0"]
	servPortList = ["3/1"]
	redPortList  = ["4/0"]

	self.myLog.info("homePortList: ")
	self.myLog.info(homePortList)
	self.myLog.info("servPortList: ")
	self.myLog.info(servPortList)
	self.myLog.info("redPortList: ")
	self.myLog.info(redPortList)

	#Now staet main loop(block)  Total combinations are 300
        for homeIndex in range(0,len(homePortList)):
                for redIndex in range(0,len(redPortList)):
                        redPort = redPortList[redIndex]
                        if redPort == lastRedPort:
                                continue

                        for servIndex in range(0, len(servPortList)):
                                homePort = homePortList[homeIndex]
	                        if homePort == redPortList[redIndex] and redIndex < len(redPortList)-1:
	                                redPort = redPortList[redIndex+1]
	                        else:
	                                redPort = redPortList[redIndex]
	                        servPort = servPortList[servIndex]
	                        if servPort == redPort or servPort == homePort:
	                                continue
	
	                        lastRedPort = redPort
				
				# This following condition is for cycle number to start with
			        if cycle <= 0:
					cycle = cycle+1
			        	continue
  
				self.myLog.info("\n ### Starting from cycle: %s ### \n"%cycle)
				self.myLog.info("\n\n\n\n\n #################### Cycle:%s #################### \n"%cycle)
				self.myLog.info("\n ###### HomePort-Redundant-Service : %s-%s-%s ###### \n"%(homePort,redPort,servPort))
				currentTime = time.ctime()
				self.myLog.info("\n Current time is : %s\n Test Start time : %s\n\n\n\n"%(currentTime, startTime))	
				# Load the session home configuration
				if homePort.split("/")[0] == "2":
					current_logical_slot = "100"
				else:
					current_logical_slot = "101"
				if prev_logical_slot != current_logical_slot:
					self.Resp.configcmd("no session-home slot %s loopback interface tunnel_local Responder"%prev_logical_slot)
					self.Resp.config_from_string(psr_var['session_home_config'] %current_logical_slot)
					prev_logical_slot = current_logical_slot

				#Load port specific configuration 
				self.myLog.info("\nLoad port specific configuration\n")
				self.cisco.clear_interface_config(intf=homePortDict['2/0'])
			        self.cisco.clear_interface_config(intf=homePortDict['2/1'])
			        self.cisco.clear_interface_config(intf=homePortDict['3/0'])
			        self.cisco.clear_interface_config(intf=homePortDict['3/1'])
				self.cisco.clear_interface_config(intf=servPortDict['2/0'])
			        self.cisco.clear_interface_config(intf=servPortDict['2/1'])
			        self.cisco.clear_interface_config(intf=servPortDict['3/0'])
			        self.cisco.clear_interface_config(intf=servPortDict['3/1'])
			        self.cisco.clear_interface_config(intf=redPortDict['4/0'])
			        self.cisco.clear_interface_config(intf=redPortDict['4/1'])

				self.myLog.info("configuring Cisco interfaces as per port configurations")
				self.cisco.configure_ipv4_vlan_interface(ip_addr=psr_var['cisco_local_primary_ip/mask'],intf=homePortDict[homePort],vlan=psr_var['vlan1'])
				self.cisco.configure_ipv4_vlan_interface(ip_addr=psr_var['cisco_local_secondary_ip/mask'],intf=redPortDict[redPort],vlan=psr_var['vlan2'])
				self.cisco.cmd("configure terminal")
				self.cisco.cmd("interface tengig %s"%servPortDict[servPort])
				self.cisco.cmd("no ip address")
				self.cisco.cmd("no shutdown")
				self.cisco.cmd("no switchport")
				self.cisco.cmd("switchport")
                                self.cisco.cmd("switchport access vlan %s"%psr_var['vlan3'])
                                self.cisco.cmd("switchport trunk encapsulation dot1q")
                                self.cisco.cmd("switchport trunk allowed vlan %s"%psr_var['vlan3'])
                                self.cisco.cmd("switchport mode trunk")
				self.cisco.cmd("end")
				self.Resp.clear_ports()
				self.Resp.config_from_string(psr_var['port_config_vlan_glcr'] %(homePort, psr_var['vlan1'], servPort, psr_var['vlan3'], redPort,psr_var['vlan2']))
				self.Ini.cmd("clear tunnel all")
				activeCard = homePort.split('/')[0]

				#Clear health stats
			        self.Ini.clear_health_stats()
			        self.Resp.clear_health_stats()

				# Time to tunnel come up
				time.sleep(psr_var['tunnelSleep'])

				#make sure that tunnel is up 
				self.myLog.info("Make sure that tunnel is up ")
				tunOp = check_tunnel_state(self.Resp)
                                if (int(tunOp) == 0):
                                        self.myLog.error("IKEv2 L2L Tunnel is not up")
                                        self.myLog.error("Cycle - %s : FAIL : TUNNEL IS NOT ESTABLISHED"%cycle)

                                        #Lets save the debug log...
                                        self.Resp.cmd("show log debug | save /hd/psr/%s.log"%cycle)
                                        cycle = cycle+1
                                        continue

				ses_yn = self.Resp.cmd("show ike-session brief")
				self.myLog.output("show ike-session brief : %s"%ses_yn)
				if ses_yn.splitlines()[-1].split()[2] != 'Y':
					self.myLog.error("Cycle - %s : FAIL : TUNNEL IS NOT ESTABLISHED"%cycle)
					#Lets save the debug log...
					self.Resp.cmd("show log debug | save /hd/psr/%s.log"%cycle)
                                	cycle = cycle+1
					continue

				# Make sure that Tunnel is up in home slot
				active_card = homePort.split('/')[0]
				self.myLog.info("Make sure that tunnel is up in Home Slot")
				homeSlot = ses_yn.splitlines()[-1].split()[0]
				if homeSlot != activeCard:
					self.myLog.error("Tunnel is not in home slot for cycle: %s - FAILED"%cycle)

				# Tunnel details
				self.myLog.info("Printing the details of the tunnel at Responder:\n\n")
				self.myLog.output("show ike-session list:%s\n"%self.Resp.cmd("show ike-session list"))
				self.myLog.output("show ike-session brief:%s\n"%self.Resp.cmd("show ike-session brief"))
				self.myLog.output("ike-session detail:%s\n"%self.Resp.cmd("show ike-session detail remote %s"%psr_var['remoteLpbk_ip']))

                                ## Added this as a part fo PR17700
                                self.myLog.output("show port counters drop:%s\n"%self.Resp.cmd("show port counters drop"))
                                self.myLog.output("diag ipsec sa slot 2 session-handle <> %s:\n"%self.Resp.cmd("diag ipsec sa slot 2 session-handle %s"%ses_yn.splitlines()[-1].split()[1]))

				# Verifying the tunnel details
				tunnel_op = verify_tunnel_details(self.Resp,name="local1",admin_status="enable",FSM_state="up",Role="Responder",nexthop=psr_var['cisco_local_primary_ip'],port=homePort,routing_protocol="static")
				if tunnel_op == 0:
					self.myLog.error("Tunnel details verification FAILED")

				self.myLog.info("\nVerifying the traffic thru tunnel for different pkt size\n")
				self.Resp.cmd("clear tunnel counters")

				#Send traffic with different pkt size from Transport to service end
				self.myLog.info("Verifying traffic with different pkt size from Transport to service end")
				for pingSize in pingSizeList:
					self.host1.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_service_ip'],psr_var['count'],pingSize))
					time.sleep(2)
					tunCnt = self.Resp.cmd("show tunnel counters")
					self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
					cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
					if cntOp != 0:
						self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
					self.Resp.cmd("clear tunnel counters")

				#Send traffic with different pkt size from Service to Transport end
				self.myLog.info("Verifying traffic with different pkt size from Service to Transport end")
				self.Resp.cmd("clear tunnel counters")
				for pingSize in pingSizeList:
					self.host2.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_ini_ip'],psr_var['count'],pingSize))
					time.sleep(2)
					tunCnt = self.Resp.cmd("show tunnel counters")
					self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
					cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
					if cntOp != 0:
						self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
					self.Resp.cmd("clear tunnel counters")

				# Verify REKEY
				self.myLog.info("Verifying Rekey")
				ike_op = parse_show_ike_session_detail(self.Resp,psr_var['remoteLpbk_ip'])
				rekey_val1 = ike_op['child_sa_negotiation_count']
				time.sleep(int(ike_op['child_sa_time_remaining']) + 3)
				ike_op = parse_show_ike_session_detail(self.Resp,psr_var['remoteLpbk_ip'])
				if int(ike_op['child_sa_negotiation_count']) <= int(rekey_val1):
					self.myLog.error("REKEY FAILED at Home Port")

				# Verifying traffic after REKEY
				self.myLog.info("\nVerifying traffic after REKEY\n")

				#Send traffic with different pkt size from Transport to service end
				self.myLog.info("Verifying traffic with different pkt size from Transport to service end")
				for pingSize in pingSizeList:
					self.host1.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_service_ip'],psr_var['count'],pingSize))
					time.sleep(2)
					tunCnt = self.Resp.cmd("show tunnel counters")
					self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
					cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
					if cntOp != 0:
						self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
					self.Resp.cmd("clear tunnel counters")

				#Send traffic with different pkt size from Service to Transport end
				self.myLog.info("Verifying traffic with different pkt size from Service to Transport end")
				self.Resp.cmd("clear tunnel counters")
				for pingSize in pingSizeList:
					self.host2.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_ini_ip'],psr_var['count'],pingSize))
					time.sleep(2)
					tunCnt = self.Resp.cmd("show tunnel counters")
					self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
					cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
					if cntOp != 0:
						self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
					self.Resp.cmd("clear tunnel counters")

				# Bringing down primary link from Cisco
				self.myLog.info("Bringing down primary link from Cisco")
				self.myLog.info("-" *70)
				self.myLog.info("Primary port Failover")
				self.myLog.info("-" *70)
				self.cisco.cmd("conf t")
				self.cisco.cmd("interface tengiga %s"%homePortDict[homePort])
			        self.cisco.cmd("shutdown")
				self.cisco.cmd("exit")
				self.cisco.cmd("interface vlan %s"%psr_var['vlan1'])
			        self.cisco.cmd("shutdown")
				self.cisco.cmd("end")
				time.sleep(10)

				#make sure that tunnel is up 
				self.myLog.info("Make sure that tunnel is up")
				tunOp = check_tunnel_state(self.Resp)
                                if (int(tunOp) == 0):
                                        self.myLog.error("IKEv2 Tunnel is not up")
                                        self.myLog.error("Cycle - %s : FAIL : TUNNEL IS NOT SWITCHED TO BACKUP PORT"%cycle)

                                        #Lets save the debug log...
                                        self.Resp.cmd("show log debug | save /hd/psr/%s.log"%cycle)
                                        cycle = cycle+1
                                        continue

				ses_yn = self.Resp.cmd("show ike-session brief")
				self.myLog.output("show ike-session brief : %s"%ses_yn)
				if ses_yn.splitlines()[-1].split()[2] != 'Y':
					self.myLog.error("Cycle - %s : FAIL : TUNNEL IS NOT swicthed to Backup Port"%cycle)
					#Lets save the debug log...
					self.Resp.cmd("show log debug | save /hd/psr/%s.log"%cycle)
                                	cycle = cycle+1
					continue

				self.myLog.info("-" *60)
				self.myLog.output("\n\nVerifying the tunnel parameters after Home port failover\n\n\n")
				self.myLog.info("-" *60)

				# Make sure that Tunnel is up in home slot
				active_card = homePort.split('/')[0]
				self.myLog.info("Make sure that tunnel is up in Home Slot")
				homeSlot = ses_yn.splitlines()[-1].split()[0]
				if homeSlot != activeCard:
					self.myLog.error("Tunnel is not in home slot for cycle: %s - FAILED"%cycle)

				# Tunnel details
				self.myLog.info("Printing the details of the tunnel at Responder after primary port failover:\n\n")
				self.myLog.output("show ike-session list:%s\n"%self.Resp.cmd("show ike-session list"))
				self.myLog.output("show ike-session brief:%s\n"%self.Resp.cmd("show ike-session brief"))
				self.myLog.output("ike-session detail:%s\n"%self.Resp.cmd("show ike-session detail remote %s"%psr_var['remoteLpbk_ip']))
				## Added this as a part fo PR17700
				self.myLog.output("show port counters drop:%s\n"%self.Resp.cmd("show port counters drop"))
				self.myLog.output("diag ipsec sa slot 2 session-handle <> %s:\n"%self.Resp.cmd("diag ipsec sa slot 2 session-handle %s"%ses_yn.splitlines()[-1].split()[1]))

				# Verifying the tunnel details
				self.myLog.info("Verifying the tunnel details")
				tunnel_op = verify_tunnel_details(self.Resp,name="local1",admin_status="enable",FSM_state="up",Role="Responder",nexthop=psr_var['cisco_local_secondary_ip'],port=redPort,routing_protocol="static")
                                if tunnel_op == 0:
                                        self.myLog.error("Tunnel details verification FAILED")

				self.myLog.info("\nVerifying the traffic thru tunnel for different pkt size\n")
				self.Resp.cmd("clear tunnel counters")

				#Send traffic with different pkt size from Transport to service end
				self.myLog.info("Verifying traffic with different pkt size from Transport to service end")
				for pingSize in pingSizeList:
					self.host1.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_service_ip'],psr_var['count'],pingSize))
					time.sleep(2)
					tunCnt = self.Resp.cmd("show tunnel counters")
					self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
					cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
					if cntOp != 0:
						self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
					self.Resp.cmd("clear tunnel counters")

				#Send traffic with different pkt size from Service to Transport end
				self.myLog.info("Verifying traffic with different pkt size from Service to Transport end")
				self.Resp.cmd("clear tunnel counters")
				for pingSize in pingSizeList:
					self.host2.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_ini_ip'],psr_var['count'],pingSize))
					time.sleep(2)
					tunCnt = self.Resp.cmd("show tunnel counters")
					self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
					cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
					if cntOp != 0:
						self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
					self.Resp.cmd("clear tunnel counters")

				# Verify REKEY
				self.myLog.info("Verifying Rekey")
				ike_op = parse_show_ike_session_detail(self.Resp,psr_var['remoteLpbk_ip'])
				rekey_val1 = ike_op['child_sa_negotiation_count']
				time.sleep(int(ike_op['child_sa_time_remaining']) + 3)
				ike_op = parse_show_ike_session_detail(self.Resp,psr_var['remoteLpbk_ip'])
				if int(ike_op['child_sa_negotiation_count']) <= int(rekey_val1):
					self.myLog.error("REKEY FAILED at Home Port")

				# Verifying traffic after REKEY
				self.myLog.info("\nVerifying traffic after REKEY\n")

				#Send traffic with different pkt size from Transport to service end
				self.myLog.info("Verifying traffic with different pkt size from Transport to service end")
				for pingSize in pingSizeList:
					self.host1.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_service_ip'],psr_var['count'],pingSize))
					time.sleep(2)
					tunCnt = self.Resp.cmd("show tunnel counters")
					self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
					cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
					if cntOp != 0:
						self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
					self.Resp.cmd("clear tunnel counters")

				#Send traffic with different pkt size from Service to Transport end
				self.myLog.info("Verifying traffic with different pkt size from Service to Transport end")
				self.Resp.cmd("clear tunnel counters")
				for pingSize in pingSizeList:
					self.host2.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_ini_ip'],psr_var['count'],pingSize))
					time.sleep(2)
					tunCnt = self.Resp.cmd("show tunnel counters")
					self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
					cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
					if cntOp != 0:
						self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
					self.Resp.cmd("clear tunnel counters")



				self.myLog.info("\n\nVerified the PSR, now need to verify the GLCR after PSR\n\n")
				self.Resp.cmd("reload card %s"%activeCard)
				time.sleep(10)

                                #make sure that tunnel is up
                                self.myLog.info("Make sure that tunnel is up")
                                tunOp = check_tunnel_state(self.Resp)
                                if (int(tunOp) == 0):
                                        self.myLog.error("IKEv2 Tunnel is not up")
                                        self.myLog.error("Cycle - %s : FAIL : TUNNEL IS NOT SWITCHED TO BACKUP SLOT"%cycle)

                                        #Lets save the debug log...
                                        self.Resp.cmd("show log debug | save /hd/psr/%s_glcr.log"%cycle)
                                        cycle = cycle+1
                                        continue

                                ses_yn = self.Resp.cmd("show ike-session brief")
                                self.myLog.output("show ike-session brief : %s"%ses_yn)
                                if ses_yn.splitlines()[-1].split()[2] != 'Y':
                                        self.myLog.error("Cycle - %s : FAIL : TUNNEL IS NOT swicthed to Backup Slot"%cycle)
                                        #Lets save the debug log...
                                        self.Resp.cmd("show log debug | save /hd/psr/%s_glcr.log"%cycle)
                                        cycle = cycle+1
                                        continue

                                self.myLog.info("-" *60)
                                self.myLog.output("\n\nVerifying the tunnel parameters after Home slot failover\n\n\n")
                                self.myLog.info("-" *60)

                                # Make sure that Tunnel is up in Backup slot
				self.myLog.info(" Make sure that Tunnel is up in Backup slot")
				bkpSlot = ses_yn.splitlines()[-1].split()[0]
                                if int(bkpSlot) != 4:
                                        self.myLog.error("Tunnel is not backed up in Redundant slot for cycle: %s - FAILED"%cycle)

                                # Tunnel details
                                self.myLog.info("Printing the details of the tunnel at Responder after primary port failover:\n\n")
                                self.myLog.output("show ike-session list:%s\n"%self.Resp.cmd("show ike-session list"))
                                self.myLog.output("show ike-session brief:%s\n"%self.Resp.cmd("show ike-session brief"))
                                self.myLog.output("ike-session detail:%s\n"%self.Resp.cmd("show ike-session detail remote %s"%psr_var['remoteLpbk_ip']))

                                ## Added this as a part fo PR17700
                                self.myLog.output("show port counters drop:%s\n"%self.Resp.cmd("show port counters drop"))
                                self.myLog.output("diag ipsec sa slot 2 session-handle <> %s:\n"%self.Resp.cmd("diag ipsec sa slot 2 session-handle %s"%ses_yn.splitlines()[-1].split()[1]))


                                # Verifying the tunnel details
                                self.myLog.info("Verifying the tunnel details")
                                tunnel_op = verify_tunnel_details(self.Resp,name="local1",admin_status="enable",FSM_state="up",Role="Responder",nexthop=psr_var['cisco_local_secondary_ip'],port=redPort,routing_protocol="static")
                                if tunnel_op == 0:
                                        self.myLog.error("Tunnel details verification FAILED")

                                self.myLog.info("\nVerifying the traffic thru tunnel for different pkt size\n")
                                self.Resp.cmd("clear tunnel counters")

                                #Send traffic with different pkt size from Transport to service end
                                self.myLog.info("Verifying traffic with different pkt size from Transport to service end")
                                for pingSize in pingSizeList:
                                        self.host1.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_service_ip'],psr_var['count'],pingSize))
                                        time.sleep(2)
                                        tunCnt = self.Resp.cmd("show tunnel counters")
                                        self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
                                        cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
                                        if cntOp != 0:
                                                self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
                                        self.Resp.cmd("clear tunnel counters")

                                #Send traffic with different pkt size from Service to Transport end
                                self.myLog.info("Verifying traffic with different pkt size from Service to Transport end")
                                self.Resp.cmd("clear tunnel counters")
                                for pingSize in pingSizeList:
                                        self.host2.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_ini_ip'],psr_var['count'],pingSize))
                                        time.sleep(2)
                                        tunCnt = self.Resp.cmd("show tunnel counters")
                                        self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
                                        cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
                                        if cntOp != 0:
                                                self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
                                        self.Resp.cmd("clear tunnel counters")
                                # Verify REKEY
                                self.myLog.info("Verifying Rekey")
                                ike_op = parse_show_ike_session_detail(self.Resp,psr_var['remoteLpbk_ip'])
                                rekey_val1 = ike_op['child_sa_negotiation_count']
                                time.sleep(int(ike_op['child_sa_time_remaining']) + 3)
                                ike_op = parse_show_ike_session_detail(self.Resp,psr_var['remoteLpbk_ip'])
                                if int(ike_op['child_sa_negotiation_count']) <= int(rekey_val1):
                                        self.myLog.error("REKEY FAILED at Home Port")

                                # Verifying traffic after REKEY
                                self.myLog.info("\nVerifying traffic after REKEY\n")

                                #Send traffic with different pkt size from Transport to service end
                                self.myLog.info("Verifying traffic with different pkt size from Transport to service end")
                                for pingSize in pingSizeList:
                                        self.host1.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_service_ip'],psr_var['count'],pingSize))
                                        time.sleep(2)
                                        tunCnt = self.Resp.cmd("show tunnel counters")
                                        self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
                                        cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
                                        if cntOp != 0:
                                                self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
                                        self.Resp.cmd("clear tunnel counters")
                                #Send traffic with different pkt size from Service to Transport end
                                self.myLog.info("Verifying traffic with different pkt size from Service to Transport end")
                                self.Resp.cmd("clear tunnel counters")
                                for pingSize in pingSizeList:
                                        self.host2.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_ini_ip'],psr_var['count'],pingSize))
                                        time.sleep(2)
                                        tunCnt = self.Resp.cmd("show tunnel counters")
                                        self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
                                        cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
                                        if cntOp != 0:
                                                self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
                                        self.Resp.cmd("clear tunnel counters")


				# Bringing up primary link Back
				self.Resp.wait4cards()
				time.sleep(10)
				self.myLog.info("Bringing up primary link back")
				self.myLog.info("-" *70)
				self.myLog.info("Primary port is UP Again")
				self.myLog.info("-" *70)
				self.cisco.cmd("conf t")
				self.cisco.cmd("interface tengig %s"%homePortDict[homePort])
			        self.cisco.cmd("no shutdown")
				self.cisco.cmd("exit")
				self.cisco.cmd("interface vlan %s"%psr_var['vlan1'])
			        self.cisco.cmd("no shutdown")
				self.cisco.cmd("end")
				time.sleep(30)


				#make sure that tunnel is up 
				self.myLog.info("Make sure that tunnel is up ")
				tunOp = check_tunnel_state(self.Resp)
                                if (int(tunOp) == 0):
                                        self.myLog.error("IKEv2 Tunnel is not up")
                                        self.myLog.error("Cycle - %s : FAIL : TUNNEL IS NOT SWITCHED BACK TO HOME PORT "%cycle)

                                        #Lets save the debug log...
                                        self.Resp.cmd("show log debug | save /hd/psr/%s.log"%cycle)
                                        cycle = cycle+1
                                        continue

				ses_yn = self.Resp.cmd("show ike-session brief")
				self.myLog.output("show ike-session brief : %s"%ses_yn)
				if ses_yn.splitlines()[-1].split()[2] != 'Y':
					self.myLog.error("Cycle - %s : FAIL : TUNNEL IS NOT SWITCHED BACK TO HOME PORT"%cycle)
					#Lets save the debug log...
					self.Resp.cmd("show log debug | save /hd/psr/%s.log"%cycle)
                                	cycle = cycle+1
					continue

				# Make sure that Tunnel is up in home slot
				active_card = homePort.split('/')[0]
				self.myLog.info("Make sure that tunnel is up in Home Slot")
				bkpSlot = ses_yn.splitlines()[-1].split()[0]
				if int(bkpSlot) != 4:
					self.myLog.error("Tunnel is not backed up in redundant slot after port switchback for cycle: %s - FAILED"%cycle)

				self.myLog.info("-" *60)
				self.myLog.output("\n\nVerifying the tunnel parameters after Home port is UP\n\n\n")
				self.myLog.info("-" *60)

				# Tunnel details
				self.myLog.info("Printing the details of the tunnel at Responder:\n\n")
				self.myLog.output("show ike-session list:%s\n"%self.Resp.cmd("show ike-session list"))
				self.myLog.output("show ike-session brief:%s\n"%self.Resp.cmd("show ike-session brief"))
				self.myLog.output("ike-session detail:%s\n"%self.Resp.cmd("show ike-session detail remote %s"%psr_var['remoteLpbk_ip']))

                                ## Added this as a part fo PR17700
                                self.myLog.output("show port counters drop:%s\n"%self.Resp.cmd("show port counters drop"))
                                self.myLog.output("diag ipsec sa slot 2 session-handle <> %s:\n"%self.Resp.cmd("diag ipsec sa slot 2 session-handle %s"%ses_yn.splitlines()[-1].split()[1]))

				# Verifying the tunnel details
				tunnel_op = verify_tunnel_details(self.Resp,name="local1",admin_status="enable",FSM_state="up",Role="Responder",nexthop=psr_var['cisco_local_primary_ip'],port=homePort,routing_protocol="static")
                                if tunnel_op == 0:
                                        self.myLog.error("Tunnel details verification FAILED")

				self.myLog.info("\nVerifying the traffic thru tunnel for different pkt size\n")
				self.Resp.cmd("clear tunnel counters")

				#Send traffic with different pkt size from Transport to service end
				self.myLog.info("Verifying traffic with different pkt size from Transport to service end")
				for pingSize in pingSizeList:
					self.host1.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_service_ip'],psr_var['count'],pingSize))
					time.sleep(2)
					tunCnt = self.Resp.cmd("show tunnel counters")
					self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
					cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
					if cntOp != 0:
						self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
					self.Resp.cmd("clear tunnel counters")

				#Send traffic with different pkt size from Service to Transport end
				self.myLog.info("Verifying traffic with different pkt size from Service to Transport end")
				self.Resp.cmd("clear tunnel counters")
				for pingSize in pingSizeList:
					self.host2.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_ini_ip'],psr_var['count'],pingSize))
					time.sleep(2)
					tunCnt = self.Resp.cmd("show tunnel counters")
					self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
					cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
					if cntOp != 0:
						self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
					self.Resp.cmd("clear tunnel counters")

				# Verify REKEY
				self.myLog.info("Verifying Rekey")
				ike_op = parse_show_ike_session_detail(self.Resp,psr_var['remoteLpbk_ip'])
				rekey_val1 = ike_op['child_sa_negotiation_count']
				time.sleep(int(ike_op['child_sa_time_remaining']) + 3)
				ike_op = parse_show_ike_session_detail(self.Resp,psr_var['remoteLpbk_ip'])
				if int(ike_op['child_sa_negotiation_count']) <= int(rekey_val1):
					self.myLog.error("REKEY FAILED at Home Port")

				# Verifying traffic after REKEY
				self.myLog.info("\nVerifying traffic after REKEY\n")

				#Send traffic with different pkt size from Transport to service end
				self.myLog.info("Verifying traffic with different pkt size from Transport to service end")
				for pingSize in pingSizeList:
					self.host1.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_service_ip'],psr_var['count'],pingSize))
					time.sleep(2)
					tunCnt = self.Resp.cmd("show tunnel counters")
					self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
					cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
					if cntOp != 0:
						self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
					self.Resp.cmd("clear tunnel counters")

				#Send traffic with different pkt size from Service to Transport end
				self.myLog.info("Verifying traffic with different pkt size from Service to Transport end")
				self.Resp.cmd("clear tunnel counters")
				for pingSize in pingSizeList:
					self.host2.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_ini_ip'],psr_var['count'],pingSize))
					time.sleep(2)
					tunCnt = self.Resp.cmd("show tunnel counters")
					self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
					cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
					if cntOp != 0:
						self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
					self.Resp.cmd("clear tunnel counters")

				# Verify the tunnel after glc-sitchback
				self.Resp.cmd("system glc-switchback")
				time.sleep(10)
				self.Resp.wait4cards()
				time.sleep(10)
				self.myLog.info("\n\n Verifyng the details after GLC switchback\n\n")

                                #make sure that tunnel is up
                                self.myLog.info("Make sure that tunnel is up ")
                                tunOp = check_tunnel_state(self.Resp)
                                if (int(tunOp) == 0):
                                        self.myLog.error("IKEv2 L2L Tunnel is not up")
                                        self.myLog.error("Cycle - %s : FAIL : TUNNEL IS NOT ESTABLISHED"%cycle)

                                        #Lets save the debug log...
                                        self.Resp.cmd("show log debug | save /hd/psr/%s.log"%cycle)
                                        cycle = cycle+1
                                        continue

                                ses_yn = self.Resp.cmd("show ike-session brief")
                                self.myLog.output("show ike-session brief : %s"%ses_yn)
                                if ses_yn.splitlines()[-1].split()[2] != 'Y':
                                        self.myLog.error("Cycle - %s : FAIL : TUNNEL IS NOT ESTABLISHED"%cycle)
                                        #Lets save the debug log...
                                        self.Resp.cmd("show log debug | save /hd/psr/%s.log"%cycle)
                                        cycle = cycle+1
                                        continue

                                # Make sure that Tunnel is up in home slot
                                self.myLog.info("Make sure that tunnel is up in Home Slot")
                                homeSlot = ses_yn.splitlines()[-1].split()[0]
                                if homeSlot != activeCard:
                                        self.myLog.error("Tunnel is not in home slot for cycle: %s - FAILED"%cycle)

                                # Tunnel details
                                self.myLog.info("Printing the details of the tunnel at Responder:\n\n")
                                self.myLog.output("show ike-session list:%s\n"%self.Resp.cmd("show ike-session list"))
                                self.myLog.output("show ike-session brief:%s\n"%self.Resp.cmd("show ike-session brief"))
                                self.myLog.output("ike-session detail:%s\n"%self.Resp.cmd("show ike-session detail remote %s"%psr_var['remoteLpbk_ip']))

                                ## Added this as a part fo PR17700
                                self.myLog.output("show port counters drop:%s\n"%self.Resp.cmd("show port counters drop"))
                                self.myLog.output("diag ipsec sa slot 2 session-handle <> %s:\n"%self.Resp.cmd("diag ipsec sa slot 2 session-handle %s"%ses_yn.splitlines()[-1].split()[1]))

                                # Verifying the tunnel details
                                tunnel_op = verify_tunnel_details(self.Resp,name="local1",admin_status="enable",FSM_state="up",Role="Responder",nexthop=psr_var['cisco_local_primary_ip'],port=homePort,routing_protocol="static")
                                if tunnel_op == 0:
                                        self.myLog.error("Tunnel details verification FAILED")

                                self.myLog.info("\nVerifying the traffic thru tunnel for different pkt size\n")
                                self.Resp.cmd("clear tunnel counters")


                                #Send traffic with different pkt size from Transport to service end
                                self.myLog.info("Verifying traffic with different pkt size from Transport to service end")
                                for pingSize in pingSizeList:
                                        self.host1.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_service_ip'],psr_var['count'],pingSize))
                                        time.sleep(2)
                                        tunCnt = self.Resp.cmd("show tunnel counters")
                                        self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
                                        cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
                                        if cntOp != 0:
                                                self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
                                        self.Resp.cmd("clear tunnel counters")

                                #Send traffic with different pkt size from Service to Transport end
                                self.myLog.info("Verifying traffic with different pkt size from Service to Transport end")
                                self.Resp.cmd("clear tunnel counters")
                                for pingSize in pingSizeList:
                                        self.host2.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_ini_ip'],psr_var['count'],pingSize))
                                        time.sleep(2)
                                        tunCnt = self.Resp.cmd("show tunnel counters")
                                        self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
                                        cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
                                        if cntOp != 0:
                                                self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
                                        self.Resp.cmd("clear tunnel counters")

                                # Verify REKEY
                                self.myLog.info("Verifying Rekey")
                                ike_op = parse_show_ike_session_detail(self.Resp,psr_var['remoteLpbk_ip'])
                                rekey_val1 = ike_op['child_sa_negotiation_count']
                                time.sleep(int(ike_op['child_sa_time_remaining']) + 3)
                                ike_op = parse_show_ike_session_detail(self.Resp,psr_var['remoteLpbk_ip'])
                                if int(ike_op['child_sa_negotiation_count']) <= int(rekey_val1):
                                        self.myLog.error("REKEY FAILED at Home Port")

                                # Verifying traffic after REKEY
                                self.myLog.info("\nVerifying traffic after REKEY\n")

                                #Send traffic with different pkt size from Transport to service end
                                self.myLog.info("Verifying traffic with different pkt size from Transport to service end")
                                for pingSize in pingSizeList:
                                        self.host1.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_service_ip'],psr_var['count'],pingSize))
                                        time.sleep(2)
                                        tunCnt = self.Resp.cmd("show tunnel counters")
                                        self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
                                        cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
                                        if cntOp != 0:
                                                self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
                                        self.Resp.cmd("clear tunnel counters")

                                #Send traffic with different pkt size from Service to Transport end
                                self.myLog.info("Verifying traffic with different pkt size from Service to Transport end")
                                self.Resp.cmd("clear tunnel counters")
                                for pingSize in pingSizeList:
                                        self.host2.cmd("sudo ping %s -c %s -s %s -M dont -i 0 -w 1"%(psr_var['linux_ini_ip'],psr_var['count'],pingSize))
                                        time.sleep(2)
                                        tunCnt = self.Resp.cmd("show tunnel counters")
                                        self.myLog.output("Tunel counters for pkt size %s : %s"%(pingSize,tunCnt))
                                        cntOp = verify_tunnel_counters_with_name(self.Resp,tun_name="local1")
                                        if cntOp != 0:
                                                self.myLog.error("Traffic is not via tunnel for pkt size %s"%pingSize)
                                        self.Resp.cmd("clear tunnel counters")

                                #Stats
				self.myLog.info("-" *70)
                                self.myLog.info("\n\nGetting statistics before going for next cycle:")
                                self.myLog.info("Current cycle:%s HomePort-Redundant-Service : %s-%s-%s\n\n"%(cycle,homePort,redPort,servPort))
				self.myLog.info("-" *70)

                                #System counters
                                sysCnters = self.Resp.cmd("show syscount")
                                self.myLog.info("System Counters : %s" %sysCnters)

                                #CRIT and ERR events
                                critErrEvnts = self.Resp.cmd("show log standard | grep \"ERR \"") + self.Resp.cmd("show log standard | grep CRIT")
                                self.myLog.info("CRIT and ERR Events : %s" %critErrEvnts)

                                #Fast path counters
                                fastPthCnters = self.Resp.cmd("show fast-path counters")
                                self.myLog.info("Fast-path counters : %s\n\n"%fastPthCnters)

                                #Port  counters
                                portCnters = self.Resp.cmd("show port counters")
                                self.myLog.info("Port counters : %s\n\n"%portCnters)

                                #Ip counters
                                ipCnters = self.Resp.cmd("show ip counters general")
                                self.myLog.info("Ip counters general: %s\n\n"%ipCnters)

                                hs = self.Resp.get_health_stats()
                                #self.failUnless(is_healthy(hs, Warn_logs=100), "Platform is not healthy")

			        # Checking SSX Health after test
			        hs = self.Resp.get_health_stats()
			        if not (is_healthy(hs)):
			                self.myLog.error("Platform is not healthy at Responder")
			        hs = self.Ini.get_health_stats()
			        if not (is_healthy(hs)):
			                self.myLog.error("Platform is not healthy at Initiator")

                                #Clear fast-path counters
                                self.Resp.cmd("clear fast-path counters")

                                #Clear port counters and Ip counters
                                self.Resp.cmd("clear port counters")
                                self.Resp.cmd("clear ip counters")

                                #Clear log debugs
                                self.Resp.cmd("clear log debug")

				# Going for next cycle
				self.myLog.info("Going for next cycle")
                                cycle = cycle+1



        # Checking SSX Health after test
        hs = self.Resp.get_health_stats()
	if not (is_healthy(hs)):
	        self.myLog.error("Platform is not healthy at Responder")
        hs = self.Ini.get_health_stats()
	if not (is_healthy(hs)):
	        self.myLog.error("Platform is not healthy at Initiator")


if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_SLA_MA_FUN_031)
        test_runner().run(suite)

