
import pexpect, time, sys


#slurp up all config
#then null it all

def clean_config(console_child):
#send an "unset all"                  THIS DOES NOT WORK, NEED TO FIND OTHER CLEANUP METHOD
#followed by a non-saving "reset"
#followed by some "unset" cleanup
    pass



#check is ipsec link is up
def check_link():
    pass

#force a reset of the ipsec connection
def reset_link():
    pass


def load_config(console_child, configfile):
    try:
        infile = open(configfile)
    except IOError:
        print "ERROR: Couldnt open input file: %s" % configfile
        return False
    for line in infile:
        child.sendline(line)

#newline, then systemname->
ns_prompt_regex = "([\r\n]+\S+-> )"

def console(host, username="netscreen", password="netscreen"):
    host = host + "-con"
    child = pexpect.spawn("telnet " + host)
    try:
        child.sendline()
        index = child.expect(["login:", ns_prompt_regex])
        if index == 0:
            child.sendline(username)
            child.expect("Password:")
            child.sendline(password)
        child.expect(ns_prompt_regex)
    except pexpect.TIMEOUT:
        print "Problem connecting in ns.console()"
        return False
    return child
