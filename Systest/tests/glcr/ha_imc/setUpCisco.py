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

DESCRIPTION: This script is used to setup all the cisco interfaces which are used in test topology.
TEST MATRIX: 
TEST CASE  : NA
TOPOLOGY   : GLC-R Setup with IXIA Connectivity

HOW TO RUN : python2.5 setUpCisco.py <route-Y/N>
AUTHOR     : rajshekar@stoke.com
REVIEWER   : 
"""

import sys, os
from string import *

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#Import Frame-work libraries
from CISCO import *
from log import *
from StokeTest import test_case, test_suite, test_runner
from log import buildLogger
from logging import getLogger
from helpers import is_healthy, insert_char_to_string
from misc import *

#Import config and topo files
from config import *
from topo import *

routeOption = sys.argv[1].lower()

class test_setUpCisco(test_case):
    myLog = getLogger()

    def setUp(self):

        #Establish a telnet session
        self.myLog.info(__doc__)
        self.cisco = CISCO(cisco["ip_addr"])

        #Initiate the telnet session
        self.cisco.console(cisco["ip_addr"])

    def tearDown(self):
	pass

    def test_setUpCisco(self):

        self.myLog.output("\n**********Setting up the cisco device used in test**************\n")
	
	self.myLog.info("\nSetting up Cisco\n")
        self.myLog.info("Enable routing at Cisco")
        self.cisco.cmd("conf t")
        self.cisco.cmd("ip routing")
        self.cisco.cmd("exit")
      
	self.myLog.info("Creating the required vrfs")
	self.cisco.cmd("configure terminal")
	self.cisco.cmd("no ip vrf %s"%haimc_var['vrf_name'])       
	self.cisco.cmd("ip vrf %s"%haimc_var['vrf_name'])
	self.cisco.cmd("rd 2:3")
	self.cisco.cmd("exit")
        
        self.cisco.cmd("no ip vrf %s"%haimc_var['vrf_name2'])
        
        self.cisco.cmd("ip vrf %s"%haimc_var['vrf_name2'])
        self.cisco.cmd("rd 2:9")
        
        self.cisco.cmd("exit")
        """
        self.cisco.cmd("no ip sla %s"%haimc_var['rtr_id1'])
        self.cisco.cmd("ip sla %s"%haimc_var['rtr_id1'])
        self.cisco.cmd("icmp-echo %s source-ip %s"%(haimc_var['active_slot2_ip'],haimc_var['cisco_active_slot2_ip']))
        self.cisco.cmd("vrf %s"%haimc_var['vrf_name2'])
        self.cisco.cmd("exit")
        self.cisco.cmd("ip sla schedule %s start-time now life forever"%haimc_var['rtr_id1'])
        self.cisco.cmd("no ip sla %s"%haimc_var['rtr_id2'])
        self.cisco.cmd("ip sla %s"%haimc_var['rtr_id2'])
        self.cisco.cmd("icmp-echo %s source-ip %s"%(haimc_var['active_slot3_ip'],haimc_var['cisco_active_slot3_ip']))
        self.cisco.cmd("vrf %s"%haimc_var['vrf_name'])
        self.cisco.cmd("exit")
        self.cisco.cmd("ip sla schedule %s start-time now life forever"%haimc_var['rtr_id2'])
        """
        self.myLog.info("Adding required vlans to database")
        self.cisco.cmd("vlan database")
        self.cisco.cmd("vlan %s"%haimc_var['vlan4slot2'])
        self.cisco.cmd("vlan %s"%haimc_var['standby_vlan4slot2'])
        self.cisco.cmd("vlan %s"%haimc_var['service_vlan4slot2'])
        self.cisco.cmd("vlan %s"%haimc_var['serback_vlan4slot2'])
        self.cisco.cmd("vlan %s"%haimc_var['vlan4slot3'])
        self.cisco.cmd("vlan %s"%haimc_var['standby_vlan4slot3'])
        self.cisco.cmd("vlan %s"%haimc_var['service_vlan4slot3'])
        self.cisco.cmd("vlan %s"%haimc_var['serback_vlan4slot3'])
        self.cisco.cmd("vlan %s"%haimc_var['ini_vlan4slot2'])
        self.cisco.cmd("vlan %s"%haimc_var['ini_vlan4slot3'])
        self.cisco.cmd("exit")
        self.cisco.cmd("exit")

	# Configuring the slot2 related stuffs.
        self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_active_slot2_ip_mask'],intf=haimc_var['port_cisco_active_4slot2'],vlan=haimc_var['vlan4slot2'],vrf=haimc_var['vrf_name2'])
        self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_standby_4slot2_ip_mask'],intf=haimc_var['port_cisco_standby_4slot2'],vlan=haimc_var['standby_vlan4slot2'],vrf=haimc_var['vrf_name2'])
	#self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_rad_intf_4slot2_ip/mask'],intf=haimc_var['port_cisco_rad_intf_4slot2'],vlan=haimc_var['service_vlan4slot2'],vrf=haimc_var['vrf_name2'])
	#self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_bkp_rad_intf_4slot2_ip/mask'],intf=haimc_var['port_cisco_bkp_rad_intf_4slot2'],vlan=haimc_var['serback_vlan4slot2'],vrf=haimc_var['vrf_name2'])

        # Configuring the slot3 related stuffs.
        self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_active_slot3_ip_mask'],intf=haimc_var['port_cisco_active_4slot3'],vlan=haimc_var['vlan4slot3'],vrf=haimc_var['vrf_name'])
        self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_standby_4slot3_ip_mask'],intf=haimc_var['port_cisco_standby_4slot3'],vlan=haimc_var['standby_vlan4slot3'],vrf=haimc_var['vrf_name'])
        #self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_rad_intf_4slot3_ip/mask'],intf=haimc_var['port_cisco_rad_intf_4slot3'],vlan=haimc_var['service_vlan4slot3'],vrf=haimc_var['vrf_name'])
        #self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_bkp_rad_intf_4slot3_ip/mask'],intf=haimc_var['port_cisco_bkp_rad_intf_4slot3'],vlan=haimc_var['serback_vlan4slot3'],vrf=haimc_var['vrf_name'])

        if p_to_rad_active_ssx_cisco_slot2[0] == p_to_rad_active_ssx_cisco_slot3[0] :
            self.cisco.cmd("end")
            self.cisco.cmd("conf t")
            self.cisco.cmd("inter tenGigabitEthernet %s"%haimc_var['port_cisco_rad_intf_4slot3'])
            self.cisco.cmd("no swi")
            self.cisco.cmd("switchport")
            self.cisco.cmd("switchport trunk encapsulation dot1q")
            self.cisco.cmd("switchport trunk allowed vlan %s,%s"%(haimc_var['service_vlan4slot3'],haimc_var['service_vlan4slot2']))
            self.cisco.cmd("switchport mode trunk")
            self.cisco.cmd("end")
            self.cisco.configure_only_vlan_interface(ip_addr=haimc_var['cisco_rad_intf_4slot3_ip/mask'],vlan=haimc_var['service_vlan4slot3'],vrf=haimc_var['vrf_name'])
            self.cisco.configure_only_vlan_interface(ip_addr=haimc_var['cisco_rad_intf_4slot2_ip/mask'],vlan=haimc_var['service_vlan4slot2'],vrf=haimc_var['vrf_name2'])

        else :
            self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_rad_intf_4slot2_ip/mask'],intf=haimc_var['port_cisco_rad_intf_4slot2'],vlan=haimc_var['service_vlan4slot2'],vrf=haimc_var['vrf_name2'])
            self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_rad_intf_4slot3_ip/mask'],intf=haimc_var['port_cisco_rad_intf_4slot3'],vlan=haimc_var['service_vlan4slot3'],vrf=haimc_var['vrf_name'])

        if p_to_rad_standby_ssx_cisco_slot3[0] == p_to_rad_standby_ssx_cisco_slot2[0] : 
            self.cisco.cmd("end")
            self.cisco.cmd("conf t")
            self.cisco.cmd("inter tenGigabitEthernet %s"%haimc_var['port_cisco_bkp_rad_intf_4slot3'])
            self.cisco.cmd("no swi")
            self.cisco.cmd("switchport")
            self.cisco.cmd("switchport trunk encapsulation dot1q")
            self.cisco.cmd("switchport trunk allowed vlan %s,%s"%(haimc_var['serback_vlan4slot2'],haimc_var['serback_vlan4slot3']))
            self.cisco.cmd("switchport mode trunk")
            self.cisco.cmd("end")
            self.cisco.configure_only_vlan_interface(ip_addr=haimc_var['cisco_bkp_rad_intf_4slot3_ip/mask'],vlan=haimc_var['serback_vlan4slot3'],vrf=haimc_var['vrf_name'])
            self.cisco.configure_only_vlan_interface(ip_addr=haimc_var['cisco_bkp_rad_intf_4slot2_ip/mask'],vlan=haimc_var['serback_vlan4slot2'],vrf=haimc_var['vrf_name2'])
        else :
            self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_bkp_rad_intf_4slot3_ip/mask'],intf=haimc_var['port_cisco_bkp_rad_intf_4slot3'],vlan=haimc_var['serback_vlan4slot3'],vrf=haimc_var['vrf_name'])
            self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_bkp_rad_intf_4slot2_ip/mask'],intf=haimc_var['port_cisco_bkp_rad_intf_4slot2'],vlan=haimc_var['serback_vlan4slot2'],vrf=haimc_var['vrf_name2'])

	# Configure Initiator side interfaces
	self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_ini_slot2_ip/mask'],intf=haimc_var['port_cisco_ini_slot2'],vlan=haimc_var['ini_vlan4slot2'],vrf=haimc_var['vrf_name2'])
	self.cisco.configure_ipv4_vlan_interface(ip_addr=haimc_var['cisco_ini_slot3_ip/mask'],intf=haimc_var['port_cisco_ini_slot3'],vlan=haimc_var['ini_vlan4slot3'],vrf=haimc_var['vrf_name'])

        # Configure IP SLA for Active paths
        self.myLog.info("Configure IP SLA for Active paths")
        self.cisco.cmd("configure terminal")
        self.cisco.cmd("ip route vrf %s %s %s"%(haimc_var['vrf_name2'],haimc_var['dummy_intf_routes_slot2'], haimc_var['ini_cisco_slot2_ip']))
        self.cisco.cmd("ip route vrf %s %s  %s"%(haimc_var['vrf_name'],haimc_var['dummy_intf_routes_slot3'], haimc_var['ini_cisco_slot3_ip']))
        self.cisco.cmd("ip route vrf %s %s %s"%(haimc_var['vrf_name2'],haimc_var['tunnel_intf_routes_slot2'], haimc_var['ini_cisco_slot2_ip']))
        self.cisco.cmd("ip route vrf %s %s %s"%(haimc_var['vrf_name'],haimc_var['tunnel_intf_routes_slot3'], haimc_var['ini_cisco_slot3_ip']))
        self.cisco.cmd("ip route vrf %s %s %s"%(haimc_var['vrf_name'], haimc_var['cisco_ssx_ses_traffic_route'],haimc_var['ixia_cisco_slot3_ip']))
        self.cisco.cmd("ip route vrf %s %s %s"%(haimc_var['vrf_name2'], haimc_var['cisco_ssx_slot3_ses_traffic_route'],haimc_var['ixia_cisco_slot2_ip']))

        if routeOption == "y":
                self.cisco.cmd("ip route vrf %s %s %s "%(haimc_var['vrf_name2'],haimc_var['cisco_lpbk_ip/mask'], haimc_var['active_slot2_ip']))
                self.cisco.cmd("ip route vrf %s %s %s "%(haimc_var['vrf_name'],haimc_var['cisco_lpbk_ip1/mask'], haimc_var['active_slot3_ip']))
                self.cisco.cmd("ip route vrf %s %s %s "%(haimc_var['vrf_name2'],haimc_var['resp_tunnel_intf_routes_slot2'],haimc_var['active_slot2_ip']))
                self.cisco.cmd("ip route vrf %s %s %s "%(haimc_var['vrf_name'],haimc_var['resp_tunnel_intf_routes_slot3'],haimc_var['active_slot3_ip']))
              
                #self.cisco.cmd("ip route vrf %s %s %s track %s"%(haimc_var['vrf_name2'],haimc_var['cisco_lpbk_ip/mask'], haimc_var['active_slot2_ip'],haimc_var['rtr_id1']))
                self.cisco.cmd("ip route vrf %s %s %s 200"%(haimc_var['vrf_name2'],haimc_var['cisco_lpbk_ip/mask'], haimc_var['standby_4slot2_ip']))
                #self.cisco.cmd("ip route vrf %s %s %s track %s"%(haimc_var['vrf_name'],haimc_var['cisco_lpbk_ip1/mask'], haimc_var['active_slot3_ip'],haimc_var['rtr_id2']))
                self.cisco.cmd("ip route vrf %s %s %s 200"%(haimc_var['vrf_name'],haimc_var['cisco_lpbk_ip1/mask'], haimc_var['standby_4slot3_ip']))
                #self.cisco.cmd("ip route vrf %s %s %s track %s"%(haimc_var['vrf_name2'],haimc_var['resp_tunnel_intf_routes_slot2'],haimc_var['active_slot2_ip'],haimc_var['rtr_id1']))
                self.cisco.cmd("ip route vrf %s %s %s 200"%(haimc_var['vrf_name2'],haimc_var['resp_tunnel_intf_routes_slot2'],haimc_var['standby_4slot2_ip']))
                #self.cisco.cmd("ip route vrf %s %s %s track %s"%(haimc_var['vrf_name'],haimc_var['resp_tunnel_intf_routes_slot3'],haimc_var['active_slot3_ip'],haimc_var['rtr_id2']))
                self.cisco.cmd("ip route vrf %s %s %s 200"%(haimc_var['vrf_name'],haimc_var['resp_tunnel_intf_routes_slot3'],haimc_var['standby_4slot3_ip']))
                self.cisco.cmd("ip route vrf %s %s %s"%(haimc_var['vrf_name2'], haimc_var['cisco_route_ini_slot2_ixia'],haimc_var['rad_intf_4slot2_ip']))
                self.cisco.cmd("ip route vrf %s %s %s 200"%(haimc_var['vrf_name2'],haimc_var['cisco_route_ini_slot2_ixia'],haimc_var['bkp_rad_intf_4slot2_ip']))
                self.cisco.cmd("ip route vrf %s %s %s"%(haimc_var['vrf_name'], haimc_var['cisco_route_ini_slot3_ixia'],haimc_var['rad_intf_4slot3_ip']))
                self.cisco.cmd("ip route vrf %s %s %s 200"%(haimc_var['vrf_name'], haimc_var['cisco_route_ini_slot3_ixia'],haimc_var['bkp_rad_intf_4slot3_ip']))

	
if __name__ == '__main__':
        if os.environ.has_key('TEST_LOG_DIR'):
                os.mkdir(os.environ['TEST_LOG_DIR'])
                os.chdir(os.environ['TEST_LOG_DIR'])
        filename = os.path.split(__file__)[1].replace('.py','.log')
        log = buildLogger(filename, debug=True, console=True)
        suite = test_suite()
        suite.addTest(test_setUpCisco)
        test_runner().run(suite)
