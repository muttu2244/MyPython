import pexpect
import time

#newline, then linux#
linux_prompt_regex = "([\r\n]linux#)"
pwalk_maxfail = 10

def telnet(host, username="regress", password="gleep7", logfile=None):
    child = pexpect.spawn("telnet " + host, logfile=logfile)
    try:
        child.expect("ogin:")
        child.sendline(username)
        child.expect("assword:")
        child.sendline(password)
        child.sendline("export PS1=linux#")
        child.expect(linux_prompt_regex)
    except pexpect.TIMEOUT:
        print "Problem connecting in linux.telnet()"
        sys.exit(1)
    return child

def ping(child, ipaddr, count=5, size=56, timeout=5, interval=0.2):
    success_regexp = ", 0% packet loss"
    timeout4resp = count * timeout + 1
    child.sendline("ping -i %.1f -n -c %d -s %d -W %d %s" % (interval, count, size, timeout, ipaddr))
    try:
        child.expect(success_regexp, timeout=timeout4resp)
        child.expect(linux_prompt_regex)
    except pexpect.TIMEOUT:
        return False
    return True

def pingwalk(child, dest, start, finish, count=1):
    orig_delay = child.delaybeforesend
    child.delaybeforesend = 0
    fail = False
    failures = 0
    for packetsize in range(start, finish):
        ret = ping(child, dest, count=count, size=packetsize)
        if not ret:
            fail = True
            failures += 1
            print "failed on ping packetsize %d" % packetsize
            if failures > pwalk_maxfail:
                print "Too many failures"
                return False
    child.delaybeforesend = orig_delay
    if fail:
        return False
    else:
        return True
    
def ifconfigv4(child, ipaddr, mask, int="eth1"):
    child.sendline("")
    child.expect(linux_prompt_regex)
    child.sendline("/sbin/ifconfig %s inet %s netmask %s up" % (int, ipaddr, mask))
    child.expect(linux_prompt_regex)

def addroutev4(child, network, maskbits, nexthop, int):
    child.sendline("")
    child.expect(linux_prompt_regex)
    child.sendline("route add -net %s/%d gw %s %s" % (network, maskbits, nexthop, int))
    child.expect(linux_prompt_regex)


