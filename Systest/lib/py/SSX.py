#!/usr/bin/python

import pexpect
import time
import misc
import sys

#newline, then systemname[context]#"
enable_prompt_regex = "([\r\n]+\S+\[\S+\]#)"
config_prompt_regex = "([\r\n]+\S+\(cfg\S*\)#)"
yesno_prompt_regex = ".*[\r\n]+.*\(yes/no\)"

def telnet(host, username="joe@local", password="joe"):
    child = pexpect.spawn("telnet -E -8 " + host)
    try:
        child.expect("Username:")
        child.sendline(username)
        child.expect("Password:")
        child.sendline(password)
        child.sendline("end")
        child.expect(enable_prompt_regex)
    except pexpect.TIMEOUT:
        print "Problem connecting in ssx_telnet()"
        sys.exit(1)
    return child

def console(host):
    child = pexpect.spawn("telnet -E -8 " + host)
    try:
        while True:
            time.sleep(1)
            misc.flush_child(child)
            child.sendline()
            index = child.expect(["Enter your option :", "ogin:", enable_prompt_regex])
            if index == 0:
                child.send("1")
                print "WARNING, someone else is using console on %s" % host
                misc.flush_child(child)
            if index == 1:
                child.sendline(username)
                child.expect("assword:")
                child.sendline(password)
                child.expect(enable_prompt_regex)
            if index == 2:
                break
    except pexpect.TIMEOUT:
        print "Problem connecting in ssx_console()"
        sys.exit(1)
        return False
    return child

def cmd(session,command):
    """Routine to send an EXEC command to a SSX

    Return nothing."""
    
    try:
        misc.flush_child(session)
        session.sendline(command)
        which = session.expect([enable_prompt_regex, yesno_prompt_regex, config_prompt_regex])
        if which == 1:
            session.sendline("yes")
    except pexpect.TIMEOUT:
        print "timeout??\n"
        pass

def cfg(session,command):
    """Routine to send a config command to a SSX

    Return nothing."""
    
    try:
        misc.flush_child(session)
        session.sendline(command)
        which = session.expect([enable_prompt_regex, config_prompt_regex])
    except pexpect.TIMEOUT:
        print "timeout 2?\n"
        pass

if __name__ == "__main__":
    print "testing...\n"
    s = console("cayman-mc-con")
    print "1\n"
    cmd(s,"config")
    print "2\n"
    cfg(s,"system hostname CAYMAN")
    print "3\n"
    cfg(s,"end")
    
