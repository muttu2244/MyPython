#!/usr/bin/env python2.5
#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

"""
DESCRIPTION             : APIs for OSPF derived from the perl module OSPF.pm and few APIs added

TEST PLAN               : OSPF Porting
AUTHOR                  : Jameer - jameer@stoke.com
REVIEWER                : Venkat - krao@stoke.com
DEPENDENCIES            : Linux.py,device.py
"""

import sys, os
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

import time
import string
import sys
import re
from pexpect import *

from logging import getLogger
log = getLogger()
from StokeTest import test_case

def verify_ospf_status(self,state="Full"):
    state = self.cmd("show ip ospf neighbor |  grep %s"%state)
    if state:
        return 0
    else  :
        return 1

def verify_no_of_neighbors(self,number=2):
    """ Returns 0 on success, 1 on failure"""
    neighborOp = self.cmd("show ip ospf neighbor |  grep -i Full")
    neighbors = int(len(ospfOp.splitlines())) - 1 

    if int(number) != int(neighbors):
	return 1
    else:
	return 0

def verify_ospf_attributes(self,spf_delay=5,hold_time=10):
    log.info("Verifying the SPF Delay")
    ospf_op = self.cmd("show ip ospf")
    log.output("Output of the command:show ip ospf\n%s"%ospf_op)
    op = re.search("SPF\s+schedule\s+delay\s+(\d+)\s+",ospf_op)
    op = op.group(1)
    if int(op) != int(spf_delay):
        log.error("SPF delay is not %d"%spf_delay)
        return 1
    log.info("TEST PASSED for SPF Delay")
    log.info("Verifying the Hold time between two SPFs")
    op = re.search("Hold\s+time\s+between\s+two\s+SPFs\s+(\d+)\s+",ospf_op)
    op = op.group(1)
    if int(op) != int(hold_time):
        log.error("Hold time between two SPFs is not %d"%hold_time)
        return 1
    log.output("TEST PASSED for Hold time")
    return 0

def verify_ospf_intf(self,context="",intf="lo0",intf_ip="11.11.11.11/32",area="0",nw="",mtu="",cost="",tx_delay="",state="",priority="",hello="",dead="",auth_type=""):
    passed = []
    failed = []
    if context:
	self.cmd("context %s"%context)
	passed.append("context:%s"%context)
    log.info("Verifying the interface state:")
    intf_op = self.cmd("show ip ospf interface %s"%intf)
    log.cmd("show ip ospf interface %s"%intf)
    log.output("output of the command:%s"%intf_op)
    if not intf_op:
        log.error("Interface %s is not confgured in OSPF"%intf)
        return 1
    log.info("Verifying the interface state")
    if intf_op.split()[2] != "UP":
        log.error("Interface state is not UP")
        return 1
    log.info("Test Passed: Interface %s state is UP"%intf)
    passed.append("intf_state:%s"%intf_op.split()[2])
    log.info("Checking interface address")
    op = re.search("Internet\s+Address\s+([\d+.\/]+)",intf_op)
    op = op.group(1)
    intf_ip = intf_ip.strip()
    if op != intf_ip:
        log.error("Failed: Interface ip is not %s"%intf_ip)
	failed.append("IP:%s"%intf_ip)
    else:
        log.info("Passed: interface ip is %s"%intf_ip)
	passed.append("IP:%s"%op)
        
    log.info("Checking the area")
    op = re.search("\s+Area\s+([\d+.]+)",intf_op)
    op = op.group(1)
    op = op.split('.')[-1]
    if int(op) != int(area):
        log.error("Failed: Area is not %s"%area)
	failed.append("AREA:%s"%area)
    else:
        log.info("Passed: Area is %s"%area)
	passed.append("AREA:%s"%area)
    if mtu:
     if mtu=="no":
        log.info("Checking that interface has no mtu")
        op = re.search("\s+MTU\s+(\d+)",intf_op)
        if op:
            log.error("Failed: Interface has mtu")
	    failed.append("MTU:%s"%mtu)
	else:
	    log.output("Passed: Interface has no mtu")
	    passed.append("MTU:%s"%mtu)
     else:
        log.info("Checking that interface has mtu")
        op = re.search("\s+MTU\s+(\d+)",intf_op)
        op = op.group(1)
        if int(op) != int(mtu):
            log.error("Failed: Interface has no mtu %s"%mtu)
	    failed.append("MTU:%s"%mtu) 
        else:
            log.info("Passed: Interface has mtu %s"%mtu)
	    passed.append("MTU:%s"%op)
    if nw:
        log.info("Verifying the network type")
	op = re.search("Network\s+Type\s+(\w+)",intf_op)
	if not op:
		log.error("Failed: Network Type is not found")
		failed.append("NW Type:%s"%nw)
	else:
		op = op.group(1)
		op = op.strip()
		if op != nw:
			log.error("Failed: Network type is not: %s"%nw)
			failed.append("NW Type:%s"%nw)
		else:
			log.output("Passed: Network Type is %s"%op)
			passed.append("NW Type:%s"%op)

    if cost:
	log.info("Verifying the COST of the Link")
	op = re.search("\s+Cost:\s+(\d+)",intf_op)
	if not op:
		log.error("Failed: Connot find Cost")
		failed.append("COST:%s"%cost)
	else:
		op = op.group(1)
		if int(op) != int(cost):
			log.error("Cost is not %s"%cost)
			failed.append("COST:%s"%cost)
		else:
			log.output("Passed: Cost is %s"%op)
			passed.append("COST:%s"%op)

    if tx_delay:
	log.info("Verifying the transmit delay") 
	op = re.search("\s+Transmit\s+Delay\s+is\s+(\d+)\s+sec",intf_op)
        if not op:
                log.error("Failed: Connot find Transmit Delay")
		failed.append("Tx Delay:%s"%tx_delay)
	else:
		op = op.group(1)
		if int(op) != int(tx_delay):
			log.error("Failed: Transmit Delay ios not %s"%tx_delay)
			failed.append("Tx Delay:%s"%tx_delay)
		else:
			log.output("Passed: Transmit delay is %s"%op)
			passed.append("Tx Delay:%s"%op)

    if state:
	log.info("Verifying the State of the interface")
	op = re.search("\s+State\s+(\w+),",intf_op)
        if not op:
                log.error("Failed: Cannot find State of the interface")
		failed.append("State:%s"%state)
	else:
		op = op.group(1)
		state = state.strip()
		if op != state:
			log.error("Failed: State is not '%s'"%state)
			failed.append("State:%s"%state)
		else:
			log.output("Passed: State of the interface '%s'"%op)
			passed.append("State:%s"%op)

    if priority:
	log.info("Verifying the Priority of the interface")
	op = re.search("\s+Priority\s+(\d+)",intf_op)
	if not op:
                log.error("Failed: Connot find Priority")
		failed.append("Priority:%s"%priority)
	else:
		op = op.group(1)
		priority = priority.strip()
		if int(op) != int(priority):
			log.error("Failed: Priority is not '%s'"%priority)
			failed.append("Priority:%s"%priority)
		else:
			log.output("Passed: Priority is '%s'"%op)
			passed.append("Priority:%s"%op)

    if hello:
	log.info("Verifying the hello interval")
	op = re.search("\s+Hello\s+(\d+)\s+msec",intf_op)
	if not op:
		log.error("Failed: Connot find Hello interval")
		failed.append("Hello:%s"%hello)
	else:
		op = op.group(1)
		op = op.replace('000','')
		hello = hello.strip()
		if int(op) != int(hello):
			log.error("Failed: Hello interval is not %s"%hello)
			failed.append("Hello:%s"%hello)
		else:
			log.output("Passed: Hello interval is %s"%op)
   			passed.append("Hello:%s"%op)

    if dead:
	log.info("Verifying dead interval")
	op = re.search("\s+Hello\s+\d+\s+msec,\s+Dead\s+(\d+)",intf_op)
	if not op:
                log.error("Failed: Connot find Dead interval")
		failed.append("Dead:%s"%dead)
        else:
                op = op.group(1)
		dead = dead.strip()
                if int(op) != int(dead):
			log.error("Failed: Dead interval is not %s"%hello)
			failed.append("Dead:%s"%dead)
                else:
                        log.output("Passed: Dead interval is %s"%op)
			passed.append("Dead:%s"%op)
    if auth_type:
	auth_type = auth_type.strip()
	if auth_type == "md":
		log.info("Verifying the interface authentication type")
		op = re.search("\s+interface\s+has\s+(.*)\s+authentication", intf_op, re.IGNORECASE)
		if not op:
	                log.error("Failed: Cannot find the authentication type")
			failed.append("auth_type:%s"%auth_type)
		else:
			op = op.group(1)
			if op != "message digest":
				log.error("Failed: Authentication is not %s"%auth_type)
				failed.append("auth_type:%s"%auth_type)
			else:
				log.output("Passed: Authentication is %s"%op)
				passed.append("auth_type:%s"%op)
	if auth_type == "simple":
		log.info("Verifying the interface authentication type")
                op = re.search("\s+interface\s+has\s+(.*)\s+authentication", intf_op, re.IGNORECASE)
                if not op:
                        log.error("Failed: Cannot find the authentication type")
                        failed.append("auth_type:%s"%auth_type)
                else:
                        op = op.group(1)
                        if op != "simple password":
                                log.error("Failed: Authentication is not %s"%auth_type)
                                failed.append("auth_type:%s"%auth_type)
                        else:
                                log.output("Passed: Authentication is %s"%op)
                                passed.append("auth_type:%s"%op)

    return passed,failed

def verify_ospf_area(self,auth_type=""):
    failed=[]
    passed=[]
    area_op = self.cmd("show ip ospf")
    log.output("Output of the command:show ip ospf\n%s"%area_op)
    if auth_type:
	log.info("Verifying the area autentication type")
	op = re.search("\s+area\s+has\s+(.*)\s+authentication", area_op, re.IGNORECASE)
	if not op:
		log.error("Failed: Cannot find Area authentication type")
		failed.append("auth_type:%s"%auth_type)
	if auth_type == "md":
		op = op.group(1)
		if op != "message digest":
			log.error("Failed: Area Authentication is not %s"%auth_type)
                        failed.append("auth_type:%s"%auth_type)
		else:
			log.info("Passed: Area Authentication is %s"%op)
			passed.append("auth_type:%s"%op)
	if auth_type=="simple":
		op = op.group(1)
                if op != "simple password":
			log.error("Failed: Area Authentication is not %s"%auth_type)
                        failed.append("auth_type:%s"%auth_type)
                else:
                        log.info("Passed: Area Authentication is %s"%op)
                        passed.append("auth_type:%s"%op)
    return passed,failed


def change_ospf_parameters(self,context="",area="",intf="",hello="",dead="",priority=""):
	if not context:
		self.error("context information is not provided")
                return 1
	if not area:
		self.error("Area information is not provided")
		return 1
	if not intf:
		self.error("Interface information is not provided")
                return 1
	if hello:
		log.info("Configuring the Hello interval")
		self.configcmd("context %s"%context)
		router_op = self.configcmd("router ospf")
		if "router-id" in router_op:
			log.error("OSPF is not running in the given context: %s"%context)
			return 1
		self.configcmd("area %s"%area)
		op = self.configcmd("interface %s"%intf)
		if "ERROR:" in op:
			log.error("Error while configuring the interafce %s with the error %s"%(intf,op))
			self.cmd("end")
			return 1
		self.configcmd("hello-interval %s"%hello)
		#self.configcmd("dead-interval %s"%dead)
		self.cmd("end")
		log.output("Configured Hello interval:%s"%hello)
	if dead:
		log.info("Configuring the Dead interval")
                self.configcmd("context %s"%context)
                router_op = self.configcmd("router ospf")
                if "router-id" in router_op:
                        log.error("OSPF is not running in the given context: %s"%context)
                        return 1
                self.configcmd("area %s"%area)
                op = self.configcmd("interface %s"%intf)
                if "ERROR:" in op:
                        log.error("Error while configuring the interafce %s with the error %s"%(intf,op))
                        self.cmd("end")
                        return 1
                self.configcmd("dead-interval %s"%dead)
                self.cmd("end")
                log.output("Configured Dead interval:%s"%dead)
	if priority:
		log.info("Configuring the priority of the interface")
		self.configcmd("context %s"%context)
                router_op = self.configcmd("router ospf")
                if "router-id" in router_op:
                        log.error("OSPF is not running in the given context: %s"%context)
                        return 1
                self.configcmd("area %s"%area)
                op = self.configcmd("interface %s"%intf)
                if "ERROR:" in op:
                        log.error("Error while configuring the interafce %s with the error %s"%(intf,op))
                        self.cmd("end")
                        return 1
                op = self.configcmd("priority %s"%priority)
		if "ERROR:" in op:
                        log.error("Error while configuring the priority for the interface %s\nerror -->%s"%(intf,op))
			return 1
		self.cmd("end")
                log.output("Configured Priority of the interface: %s"%priority)

	return 0

 
def chk_ospf_lsa(self,context="",lsa_type="",lId="",adv_router="",self_origin="",area="",flag="",nlinks="",linkList="",att_rtr="",net_mask="",met_type="",metric="",fwd_addr="",tag="",stub="",adv_rtr_unreach="",opt="",neg=""):
	''' Command eg: 'show ip ospf database area 0.0.0.0 router 11.11.11.11 adv-router 11.11.11.11' '''
	passed=[]
	failed=[]
	if context:
		self.cmd("context %s"%context)
	cmd_op = "sh ip ospf database "
	if area:
		cmd_op = cmd_op + " area %s "%area
	if self_origin:
		cmd_op = cmd_op + "self-originate "
	if "ext" in lsa_type:
		cmd_op = cmd_op + "external %s "%lId
	if "rout" in lsa_type:
		cmd_op = cmd_op + "router %s "%lId
	if "sum" in lsa_type:
		cmd_op = cmd_op + "summary %s "%lId
	elif adv_router:
		cmd_op = cmd_op + " adv-router %s"%adv_router
	lsa_op = self.cmd(cmd_op)
	if not lsa_op:
		log.error("Parameters given are wrong")	
		return 1
	log.output("output of the command: %s\n%s"%(cmd_op,lsa_op))
	if "ext" in lsa_type:
	 log.info("Verifying the external LSA")
	 if net_mask:
		log.info("Verifying the Network Mask")
		op = re.search("\s+Network\s+Mask:\s+\/(\d+)",lsa_op,re.IGNORECASE)
		if not op:
			log.error("Test Failed: Cannot find Network Mask")
			failed.append("No Network Mask")
		else:
			op = op.group(1)
			if int(op) != int(net_mask):
				log.error("Network Mask is not %s"%net_mask)
				failed.append("Mask:%s"%net_mask)
			else:
				log.output("Test Passed: Network Mask is %s"%op)
				passed.append("Mask:%s"%op)
	 if met_type:
		log.info("Verifying the Metric Type")
		op = re.search("\s+Metric\s+Type:\s+(\d+)",lsa_op,re.IGNORECASE)
		if not op:
			log.error("Test Failed: Cannot find Metric Type")
                        failed.append("Metric Type:%s"%met_type)
		else:
			op = op.group(1)
                        if int(op) != int(met_type):
				log.error("Test Failed: Metric Type is not E%s"%met_type)
				failed.append("Metric Type:%s"%met_type)
			else:	
				log.output("Test Passed:  Metric Type is E%s"%op)
				passed.append("Metric Type:%s"%op)
	 if metric:
		log.info("Verifying the Metric Value")
		op = re.search("\s+Metric:\s+(\d+)",lsa_op,re.IGNORECASE)
                if not op:
                        log.error("Test Failed: Cannot find Metric")
                        failed.append("Metric:%s"%metric)
		else:
			op = op.group(1)
                        if int(op) != int(metric):
				log.error("Test Failed: Metric Val is not %s"%metric)
				failed.append("Metric:%s"%metric)
			else:
                                log.output("Test Passed:  Metric is %s"%op)
                                passed.append("Metric:%s"%op)


	if "rout" in lsa_type:
	 log.info("Verifying the Router LSA")
	 if area and stub:
		log.info("Verifying the Stub area")
		if int(stub) == 0:
			#Not expected the stub area
			op = re.search("\(area\s+%s\s+\[stub\]"%area,lsa_op,re.IGNORECASE)
			if not op:
				log.output("TEST PASSED: Area - %s is not a stub area"%area)
				passed.append("Area:not a stub")
			else:
				log.output("TEST FAILED: Area - %s is a stub area"%area)	
				failed.append("Area:is stub")
		elif int(stub) == 1:
			op = re.search("\(area\s+%s\s+\[stub\]\)"%area,lsa_op,re.IGNORECASE)
			if op:
				log.output("TEST PASSED: Area - %s is a stub area"%area)
                                passed.append("Area:is stub")
			else:
				log.error("TEST FAILED: Area %s is not a stub area"%area)
                                failed.append("Area:not a stub")
				
	 if flag:
		log.info("Verifying the flag")
		op = re.search("flags:\s+(0x[0-9a-f]+)", lsa_op, re.IGNORECASE)
		if not op:
			log.error("Test Failed: Cannot find Flags")
			failed.append("flags:%s"%flag)
		else:
			op = op.group(1)
			flag = flag.strip()
			if op != flag:
				log.error("Test Failed: flag is not %s"%flag)
				failed.append("flags:%s"%flag)
			else:
				log.output("Test Passed: Flag is %s"%op)
				passed.append("flag:%s"%op)
	 if metric:
		log.info("Verifying the metric")
		op = re.search("TOS\s+0\s+metric:\s+([0-9]+)", lsa_op, re.IGNORECASE)
		if not op:
			log.error("Test Failed: Cannot find Flags")
			failed.append("metric:%s"%metric)
		else:
			op = op.group(1)
			metric = metric.strip()
			if int(op) != int(metric):
				log.error("Test Failed: flag is not %s"%flag)
				failed.append("metric:%s"%metric)
			else:
				log.output("Test Passed: Flag is %s"%op)
				passed.append("metric:%s"%op)

	if "sum" in lsa_type:
	 log.info("Verifying the summary LSA")
	 if net_mask:
		log.info("Verifying the Network Mask")
		op = re.search("\s+Network\s+Mask:\s+\/(\d+)",lsa_op,re.IGNORECASE)
                if not op:
                        log.error("Test Failed: Cannot find Network Mask")
                        failed.append("No Network Mask")
                else:
                        op = op.group(1)
                        if int(op) != int(net_mask):
                                log.error("Network Mask is not %s"%net_mask)
                                failed.append("Mask:%s"%net_mask)
                        else:
                                log.output("Test Passed: Network Mask is %s"%op)
                                passed.append("Mask:%s"%op)

         if metric:
                log.info("Verifying the Metric Value")
                op = re.search("\s+Metric:\s+(\d+)",lsa_op,re.IGNORECASE)
                if not op:
                        log.error("Test Failed: Cannot find Metric")
                        failed.append("Metric:%s"%metric)
                else:
                        op = op.group(1)
                        if int(op) != int(metric):
                                log.error("Test Failed: Metric Val is not %s"%metric)
                                failed.append("Metric:%s"%metric)
                        else:
                                log.output("Test Passed:  Metric is %s"%op)
                                passed.append("Metric:%s"%op)


	return passed,failed


def chk_ospf_nbr(self,context="", nbrId="", addr="", pri="", state="", drAddr="", bdrAddr="", intf="", area="", stub=""):
	failed= []
	passed=[]
	if context:
		self.cmd("context %s"%context)
	if not intf:
		log.error("Interface Name is not provided")
		failed.append("Intetrface not provided")
		return passed,failed
	if not nbrId:
		log.error("Neighbor ID is not provided")
                failed.append("No Neighbor ID")
                return passed,failed
	command = "show ip ospf neighbor interface %s %s detail"%(intf, nbrId)
	nbr_op = self.cmd(command)
	log.output("output of the command: %s\n%s"%(command,nbr_op))
	if not nbr_op:
		log.error("Provided wrong infirmation to 'chk_ospf_nbr'")
		failed.append("Wrong Input")
	if addr:
		log.info("Verifying the interface address")
		op = re.search("\s+interface\s+address\s+([0-9.]+)",nbr_op,re.IGNORECASE)
		if not op:
			log.error("Test Failed: Cannot find Interface address")
			failed.append("address:%s"%addr)
		else:
			op = op.group(1)
			addr = addr.strip()
			if op != addr:
				log.error("Test Failed: Interface addr is not %s"%addr)
				failed.append("address:%s"%addr)
			else:
				log.output("Test Passed: Interface address is %s"%op)
				passed.append("Address:%s"%op)
	if pri:
		log.info("Verifying the Priority of the interface")
		op = re.search("\s+Neighbor\s+priority\s+is\s+(\d+)",nbr_op,re.IGNORECASE)
		if not op:
                        log.error("Test Failed: Cannot find priority")
			failed.append("Priority:%s"%pri)
		else:
			op = op.group(1)
			if int(op) != int(pri):
				log.error("Test Failed: priority is not %s"%pri)
				failed.append("Pririty:%s"%pri)
			else:
				log.output("Test Passed: priority is %s"%op)
				passed.append("Pririty:%s"%op)
	if state:
		log.info("Verifying the State")
		op = re.search("\s+state\s+is\s+(\w+)\/",nbr_op,re.IGNORECASE)
		if not op:
			log.error("Test Failed: Cannot find State")
			failed.append("state:%s"%state)
		else:
			op = op.group(1)
			if op.upper() != state.upper():
				log.error("Test Failed: State is not %s"%state)
				failed.append("state:%s"%state)
			else:
                                log.output("Test Passed: State is %s"%op)
				passed.append("state:%s"%op)
	if drAddr:
		log.info("Verifying the DR Adresss")
		op = re.search("\s+DR\s+is\s+([0-9.]+)",nbr_op,re.IGNORECASE)
		if not op:
			log.error("Test Failed: Cannot find DR Address")
			failed.append("DR addr:%s"%drAddr)
		else:
			op = op.group(1)
			drAddr =  drAddr.strip()
			if op != drAddr:
				log.error("Test Failed: DR Address is not %s"%drAddr)
				failed.append("DR addr:%s"%drAddr)
			else:
				log.output("Test Passed: DR Address is %s"%op)
				passed.append("DR addr:%s"%op)
	if bdrAddr:
		log.info("Verifying the BDR Adresss")
		op = re.search("BDR\s+is\s+([0-9.]+)",nbr_op,re.IGNORECASE)
                if not op:
                        log.error("Test Failed: Cannot find BDR Address")
                        failed.append("BDR addr:%s"%bdrAddr)
                else:
                        op = op.group(1)
                        bdrAddr =  bdrAddr.strip()
                        if op != bdrAddr:
                                log.error("Test Failed: DR Address is not %s"%bdrAddr)
                                failed.append("BDR addr:%s"%bdrAddr)
                        else:
                                log.output("Test Passed: DR Address is %s"%op)
                                passed.append("BDR addr:%s"%op)
	return passed,failed

def chk_ip_route_proto(self,context="",route="",admin="",proto="",metric="",tag="",next_hop="",bkUp_hop=""):
	passed=[]
	failed=[]
	if context:
		self.cmd("context %s"%context)
	rt_op = self.cmd("show ip route %s"%route)
	log.output("output of the command: show ip route %s\n%s"%(route,rt_op))
	if not rt_op:
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
	if tag:
		log.info("Verifying the Tag")
		op = re.search("\s+tag\s+(\d+)",rt_op,re.IGNORECASE)
                if not op:
                        log.error("Test Failed: Cannot find Tag")
                        failed.append("Tag:%s"%tag)
		else:
			op = op.group(1)
			if int(op) != int(tag):
				log.error("Test Failed: Tag is not %s"%tag)
				failed.append("Tag:%s"%tag)
			else:
                                log.output("Test Passed: Tag is %s"%op)
                                passed.append("Tag:%s"%op)
	if next_hop:
		log.info("Verifying the Next hop")
		op = re.search("\s+Learned\s+from\s+([0-9.]+)",rt_op,re.IGNORECASE)
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
	if bkUp_hop:
		log.info("Verifying the Backup nexthop")
		op = re.search("\s+Backup\s+nexthop\s+([0-9.]+)",rt_op,re.IGNORECASE)
                if not op:
                        log.error("Test Failed: Cannot find Backup nexthop")
                        failed.append("Nexthop:%s"%next_hop)
                else:
                        op = op.group(1)
			bkUp_hop = bkUp_hop.strip()
                        if op != bkUp_hop:
                                log.error("Test Failed: Backup nexthop is not %s"% bkUp_hop)
                                failed.append("backUphop:%s"%bkUp_hop)
                        else:
                                log.output("Test Passed: Backup nexthop is %s"%op)
                                passed.append("backUphop:%s"%op)

	return passed,failed



def verfiy_rtr_state(myrtr,rtrId):
	"""
	Let me write API First
	"""
	state = myrtr.cmd("show rtr |  grep %s"% rtrId)
	if state == None:
		log.error("No rtr configured")
		return 127
	if state.split()[-1] == "REACHABLE":
		log.info("RTR ID '%s' is reachable" % rtrId)
		return 0
	if state.split()[-1] == "UNREACHABLE":
		log.info("RTR ID '%s' is unreachable" % rtrId)
                return 1
	else:
		log.debug("RTR ID '%s' is not running")
		return 255

def verify_bgp_status(myPeer, contextName, NoOfNeighbors=1):
        """
        Let me write API First
        """
        myPeer.cmd("context %s"% contextName)
        bgpOp = myPeer.cmd("show ip bgp neighbors")
        bgpOp = re.search("\s+Connections\s+established\s+(\d+)",bgpOp)
        if not bgpOp:
                log.error("Test failed: Failed to fing the BGP neighbor")
                return 255
        bgpOp = bgpOp.group(1)
        if int(bgpOp) == int(NoOfNeighbors):
                return 0
        else:
                return 1

