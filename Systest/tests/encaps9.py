#!/usr/bin/env python2.5

import sys, os, getopt
mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


import enum
from SSX import SSX 		#Venkat
#import SSX
from NS import NS		#Venkat
#from NS import NS2
from Linux import Linux		#Venkat
from StokeTest import test_case, test_suite, test_runner
from  helpers import *
import reslock
import signal
import traceback
import misc
import re
import time

# logging stuff.  remove debug for less verbosity in logging.
# this will be a commandline option later.
from log import buildLogger
from logging import getLogger
from misc import pretty_print
from topo import *
from config import *
#import encaps.cfg,ns1.cfg.v44, ns1.cfg.v46, ns2.cfg.v44, ns2.cfg.v44.secondary, ns2.cfg.v46.secondary, ns2.cfg.v46, ns_clear.cfg  

saveCfgSsx = False
#log = buildLogger("encaps.log", debug=True)
#log = buildLogger("encaps.log",debug=True,console=True)

class encaps(test_case):
 global log
 log=getLogger()
 def setUp(self):
     """ """

 def tearDown(self):
     """ """
 def pretty_print(toponum, test):
     """Log the details of the test, depending the verbosity level."""
     [cctsvc1, mod1, encap1, cctsvc2, mod2, encap2, portcfg] = test
     log.cmd("Topo %d %s" % (toponum, str(test)))

# #need to clean up and make some nice prettyprinting here
     log.debug("\n\nTopo %d --------------------------" % toponum)
     log.debug("Circuit 1")
     log.debug("Port services defined: %s" % ",".join(cctsvc1))
     for svc in cctsvc1:
         print svc,
     log.debug("Circuit encap modifier: %s" % mod1)
     log.debug("Encapsulation: %s" % encap1)
     log.debug("Connected via: %s" % portcfg)
     log.debug("Circuit 2")
     log.debug("Port services defined: %s" % ",".join(cctsvc2))
     for svc in cctsvc2:
         print svc,
     log.debug("Circuit encap modifier: %s" % mod2)
     log.debug("Encapsulation: %s" % encap2)
    
 def OnIntr(signum, stackframe):
    log.warning("Got signal %s" % str(signum))
    unlock_resources()
    sys.exit(1)
    child.interact()
    
 locks = {}
#we need 1 ssx, 2 netscreens and 2 linux boxes for this test suite

 def lock_resources():
    global locks
    locks = {"ssx" : ["qa-tmp3"], "netscreen" : ["qa-ns2", "qa-ns1"], "linux": ["tahiti","ebini"]}
   
 def unlock_resources():
    reslock.remove_locks()
    pass

 ssx = linux1 = linux2 = ns1 = ns2 = None
 ssx_name = linux1 = linux2 = ns1_name = ns2_name = None
 def test_main(self):
#def main(self):			#Venkat
    #log.exception("exception")
    global ssx, linux1, linux2, ns1, ns2
    global ssx_name, linux1, linux2, ns1_name, ns2_name, linux1_name, linux2_name, cfgPath
    
    #cedar 
    #encaps =['v4', 'v6', 'ipsec v44', 'ipsec v46', 'pppoe', ]
    #modifiers = ['raw', 'dot1q', 'dot1q untagged']
    #portservice = [['none'], ['service ipsec'], ['service dot1q'], ['service ipsec', 'service dot1q']]
    #portcfgs = ['same port', 'same card', 'different card']

    #pre-cedar encap/forwarding set
    encaps =['v4', 'v6', 'ipsec v44', 'ipsec v46', 'pppoe','ipip']
    #encaps =['v6']    
    modifiers = ['raw', 'dot1q', 'dot1q untagged']
    cctservices = [['none'], ['service ipsec'], ['service pppoe']]
    portcfgs = ['same vlan', 'same port', 'same card', 'different card', ]
    cfgPath = "/volume/labtools/systest/tests/encaps"

    log.info("Generating test matrix...")
    test_list = enum.gen_tests(cctservices, modifiers, encaps, cctservices, modifiers, encaps, portcfgs)




    #Printing All combinations of encaps script

    #enum.pretty_print_list(test_list)


#    sys.exit(0)
#get our boxes
#    lock_resources()

    # alter the top level naming scheme for test output files.  having date and time makes
    # it easier to locate the last test run quickly.
    logdir = ""
    for i in time.localtime()[:-5]:
        logdir += str(i)
    #logdir = str(os.getpid())

    setup_logdir = "%s/setup" % logdir
    if not os.path.isdir(setup_logdir):
        os.makedirs(setup_logdir)
#get console on ssx
#     ssx_name =  locks["ssx"][0]


    ssx_name = ssx['name']
    #ssx = SSX(ssx['name'])		#Venkat
    ssx = SSX(ssx['name']+"-mc-con")		#Venkat
    ssx.telnet()		#Venkat
    saveCfgSsx = False
    #ssx = SSX(ssx_name + "-mc-con")
    #ssx = SSX.SSXConsole(ssx_name + "-mc-con")
    ssx.ses.logfile=open("%s/ssx.log" % setup_logdir,"w+")
    
#get connections to linux boxes
#     linux1 = locks["linux"][0]
#     linux2 = locks["linux"][1]
    #linux1 = "tahiti"
    #linux2 = "ebini"
    #linux1_name = host1['name']
    linux1_name = "tahiti"
    log.info("linux1 :%s" % linux1_name)
    #linux2_name = host2['name']
    linux2_name = "ebini"
    linux1 =  Linux(host1['name'])		#Venkat
    linux1.telnet()		#Venkat
    #linux1 = Linux.LinuxTelnet(linux1)
    linux2 =  Linux(host2['name'])		#Venkat
    linux2.telnet()		#Venkat
    #linux2 = Linux.LinuxTelnet(linux2)
    linux1.ses.logfile=open("%s/linux1.log" % setup_logdir,"w+")
    linux2.ses.logfile=open("%s/linux2.log" % setup_logdir,"w+")    

#get consoles on netscreens
#     ns1_name = locks["netscreen"][0]
#     ns2_name = locks["netscreen"][1]
    ns1_name = "qa-ns1"
    ns2_name = "qa-ns2"
    
    #ns1 = NS.NSConsole(ns1_name + "-con")
    ns1 = NS(ns1_name + "-con")         	#Venkat
    #ns1 = NS2(ns1_name + "-con")
    #ns2 = NS.NSConsole(ns2_name + "-con")
    ns2 = NS(ns2_name + "-con")			#Venkat
    #ns2 = NS2(ns2_name + "-con")
    ns1.telnet()
    ns2.telnet()

 #   ns1.ses.logfile=open("%s/ns1.log" % setup_logdir,"w+")
 #   ns2.ses.logfile=open("%s/ns2.log" % setup_logdir,"w+")    

 
    #configure the context on the ssx:
    ssx.cmd("clear conf")
    cache_cfg_file = "testtemp.cfg"
    #ssx.cfg_from_file("encaps.cfg")
    #log.debug("saveCfgSsx:%s" % saveCfgSsx)a
    saveCfgSsx = 0 #temp
    if saveCfgSsx:
       ssx.cmd("load configuration %s"  % cache_cfg_file)
    else:
       ssx.config_from_string(script_var['encaps_cfg'])		#Venkat
       #ssx.config_from_file("%s/encaps.cfg')		#Venkat
       #ssx._get_to_exec()
       ssx.cmd("save conf %s" % cache_cfg_file)
       saveCfgSsx = True

    # these are examples of how to run test cases individually.
#    test_list = [test_list[11], test_list[13], test_list[14], test_list[17],test_list[18],test_list[19],test_list[20]]


    #test_indices = range(0, len(test_list))


    #test = int(sys.argv[1])
    test_indices = range(800,900)
    sameport_ipip = [820,868,895]
    for test in sameport_ipip:
	test_indices.remove(test)
    #test_indices = range(0,1034)
    #sameport_ipip = [3,75,272,281,292,363,403,424,480,557,780,820,868,895,920,935,983,992,1002,1017,1029,1033]
    #for test in sameport_ipip:
	#test_indices.remove(test)
	


    #if sys.argv[1] == "sanity":	
    #test_indices = [0,2,7,10,18,28,35,48,67,83,97,101,105,106,112,117,126,132,136,139,142,144,150,162,163,167,172,180,185,189,215,221,228,287,298,302,305,316,321,331,387,390,392,394,415,455,463,470,473,526,1000]





    #Rigged up to run a test case one extra time if it fails
    done = False
    retry = False
    index = 0
    someFailed = False
    numFailed = 0
    topoFailed = []
    
    while not done:
        i = test_indices[index]
        if not retry:
            this_logdir = "%s/test%d" % (logdir, i)
        else:
            this_logdir = "%s/test%d-2" % (logdir, i)

        if not os.path.isdir(this_logdir):
            os.makedirs(this_logdir)

        ssx.ses.logfile=open("%s/ssx.log" % this_logdir,"w+")
        linux1.ses.logfile=open("%s/linux1.log" % this_logdir,"w+")
        linux2.ses.logfile=open("%s/linux2.log" % this_logdir,"w+")
        #ns1.ses.logfile=open("%s/ns1.log" % this_logdir,"w+")
        #ns2.ses.logfile=open("%s/ns2.log" % this_logdir,"w+")
        

        pretty_print(i,test_list[i])

        #clean up our configs/binds/etc
#        ssx.clear_config()
#        ssx.cmd("conf load %s" % cache_cfg_file)

        
        try:
            self.dotest(test_list[i])
        except misc.TestFailure, val:
            if retry == True:
                log.result("Topo:%d **FAILED AGAIN: %s" % (i,val))
		topoFailed.append(i)
                retry = False
                someFailed = True
                numFailed += 1
            else:
                log.result(" Failed, trying again: %s\n\n" % val)
                retry = True
        else:
            log.result("Topo:%d  Passed\n\n" % i)
            retry = False
        if not retry:
            index += 1
        if index == len(test_indices):
            done = True
        hs = ssx.get_health_stats()
        health=is_healthy(hs,Warn_logs=100, Err_logs=0)
        self.failUnless(health)
	#if not health:
#		log.debug("Platform is not healthy")
#		sys.exit(1)
    self.failUnless(not numFailed,"Failed tests are %s" % topoFailed)
    if not someFailed:
        log.result("All tests passed")
        return True
    else:
        log.result("Some tests failed: %d failures" % numFailed)
        return False
    
#unlock shit at the end
#     unlock_resources()

#encapsulate the circuit layerings in a class?
#useful for comparing the layering, to determine
#if/when cct configs are related (same port, same vlan)
 '''
 class CCT:
    def __init__(self):
        self.dot1q = False
        self.ipsec = False
        self.v44 = False
        self.v46 = False
        self.pppoe = False
        self.ipip = False
        self.port = None
        self.vlan = None
        self.vlan_untagged = False
        self.bind = ""
        self.service_ipsec = False
        self.service_pppoe = False        
    def __str__(self):
        retstr = "port eth %s" % self.port
        if self.dot1q:
            retstr += " dot1q"
        retstr += "\n"
        retstr += "enable\n"
        if self.dot1q:
            if self.vlan_untagged:
                retstr += "vlan 0 untagged\n"
            else:
                retstr += "vlan %d\n" % self.vlan
        if self.service_ipsec:
            retstr += "service ipsec\n"
        if self.service_pppoe:
            retstr += "service pppoe\n"
        if self.v44:
            retstr += self.binding
            retstr += "ipsec policy ikev1 phase1 name p11\n"
            retstr += "ipsec policy ikev1 phase2 name p21\n"
        elif self.v46:
            retstr += self.binding
            retstr += "ipsec policy ikev1 phase1 name p11\n"
            retstr += "ipsec policy ikev1 phase2 name p21\n"
        else: #base ip case
            retstr += self.binding
        retstr += "end\nconf\n"	#Venkat
        #retstr += "exit\nexit\nexit\n"	#Venkat
        #retstr += "end\n"
        return retstr
    
    #determines base cct equality
    def __eq__(self, other):
        if self.port == other.port:
            if self.vlan == other.vlan:
                if self.vlan_untagged == other.vlan_untagged:
                    return True
        return False

 '''
 def dotest(self,test):
 #def dotest(test):
    global ssx, linux1, linux2, ns1, ns2
    global ssx_name, linux1, linux2, ns1_name, ns2_name



    #needed for special case of same cct for both sides
    do_ns2_secondary = False
    
    #here we need to think about addressing.. all static context config would be easiest

    # 1.1.1.2 <-> 1.1.1.1  2.2.2.1 <-> 2.2.2.2       v4 simple transit cases 
    # 3.3.3.2 <-> 3.3.3.1  4.4.4.1 <-> 4.4.4.2       v4 session cases
    # 10.1.1.2 <-> 10.1.1.1 11.1.1.1 <-> 11.1.1.2    v4 tunnel layer


    # 1000::2 <-> 1000::1 2000::1 <-> 2000::2                    v6 simple transit cases 

    
    cctservice1, modifiers1, encaps1, cctservice2, modifiers2, encaps2, portcfg = test


    #fix these up to consult vgroup_old database for ssx specific vlans
    vlanA = 1501
    vlanB = 1502

    cct1 = CCT()
    cct2 = CCT()

    #same port.. use 3/0
    #same card.. use 3/0 and 3/1
    #different card.. use 3/0 and 4/0
    if portcfg == "same vlan":
        cct1.port = "2/0"
        #cct1.port = "3/0"	#Salvador
        cct2.port = "2/0"
        #cct2.port = "3/0"	#Salvador
        vlan1 = vlanA
        vlan2 = vlanA
    elif portcfg == "same port":
        cct1.port = "2/0"
        #cct1.port = "3/0"
        cct2.port = "2/0"
        #cct2.port = "3/0"
        vlan1 = vlanA
        vlan2 = vlanB
    elif portcfg == "same card":
        cct1.port = "2/0"
        #cct1.port = "3/0"
        cct2.port = "2/1"
        #cct2.port = "3/1"
        vlan1 = vlanA
        vlan2 = vlanB
    elif portcfg == "different card":
        cct1.port = "2/0"
        #cct1.port = "3/0"
        cct2.port = "4/0"
        vlan1 = vlanA
        vlan2 = vlanB

    if re.match("dot1q$", modifiers1):
        cct1.vlan = vlan1
        cct1.dot1q = True
    if re.match("dot1q$", modifiers2):
        cct2.vlan = vlan2
        cct2.dot1q = True        
    if re.search("untagged", modifiers1):
        cct1.vlan_untagged = True
        cct1.dot1q = True
    if re.search("untagged", modifiers2):
        cct2.vlan_untagged = True
        cct2.dot1q = True        

    if "service ipsec" in cctservice1:
        cct1.service_ipsec = True

    if "service ipsec" in cctservice2:
        cct2.service_ipsec = True

    if "service pppoe" in cctservice1:
        cct1.service_pppoe = True

    if "service pppoe" in cctservice2:
        cct2.service_pppoe = True

#    print "cct1: ", cct1.port, cct1.vlan
#    print "cct2: ", cct2.port, cct2.vlan    

    #ints to define
    #v4_transit_1
    #v4_transit_2
    #v4_session_1
    #v4_session_2
    #v6_transit_1
    #v6_transit_2
    #v4_tunnel_1
    #v4_tunnel_2
    #v6_tunnel_1
    #v6_tunnel_2
    ssx.clear_health_stats() 
    linux1.cmd("sudo pkill pppd")
    linux2.cmd("sudo pkill pppd")
    linux2.cmd("sudo /sbin/ip tunnel del to_ssx", timeout = 10)
    linux1.cmd("sudo /sbin/ip tunnel del to_ssx", timeout = 10)


    #delete ports
    ssx.cmd("end")
    ssx.configcmd("no port eth 2/0")
    #ssx.configcmd("no port eth 3/0")		#Slavador
    ssx.configcmd("no port eth 2/1")
    #ssx.configcmd("no port eth 3/1")		#Slavador
    ssx.configcmd("no port eth 4/0")
    ssx.cmd("context test")
    ssx.cmd("clear sess all") #fucking stupid ntt requirement forces me to do this
    
#    ssx.cfg("no port eth %s" % cct1.port)
#    if cct1.port != cct2.port:
#        ssx.cfg("no port eth %s" % cct2.port)    

    #cct1
    if encaps1 == "ipsec v44":
        cct1.v44 = True
        cct1.binding = "bind int v4_transit_1 test\n"
        cct1.ipsec = True
        linux1_addr = "10.1.1.2/24"
        linux1_nhop = "10.1.1.1"
        linux1_phy_net = "10.1.1.0/24"
        linux1_visible_net = "3.3.3.0/24"
        linux1_visible_addr = "3.3.3.2"        
    elif encaps1 == "ipsec v46":
        cct1.v46 = True
        cct1.binding = "bind int v6_transit_1 test\n"
        cct1.ipsec = True
        linux1_addr = "10.1.1.2/24"
        linux1_nhop = "10.1.1.1"
        linux1_visible_net = "3.3.3.0/24"        
        linux1_visible_addr = "3.3.3.2"        
    #need to add code for pppoe case
    elif encaps1 == "pppoe":
        cct1.pppoe = True
        cct1.binding = "" #no binding needed for pppoe cct
        linux1_addr = "3.3.3.2" #linux1 intf addr is actually negotiated
        linux1_nhop = "3.3.3.1"
        linux1_visible_net = "3.3.3.0/24"        
        linux1_visible_addr = "3.3.3.2"        

    #handle raw ethernet binding case
    elif encaps1 == "v4":
        cct1.binding = "bind int v4_transit_1 test\n"
        linux1_addr = "1.1.1.2/24"
        linux1_nhop = "1.1.1.1"
        linux1_visible_net = "1.1.1.0/24"
        linux1_visible_addr = "1.1.1.2"
    elif encaps1 == "v6":
        cct1.binding = "bind int v6_transit_1 test\n"
        linux1_addr = "1000::2/64"
        linux1_nhop = "1000::1"
        linux1_visible_net = "1000::0/64"
        linux1_visible_addr = "1000::2"

    elif encaps1 == "ipip":
        cct1.ipip = True
        #if not cct1 == cct2:
        cct1.binding = "bind interface ipip_int test\n"
        linux1_addr = "55.55.55.0/24"
        linux1_nhop = "5.5.5.1"
        linux1_visible_net = "5.5.5.0/24"
        linux1_visible_addr = "5.5.5.2"

    #cct2
    if encaps2 == "ipsec v44":
        cct2.v44 = True
        cct2.ipsec = True
        linux2_addr = "20.1.1.2/24"
        linux2_nhop = "20.1.1.1"
        linux2_address = "20.1.1.2"
        linux2_phy_net = "20.1.1.0/24"
        linux2_visible_net = "4.4.4.0/24"
        linux2_visible_addr = "4.4.4.2"
        if not cct1 == cct2:
            cct2.binding = "bind int v4_transit_2 test\n"
        else:
            cct2.binding = cct1.binding #already bound to a port, clone to add ipsec policies
            do_ns2_secondary = True
    elif encaps2 == "ipsec v46":
        cct2.v46 = True
        cct2.ipsec = True
        linux2_addr = "20.1.1.2/24"
        linux2_nhop = "20.1.1.1"
        linux2_address = "20.1.1.2"
        linux2_visible_net = "4.4.4.0/24"
        linux2_visible_addr = "4.4.4.2"
        if not cct1 == cct2:
            cct2.binding = "bind int v6_transit_2 test\n"
        else:
            cct2.binding =  "bind int v6_transit_1 test\n" #need some ipv6
            do_ns2_secondary = True
    elif encaps2 == "pppoe":
        cct2.pppoe = True
        cct2.binding = "" #no binding needed for pppoe cct
        linux2_addr = "4.4.4.2" #linux1 intf addr is actually negotiated
        linux2_nhop = "4.4.4.1"
        linux2_visible_net = "4.4.4.0/24"
        linux2_visible_addr = "4.4.4.2"
    #handle raw ethernet binding case
    elif encaps2 == "v4":
        if not cct1 == cct2:
            cct2.binding = "bind int v4_transit_2 test\n"
            linux2_addr = "2.2.2.2/24"
            linux2_nhop = "2.2.2.1"
            linux2_visible_net = "2.2.2.0/24"
            linux2_visible_addr = "2.2.2.2"
        else:
            cct2.binding = "" #cct already bound to int
            linux2_addr = "1.1.2.3/24"
            linux2_nhop = "1.1.2.1"
            linux2_visible_net = "1.1.2.0/24"
            linux2_visible_addr = "1.1.2.3"

    elif encaps2 == "v6":
        if not cct1 == cct2:
            cct2.binding = "bind int v6_transit_2 test\n"
            linux2_addr = "2000::2/64"
            linux2_nhop = "2000::1"
            linux2_visible_net = "2000::0/64"
            linux2_visible_addr = "2000::2"
        else:
            cct2.binding = "" #cct already bound to an int
            linux2_addr = "1000:1::3/64"
            linux2_nhop = "1000:1::1"
            linux2_visible_net = "1000:1::0/64"
            linux2_visible_addr = "1000:1::3"

    elif encaps2 == "ipip":
	    cct2.ipip = True
        #if not cct1 == cct2:
            cct2.binding = "bind interface ipip_int2 test\n"
            linux2_addr = "66.66.66.0/24"
            linux2_nhop = "6.6.6.1"
            linux2_visible_net = "6.6.6.0/24"
            linux2_visible_addr = "6.6.6.2"
        #else:
            #cct2.binding = "bind interface ipip_int test\n"
            #linux2_addr = "55.55.55.0/24"
            #linux2_nhop = "55.55.55.1"
            #linux2_visible_net = "5.5.5.0/24"
            #linux2_visible_addr = "5.5.5.1"
        #    linux2_addr = "1000:1::3/64"
        #    linux2_nhop = "1000:1::1"
        #    linux2_visible_net = "1000:1::0/64"
        #    linux2_visible_addr = "1000:1::3"


    #config the ssx
    ssx.config_from_string(str(cct1))
    ssx.config_from_string(str(cct2))
    

    #set up the vlan connections
    #can have ssx->netscreen->linux
    #or ssx->linux
    #for each cct
    if portcfg == "same vlan":
        if not cct1.vlan_untagged:
            if cct1.ipsec and cct2.ipsec:
                vlan_cfg_str="""
                             vlan=%d
                             ssx_name:%s tagged
                             ns1_name:e0
                             ns2_name:0
                             """ % (cct1.vlan, self.vg_port_name(cct1.port))
                misc.vgroup_old(vlan_cfg_str,globals())
            elif cct1.ipsec and not cct2.ipsec:
                vlan_cfg_str="""
                             vlan=%d
                             ssx_name:%s tagged
                             ns1_name:e0
                             linux2_name:e2
                             """ % (cct1.vlan, self.vg_port_name(cct1.port))
                misc.vgroup_old(vlan_cfg_str,globals())
            elif not cct1.ipsec and cct2.ipsec:
                vlan_cfg_str="""
                             vlan=%d
                             ssx_name:%s tagged
                             ns2_name:0
                             linux1_name:%s
                             """ % (cct1.vlan, self.vg_port_name(cct1.port),host1['port'])
                misc.vgroup_old(vlan_cfg_str,globals())
            else: #no ipsec anywhere, same vlan
                vlan_cfg_str="""
                             vlan=%d
                             ssx_name:%s tagged
                             linux1_name:%s
                             linux2_name:%s
                             """ % (cct1.vlan, self.vg_port_name(cct1.port),host1['port'],host2['port'])
                misc.vgroup_old(vlan_cfg_str,globals())
        else: #case of 'same vlan', but artificial "vlan untagged" case
            if cct1.ipsec and cct2.ipsec:
                vlan_cfg_str="""
                             ssx_name:%s
                             ns1_name:e0
                             ns2_name:0
                             """ % self.vg_port_name(cct1.port)
                misc.vgroup_old(vlan_cfg_str,globals())
            elif cct1.ipsec and not cct2.ipsec:
                vlan_cfg_str="""
                             ssx_name:%s
                             ns1_name:e0
                             linux2_name:%s
                             """ % (self.vg_port_name(cct1.port),host1['port'])
                misc.vgroup_old(vlan_cfg_str,globals())
            elif not cct1.ipsec and cct2.ipsec:
                vlan_cfg_str="""
                             ssx_name:%s
                             ns2_name:0
                             linux1_name:%s
                             """ % (self.vg_port_name(cct1.port),host1['port'])
                misc.vgroup_old(vlan_cfg_str,globals())
            else: #no ipsec anywhere, same vlan untagged
                vlan_cfg_str="""
                             ssx_name:%s
                             linux1_name:%s
                             linux2_name:%s
                             """ % (self.vg_port_name(cct1.port),host1['port'],host2['port'])
                misc.vgroup_old(vlan_cfg_str,globals())
            
    elif cct1 == cct2:
        #handle same broadcast domains first
        #this would be cases of both on same eth cct or both untagged
        if cct1.vlan_untagged and cct2.vlan_untagged:
            if cct1.ipsec and cct2.ipsec:
                vlan_cfg_str="""
                             ssx_name:%s
                             ns1_name:e0
                             ns2_name:0
                             """ % self.vg_port_name(cct1.port)
                misc.vgroup_old(vlan_cfg_str,globals())
            elif cct1.ipsec and not cct2.ipsec:
                vlan_cfg_str="""
                             ssx_name:%s
                             ns1_name:e0
                             linux2_name:%s
                             """ % (self.vg_port_name(cct1.port),host1['port'])
                misc.vgroup_old(vlan_cfg_str,globals())
            elif not cct1.ipsec and cct2.ipsec:
                vlan_cfg_str="""
                             ssx_name:%s
                             ns2_name:0
                             linux1_name:%s
                             """ % (self.vg_port_name(cct1.port),host1['port'])
                misc.vgroup_old(vlan_cfg_str,globals())
            else: #raw untagged case both ccts
                vlan_cfg_str="""
                             ssx_name:%s
                             linux1_name:%s
                             linux2_name:%s
                             """ % (self.vg_port_name(cct1.port),host1['port'],host2['port'])
                misc.vgroup_old(vlan_cfg_str,globals())
        elif (encaps1 == encaps2 == "v4") or (encaps1 == encaps2 == "v6") or (encaps1 == 'pppoe' and encaps2 == 'v4') or (encaps1 == 'v4' and encaps2 == 'pppoe') or (encaps1 == "pppoe" and encaps2 == "pppoe"):
            vlan_cfg_str="""
                         ssx_name:%s
                         linux1_name:%s
                         linux2_name:%s
                         """ % (self.vg_port_name(cct1.port),host1['port'],host2['port'])
            misc.vgroup_old(vlan_cfg_str,globals())
        elif cct1.ipsec and cct2.ipsec:
            vlan_cfg_str="""
                         ssx_name:%s
                         ns1_name:e0
                         ns2_name:0
                         """ % self.vg_port_name(cct1.port)
            misc.vgroup_old(vlan_cfg_str,globals())
        elif cct1.ipsec and not cct2.ipsec:
            vlan_cfg_str="""
                         ssx_name:%s
                         ns1_name:e0
                         linux2_name:%s
                         """ % (self.vg_port_name(cct1.port),host1['port'])
            misc.vgroup_old(vlan_cfg_str,globals())
        elif not cct1.ipsec and cct2.ipsec:
            vlan_cfg_str="""
                         ssx_name:%s
                         ns2_name:0
                         linux1_name:%s
                         """ % (self.vg_port_name(cct1.port),host1['port'])
            misc.vgroup_old(vlan_cfg_str,globals())

            
    else: #all other cases
        if cct1.ipsec:
            if cct1.vlan:
                #connect ssx cct1 port to ns1-untrust with vlan
                vlan_cfg_str="""
                    vlan=%d
                    ssx_name:%s tagged
                    ns1_name:e0
                    """ % (cct1.vlan, self.vg_port_name(cct1.port))
                misc.vgroup_old(vlan_cfg_str,globals())
            else:
                #connect ssx cct1 port to ns1-untrust 
                vlan_cfg_str="""
                    ssx_name:%s
                    ns1_name:e0
                    """ % self.vg_port_name(cct1.port)
                misc.vgroup_old(vlan_cfg_str,globals())
        else:
            if cct1.vlan:
                #connect ssx cct1 port to linux1_name with vlan
                vlan_cfg_str="""
                    vlan=%d
                    ssx_name:%s tagged
                    linux1_name:%s
                    """ % (cct1.vlan, self.vg_port_name(cct1.port),host1['port'])
                misc.vgroup_old(vlan_cfg_str,globals())
            else:
                #connect ssx cct1 port to linux1_name
                vlan_cfg_str="""
                    ssx_name:%s
                    linux1_name:%s
                    """ % (self.vg_port_name(cct1.port),host1['port'])
                misc.vgroup_old(vlan_cfg_str,globals())


        #same thing for cct2
        if cct2.ipsec:
            if cct2.vlan:
                #connect ssx cct2 port to ns2-untrust with vlan
                vlan_cfg_str="""
                    vlan=%d
                    ssx_name:%s tagged
                    ns2_name:0
                    """ % (cct2.vlan, self.vg_port_name(cct2.port))
                misc.vgroup_old(vlan_cfg_str,globals())
            else:
                #connect ssx cct2 port to ns2-untrust 
                vlan_cfg_str="""
                    ssx_name:%s
                    ns2_name:0
                    """ % self.vg_port_name(cct2.port)
                misc.vgroup_old(vlan_cfg_str,globals())
        else:
            if cct2.vlan:
                #connect ssx cct2 port to linux2 with vlan
                vlan_cfg_str="""
                    vlan=%d
                    ssx_name:%s tagged
                    linux2_name:%s
                    """ % (cct2.vlan, self.vg_port_name(cct2.port),host2['port'])
                misc.vgroup_old(vlan_cfg_str,globals())
            else:
                #connect ssx cct2 port to linux2
                vlan_cfg_str="""
                    ssx_name:%s
                    linux2_name:%s
                    """ % (self.vg_port_name(cct2.port),host2['port'])
                misc.vgroup_old(vlan_cfg_str,globals())

    #now handle linux--netscreen connections
    #(factored out of above as always the same)
    if cct1.ipsec:
        #connect ns1-trust linux1_name
        vlan_cfg_str="""
                     linux1_name:%s
                     ns1_name:e1
                     """ % host2['port']
        misc.vgroup_old(vlan_cfg_str,globals())
    if cct2.ipsec:
        #connect ns2-trust linux2
        vlan_cfg_str="""
                     linux2_name:%s
                     ns2_name:1
                     """ % host2['port']
        misc.vgroup_old(vlan_cfg_str,globals())
    

    #configure netscreens, if need be 
    if cct1.v44:
        ns1.config_from_string(script_var['ns_clear_cfg'])
        #ns1.load_config("%s/ns_clear.cfg')
        ns1.config_from_string(script_var['ns1_cfg_v44'])
    elif cct1.v46:
        ns1.config_from_string(script_var['ns_clear_cfg'])
        ns1.config_from_string(script_var['ns1_cfg_v46'])

    if cct2.v44:
        ns2.config_from_string(script_var['ns_clear_cfg'])
        if do_ns2_secondary:
            ns2.config_from_string(script_var['ns2_cfg_v44_secondary'])
        else:
            ns2.config_from_string(script_var['ns2_cfg_v44'])        
    elif cct2.v46:

        ns2.config_from_string(script_var['ns_clear_cfg'])
        if do_ns2_secondary:
            ns2.config_from_string(script_var['ns2_cfg_v46_secondary'])
        else:
            ns2.config_from_string(script_var['ns2_cfg_v46'])


    #linux1 setup
    if cct1.pppoe:
        #blow away possible routes from last test etc
        linux1.cmd("sudo /sbin/ip addr flush dev eth2", timeout = 20)
        #blow away possible previous /usr/sbin/pppd
        linux1.cmd("sudo pkill pppd")
        time.sleep(2) #wait for possible old pppoe to die
        #linux1.cmd("sudo pppoe-connect eth2 user1")
        linux1.cmd("sudo /usr/sbin/pppd pty 'pppoe -I eth2' user user1 noaccomp noccp unit 0")
        time.sleep(5) #wait for pppoe to come up
	unit=re.search("ppp(\d+)",linux1.cmd("sudo /sbin/ifconfig | grep ppp"))
	ppp_int= "ppp" + unit.group(1)
        linux1.add_route(linux2_visible_net, linux1_nhop, ppp_int)
        #linux1.add_route(linux1_phy_net, linux1_nhop, ppp_int)

    elif cct1.ipip:
        #blow away possible routes from last test etc
        linux1.cmd("sudo /sbin/ip addr flush dev eth2", timeout = 20)
        linux1.cmd("sudo /sbin/ip tunnel del to_ssx", timeout = 10)
	linux1.cmd("sudo /sbin/ifconfig eth2 55.55.55.2 netmask 255.255.255.0")
        linux1.cmd("sudo /sbin/ip tunnel add to_ssx mode ipip remote 55.55.55.1 local 55.55.55.2")
	linux1.cmd("sudo /sbin/ifconfig to_ssx 5.5.5.2 netmask 255.255.255.0")
	linux1.cmd("sudo /sbin/ip route add 5.5.5.0/24 via 55.55.55.1 dev to_ssx onlink")
	linux1.cmd("sudo /sbin/ip route add 4.4.4.0/24 via 5.5.5.1 dev to_ssx onlink")
	linux1.cmd("sudo /sbin/ip route add 2.2.2.0/24 via 5.5.5.1 dev to_ssx onlink")
	linux1.cmd("sudo /sbin/ip route add 6.6.6.0/24 via 5.5.5.1 dev to_ssx onlink")
        #linux1.add_route(linux2_visible_net, linux1_nhop, "to_ssx onlink")	#Venkat

    else:
        linux1.configure_ip_interface("eth2", linux1_addr)	#Venkat
        #linux1.configure_ip_interface(linux1_addr, "eth2")
        #linux1.add_route(linux2_addr, linux1_nhop, "eth2")
        linux1.add_route(linux2_visible_net, linux1_nhop, "eth2")	#Venkat
        #linux1.add_route(linux1_phy_net, linux1_nhop, "eth2")	#Venkat
    
    #linux2 setup
    if cct2.pppoe:
        #blow away possible routes from last test etc
        linux2.cmd("sudo /sbin/ip addr flush dev eth2", timeout = 20)
        #linux2.configure_ip_interface("eth2", linux2_addr)
        #blow away possible previous /usr/sbin/pppd
        #linux2.cmd("sudo pppoe-stop")
        linux2.cmd("sudo pkill pppd")
        #linux2.cmd("sudo kill `cat /var/run/ppp0.pid`")
        #linux2.cmd("/bin/rm -f /var/run/ppp0.pid")        
        time.sleep(2) #wait for possible old pppoe to die
        #linux2.cmd("sudo pppoe-connect eth2 user2")
        linux2.cmd("sudo /usr/sbin/pppd pty 'pppoe -I eth2' user user2 noaccomp noccp unit 0")
        time.sleep(5) #wait for pppoe to come up
	unit=re.search("ppp(\d+)",linux2.cmd("sudo /sbin/ifconfig | grep ppp"))
	ppp_int= "ppp" + unit.group(1)
        linux2.add_route(linux1_visible_net, linux2_nhop, ppp_int)
        #linux2.add_route(linux2_phy_net, linux2_nhop, ppp_int)
        #linux2.add_route(linux2_phy_net, linux2_nhop, "eth2")    

    elif cct2.ipip:
        #blow away possible routes from last test etc
        linux2.cmd("sudo /sbin/ip addr flush dev eth2", timeout = 20)
        linux2.cmd("sudo /sbin/ip tunnel del to_ssx", timeout = 10)
	linux2.cmd("sudo /sbin/ifconfig eth2 66.66.66.2 netmask 255.255.255.0")
        linux2.cmd("sudo /sbin/ip tunnel add to_ssx mode ipip remote 66.66.66.1 local 66.66.66.2")
	linux2.cmd("sudo /sbin/ifconfig to_ssx 6.6.6.2 netmask 255.255.255.0")
	linux2.cmd("sudo /sbin/ip route add 6.6.6.0/24 via 66.66.66.1 dev to_ssx onlink")
	linux2.cmd("sudo /sbin/ip route add 1.1.1.0/24 via 6.6.6.1 dev to_ssx onlink")
	linux2.cmd("sudo /sbin/ip route add 3.3.3.0/24 via 6.6.6.1 dev to_ssx onlink")
	linux2.cmd("sudo /sbin/ip route add 5.5.5.0/24 via 6.6.6.1 dev to_ssx onlink")
        #linux2.add_route(linux1_visible_net, linux2_nhop, "to_ssx onlink")    

    else:
        linux2.configure_ip_interface("eth2", linux2_addr)
        linux2.add_route(linux1_visible_net, linux2_nhop, "eth2")    

 

    #dump out some test datas
    log.info("cct1 port: %s cct1 vlan: %s cct1 untagged: %s" %
                (cct1.port, cct1.vlan, cct1.vlan_untagged))
    log.info("cct2 port: %s cct2 vlan: %s cct2 untagged: %s" %
                (cct2.port, str(cct2.vlan), cct2.vlan_untagged))
    
    #RUN TESTS

    if cct1.pppoe or cct2.pppoe:
        endsize = 1492  #TEMP TEMP TEMP until fast path pppoe frag
    else:
        #endsize = 1600
        endsize = 45


    #for v6 case, need v6 pingwalk..
    if encaps1 == "v6":
        #ping6 to ssx to handle ssx-linux1 nd
        #ping6 to end host to handle ssx-linux2 nd
	time.sleep(5)
        linux1.cmd("ping6 -c 2 %s -w 2" % linux1_nhop)
        linux1.cmd("ping6 -c 2 %s -w 2" % linux2_visible_addr)
        linux2.cmd("ping6 -c 2 %s -w 2" % linux2_nhop)            
        linux2.cmd("ping6 -c 2 %s -w 2" % linux1_visible_addr)    
        #do v6 pingwalk to linux2
        retval = linux1.pingwalk6_fast(linux2_visible_addr, "eth2", endsize=endsize, deadline=1, count=10)      #Venkat
        if not retval:
            misc.testfailure("Pingwalk from linux1 to linux2 failed")
    else:
	time.sleep(5)
        linux1.cmd("ping -c 2 %s -w 2" % linux1_nhop)
        linux2.cmd("ping -c 2 %s -w 2" % linux1_nhop)    
        linux1.cmd("ping -c 2 %s -w 2" % linux2_visible_addr)
        linux2.cmd("ping -c 2 %s -w 2" % linux1_visible_addr)    
        linux1.cmd("ping -c 2 %s -w 2" % linux2_visible_addr)
        linux2.cmd("ping -c 2 %s -w 2" % linux1_visible_addr)    

        if cct1.pppoe:
            retval = linux1.pingwalk_fast(linux2_visible_addr, "ppp0", endsize=endsize, deadline=1, count=10)
            if not retval:
                misc.testfailure("Pingwalk from linux1 to linux2 failed")
	elif cct1.ipip:
             retval = linux1.pingwalk_fast(linux2_visible_addr, "to_ssx", endsize=endsize, deadline=1, count=10)
             if not retval:
                misc.testfailure("Pingwalk from linux1 to linux2 failed")

        else:
            #now do pingwalks to linux2
            retval = linux1.pingwalk_fast(linux2_visible_addr, "eth2", endsize=endsize, deadline=1, count=10)           #Venkat
            if not retval:
                misc.testfailure("Pingwalk from linux1 to linux2 failed")
	
    mtuOutput=ssx.cmd("sh ip host")
    log.debug("show ip host Output:%s\n\n" % mtuOutput)
    ssx.cmd("context test")
    sesCounters=ssx.cmd("show sess cou")
    if (encaps1 == "ipip" or encaps2 == "ipip"):
       tunCounters=ssx.cmd("show tun cou")
       if not tunCounters:
               log.info("*" * 50)
               log.info("No Tunnels exists in SSX")
               log.info("*" * 50)
            #   sys.exit(1)
       else:
               log.info("*" * 50)
               log.info("Tunnel counters in SSX : %s\n\n" % tunCounters)
               log.info("*" * 50)

    if not sesCounters:
               log.info("*" * 50)
               log.info("No sessions exists in SSX")
               log.info("*" * 50)
            #   sys.exit(1)
    else:
               log.info("*" * 50)
               log.info("Session counters in SSX : %s\n\n" % sesCounters)
               log.info("*" * 50)



 def vg_port_name(self,portname):
    return re.sub("/", ":", portname)
class CCT:
    def __init__(self):
        self.dot1q = False
        self.ipsec = False
        self.v44 = False
        self.v46 = False
        self.pppoe = False
        self.ipip = False
        self.port = None
        self.vlan = None
        self.vlan_untagged = False
        self.bind = ""
        self.service_ipsec = False
        self.service_pppoe = False
    def __str__(self):
        retstr = "port eth %s" % self.port
        if self.dot1q:
            retstr += " dot1q"
        retstr += "\n"
        retstr += "enable\n"
        if self.dot1q:
            if self.vlan_untagged:
                retstr += "vlan 0 untagged\n"
            else:
                retstr += "vlan %d\n" % self.vlan
        if self.service_ipsec:
            retstr += "service ipsec\n"
        if self.service_pppoe:
            retstr += "service pppoe\n"
        if self.v44:
            retstr += self.binding
            retstr += "ipsec policy ikev1 phase1 name p11\n"
            retstr += "ipsec policy ikev1 phase2 name p21\n"
        elif self.v46:
            retstr += self.binding
            retstr += "ipsec policy ikev1 phase1 name p11\n"
            retstr += "ipsec policy ikev1 phase2 name p21\n"
        else: #base ip case
            retstr += self.binding
        retstr += "end\nconf\n" #Venkat
        #retstr += "exit\nexit\nexit\n" #Venkat
        #retstr += "end\n"
        return retstr

    #determines base cct equality
    def __eq__(self, other):
        if self.port == other.port:
            if self.vlan == other.vlan:
                if self.vlan_untagged == other.vlan_untagged:
                    return True
        return False


if __name__=="__main__":
    #try:
    #    misc.safe_run(main, unlock_resources)
    #except:
#	print ""
    testlogdir = ""
    if os.environ.has_key('TEST_LOG_DIR'):
        testlogdir = os.environ['TEST_LOG_DIR']

    opts, args = getopt.getopt(sys.argv[1:], "d:")
    for o, a in opts:
        if o == "-d":
            testlogdir = a

    if testlogdir != "":
        os.mkdir(testlogdir)
        os.chdir(testlogdir)

    log = buildLogger('encaps.log', debug=True, console=True)

    suite = test_suite()
    suite.addTest(encaps)
    test_runner().run(suite)
    #test_runner(stream=sys.stdout).run(suite)


# ssx1="qa-tmp3"
# ns1="qa-ns1"
#
# vlan1= """
# vlan=10
# ssx1:1:1 tagged
# ns1:0
# """
# vlan1= "vlan=10 ssx1:1:1,tagged ns1:0"

#vgroup_old(vlan1, globals())

