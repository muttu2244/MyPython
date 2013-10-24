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

from pdb import set_trace as st

import sys, os
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

import sys, os, pexpect, time, traceback, re, popen2
from logging import getLogger

log = getLogger()
            
## need to refactor here
def wait4something(maxtime, wait_interval, testfunc, *args, **kwargs):
    maxtries = maxtime / wait_interval
    if testfunc(*args, **kwargs):
        return True
    while True:
        time.sleep(wait_interval)
        if testfunc(*args, **kwargs):
            break
        maxtries -= 1
        if not maxtries:
            return False
    return True

def time_func(func):
    print time.ctime()
    func()
    print time.ctime()

def safe_run(func, handler=None):
    """Run the function.  If an exception creeps up to this level,
    execute the handler and exit.
    """
    try:
        func()
    except:
        if handler:
            handler()
        log.exception("Following exception received.  Exiting...")
        #(type,value,tb) = sys.exc_info() 
        #print "Got a %s exception" % type
        #traceback.print_exc()
        sys.exit(1)

def print_exception():
    (type,value,tb) = sys.exc_info() 
    traceback.print_exc()

class TestFailure(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class TestError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class TestAbort(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

qa_script_debug = False

def testerror(mystr):
    raise TestError(mystr)

def testabort(mystr):
    print "Test Aborted : %s" %mystr
    raise TestAbort(mystr)

def testfailure(mystr):
    if qa_script_debug:
        stack=traceback.extract_stack()
        stack_str = traceback.format_list(stack[:-1])
        for line in stack_str:
            print line,
            print "\t%s" %  mystr
    raise TestFailure(mystr)

def flush_child(child):
    """discard any input from child process and reset state of
    pexpect object.. buffers, match obj etc, returning any data
    read from child process"""
    crap = ""
    try:
        time.sleep(0.1)
        crap = child.read_nonblocking(size=2048,timeout=0.01)
    except:
        pass
    child.before = None
    child.match = None
    child.match_index = None
    child.after = None
    child.buffer = ""
    return crap

# ssx1="salvador"
# ns1="qa-ns1"
#
# vlan1= """
# vlan=10
# ssx1:1:1 tagged
# ns1:e0
# """
# vlan1= "vlan=10 ssx1:1:1,tagged ns1:e0"

#vgroup(vlan1, locals())

def vgroup(con):
    """ """
    return True
    rc = None
    from subprocess import call
    try:
        rc = call("/volume/labtools/util/vgroup %s" % con)
    except:
        log.exception("Problem calling vgroup.")
    if rc:
        log.error("Something went wrong with vgroup %s" % con)

def vgroup_old(vstr, namespace):
    return True
    vg_argstr = ""
    vlan_numstr = False
    vlanreg = re.compile("vlan\s*=\s*(\d+)")
    vstr = eat_blank_lines(vstr)
    for line in vstr.splitlines():
	keywords = line.split()
	m = vlanreg.match(keywords[0])
	if m:
	    #handle vlan keyword
	    vlan_numstr = m.group(1)
#use absolute vlan numbers for now
#	    vg_argstr += "-V %s " % vlan_numstr
	    vg_argstr += "-v %s " % vlan_numstr            
	else: 
	    colonfields = keywords[0].split(":")
	    varname = colonfields[0]
	    portstr = ":".join(colonfields[1:])
	    resname = namespace[varname]
	    vg_argstr += "%s:%s" % (resname, portstr)
	    if len(keywords) > 1:
		if re.match("tagged", keywords[1]):
		    vg_argstr += ",tagged"
	vg_argstr += " "
    #call vgroup.pl
    cmd = "/volume/labtools/util/vgroup.pl %s" % vg_argstr
    log.cmd(cmd)
    vg_output, retcode = shellcmd_read(cmd)
    if retcode or not vg_output:
	print "ERROR: vgroup(): vgroup.pl failed"
	print "vgroup.pl output:\n%s" % vg_output
	testerror("vgroup problem")
    vg_out_reg = re.compile("Info: VLAN used: (\d+)")
    m = vg_out_reg.search(vg_output)
    if m:
	retvlan = m.group(1)
        return retvlan
    else:
        print "ERROR: vgroup(): vgroup.pl failed"
	print "vgroup.pl output:\n%s" % vg_output
	testerror("vgroup problem")


def vgroup_new(vstr):
    return True
    vg_argstr = ""
    vlan_numstr = False
    vlanreg = re.compile("vlan\s*=\s*(\d+)")
    vstr = eat_blank_lines(vstr)
    #for line in vstr.splitlines():
    for line in vstr.split():
        keywords = line.split()
        m = vlanreg.match(keywords[0])
        if m:
            #handle vlan keyword
            vlan_numstr = m.group(1)
#use absolute vlan numbers for now
#           vg_argstr += "-V %s " % vlan_numstr
            vg_argstr += "-v %s " % vlan_numstr
        else:
            colonfields = keywords[0].split(":")
            varname = colonfields[0]
            portstr = ":".join(colonfields[1:])
            vg_argstr += "%s:%s" % (varname, portstr)
            if len(keywords) > 1:
                if re.match("tagged", keywords[1]):
                    vg_argstr += ",tagged"
        vg_argstr += " "
    #call vgroup.pl
    cmd = "/volume/labtools/util/vgroup.pl %s" % vg_argstr
    log.cmd(cmd)
    vg_output, retcode = shellcmd_read(cmd)
    if retcode or not vg_output:
        print "ERROR: vgroup(): vgroup.pl failed"
        print "vgroup.pl output:\n%s" % vg_output
        testerror("vgroup problem")
    vg_out_reg = re.compile("Info: VLAN used: (\d+)")
    m = vg_out_reg.search(vg_output)
    if m:
        retvlan = m.group(1)
        return retvlan
    else:
        print "ERROR: vgroup(): vgroup.pl failed"
        print "vgroup.pl output:\n%s" % vg_output
        testerror("vgroup problem")

def shellcmd_read(str):
    """Run argument string as shell command, and return its output as a string"""
    child = popen2.Popen4(str)
    output = child.fromchild.read()
    #Commented the child.poll() and added child.wait() as poll() returns the status of the 
    #process instead wait() - wait for process and returns the status of the process
    #Added by jameer@stoke.com, reviewed by krao@stoke.com
    #retcode = child.poll()
    retcode = child.wait()
    #Added checkpoint as per wait() return status.
    #if retcode == -1:
    if retcode != 0:
	print "ERROR: shellcmd_read(): child never returned"
	print "Command string: %s" % str
	sys.exit(1)
    return output, retcode

def eat_leading_whitespace(mystr):
    retstr = ""
    non_whitespace_reg = re.compile("^\s*(\S.*)$")
    for line in mystr.splitlines():
	m = non_whitespace_reg.match(line)
	if m:
	    retstr += m.group(1) + "\n"
    return retstr

def eat_blank_lines(mystr):
    """Return copy of argument string with whitespace-only lines removed"""
    blankregexp = re.compile("^[\s]*$")
    retstr = ""
    for line in mystr.splitlines():
	if not blankregexp.match(line):
	    retstr += line + "\n"
    return retstr

def readfile(filename):
    """Read contents of a file, and return as string"""
    try:
	infile = open(filename, "r")
	return infile.read()
    except IOError:
	print "Couldnt open file %s" % filename
	sys.exit(1)

def debug_child(child):
    """dump out a pexpect object and its match groups"""
    print ":::::::::: str of child :::::::::: \n%s" % child
    print ":::::::::: match.groups() :::::::::: %s" % child.match.groups()

def nada():
    pass

def pretty_print(toponum, test):
    """Log the details of the test, depending the verbosity level.
    
    XXX this should not exist in this module.  However, to minimize
    the impact of the changes coming down the pipe, I'm dropping
    this here for the time being.  it really belongs in misc.py.
    --jpittman
    
    """
    [cctsvc1, mod1, encap1, cctsvc2, mod2, encap2, portcfg] = test
    log.test("Topo %d %s" % (toponum, str(test)))

#need to clean up and make some nice prettyprinting here
    log.debug("Topo %d --------------------------" % toponum)
    log.debug("Circuit 1")
    log.debug("Port services defined: %s" % ",".join(cctsvc1))
    #for svc in cctsvc1:
    #    print svc,
    log.debug("Circuit encap modifier: %s" % mod1)
    log.debug("Encapsulation: %s" % encap1)
    log.debug("Connected via: %s" % portcfg)
    log.debug("Circuit 2")
    log.debug("Port services defined: %s" % ",".join(cctsvc2))
    #for svc in cctsvc2:
    #    print svc,
    log.debug("Circuit encap modifier: %s" % mod2)
    log.debug("Encapsulation: %s" % encap2)
