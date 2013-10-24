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

import  time, misc, re
from pexpect import *
from Host import Host
from logging import getLogger
log = getLogger()

ixia_prompt_regex = "[\r\n]*Ixia>"

class IXIA(Host):

    def __init__(self, host, username= "", password= "", stdprompt=ixia_prompt_regex):
        """Ixia specific init method.  Basically just filling in the blanks."""

        Host.__init__(self, host, username, password, stdprompt)
        log.output("Ixia object for host %s created." % host)
	#self.cmd("")


    def cmd(self, command, timeout = 60):
        """Routine to send an EXEC command to a Ixia
        Returns output of command as a string."""
        retstr = ""
	#log.debug("%s"%command)
	log.cmd(command)
        try:
	    self.ses.delaybeforesend = 0.5
            self.ses.sendline(command)
            self.ses.expect(ixia_prompt_regex, timeout)
	    #log.info("before %s; after %s" %(self.ses.before, self.ses.after))
            retstr += self.ses.before
        except TIMEOUT:
            misc.TestError("Timeout in Ixia.cmd for command %s\n" % command)
        return retstr.strip().splitlines()[-1]



