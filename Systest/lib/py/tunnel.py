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
DESCRIPTION             : This Script contains following IPIP  APIs which has
                          been used in the SANITY Testcases
                          
                          This API is being extended to generate the tunnel configuration as well
                          existing CLI tool is located in /systest/util/8ktun/

AUTHOR                  : Original unknown
                          Jeremiah Alfrey - jalfrey@stoke.com
                          code from:
                          Rajshakar rajshakar@stoke.com
                          Venkat Kalidini krao@stoke.com
REVIEWER                :
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

from logging import getLogger
log = getLogger()
#from StokeTest import test_case

# used to get the configuration required to generate the tunnel configuration
from config import *
from topo import * 

# used for: 
# validIP = validate the IP's provided
import issu 

# file creation stuff
import os

## New Code forklifted from /systest/util/8ktun ##
# Jeremiah Alfrey jalfrey@stoke.com


debug = True


def exit_log_dir():
    """
    The Logging functions change the current working directory (CWD) to /Logs
    that means all the files end up in /Logs instead of the script directory.
    This leads to confusion and a mess. Also any files created end up in the
    log directory instead of the script directory. 
    """
    current_dir = os.getcwd()
    
    if debug:
        print 'current working dir is:', current_dir
    
    dir_name = os.path.split(current_dir)
    
    
        
    if 'Logs' in dir_name:
        if debug:
            print 'we are in the log dir!'
        in_log_dir = True
    else:
        if debug:
            print 'we are not in the log dir!'
        in_log_dir = False
        
    if in_log_dir:
        os.chdir('../')
        
    return 0

def generate_tunnel_config_initiator(max_tun, \
                                     context, \
                                     startIp, \
                                     remoteStartIp, \
                                     transportIp, \
                                     nextHop, \
                                     dummyPort, \
                                     bind2Port, \
                                     trafficRt, \
                                     remoteIp, \
                                     slot, \
                                     output_file):
                                     

    """
    This API will take in all values required to generate the tunnel configuration from scratch
    It can generate tunnels for both card 2 and card 3. To make a complete working test bed you 
    will need to run generate_tunnel_config_reponder as well. The values passed must match. 
    Many of the configuration options come from the config.py in your CWD
    
    Variable definition list:
    topo.max_tun_slot3                          = max_tun
    haimc_var['Ini_context_name2']              = context
    haimc_var['dummy_intf_slot3_startIp']       = startIP
    haimc_var['tunnel_intf_slot3_startIp']      = remotStartIp
    haimc_var['ini_cisco_slot3_ip/mask']        = transportIp
    haimc_var['cisco_ini_slot3_ip']             = nextHop
    topo.dummy_ports[1]                         = dummyPort
    haimc_var['port_ini_slot3']                 = bind2Port
    haimc_var['ini_slot3_route_startIp']        = trafficRt
    haimc_var['lpbk_ip1']                       = remoteIp
    slot                                        = slot
    output_filename                             = output_file
    """


    
    """
    max_tun = int(sys.argv[1])
    context = sys.argv[2]
    a, b, c, d = sys.argv[3].split('.')   # This is for Dummy interfaces [4094 vlans]
    w, x, y, z = sys.argv[4].split('.')   # This is for Tunnel interfaces
    transportIp = sys.argv[5]
    nextHop = sys.argv[6]
    dummyPort = sys.argv[7]
    bind2Port = sys.argv[8]
    p, q, r, s = sys.argv[9].split('.')   # This is traffic selector for tunnel.
    remoteIp = sys.argv[10]
    """
    # make sure to write the files in CWD instead of log dir.
    exit_log_dir()

    debug = True
    
    
    # make sure to write the files in CWD instead of log dir.
    exit_log_dir()
    
    
    if debug:
        print 'now in tunnel.py method generate_tunnel'
    
    if debug:
        print 'validating the variables passed to the function:'
    ## Variable Validation Section ##
    if int(max_tun):
        pass

    if int(max_tun) > 4096:
        print 'SSX does not support more then 4096 tunnesl per card!'
        return 'invalid tunnel count. Too high'
    elif int(max_tun) < 1:
        print 'impossible to generate 0 or negative tunnel count'
        return 'invalid tunnel count provided'            
    if not issu.validIP(startIp):
        print 'the value for startIp:', startIp, 'is not a valid IP address'
        return 'invalid IP provided for startIp'
    if not issu.validIP(remoteStartIp):
        print 'the value for remoteStartIp:', remoteStartIp, 'is not a valid IP address'
        return 'invalid IP provided for remoteStartIp' 
    transportIp_parts = transportIp.split('/')
    if not issu.validIP(transportIp_parts[0]):
        print 'the value for transportIp:', transportIp, 'is not a valid IP address'
        return 'invalid IP provided for transportIp'    
    if not issu.validIP(nextHop):
        print 'the value for nextHop:', nextHop, 'is not a valid IP address'
        return 'invalid IP provided for nextHop'    

    dummyPort_parts = dummyPort.split('/')
    if not (dummyPort_parts[0] in ['2', '3', '4']):
        print 'invalid dummy port provided:', dummyPort
        print 'valid ports must be on card 2, 3 or 4'
        return 'invalid dummy port provided'
    elif not (dummyPort_parts[1] in ['0', '1', '2', '3']):
        print 'invalid dummy port provided:', dummyPort
        print 'valid ports must are 0, 1, 2, 3'
        return 'invalid dummy port provided'
        
    bind2Port_parts = bind2Port.split('/')
    if not (bind2Port_parts[0] in ['2', '3', '4']):
        print 'invalid bind2Port port provided:', bind2Port
        print 'valid ports must be on card 2, 3 or 4'
        return 'invalid bind2Port port provided'
    elif not (bind2Port_parts[1] in ['0', '1', '2', '3']):
        print 'invalid bind2Port port provided:', bind2Port
        print 'valid ports must are 0, 1, 2, 3'
        return 'invalid bind2Port port provided'
    
    if not issu.validIP(trafficRt):
        print 'the value for trafficRt:', trafficRt, 'is not a valid IP address'
        return 'invalid IP provided for trafficRt'

    if not issu.validIP(remoteIp):
        print 'the value for remoteIp:', remoteIp, 'is not a valid IP address'
        return 'invalid IP provided for remoteIp'


    if not slot in [2,3]:
        print 'invalid slot provided:', slot, 'must either be 2 or 3'
        return 'invalid slot number provided'
    
    if os.path.exists(output_file):
        print 'the output file:', output_file, 'already exists.'
        print 'File will be overwritten (replaced) if possible.'
    
    if debug:
        print 'completed validating variables'
    
    # open output file for writing
    
    if debug:
        print 'opening the output file:', output_file, 'for writing'
    
    try: 
        out_file = open(output_file, 'w')
    except:
        print 'unable to open the output file:', output_file, 'for writing!'
        return 'unable to write output file'
        
    # This is some legacy code it works find but uses single variable names. 
    # we need to split the three IP Addresses provided into these variables
    # this is used to increment the IP's
    
    a, b, c, d = startIp.split('.')
    p, q, r, s = trafficRt.split('.')
    w, x, y, z = remoteStartIp.split('.')

    # Convert to int for str
    a = int(a) ; b = int(b) ; c = int(c) ; d = int (d)
    p = int(p) ; q = int(q) ; r = int(r) ; s = int (s)
    w = int(w) ; x = int(x) ; y = int(y) ; z = int (z)

    if debug:
        print 'generating configuration for context', context 



    # Let me write common stuffs first
    # this should be part of default.cfg on the SSX
    #out_file.write("system hostname %s"%topo.ssx_ini['hostname']
    out_file.write("ipsec global profile\n")
    out_file.write("dpd interval %s retry-interval %s maximum-retries %s\n"%(haimc_var['dpd_interval'], haimc_var['retry_interval'], haimc_var['dpd_maximum_retries']))
    out_file.write("retransmit interval %s maximum-retries %s send-retransmit-response\n"%(haimc_var['retransmit_interval'], haimc_var['sess_max_retries']))
    out_file.write("exit\n")
    out_file.write("context %s\n"%context)
    out_file.write("interface transport\n")
    out_file.write("arp arpa\n")
    out_file.write("arp refresh\n")
    out_file.write("ip address %s\n"%transportIp)
    out_file.write("exit\n")
    out_file.write("ipsec policy ikev2 phase1 name ikev2_phase1\n")
    out_file.write("suite1\n")
    out_file.write("gw-authentication psk %s\n"%haimc_var['psk_key'])
    out_file.write("peer-authentication psk\n")
    out_file.write("hard-lifetime %s secs\n"%haimc_var['phase1_soft_life'])
    out_file.write("soft-lifetime %s secs\n"%haimc_var['phase1_hard_life'])
    out_file.write("exit\n")
    out_file.write("exit\n")
    out_file.write("ipsec policy ikev2 phase2 name ikev2_phase2\n")
    out_file.write("suite1\n")
    out_file.write("hard-lifetime %s secs\n"%haimc_var['phase2_soft_life'])
    out_file.write("soft-lifetime %s secs\n"%haimc_var['phase2_hard_life'])
    out_file.write("exit\n")
    out_file.write("exit\n")
    out_file.write("initiator-policy INITIATOR_PLAN\n")
    out_file.write("retry-interval 10\n")
    out_file.write("retry-number 30\n")
    out_file.write("hold-off-interval 60\n")
    out_file.write("exit\n")
    out_file.write("ip route %s/32 %s\n"%(remoteIp, nextHop))
    out_file.write("exit\n")
    '''
    4-aug-11:Inserting code to have single tunnel interface for all tunnels
    -Ashu
    '''
    out_file.write("context %s\n"%context)
    out_file.write("interface Ini_tun_global tunnel\n")
    out_file.write("ip address %d.%d.%d.%d/32\n"%(w,x,y,z))
    out_file.write("exit\n")
    out_file.write("exit\n")

    # Logic to generate the tunnel
    d = d + 1
    for i in xrange(max_tun):
        if c == 255:
           b += 1
           c = 1
        if b == 255:
           a += 1
           b = 1
        c += 1

        if not (a == 127):
            out_file.write("context %s\n"%context)
            out_file.write("interface %s \n"%i)
            out_file.write("arp arpa\n")
            out_file.write("arp refresh\n")
            out_file.write("ip address %d.%d.%d.%d/24\n"%(a,b,c,d))
            out_file.write("exit\n")
            out_file.write("exit\n")

        z = z + 1
        if z == 255:
           y += 1
           z = 1
        if y == 255:
           x += 1
           y = 1
       
        if not (w == 127): 
            '''
            4-aug-11: commenting out code for multiple tunnel interface
            Ashu
            '''
            #out_file.write("interface Ini_tun%d tunnel\n"%i)
            #out_file.write("ip address %d.%d.%d.%d/32\n"%(w,x,y,z))
            #out_file.write("exit\n")
            #out_file.write("exit\n")
            
        out_file.write("tunnel %s_tun%d type ipsec protocol ip44 context %s\n"%(context, i, context))
        out_file.write("enable\n")
        out_file.write("tunnel-setup-role initiator-responder initiator-policy INITIATOR_PLAN\n")
        out_file.write("ip local %d.%d.%d.%d remote %s\n"%(a, b, c, d, remoteIp))
        #out_file.write("bind interface Ini_tun%s %s\n"%(i, context))
        out_file.write("bind interface Ini_tun_global %s\n"%context)
        if s == 256:
            r += 1
            s = 0
        if r == 256:
            q += 1
            r = 0
        if q == 256:
            p += 1
            q = 0
        out_file.write("ip route %d.%d.%d.%d/32\n"%(p, q, r, s))
        s += 1
        out_file.write("exit\n")
        out_file.write("ipsec policy ikev2 phase1 name ikev2_phase1\n")
        out_file.write("exit\n")
        out_file.write("ipsec policy ikev2 phase2 name ikev2_phase2\n")
        out_file.write("exit\n")


    # To bind dummy interfaces to port
    out_file.write("port ethernet %s dot1q\n"%bind2Port)
    if slot == 2:
        out_file.write("vlan %s\n"%haimc_var['ini_vlan4slot2'])
    elif slot == 3:
        out_file.write("vlan %s\n"%haimc_var['ini_vlan4slot3'])
    else:
        print 'invalid slot provided:', slot
    out_file.write("bind interface transport %s\n"%context)
    out_file.write("exit\n")
    out_file.write("service ipsec\n")
    out_file.write("exit\n")
    out_file.write("enable\n")
    out_file.write("exit\n")
    out_file.write("port ethernet %s dot1q\n"%dummyPort)
    out_file.write("enable\n")

    for i in xrange(max_tun):
        out_file.write("vlan %s\n"%i)
        out_file.write("bind interface %s %s\n"%(i, context))
        out_file.write("exit\n")
        out_file.write("service ipsec\n")
        out_file.write("exit\n")	




def generate_tunnel_config_responder(max_tun, context, startIp, localIp, routeOption, trafficRt, remoteStartIp, slot, output_file):
    """
    This API will take in all values required to generate the tunnel configuration from scratch
    It can generate tunnels for both card 2 and card 3. To make a complete working test bed you 
    will need to run generate_tunnel_config_initiator as well. The values passed must match. 
    Many of the configuration options come from the config.py in your CWD
    
    Variable definition list:
    max_tun = Maximum tunnels to generate per this context (total tunnels)
    context = Context name to put the tunnels under
    startIp = 
    localIp = Loopback IP to send the traffic to (tunnel endpoint)
    routeOption = 
    trafficRt =
    remoteStartIp = 
    slot = This should be a number like 2 or 3
    output_file = filename to write config into
    """
    debug = True
    

    # make sure to write the files in CWD instead of log dir.
    exit_log_dir()

    
    if debug:
        print 'now in tunnel.py method generate_tunnel'
    
    if debug:
        print 'validating the variables passed to the function:'
    ## Variable Validation Section ##
    if not issu.validIP(startIp):
        print 'the value for startIp:', startIp, 'is not a valid IP address'
        return 'invalid IP provided for startIp'    
    if not issu.validIP(localIp):
        print 'the value for localIp:', localIp, 'is not a valid IP address'
        return 'invalid IP provided for localIp'
    if not issu.validIP(trafficRt):
        print 'the value for trafficRt:', trafficRt, 'is not a valid IP address'
        return 'invalid IP provided for trafficRt'
    if not issu.validIP(remoteStartIp):
        print 'the value for remoteStartIp:', remoteStartIp, 'is not a valid IP address'
        return 'invalid IP provided for remoteStartIp'
    if not slot in [2,3]:
        print 'invalid slot provided:', slot, 'must either be 2 or 3'
        return 'invalid slot number provided'
    try:
        max_tun = int(max_tun)
    except:
        print 'maximun tunnels needs to be an integer!'
        sys.exit(1)
    
    if os.path.exists(output_file):
        print 'the output file:', output_file, 'already exists.'
        print 'File will be overwritten (replaced) if possible.'
    
    if debug:
        print 'completed validating variables'
    
    # open output file for writing
    
    if debug:
        print 'opening the output file:', output_file, 'for writing'
    
    try: 
        out_file = open(output_file, 'w')
    except:
        print 'unable to open the output file:', output_file, 'for writing!'
        return 'unable to write output file'
        
    # This is some legacy code it works find but uses single variable names. 
    # we need to split the three IP Addresses provided into these variables
    # this is used to increment the IP's
    
    a, b, c, d = startIp.split('.')
    p, q, r, s = trafficRt.split('.')
    w, x, y, z = remoteStartIp.split('.')

    # Convert to int for str
    a = int(a) ; b = int(b) ; c = int(c) ; d = int (d)
    p = int(p) ; q = int(q) ; r = int(r) ; s = int (s)
    w = int(w) ; x = int(x) ; y = int(y) ; z = int (z)

    if debug:
        print 'generating configuration for context', context 

    # Configuration starts
    # this should be found in the defaul.cfg already loaded on the SSX
    #out_file.write("system hostname %s\n"%topo.ssx_resp['hostname'])
    out_file.write("ipsec global profile\n")
    out_file.write("dpd interval %s retry-interval %s maximum-retries %s\n"%(haimc_var['dpd_interval'], haimc_var['retry_interval'], haimc_var['dpd_maximum_retries']))
    out_file.write("retransmit interval %s maximum-retries %s send-retransmit-response\n"%(haimc_var['retransmit_interval'], haimc_var['sess_max_retries']))
    out_file.write("exit\n")
    out_file.write("context %s\n"% context)
    out_file.write("interface transport\n")
    out_file.write("arp arpa\n")
    out_file.write("arp refresh\n")
    if slot == 2:
        out_file.write("ip address %s\n"%haimc_var['active_slot2_ip/mask'])
    elif slot == 3:
        out_file.write("ip address %s\n"%haimc_var['active_slot3_ip/mask'])
    else:
        print 'invalid slot provided:', slot
        sys.exit(1)        
    out_file.write("exit\n")
    out_file.write("interface transback\n")
    out_file.write("arp arpa\n")
    out_file.write("arp refresh\n")
    if slot == 2:
        out_file.write("ip address %s\n"%haimc_var['standby_4slot2_ip/mask'])
    elif slot == 3:
        out_file.write("ip address %s\n"%haimc_var['standby_4slot3_ip/mask'])
    else:
        print 'invalid slot provided:', slot        
        sys.exit(1)  
    out_file.write("exit\n")
    out_file.write("interface service\n")
    out_file.write("arp arpa\n")
    out_file.write("arp refresh\n")
    if slot == 2:
        out_file.write("ip address %s\n"%haimc_var['rad_intf_4slot2_ip/mask'])
    elif slot == 3:
        out_file.write("ip address %s\n"%haimc_var['rad_intf_4slot3_ip/mask'])
    else:
        print 'invalid slot provided:', slot      
        sys.exit(1)  
    out_file.write("exit\n")
    out_file.write("interface serback\n")
    out_file.write("arp arpa\n")
    out_file.write("arp refresh\n")
    if slot == 2:
        out_file.write("ip address %s\n"%haimc_var['bkp_rad_intf_4slot2_ip/mask'])
    elif slot == 3:
        out_file.write("ip address %s\n"%haimc_var['bkp_rad_intf_4slot3_ip/mask'])
    else:
        print 'invalid slot provided:', slot      
        sys.exit(1)  
    out_file.write("exit\n")
    out_file.write("interface lpbk-1 loopback\n")
    out_file.write("ip address %s/32\n"%localIp)
    out_file.write("exit\n")
    out_file.write("ipsec policy ikev2 phase1 name ikev2_phase1\n")
    out_file.write("suite1\n")
    out_file.write("gw-authentication psk %s\n"%haimc_var['psk_key'])
    out_file.write("peer-authentication psk\n")
    out_file.write("hard-lifetime %s secs\n"%haimc_var['phase1_soft_life'])
    out_file.write("soft-lifetime %s secs\n"%haimc_var['phase1_hard_life'])
    out_file.write("exit\n")
    out_file.write("exit\n")
    out_file.write("ipsec policy ikev2 phase2 name ikev2_phase2\n")
    out_file.write("suite1\n")
    out_file.write("hard-lifetime %s secs\n"%haimc_var['phase2_soft_life'])
    out_file.write("soft-lifetime %s secs\n"%haimc_var['phase2_hard_life'])
    out_file.write("exit\n")
    out_file.write("exit\n")
    if slot == 2:
        out_file.write("rtr %s\n"%haimc_var['rtr_id1'])
    elif slot == 3:
        out_file.write("rtr %s\n"%haimc_var['rtr_id2'])
    else:
        print 'invalid slot provided:', slot       
        sys.exit(1)  
    if slot == 2:
        out_file.write("type echo protocol ipicmpecho %s source %s\n"%(haimc_var['cisco_active_slot2_ip'],haimc_var['active_slot2_ip']))
    elif slot == 3:
        out_file.write("type echo protocol ipicmpecho %s source %s\n"%(haimc_var['cisco_active_slot3_ip'],haimc_var['active_slot3_ip']))
    else:
        print 'invalid slot provided:', slot       
        sys.exit(1)  
    out_file.write("exit\n")
    if slot == 2:
        out_file.write("rtr schedule %s\n"%haimc_var['rtr_id1'])
    elif slot == 3:
        out_file.write("rtr schedule %s\n"%haimc_var['rtr_id2'])
    else:
        print 'invalid slot provided:', slot       
        sys.exit(1)  

    # Since this section is optional
    # the variables should also be optional in the config itself. 
    if routeOption == 'y':
        if slot == 2:
            out_file.write("ip route %s %s track %s\n"%(haimc_var['routes_to_ini_ip_slot2'], haimc_var['cisco_active_slot2_ip'],haimc_var['rtr_id1']) )
            out_file.write("ip route %s %s admin-distance 20\n"%(haimc_var['routes_to_ini_ip_slot2'], haimc_var['cisco_standby_4slot2_ip']))
            out_file.write("ip route %s %s\n"%(haimc_var['cisco_ssx_slot3_ses_traffic_route'], haimc_var['cisco_rad_intf_4slot2_ip']))
            out_file.write("ip route %s %s admin-distance 20\n"%(haimc_var['cisco_ssx_slot3_ses_traffic_route'], haimc_var['cisco_bkp_rad_intf_4slot2_ip']))
            out_file.write("ip route %s %s track %s\n"%(haimc_var['dummy_intf_routes_slot2'], haimc_var['cisco_active_slot2_ip'],haimc_var['rtr_id1']))
            out_file.write("ip route %s %s admin-distance 20\n"%(haimc_var['dummy_intf_routes_slot2'], haimc_var['cisco_standby_4slot2_ip']))
        elif slot == 3:
            out_file.write("ip route %s %s track %s\n"%(haimc_var['routes_to_ini_ip_slot3'], haimc_var['cisco_active_slot3_ip'],haimc_var['rtr_id1']) )
            out_file.write("ip route %s %s admin-distance 20\n"%(haimc_var['routes_to_ini_ip_slot3'], haimc_var['cisco_standby_4slot3_ip']))
            out_file.write("ip route %s %s\n"%(haimc_var['cisco_ssx_slot3_ses_traffic_route'], haimc_var['cisco_rad_intf_4slot3_ip']))
            out_file.write("ip route %s %s admin-distance 20\n"%(haimc_var['cisco_ssx_slot3_ses_traffic_route'], haimc_var['cisco_bkp_rad_intf_4slot3_ip']))
            out_file.write("ip route %s %s track %s\n"%(haimc_var['dummy_intf_routes_slot3'], haimc_var['cisco_active_slot3_ip'],haimc_var['rtr_id1']))
            out_file.write("ip route %s %s admin-distance 20\n"%(haimc_var['dummy_intf_routes_slot3'], haimc_var['cisco_standby_4slot3_ip']))
        else:
            print 'invalid slot provided:', slot       
            sys.exit(1) 

    #print "ip route %s/32 %s"%(remoteIp, nextHop)
    out_file.write("exit\n")

    # Session home config
    if slot == 2:
        out_file.write("session-home slot 100 loopback interface lpbk-1 %s\n"% context )
        out_file.write("ipsec session context name %s\n"% context )
    elif slot == 3:
        out_file.write("session-home slot 101 loopback interface lpbk-1 %s\n"% context )
        out_file.write("ipsec session context name %s\n"% context )
    else:
        print 'invalid slot provided:', slot       
        sys.exit(1) 
    
    out_file.write("ipsec policy ikev2 phase1 name ikev2_phase1\n")
    out_file.write("ipsec policy ikev2 phase2 name ikev2_phase2\n")
    out_file.write("exit\n")
    '''
    4-aug-11:Inserting code to have single tunnel interface for all tunnels
    -Ashu
    '''

    out_file.write("context %s\n"% context )
    out_file.write("interface resp_tun_global tunnel\n")
    out_file.write("ip address %d.%d.%d.%d/32\n"%(a,b,c,d))
    out_file.write("exit\n")
    out_file.write("exit\n")

    d = d + 1
    z = z + 1
    for i in xrange(max_tun):
        if c == 255:
           b += 1
           c = 1
        if b == 255:
           a += 1
           b = 1
        c += 1

        if not (a == 127):
            '''
            4-aug-11: commenting out code for multiple tunnel interface
            Ashu
            '''

            #print "context %s"%haimc_var['context1']
            #print "interface resp_tun%d tunnel"%i
            #print "ip address %d.%d.%d.%d/32"%(a,b,c,d)
            #print "exit"
            #print "exit"

            out_file.write("tunnel %s_tun%d type ipsec protocol ip44 context %s\n"%( context , i, haimc_var['context1']))
            out_file.write("enable\n")
            #print "tunnel-setup-role initiator-responder"
            if y == 255:
                x += 1
                y = 1
            if x == 255:
                w += 1
                x = 1
            y += 1

        out_file.write("ip local %s remote %d.%d.%d.%d\n"%(localIp, w, x, y, z))
        #print "bind interface resp_tun%s %s"%(i, haimc_var['context1'])

        out_file.write("bind interface resp_tun_global %s\n"% context )

    
        if s == 256:
            r += 1
            s = 0
        if r == 256:
            q += 1
            r = 0
        if q == 256:
            p += 1
            q = 0
        out_file.write("ip route %d.%d.%d.%d/32\n"%(p, q, r, s))
        s += 1
        out_file.write("exit\n")
        out_file.write("ipsec policy ikev2 phase1 name ikev2_phase1\n")
        out_file.write("exit\n")
        out_file.write("ipsec policy ikev2 phase2 name ikev2_phase2\n")
        out_file.write("exit\n")


    # To bind transport and service interfaces
    if slot == 2:
        out_file.write("port ethernet %s dot1q\n"%haimc_var['port_ssx_active_4slot2'])
        out_file.write("vlan %s \n"%haimc_var['vlan4slot2'])
    elif slot == 3:
        out_file.write("port ethernet %s dot1q\n"%haimc_var['port_ssx_active_4slot3'])
        out_file.write("vlan % \ns"%haimc_var['vlan4slot3'])
    else:
        print 'invalid slot provided:', slot       
        sys.exit(1)
    out_file.write("bind interface transport %s\n"% context )
    out_file.write("exit\n")
    out_file.write("service ipsec\n")
    out_file.write("exit\n")
    out_file.write("enable\n")
    out_file.write("exit\n")
    # If radius is not configured/required we skip creating the interfaces for it
    if haimc_var.has_key('port_ssx_rad_intf_4slot2') or haimc_var.has_key('port_ssx_rad_intf_4slot3'):
        if slot == 2:
            out_file.write("port ethernet %s dot1q\n"%haimc_var['port_ssx_rad_intf_4slot2'])
            out_file.write("vlan %s\n"%haimc_var['service_vlan4slot2'])
        elif slot == 3:
            out_file.write("port ethernet %s dot1q\n"%haimc_var['port_ssx_rad_intf_4slot3'])
            out_file.write("vlan %s\n"%haimc_var['service_vlan4slot3'])
        else:
            print 'invalid slot provided:', slot       
            sys.exit(1) 
        out_file.write("bind interface service %s\n"% context )
        out_file.write("exit\n")
        out_file.write("exit\n")
        out_file.write("enable\n")
        out_file.write("exit\n")
    if slot == 2:
        out_file.write("port ethernet %s dot1q\n"%haimc_var['port_ssx_standby_4slot2'])
        out_file.write("vlan %s\n"%haimc_var['standby_vlan4slot2'])
    elif slot == 3:
        out_file.write("port ethernet %s dot1q\n"%haimc_var['port_ssx_standby_4slot3'])
        out_file.write("vlan %s\n"%haimc_var['standby_vlan4slot3'])
    else:
        print 'invalid slot provided:', slot       
        sys.exit(1) 
    out_file.write("bind interface transback %s\n"% context )
    out_file.write("exit\n")
    out_file.write("service ipsec\n")
    out_file.write("exit\n")
    out_file.write("enable\n")
    out_file.write("exit\n")
    # If radius is not configured/required we skip creating the interfaces for it
    if haimc_var.has_key('port_ssx_bkp_rad_intf_4slot2') or haimc_var.has_key('port_ssx_bkp_rad_intf_4slot3'):
        if slot == 2:
            out_file.write("port ethernet %s dot1q\n"%haimc_var['port_ssx_bkp_rad_intf_4slot2'])
            out_file.write("vlan %s\n"%haimc_var['serback_vlan4slot2'])
        elif slot == 3:
            out_file.write("port ethernet %s dot1q\n"%haimc_var['port_ssx_bkp_rad_intf_4slot3'])
            out_file.write("vlan %s\n"%haimc_var['serback_vlan4slot3'])
        else:
            print 'invalid slot provided:', slot       
            sys.exit(1)
        out_file.write("bind interface serback %s\n"% context )
        out_file.write("exit\n")
        out_file.write("exit\n")
        out_file.write("enable\n")
        out_file.write("exit\n")
    
    
    # Close the file now it's full of the config
    if debug:
        print 'closing output file:', output_file
    out_file.close()


def join_files(first_file, second_file, destination_file):
    """
    This method takes the two files and concatenates them together to form 
    the destination file. 
    """
    
    exit_log_dir()

    if debug:
        print 'in tunnel.py join_files'
    

            
    if os.path.exists(first_file):
        if debug:
            print 'located file:', first_file
        if os.path.exists(second_file):
            if debug:
                print 'located second file:', second_file
                print 'cating the first file into the destination file'
            os.popen("cat %s > %s " % (first_file, destination_file))
            if debug:
                print 'cating the second file into the destination file'
            os.popen("cat %s >> %s " % (second_file, destination_file))
            if debug:
                print 'your final file is named:', destination_file
        else:
            print 'unable to locate file:', second_file
            sys.exit(1)
    return 0




## Old code that was alreay here ##
# Code is in uknown state. Dunno if it works


def  verify_tunnel_counters_with_name(self,tun_name) :
           """ Verify tunnel counters for each tunnel with tunnel name
               returns 0 - if Inpkts and outPkts both are non-zero.
	       returns 1 - if Inpkts and outPkts both are zero.
               returns 2 - if either of Inpkts or outPkts is zero.
               returns 3 - if tunnel does not exist
           """
           output = self.cmd(" show tunnel counters | grep -v \"---\" | grep -v \"UTC\" ")
           tunn_counters = re.compile("""^(?P<name>\S+)
                                           \s+
                                           (?P<CircHdl>\S+)\s+
                                           (?P<InPkts>\S+)\s+
                                           (?P<outPkts>\S+)
                                           """, re.VERBOSE)
           rt_val = {}
           in_ctrs = {}
           out_ctrs = {}
           tmp = {}
           failCount = 0
           for line in output.splitlines():
               m = tunn_counters.match(line)
               if m:
                   tmp[m.groupdict()['name']] = m.groupdict()
               if tmp:
                   rt_val = tmp
           print rt_val
           if tun_name in    rt_val:
               in_ctrs  = int(rt_val[tun_name]['InPkts'])
               out_ctrs  = int(rt_val[tun_name]['outPkts'])
               if ((in_ctrs == 0) and (out_ctrs == 0)):
                   failCount = 1
               elif ((out_ctrs == 0) or (in_ctrs == 0)):
                   failCount = 2
           else :
                failCount = 3


           return failCount

def tunnel_change(self,tun_name,context_name,role) :
     output = self.cmd("configuration")
     output = self.cmd("tunnel %s type ipsec protocol ip44 context %s"%(tun_name,context_name))
     output = self.cmd("enable")
     if role == "Resp" :
         output = self.cmd("no tunnel-setup-role")
     else :
         output = self.cmd("tunnel-setup-role initiator-responder")
     self.cmd("end")
     return output
   
     output = self.cmd("end")


def change_rt_mask(self,context_name,tun_name,local_tun_ip,remote_tun_ip,from_rt,to_rt,intf_name,gw,from_mask,to_mask,role="Resp"):

     output = self.cmd("end")
     output = self.cmd("configuration")
     output = self.cmd("context %s"%context_name)
     output = self.cmd("no ip route %s %s %s"%(to_rt,to_mask,gw))
     output = self.cmd("exit")
     output = self.cmd("tunnel %s type ipsec protocol ip44 context %s"%(tun_name,context_name))
     
     output = self.cmd("enable")
     if role == "Resp" :
         output = self.cmd("no tunnel-setup-role")
     else :
         output = self.cmd("tunnel-setup-role initiator-responder")
     output = self.cmd("ip local %s remote %s"%(local_tun_ip,remote_tun_ip))
     output = self.cmd("bind interface %s %s"%(intf_name,context_name))
     output = self.cmd("no ip route %s %s"%(from_rt,from_mask))
     output = self.cmd("ip route %s %s"%(to_rt,to_mask))
     output = self.cmd("exit")
     output = self.cmd("exit")
     output = self.cmd("context %s"%context_name)
 
     output = self.cmd("ip route %s %s %s"%(from_rt,from_mask,gw))
     output = self.cmd("end")




def change_rt_tunnel(self,context_name,tun_name,local_tun_ip,remote_tun_ip,from_rt,to_rt,intf_name,gw,from_mask,to_mask,role="Resp"):

     output = self.cmd("end")
     output = self.cmd("configuration")
     output = self.cmd("tunnel %s type ipsec protocol ip44 context %s"%(tun_name,context_name))
     output = self.cmd("enable")
     if role == "Resp" :
         output = self.cmd("no tunnel-setup-role")
     else :
         output = self.cmd("tunnel-setup-role initiator-responder")
     output = self.cmd("ip local %s remote %s"%(local_tun_ip,remote_tun_ip))
     output = self.cmd("bind interface %s %s"%(intf_name,context_name))
     output = self.cmd("no ip route %s %s"%(from_rt,from_mask))
     output = self.cmd("ip route %s %s"%(to_rt,to_mask))
     output = self.cmd("end")
 


def change_rt_route(self,context_name,from_rt,to_rt,gw,from_mask,to_mask):

     output = self.cmd("end")
     output = self.cmd("configuration")
     output = self.cmd("context %s"%context_name)
     output = self.cmd("no ip route %s %s %s"%(to_rt,to_mask,gw))
     output = self.cmd("ip route %s %s %s"%(from_rt,from_mask,gw))
     output = self.cmd("end")




def change_rt_tunnel(self,context_name,tun_name,local_tun_ip,remote_tun_ip,from_rt,to_rt,intf_name,gw,from_mask,to_mask,role="Resp"):

     output = self.cmd("end")
     output = self.cmd("configuration")
     output = self.cmd("tunnel %s type ipsec protocol ip44 context %s"%(tun_name,context_name))
     output = self.cmd("enable")
     if role == "Resp" :
         output = self.cmd("no tunnel-setup-role")
     else :
         output = self.cmd("tunnel-setup-role initiator-responder")
     output = self.cmd("ip local %s remote %s"%(local_tun_ip,remote_tun_ip))
     output = self.cmd("bind interface %s %s"%(intf_name,context_name))
     output = self.cmd("no ip route %s %s"%(from_rt,from_mask))
     output = self.cmd("ip route %s %s"%(to_rt,to_mask))
     output = self.cmd("end")

def get_tunnel_details(self,name = "",handle = ""):

    """
    Description:- This API displays  the output of "show tunnel name tun_01" and
                   "show tunnel handle 012345" commands.
    Input:- It takes tunnel name or tunnel handle.It is better to give either of one
              because both commands will display the same output.
    Output:- It returns the output in the form of dictionary.
    Author:- Rajshekar, rajshekar@stoke.com.
    Reviewer: - Modified by Jameer to get the port and next hop details as well and handles were returning properly
    """

    if name :
       cmd = "show tunnel name %s"% name
    elif handle :
       cmd = "show tunnel handle %s"% name

    output = self.cmd(cmd)


    if "ERROR" in output :
        return False

    regexp_list = [ '\s*Name\s*(?P<tun_name>\w+)' ,
                    '\s*Tunnel\s*Circuit\s*Handle\s*(?P<tun_ckt_handle>\w+)',
                    '\s*Session\s*Handle\s*(?P<ses_handle>\w+)',
                    '\s*Admin\s*Status\s*(?P<admin_status>\w+)',
                    '\s*FSM\s*State\s*(?P<FSM_state>\w+)',
                    '\s*Transport\s*(?P<transport_context>\w+)',
                    '\s*Local\s*Transport\s*Endpoint\s*(?P<localTransEndPoint>\S*)',
                    '\s*Remote\s*Transport\s*Endpoint\s*(?P<remoteTransEndPoint>\S*)',
                    '\s*Role\s*(?P<Role>\w+)',
                    '\s*Routed\s+via\s+(?P<nexthop>[0-9.]+)',
                    '\s*Routed\s+via.*(?P<port>\(\s*Slot\s+\d+,\s+Port\s+\d+)',
                    '\s*Routed\s+via.*\s+Protocol\s+(?P<routing_protocol>\w+)',
                    '\s*Tunnel\s*creation\s*mode\s*(?P<tunCreationMode>\w+)',
                    '\s*Last\s*reset\s*reason\s*(?P<lastResetReason>\S*)']

    actual = {}
    for regexp in regexp_list :
        obj = re.compile(regexp,re.I)
        mat = obj.search(output)
        if mat :
           dict = mat.groupdict()
           for key in dict.keys() :
               if key == "port":
                   dict[key] = re.search('\s*Slot\s+(\d+),\s+Port\s+(\d+)',dict[key])
                   dict[key] = dict[key].group(1)+"/"+dict[key].group(2)
               actual[key] = dict[key]
    return actual


def verify_tunnel_details(self,tun_name = "None" , tun_ckt_handle = "None" , ses_handle = "None",
                  admin_status = "None", FSM_state = "None", transport_context = "None",
                  port = "None", routing_protocol = "None",nexthop = "None",
                  localTransEndPoint = "None", remoteTransEndPoint = "None",
                  Role  = "None", tunCreationMode  = "None", lastResetReason = "None",
                  name = "",handle = ""):

    """
    Description:- This API verifies the output of "show tunnel name tun_01" and
                   "show tunnel handle 012345" commands.
    Input:- It takes the different parameters related to tunnel i.e tunnel handle session
             handle......
    Output:- It returns either Pass or Fail.
    Author:- Rajshekar, rajshekar@stoke.com.
    Reviewer: Modified by Jameer to handle the modfied params as mentioned in get_verify_tunnel_details() API
    """

    if name :
       actual = get_tunnel_details(self,name = name)
       if not actual:
            return 0
    if handle :
       actual = get_tunnel_details(self,handle = handle)
       if not actual:
            return 0

    expected = {'tun_name':tun_name,'tun_ckt_handle':tun_ckt_handle,'ses_handle':ses_handle,
    'admin_status':admin_status,'FSM_state':FSM_state,'transport_context':transport_context,
    'port':port,'routing_protocol':routing_protocol,"nexthop":nexthop,
    'localTransEndPoint':localTransEndPoint,'remoteTransEndPoint':remoteTransEndPoint,'Role':Role,
    'tunCreationMode':tunCreationMode,'lastResetReason':lastResetReason }
    log.debug(expected)
    log.debug(actual)

    for keys in expected.keys():
        if expected[keys] != 'None':
            obj = re.compile("[Ii]nitiator")
            obj1 = re.compile("[Rr]esponder")
            m = obj.search(expected[keys])
            m1 = obj1.search(expected[keys])
            if m:
                n = obj.search(actual[keys])
                print n
                if not n:
                    return 0
            elif m1:
                n = obj1.search(actual[keys])
                print n
                if not n:
                    return 0
            elif expected[keys] != actual[keys]:
              return 0
    return 1
