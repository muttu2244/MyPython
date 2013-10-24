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

"""This module contains the basic building blocks for connecting and manipulating
remote devices.  In here you will find two classes:  Host and ConsoleServer.

Host is the basic super class used to managing most of the things you will need to
connect to devices.  ConsoleServer serves an example of how to subclass Host when
solving device or os specific issues.

"""

from logging import getLogger
from pdb import set_trace as st
import pexpect
import sys
import pxssh

log = getLogger()


class Host(object):
    """Super class for all interaction with remote machines.

    Here's an example of how to use this class:

    m = Host("qa-ns1-con", "netscreen", "netscreen", "[\r\n]*\S+->")
    m.telnet()
    m.cmd("get config")
    m.cmd("get admin")
    m.close()
    """

    def __init__(self, host, username, passwd, stdprompt, cfgprompt=None,
                 confirmprompt=None):
        """ """
        self.complete = False
        self.host = host
        self.username = username
        self.passwd = passwd
        self.yes = True
        self.std = stdprompt
        self.cfg = cfgprompt
        self.confirm = confirmprompt
        self.prompts = self._build_prompts()
        self.login_prompts = self._build_login_prompts()
        self.ses = None

    def _build_prompts(self):
        """Build a dictionary that maps prompts to types of functionality."""
        prompts = dict()
	prompts["[Uu]sername: $"] = self.username
        prompts["[Pp]assword:"] = self.passwd
        prompts["--- more ---"] = self.blankline
        prompts["\[sudo\] password for regress:"] = self.passwd
        prompts[self.std] = self._standard_prompt
        if self.cfg:
            prompts[self.cfg] = self._standard_prompt
        if self.confirm:
            prompts[self.confirm] = self._confirmation_prompt
        return prompts

    def _build_login_prompts(self):    
        prompts = dict()
        prompts["[Ll]ogin: $"] = self.username
        prompts["[Uu]sername: $"] = self.username
        prompts["[Pp]assword:"] = self.passwd
        prompts["\[sudo\] password for regress:"] = self.passwd
        prompts[self.std] = self._standard_prompt
        return prompts
    
    # Telnet is wonderfull and all but it's terribly insecure and should no longer
    # be used. So we have the choice of changing this code or changin all the 
    # scripts to use a new function.
    def telnet(self, timeout = 200):
        """Telnet directly to a machine to interact with it."""
        try:
            self.ses = pexpect.spawn("telnet -E -8 %s" % self.host, timeout=timeout)
            log.debug("Trying to connect to host %s" % self.host)
            self._handle_login(timeout)
            #self.cmd("")
            log.info("Connected to host %s" % self.host)
        # XXX add an exception for timeouts
        except pexpect.TIMEOUT:
            log.exception("")
            log.error("before was set to:")
            self._log(self.ses.before)
            self.ses.close()
        except:
            log.exception("Failed to connect to host %s" % self.host)
            self.ses.close()
        #return self.ses
    
    
    def ssh(self):
        """Handle SSH login to a host"""
        
        #log.debug('We made it into the SSH function')

        #log.debug('instantiating the pxssh object')
        self.ses = pxssh.pxssh()
        #print 'we just created a pxssh object'
        
        """
        log.debug('The credentials to be used are:')
        log_msg = 'host:', self.host
        log.debug(log_msg)
        log_msg = 'Username:', self.username
        log.debug(log_msg)
        log_msg = 'Password:', self.passwd
        log.debug(log_msg)
        """
        
        try:
            log_msg = 'Trying to login to host: ' + self.host + ' as user: ' + self.username\
                      + ' with password: ' + self.passwd
            log.info(log_msg)
            #print 'This is after the log message'
            print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            self.ses.login(self.host, self.username, self.passwd)
            print "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
	    print self.ses.before
        except pxssh.ExceptionPxssh, e:
               print "pxssh failed on login."
               print str(e)
    
        """    
            except NameError:
            print NameError
            log.error(NameError)
            log.error('Failed to open an SSH session to the host!')
            sys.exit(1)
        """ 
        
        
        #log.debug('past the last except statement!!!!')

        
    def test_funct(self):
        """This fucntion is to test it being called and returning"""
        print 'Now in the test function'
        log.debug('This is a debug message from the test function')
        log.info('This is an info message from the test function')
        log.error('This is an error message from the test function')
        log.output('This is generic output form the test function')
        

    def _handle_login(self, timeout=10):
        """Handles authenticating to a host."""

        self._cmd(prompts=self.login_prompts, timeout=timeout)
        
    def sudo(self):
        self.cmd(self.passwd)

    def _confirmation_prompt(self):
        """This is an empty method for handling confirmation prompts.  When you subclass
        host, if you encounter a yes/no prompt of some sort, you need implement it in
        subclass.

        The reasoning behind making this an empty method is force the implementor of the
        subclass to address a subtle problem with confirmation prompts.  Namely, different
        hosts accept their yes/no values differently.  For example, so environments accept
        either a "y" or a "n".  Others expect you to type the full word, "yes" or "no".
        This detail is not clear until you're implementing.

        A typical example of implementing this method in a sub class would look like this:

        def confirmation_prompt(self):
            if self.yes:
                self.cmd("y")
            else:
                self.cmd("n")

        In the example above, note the use of the object attribute "yes".  By default, when the
        class object is instantiated, it's set to True.  So any time that this method is used,
        it will answer the confirm prompt with a "yes".  If you need to the code to answer the
        confirm prompt with a "no", you would do so somewhere in the code before the prompt could
        be run.  And you do so like this:

        m = Host(args)
        m.yes = False
        m.telnet()
        m.cmd(<some command that will run into a confirmation prompt>)
        m.close()
        """
        log.error("Superclass Host method.  You need to subclass me.")
        log.error("Check out the docstring for Host.confirmation_prompt")

    def _standard_prompt(self):
        """This is a convenience function that you use to mark the completion of
        command run.
        """
        self.complete = True
    
    def close(self):
        """This properly handles the closing down of a session with a host."""
	argType = self
        """
        if "SSX" in str(argType):
                self.getMemorySnap()
        """
        self.ses.close()
        log.debug("Closing down the session to host %s." % self.host)
        
    def cmd(self, line, send=False, timeout=100):
        """Send a command via the established session and return the
        results.
        """
        return self._cmd(line, send, timeout)
    
    def interactive_cmd(self, line, prompts, send=False, timeout=10):
        """ """
        prompts.update(self.prompts)
        return self._cmd(line, send, timeout, prompts)

    def blankline(self):
        self.ses.sendline("")
    
    def _log(self, output):
        """convienance function for logging multiple lines from a ses.before buffer.
        """
        for line in output.split('\r\n')[1:]:
            log.output("%-10s: %s" % (self.host, line.rstrip("\r\n")))

    def flush(self):
        """discard any input from child process and reset state of
        pexpect object.. buffers, match obj etc, returning any data
        read from child process"""
        log.debug("Running flush.")
        crap = ""
        try:
            time.sleep(0.1)
            crap = self.ses.read_nonblocking(size=2048,timeout=0.01)
        except:
            pass
        self.ses.before = None
        self.ses.match = None
        self.ses.match_index = None
        self.ses.after = None
        self.ses.buffer = ""
        log.debug("Crap: %s" % crap)
        return crap
    
    def _cmd(self, line=None, send=False, timeout=12000, prompts=None):

        def pushline(line):
            if send:
                self.ses.send(line)
            else:
                self.ses.sendline(line)
	    if self.ses.after:
                log.cmd("%-10s: %s %s" % (self.host, self.ses.after.lstrip(),line))
	    else:
                log.cmd("%-10s: %s %s" % (self.host, self.ses.before.lstrip(),line))

        output = str()
        if prompts:
            pass
        else:
            prompts = self.prompts
        self.complete = False
        keys = prompts.keys()
        
        if line or line == str():
            pushline(line)
            
        while not self.complete:
            try:
                result = self.ses.expect(keys, timeout)
                prompt = prompts[keys[result]]
                if isinstance(prompt, str):
                    pushline(prompt)
                else:
                    prompt()
                    output += self.ses.before
            except pexpect.TIMEOUT:
                raise
            except:
                log.exception("Line failed to run: %s" % line)
                raise
        self._log(output)
        return output.lstrip(line)



class CycladesConsoleServer(Host):
    """For connecting through a console server.

    This class serves two purposes.  It's here as an example of how to implement a
    sub class of Host.

    It's also here to address an issue with the Cyclades console servers.  With the ability
    to mirror a console session, it introduces a problem that you need to address a menu on
    the console server before actually reaching the machine that you're trying to contact.
    The class is implemented to take over the primary session on the console port, because
    it's expected to be running via automation.

    Which means that it could also step on someone else's toes.  So be careful.

    Here's an example of how to use this class:

    m = CycladesConsoleServer("bahamas-mc-con", "joe@local", "joe", "[\r\n]*\S+\[\S+\](-STANDBY)*")
    m.telnet()
    m.cmd("show config")
    m.close()
    
    """

    def __init__(self, host, username, password, stdprompt, cfgprompt=None,
                 confirmprompt=None):
        """Cyclade console server specific init method."""
        Host.__init__(self, host, username, password, stdprompt, cfgprompt,
                      confirmprompt)
        self.option = False

    def _build_login_prompts(self):
         """Add the cyclade specific prompt that can trip us up."""
         prompts = Host._build_login_prompts(self)
         prompts["Enter your option :"] = self.regular_session
         return prompts
    
    def regular_session(self):
        """This method is used if we hit the cyclade prompt if someone is already
        on the console port.
        """
        
        if self.option:
            self.ses.sendline()
            self.ses.sendline()
            #sudo /sbin/ip addr flush dev eth1return
        else:
            self.option = True
            log.warning("Someone else is using console on %s" % self.host)
            Host.cmd(self, "1")
            
