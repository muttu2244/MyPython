#! /usr/bin/env python
#############################################################################
##                                                                         ##
## scapy6.py --- IPv6 support for Scapy                                    ##
##               see http://namabiiru.hongo.wide.ad.jp/scapy6/             ##
##               for more informations                                     ##
##                                                                         ##
## Copyright (C) 2005  Guillaume Valadon <guedou@hongo.wide.ad.jp>         ##
##                     Arnaud Ebalard <arnaud.ebalard@eads.net>            ##
##                                                                         ##
## This program is free software; you can redistribute it and/or modify it ##
## under the terms of the GNU General Public License version 2 as          ##
## published by the Free Software Foundation; version 2.                   ##
##                                                                         ##
## This program is distributed in the hope that it will be useful, but     ##
## WITHOUT ANY WARRANTY; without even the implied warranty of              ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU       ##
## General Public License for more details.                                ##
##                                                                         ##
#############################################################################

from scapy import *
import __builtin__


#############################################################################
# Helpers                                                                  ##
#############################################################################

def get_cls(name, fallback_cls):
    return __builtin__.__dict__.get(name, fallback_cls)


#############################################################################
## Constants                                                               ##
#############################################################################

ETH_P_IPV6 = 0x86dd
NETBSD = sys.platform.startswith("netbsd")

# From net/ipv6.h on Linux (+ Additions)
IPV6_ADDR_UNICAST     = 0x01
IPV6_ADDR_MULTICAST   = 0x02
IPV6_ADDR_CAST_MASK   = 0x0F
IPV6_ADDR_LOOPBACK    = 0x10
IPV6_ADDR_GLOBAL      = 0x00
IPV6_ADDR_LINKLOCAL   = 0x20
IPV6_ADDR_SITELOCAL   = 0x40     # deprecated since Sept. 2004 by RFC 3879
IPV6_ADDR_SCOPE_MASK  = 0xF0
#IPV6_ADDR_COMPATv4   = 0x80     # deprecated; i.e. ::/96
#IPV6_ADDR_MAPPED     = 0x1000   # i.e.; ::ffff:0.0.0.0/96
IPV6_ADDR_6TO4        = 0x0100   # Added to have more specific info (should be 0x0101 ?)
IPV6_ADDR_UNSPECIFIED = 0x10000


#############################################################################
#############################################################################
###                      Routing/Interfaces stuff                         ###
#############################################################################
#############################################################################

def construct_source_candidate_set(addr, plen, laddr):
    """
    Given all addresses assigned to a specific interface ('laddr' parameter),
    this function returns the "candidate set" associated with 'addr/plen'.
    
    Basically, the function filters all interface addresses to keep only those
    that have the same scope as provided prefix.
    
    This is on this list of addresses that the source selection mechanism 
    will then be performed to select the best source address associated
    with some specific destination that uses this prefix.
    """

    cset = []
    if in6_isgladdr(addr):
	cset = filter(lambda x: x[1] == IPV6_ADDR_GLOBAL, laddr)
    elif in6_islladdr(addr):
	cset = filter(lambda x: x[1] == IPV6_ADDR_LINKLOCAL, laddr)
    elif in6_issladdr(addr):
	cset = filter(lambda x: x[1] == IPV6_ADDR_SITELOCAL, laddr)
    elif in6_ismaddr(addr):
	if in6_ismnladdr(addr):
	    cset = [('::1', 16, 'lo')]
	elif in6_ismgladdr(addr):
	    cset = filter(lambda x: x[1] == IPV6_ADDR_GLOBAL, laddr)
	elif in6_ismlladdr(addr):
	    cset = filter(lambda x: x[1] == IPV6_ADDR_LINKLOCAL, laddr)
	elif in6_ismsladdr(addr):
	    cset = filter(lambda x: x[1] == IPV6_ADDR_SITELOCAL, laddr)
    elif addr == '::' and plen == 0:
	cset = filter(lambda x: x[1] == IPV6_ADDR_GLOBAL, laddr)
    cset = map(lambda x: x[0], cset)
    return cset            

def get_source_addr_from_candidate_set(dst, candidate_set):
    """
    This function implement a limited version of source address selection
    algorithm defined in section 5 of RFC 3484. The format is very different
    from that described in the document because it operates on a set 
    of candidate source address for some specific route.
    
    Rationale behind the implementation is to be able to make the right 
    choice for a 6to4 destination when both a 6to4 address and a IPv6 native
    address are available for that interface.
    """
    
    if len(candidate_set) == 0:
	# Should not happen
	return None
    
    if in6_isaddr6to4(dst):
	tmp = filter(lambda x: in6_isaddr6to4(x), candidate_set)
	if len(tmp) != 0:
	    return tmp[0]

    return candidate_set[0]

class Route6:

    def __init__(self):
        self.resync()

    def flush(self):
        self.routes = []

    def resync(self):
        # TODO : At the moment, resync will drop existing Teredo routes
        #        if any. Change that ...
	self.routes = read_routes6()
	if self.routes == []:
	     log_loading.info("No IPv6 support in kernel")
        
    def __repr__(self):
        rtlst = [('Destination', 'Next Hop', "iface", "src candidates")]

        for net,msk,gw,iface,cset in self.routes:
	    rtlst.append(('%s/%i'% (net,msk), gw, iface, ", ".join(cset)))

        colwidth = map(lambda x: max(map(lambda y: len(y), x)), apply(zip, rtlst))
        fmt = "  ".join(map(lambda x: "%%-%ds"%x, colwidth))
        rt = "\n".join(map(lambda x: fmt % x, rtlst))

        return rt


    # Unlike Scapy's Route.make_route() function, we do not have 'host' and 'net'
    # parameters. We only have a 'dst' parameter that accepts 'prefix' and 
    # 'prefix/prefixlen' values.
    # WARNING: Providing a specific device will at the moment not work correctly.
    def make_route(self, dst, gw=None, dev=None):
        """Internal function : create a route for 'dst' via 'gw'.
        """
        prefix, plen = (dst.split("/")+["128"])[:2]
        plen = int(plen)

        if gw is None:
            gw = "::"
        if dev is None:
            dev, ifaddr, x = self.route(gw)
        else:
            # TODO: do better than that
            # replace that unique address by the list of all addresses
            lifaddr = in6_getifaddr()             
            devaddrs = filter(lambda x: x[2] == dev, lifaddr)
            ifaddr = construct_source_candidate_set(prefix, plen, devaddrs)

        return (prefix, plen, gw, dev, ifaddr)

    
    def add(self, *args, **kargs):
        """Ex:
        add(dst="2001:db8:cafe:f000::/56")
        add(dst="2001:db8:cafe:f000::/56", gw="2001:db8:cafe::1")
        add(dst="2001:db8:cafe:f000::/64", gw="2001:db8:cafe::1", dev="eth0")
        """
        self.routes.append(self.make_route(*args, **kargs))


    # TODO: we can do better. We should be able to remove a route only based
    #       on dst if it is not ambiguous
    def delt(self, *args, **kargs):
        """ Ex: delt(dst="2001:db8:cafe:f000::/56", gw="2001:db8:deca::1") """
        route = self.make_route(*args,**kargs)
        try:
            i=self.routes.index(route)
            del(self.routes[i])
        except ValueError:
            warning("no matching route found")

        
    def ifchange(self, iff, addr):
        the_addr,the_plen = (addr.split("/")+["128"])[:2]
        the_plen = int(addr)

        naddr = socket.inet_pton(socket.AF_INET6, the_addr)
        nmask = in6_cidr2mask(the_plen)
        the_net = socket.inet_ntop(socket.AF_INET6, in6_and(nmask,naddr))
        
        for i in range(len(self.routes)):
            net,plen,gw,iface,addr = self.routes[i]
            if iface != iff:
                continue
            if gw == '::':
                self.routes[i] = (the_net,the_plen,gw,iface,the_addr)
            else:
                self.routes[i] = (net,the_plen,gw,iface,the_addr)
        ip6_neigh_cache.flush()

    def ifdel(self, iff):
        """ removes all route entries that uses 'iff' interface. """
        new_routes=[]
        for rt in self.routes:
            if rt[3] != iff:
                new_routes.append(rt)
        self.routes = new_routes


    def ifadd(self, iff, addr):
        """
        Add an interface 'iff' with provided address into routing table.
        
        Ex: ifadd('eth0', '2001:bd8:cafe:1::1/64') will add following entry into 
            Scapy6 internal routing table:

            Destination           Next Hop  iface  Def src @
            2001:bd8:cafe:1::/64  ::        eth0   2001:bd8:cafe:1::1

            prefix length value can be omitted. In that case, a value of 128
            will be used.
        """
        addr, plen = (addr.split("/")+["128"])[:2]
        addr = in6_ptop(addr)
        plen = int(plen)
        naddr = socket.inet_pton(socket.AF_INET6, addr)
        nmask = in6_cidr2mask(plen)
        prefix = socket.inet_ntop(socket.AF_INET6, in6_and(nmask,naddr))
        self.routes.append((prefix,plen,'::',iff,[addr]))

    def route(self, dst, dev=None):
        """
        Provide best route to IPv6 destination address, based on Scapy6 
        internal routing table content.

        When a set of address is passed (e.g. 2001:db8:cafe:*::1-5) an address
        of the set is used. Be aware of that behavior when using wildcards in
        upper parts of addresses !

        If 'dst' parameter is a FQDN, name resolution is performed and result
        is used.

        if optional 'dev' parameter is provided a specific interface, filtering
        is performed to limit search to route associated to that interface.
        """
        # Transform "2001:db8:cafe:*::1-5:0/120" to one IPv6 address of the set
        dst = dst.split("/")[0]
        savedst = dst # In case following inet_pton() fails 
        dst = dst.replace("*","0")
        l = dst.find("-")
        while l >= 0:
            m = (dst[l:]+":").find(":")
            dst = dst[:l]+dst[l+m:]
            l = dst.find("-")
            
        try:
            socket.inet_pton(socket.AF_INET6, dst)
        except socket.error:
            dst = socket.getaddrinfo(savedst, None, socket.AF_INET6)[0][-1][0]
            # TODO : Check if name resolution went well

        pathes = []

        # TODO : review all kinds of addresses (scope and *cast) to see
        #        if we are able to cope with everything possible. I'm convinced 
        #        it's not the case.
        # -- arnaud
        for p, plen, gw, iface, cset in self.routes:
            if dev is not None and iface != dev:
                continue
            if in6_isincluded(dst, p, plen):
                pathes.append((plen, (iface, cset, gw)))
            elif (in6_ismlladdr(dst) and in6_islladdr(p) and in6_islladdr(cset[0])):
                pathes.append((plen, (iface, cset, gw)))
                
        if not pathes:
            warning("No route found for IPv6 destination %s (no default route?)" % dst)
            return ("lo", "::", "::") # XXX Linux specific

        pathes.sort()
        pathes.reverse()

        best_plen = pathes[0][0]
        pathes = filter(lambda x: x[0] == best_plen, pathes)

        res = []
        for p in pathes: # Here we select best source address for every route
            tmp = p[1]
            srcaddr = get_source_addr_from_candidate_set(dst, p[1][1])
            if srcaddr is not None:
                res.append((p[0], (tmp[0], srcaddr, tmp[2])))

        # Symptom  : 2 routes with same weight (our weight is plen)
        # Solution : 
        #  - dst is unicast global. Check if it is 6to4 and we have a source 
        #    6to4 address in those available
        #  - dst is link local (unicast or multicast) and multiple output
        #    interfaces are available. Take main one (conf.iface)
        #  - if none of the previous or ambiguity persists, be lazy and keep
        #    first one
        #  XXX TODO : in a _near_ future, include metric in the game

        if len(res) > 1:
            tmp = []
            if in6_isgladdr(dst) and in6_isaddr6to4(dst):
                # TODO : see if taking the longest match between dst and
                #        every source addresses would provide better results
                tmp = filter(lambda x: in6_isaddr6to4(x[1][1]), res)
            elif in6_ismaddr(dst) or in6_islladdr(dst):
                # TODO : I'm sure we are not covering all addresses. Check that
                tmp = filter(lambda x: x[1][0] == conf.iface, res)

            if tmp:
                res = tmp
        
        return res[0][1]

def get_if_raw_addr6(iff):
    """
    Returns the main global unicast address associated with provided 
    interface, in network format. If no global address is found, None 
    is returned. 
    """
    r = filter(lambda x: x[2] == iff and x[1] == IPV6_ADDR_GLOBAL, in6_getifaddr())
    if len(r) == 0:
        return None
    else:
        r = r[0][0] 
    return socket.inet_pton(socket.AF_INET6, r)

if not LINUX:

    def in6_getifaddr():
        ret = []
	i = dnet.intf()
        for int in i:
	    ifname = int['name']
            v6 = []
	    if int.has_key('alias_addrs'):
		v6 = int['alias_addrs']
	    for a in v6:
		if a.type != dnet.ADDR_TYPE_IP6:
		    continue

		xx = str(a).split('/')[0]
		addr = in6_ptop(xx)

		if in6_isgladdr(addr):
		    scope = IPV6_ADDR_GLOBAL
		elif in6_islladdr(addr):
		    scope = IPV6_ADDR_LINKLOCAL
		elif in6_issladdr(addr):
		    scope = IPV6_ADDR_SITELOCAL
		elif in6_ismaddr(addr):
		    scope = IPV6_ADDR_MULTICAST
                elif addr == '::1':
		    scope = IPV6_ADDR_LOOPBACK
		else:
		    scope = -1 

		ret += [ (xx, scope, ifname) ]
        return ret

    def read_routes6():
        f = os.popen("netstat -rn -f inet6")
        ok = -1
        routes = []
        lifaddr = in6_getifaddr()
        for l in f.readlines():
            if not l:
                break
            l = l.strip()
            if ok < 0:
                ok = l.find('Destination')
                continue
            # gv 12/12/06: under debugging	
	    #if NETBSD:
	    #    dest,nh,fl,_,_,_,dev = l.split()[:7]
	    #else:
	    if 1:
                d,nh,fl,dev = l.split()[:4]
	    if filter(lambda x: x[2] == dev, lifaddr) == []:
	        continue
            if 'L' in fl: # drop MAC addresses
                continue

            if 'link' in nh:
	     	nh = '::'

	    cset = [] # candidate set (possible source addresses)
	    dp = 128
	    if d == 'default':
		d = '::'
		dp = 0
	    if '/' in d:
		d,dp = d.split("/")
		dp = int(dp)
	    if '%' in d:
		d,dev = d.split('%')
	    if '%' in nh:
		nh,dev = nh.split('%')
	    if 'lo' in dev:
		cset = ['::1']
		nh = '::'
            else:
		devaddrs = filter(lambda x: x[2] == dev, lifaddr)
		cset = construct_source_candidate_set(d, dp, devaddrs)

            if len(cset) != 0:
		routes.append((d, dp, nh, dev, cset))

        f.close()
        return routes

else:	

    def in6_getifaddr():
        ret = []
	try:
	    f = open("/proc/net/if_inet6","r")
	except IOError, err:    
	    return ret
	l = f.readlines()
	for i in l:
	    # addr, index, plen, scope, flags, ifname
	    tmp = i.split()
	    addr = struct.unpack('4s4s4s4s4s4s4s4s', tmp[0])
	    addr = in6_ptop(':'.join(addr))
	    ret.append((addr, int(tmp[3], 16), tmp[5])) # (addr, scope, iface)
       	return ret

    def read_routes6():
	try:
	    f = open("/proc/net/ipv6_route","r")
	except IOError, err:
	    return []
	# 1. destination network
	# 2. destination prefix length
	# 3. source network displayed
	# 4. source prefix length
        # 5. next hop
	# 6. metric
	# 7. reference counter (?!?)
	# 8. use counter (?!?)
	# 9. flags
	# 10. device name
        routes = []
	def proc2r(p):
   	    ret = struct.unpack('4s4s4s4s4s4s4s4s', p)
	    ret = ':'.join(ret)
	    return in6_ptop(ret)
        
        #def find_ifaddr(addr, plen, laddr):
        #    """
        #    Given all addresses assigned to a specific interface ('laddr' parameter),
        #    this function returns the "candidate set" associated with 'addr/plen'.

        #    Basically, the function filters all interface addresses to keep only those
        #    that have the same scope as provided prefix.

        #    This is on this list of addresses that the source selection mechanism 
        #    will then be performed to select the best source address associated
        #    with some specific destination that uses this prefix.
        #    """
        #    ifaddr = []
        #    if in6_isgladdr(addr):
        #        ifaddr = filter(lambda x: x[1] == IPV6_ADDR_GLOBAL, laddr)[0]
        #    elif in6_islladdr(addr):
        #        ifaddr = filter(lambda x: x[1] == IPV6_ADDR_LINKLOCAL, laddr)[0]
        #    elif in6_issladdr(addr):
        #        ifaddr = filter(lambda x: x[1] == IPV6_ADDR_SITELOCAL, laddr)[0]
        #    elif in6_ismaddr(addr):
        #        if in6_ismnladdr(addr):
        #          ifaddr = ['::1']
        #        elif in6_ismgladdr(addr):
        #          ifaddr = filter(lambda x: x[1] == IPV6_ADDR_GLOBAL, laddr)[0]
        #        elif in6_ismlladdr(addr):
        #          ifaddr = filter(lambda x: x[1] == IPV6_ADDR_LINKLOCAL, laddr)[0]
        #        elif in6_ismsladdr(addr):
        #          ifaddr = filter(lambda x: x[1] == IPV6_ADDR_SITELOCAL, laddr)[0]
        #    elif addr == '::' and plen == 0:
        #        ifaddr = filter(lambda x: x[1] == IPV6_ADDR_GLOBAL, laddr)[0][0]
        #    return ifaddr


        # arnaud - 2006-08-10 : set these 2 values here temporarily
        # TODO : remove them
        # They are in version 10.0.4.60 of Scapy. Let users time to update
        # their version. 
        RTF_UP     = 0x0001
        RTF_REJECT = 0x0200
        
	lifaddr = in6_getifaddr() 
        for l in f.readlines():
	    d,dp,s,sp,nh,m,rc,us,fl,dev = l.split()
            fl = int(fl, 16)

            if fl & RTF_UP == 0:
                continue
            if fl & RTF_REJECT:
                continue

	    d = proc2r(d) ; dp = int(dp, 16)
	    s = proc2r(s) ; sp = int(sp, 16)
	    nh = proc2r(nh)

            cset = [] # candidate set (possible source addresses)
	    if dev == 'lo':
		if d == '::':
		    continue
		cset = ['::1']
	    else:
                devaddrs = filter(lambda x: x[2] == dev, lifaddr)
		cset = construct_source_candidate_set(d, dp, devaddrs)
	    
            if len(cset) != 0:
		routes.append((d, dp, nh, dev, cset))
	f.close()
	return routes	


##########################
## Neighbor cache stuff ##
##########################

NEIGHTIMEOUT=120

def neighsol(addr, src, iface, timeout=1):
    """
    Sends an ICMPv6 Neighbor Solicitation message to get the MAC address
    of the neighbor with specified IPv6 address addr. 'src' address is 
    used as source of the message. Message is sent on iface. By default,
    timeout waiting for an answer is 1 second.

    If no answer is gathered, None is returned. Else, the answer is 
    returned (ethernet frame).
    """

    nsma = in6_getnsma(socket.inet_pton(socket.AF_INET6, addr))
    d = socket.inet_ntop(socket.AF_INET6, nsma)
    dm = in6_getnsmac(nsma)
    p = Ether(dst=dm)/IPv6(dst=d, src=src, hlim=255)
    p /= ICMPv6ND_NS(tgt=addr)
    p /= ICMPv6NDOptSrcLLAddr(lladdr=get_if_hwaddr(iface))
    res = srp1(p,type=ETH_P_IPV6, iface=iface, timeout=1, verbose=0)    

    return res

class neighborCache:

    # TODO : add some method to modify default value for timeout
    # TODO : See what we can do for updating the neighbor cache
    #        when receiving a packet.

    def __init__(self):
        self.neighcache = {}

    def flush(self, statictoo=True):
        self.neighcache = {}
        
    def __repr__(self):
        res = [("Peer", "Link layer address", "State")]
        for addr in self.neighcache.keys():
            cur_entry = self.neighcache[addr]
            status = "REACHABLE"
            last_contact = cur_entry[1]
            if last_contact == 0:
                status = "STATIC"
            elif ((time.time() - last_contact) < NEIGHTIMEOUT):
                status = "REACHABLE"
            else:
                status = "STALE"
            res.append((addr, cur_entry[0], status))

        colwidth = map(lambda x: max(map(lambda y: len(y), x)), apply(zip, res))
        fmt = "  ".join(map(lambda x: "%%-%ds"%x, colwidth))
        res = "\n".join(map(lambda x: fmt % x, res))
        return res

    def addNeighbor(self, ip6, mac, static=False):
        """
        Add a neighbor to the cache. If optional parameter 'static' is not 
        set to True (the default), the entry will expire in 2 minutes. If 
        'static' is set to True, the entry in the neighbor cache is made 
        static. This is practical in those cases :

        - peer's addresse is not advertised to be on-link
        - peer's do not answer to NS
        - you don't want to make queries to keep time or be stealthy, ...
        """
        t = 0
        if not static:
            t = time.time()
        self.neighcache[ip6] = (mac, t)

    def makeStatic(self, ip6):
        """
        make the entry static in Scapy6 internal neighbor cache for 
        'ip6' neighbor.
        """
        if self.neighcache.has_key(ip6):
            mac = self.neighcache[ip6][0]
            self.neighcache[ip6] = (mac, 0)
        else:
            warning("Unable to make neighbor cache entry for %s static. It does not exist." % ip6)

    def removeStatic(self, ip6):
        """
        remove the static status for 'ip6' entry in Scapy6 internal 
        neighbor cache.
        """
        if self.neighcache.has_key(ip6):
            mac = self.neighcache[ip6][0]
            self.neighcache[ip6] = (mac, time.time())
        else:
            warning("Unable to make neighbor cache entry for %s static. It does not exist." % ip6)

    def get(self, ip6):
        """
        Returns the link layer address to use for IPv6 traffic to 'ip6' address. 
        If searched IPv6 address is multicast, then, ethernet address is computed.
        If that's not the case, Scapy6 routing table is used to find next hop for
        provided address. If one is found, cache is searched. If a valid (REACHABLE 
        or STATIC) entry exist, content is returned. Else, resolution is perfomed
        by sending a Neighbor solicitation. 

        In all cases, if lookup fails, None is returned.
        """
        
        if in6_ismaddr(ip6): # Multicast 
            mac = in6_getnsmac(socket.inet_pton(socket.AF_INET6, ip6))
            return mac
    
        iff,a,nh = conf.route6.route(ip6, dev=conf.iface)

        if iff == "lo":
            return "ff:ff:ff:ff:ff:ff"

        if nh != '::': 
            ip6 = nh # Found next hop

        if self.neighcache.has_key(ip6): # search the cache
            mac, timeout = self.neighcache[ip6]
            if timeout and (time.time()-timeout < NEIGHTIMEOUT):
                return mac
            
        res = neighsol(ip6, a, iff)
            
        if res is not None:
            mac = res.src
            self.neighcache[ip6] = (mac,time.time())
            return mac

        return None

ip6_neigh_cache = neighborCache()

def getmacbyip6(ip6):
    """
    Returns the mac address to be used for provided 'ip6' peer. 
    neighborCache.get() method is used on instantiated neighbor cache.
    Resolution mechanism is described in associated doc string.
    """
    return ip6_neigh_cache.get(ip6)


#############################################################################
#############################################################################
###              IPv6 addresses manipulation routines                     ###
#############################################################################
#############################################################################

class Net6(Gen): # syntax ex. fec0::/126
    """Generate a list of IPv6s from a network address or a name"""
    name = "ipv6"
    ipaddress = re.compile(r"^([a-fA-F0-9:]+)(/[1]?[0-3]?[0-9])?$")

    def __init__(self, net):
        self.repr = net

        tmp = net.split('/')+["128"]
        if not self.ipaddress.match(net):
            tmp[0]=socket.getaddrinfo(tmp[0], None, socket.AF_INET6)[0][-1][0]

        netmask = int(tmp[1])
	self.net = socket.inet_pton(socket.AF_INET6, tmp[0])
        self.mask = in6_cidr2mask(netmask)
	self.plen = netmask

    def __iter__(self):
        def m8(i):
	    if i % 8 == 0:
                return i
        tuple = filter(lambda x: m8(x), xrange(8, 129))

        a = in6_and(self.net, self.mask)
        tmp = map(lambda x:  x, struct.unpack('16B', a))
   
        def parse_digit(a, netmask):
            netmask = min(8,max(netmask,0))
            a = (int(a) & (0xffL<<netmask),(int(a) | (0xffL>>(8-netmask)))+1)
            return a
        self.parsed = map(lambda x,y: parse_digit(x,y), tmp, map(lambda x,nm=self.plen: x-nm, tuple))

        def rec(n, l): 
	    if n and  n % 2 == 0:
		sep = ':'
	    else:	
                sep = ''
            if n == 16:
		return l
            else:
	        ll = []
		for i in xrange(*self.parsed[n]):
		    for y in l:
		        ll += [y+sep+'%.2x'%i]
		return rec(n+1, ll)

        return iter(rec(0, ['']))

    def __repr__(self):
        return "<Net6 %s>" % self.repr


# Think before modify it : for instance, FE::1 does exist and is unicast
# there are many others like that.
# TODO : integrate Unique Local Addresses
def in6_getAddrType(addr):
    naddr = socket.inet_pton(socket.AF_INET6, addr)
    paddr = socket.inet_ntop(socket.AF_INET6, naddr) # normalize
    addrType = 0
    # _Assignable_ Global Unicast Address space
    # is defined in RFC 3513 as those in 2000::/3
    if ((struct.unpack("B", naddr[0])[0] & 0xE0) == 0x20):
        addrType = (IPV6_ADDR_UNICAST | IPV6_ADDR_GLOBAL)
        if naddr[:2] == ' \x02': # Mark 6to4 @
            addrType |= IPV6_ADDR_6TO4
    elif naddr[0] == '\xff': # multicast
        addrScope = paddr[3]
        if addrScope == '2':
            addrType = (IPV6_ADDR_LINKLOCAL | IPV6_ADDR_MULTICAST)
        elif addrScope == 'e':
            addrType = (IPV6_ADDR_GLOBAL | IPV6_ADDR_MULTICAST)
        else:
            addrType = (IPV6_ADDR_GLOBAL | IPV6_ADDR_MULTICAST)
    elif ((naddr[0] == '\xfe') and ((int(paddr[2], 16) & 0xC) == 0x8)):
        addrType = (IPV6_ADDR_UNICAST | IPV6_ADDR_LINKLOCAL)
    elif paddr == "::1":
        addrType = IPV6_ADDR_LOOPBACK
    elif paddr == "::":
        addrType = IPV6_ADDR_UNSPECIFIED
    else:
        # Everything else is global unicast (RFC 3513)
        # Even old deprecated (RFC3879) Site-Local addresses
        addrType = (IPV6_ADDR_GLOBAL | IPV6_ADDR_UNICAST)

    return addrType

def find_ifaddr2(addr, plen, laddr):
    dstAddrType = in6_getAddrType(addr)
    
    if dstAddrType == IPV6_ADDR_UNSPECIFIED: # Should'nt happen as dst addr
	return None

    if dstAddrType == IPV6_ADDR_LOOPBACK: 
	return None

    tmp = [[]] + map(lambda (x,y,z): (in6_getAddrType(x), x, y, z), laddr)
    def filterSameScope(l, t):
	if (t[0] & dstAddrType & IPV6_ADDR_SCOPE_MASK) == 0:
	    l.append(t)
	return l
    sameScope = reduce(filterSameScope, tmp)
    
    l =  len(sameScope) 
    if l == 1:  # Only one address for our scope
	return sameScope[0][1]

    elif l > 1: # Muliple addresses for our scope
	stfAddr = filter(lambda x: x[0] & IPV6_ADDR_6TO4, sameScope)
	nativeAddr = filter(lambda x: not (x[0] & IPV6_ADDR_6TO4), sameScope)

	if not (dstAddrType & IPV6_ADDR_6TO4): # destination is not 6to4
	   if len(nativeAddr) != 0:
	       return nativeAddr[0][1]
	   return stfAddr[0][1]

	else:  # Destination is 6to4, try to use source 6to4 addr if any
	    if len(stfAddr) != 0:
		return stfAddr[0][1]
	    return nativeAddr[0][1]
    else:
	return None


def in6_mactoifaceid(mac, ulbit=None):
    """
    Compute the interface ID in modified EUI-64 format associated 
    to the Ethernet address provided as input.
    value taken by U/L bit in the interface identifier is basically 
    the reversed value of that in given MAC address it can be forced
    to a specific value by using optional 'ulbit' parameter.
    """
    if len(mac) != 17: return None
    m = "".join(mac.split(':'))
    if len(m) != 12: return None
    first = int(m[0:2], 16)
    if ulbit is None or not (ulbit == 0 or ulbit == 1):
        ulbit = [1,'-',0][first & 0x02]
    ulbit *= 2
    first = "%.02x" % ((first & 0xFD) | ulbit)
    eui64 = first + m[2:4] + ":" + m[4:6] + "FF:FE" + m[6:8] + ":" + m[8:12]
    return eui64.upper()

def in6_ifaceidtomac(ifaceid): # TODO: finish commenting function behavior
    """
    Extract the mac address from provided iface ID. Iface ID is provided 
    in printable format ("XXXX:XXFF:FEXX:XXXX", eventually compressed). None 
    is returned on error.
    """
    try:
        ifaceid = socket.inet_pton(socket.AF_INET6, "::"+ifaceid)[8:16]
    except:
        return None
    if ifaceid[3:5] != '\xff\xfe':
        return None
    first = struct.unpack("B", ifaceid[:1])[0]
    ulbit = 2*[1,'-',0][first & 0x02]
    first = struct.pack("B", ((first & 0xFD) | ulbit))
    oui = first + ifaceid[1:3]
    end = ifaceid[5:]
    l = map(lambda x: "%.02x" % struct.unpack("B", x)[0], list(oui+end))
    return ":".join(l)

def in6_getLinkScopedMcastAddr(addr, grpid=None, scope=2):
    """
    Generate a Link-Scoped Multicast Address as described in RFC 4489.
    Returned value is in printable notation.

    'addr' parameter specifies the link-local address to use for generating
    Link-scoped multicast address IID.
    
    By default, the function returns a ::/96 prefix (aka last 32 bits of 
    returned address are null). If a group id is provided through 'grpid' 
    parameter, last 32 bits of the address are set to that value (accepted 
    formats : '\x12\x34\x56\x78' or '12345678' or 0x12345678 or 305419896).

    By default, generated address scope is Link-Local (2). That value can 
    be modified by passing a specific 'scope' value as an argument of the
    function. RFC 4489 only authorizes scope values <= 2. Enforcement
    is performed by the function (None will be returned).
    
    If no link-local address can be used to generate the Link-Scoped IPv6
    Multicast address, or if another error occurs, None is returned.
    """
    if not scope in [0, 1, 2]:
        return None    
    try:
        if not in6_islladdr(addr):
            return None
        addr = socket.inet_pton(socket.AF_INET6, addr)
    except:
        warning("in6_getLinkScopedMcastPrefix(): Invalid address provided")
        return None

    iid = addr[8:]

    if grpid is None:
        grpid = '\x00\x00\x00\x00'
    else:
        if type(grpid) is str:
            if len(grpid) == 8:
                try:
                    grpid = int(grpid, 16) & 0xffffffff
                except:
                    warning("in6_getLinkScopedMcastPrefix(): Invalid group id provided")
                    return None
            elif len(grpid) == 4:
                try:
                    grpid = struct.unpack("!I", grpid)[0]
                except:
                    warning("in6_getLinkScopedMcastPrefix(): Invalid group id provided")
                    return None
        grpid = struct.pack("!I", grpid)

    flgscope = struct.pack("B", 0xff & ((0x3 << 4) | scope))
    plen = '\xff'
    res = '\x00'
    a = '\xff' + flgscope + res + plen + iid + grpid

    return socket.inet_ntop(socket.AF_INET6, a)

def in6_get6to4Prefix(addr):
    """
    Returns the /48 6to4 prefix associated with provided IPv4 address
    On error, None is returned. No check is performed on public/private
    status of the address
    """
    try:
        addr = socket.inet_pton(socket.AF_INET, addr)
        addr = socket.inet_ntop(socket.AF_INET6, '\x20\x02'+addr+'\x00'*10)
    except:
        return None
    return addr

def in6_getLocalUniquePrefix():
    """
    Returns a pseudo-randomly generated Local Unique prefix. Function
    follows recommandation of Section 3.2.2 of RFC 4193 for prefix
    generation.
    """
    # Extracted from RFC 1305 (NTP) :
    # NTP timestamps are represented as a 64-bit unsigned fixed-point number, 
    # in seconds relative to 0h on 1 January 1900. The integer part is in the 
    # first 32 bits and the fraction part in the last 32 bits.

    # epoch = (1900, 1, 1, 0, 0, 0, 5, 1, 0) 
    # x = time.time()
    # from time import gmtime, strftime, gmtime, mktime
    # delta = mktime(gmtime(0)) - mktime(self.epoch)
    # x = x-delta

    tod = time.time() # time of day. Will bother with epoch later
    i = int(tod)
    j = int((tod - i)*(2**32))
    tod = struct.pack("!II", i,j)
    # TODO: Add some check regarding system address gathering
    rawmac = get_if_raw_hwaddr(conf.iface)[1]
    mac = ":".join(map(lambda x: "%.02x" % ord(x), list(rawmac)))
    # construct modified EUI-64 ID
    eui64 = socket.inet_pton(socket.AF_INET6, '::' + in6_mactoifaceid(mac))[8:] 
    import sha
    globalid = sha.new(tod+eui64).digest()[:5]
    return socket.inet_ntop(socket.AF_INET6, '\xfd' + globalid + '\x00'*10)
    
_rfc1924map = [ '0','1','2','3','4','5','6','7','8','9','A','B','C','D','E',
                'F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T',
                'U','V','W','X','Y','Z','a','b','c','d','e','f','g','h','i',
                'j','k','l','m','n','o','p','q','r','s','t','u','v','w','x',
                'y','z','!','#','$','%','&','(',')','*','+','-',';','<','=',
                '>','?','@','^','_','`','{','|','}','~' ]

def in6_ctop(addr):
    """
    Convert an IPv6 address in Compact Representation Notation 
    (RFC 1924) to printable representation ;-)
    Returns None on error.
    """
    if len(addr) != 20 or not reduce(lambda x,y: x and y, 
                                     map(lambda x: x in _rfc1924map, addr)):
        return None
    i = 0
    for c in addr:
        j = _rfc1924map.index(c)
        i = 85*i + j
    res = []
    for j in range(4):
        res.append(struct.pack("!I", i%2**32))
        i = i/(2**32)
    res.reverse()
    return socket.inet_ntop(socket.AF_INET6, "".join(res))

def in6_ptoc(addr):
    """
    Converts an IPv6 address in printable representation to RFC 
    1924 Compact Representation ;-) 
    Returns None on error.
    """    
    try:
        d=struct.unpack("!IIII", socket.inet_pton(socket.AF_INET6, addr))
    except:
        return None
    res = 0
    m = [2**96, 2**64, 2**32, 1]
    for i in range(4):
        res += d[i]*m[i]
    rem = res
    res = []
    while rem:
        res.append(_rfc1924map[rem%85])
        rem = rem/85
    res.reverse()
    return "".join(res)

    
def in6_isaddr6to4(x):
    x = socket.inet_pton(socket.AF_INET6, x)
    return x[:2] == ' \x02'

conf.teredoPrefix = "2001::" # old one was 3ffe:831f
conf.teredoServerPort = 3544

def in6_isaddrTeredo(x):
    our = socket.inet_pton(socket.AF_INET6, x)[0:4]
    teredoPrefix = socket.inet_pton(socket.AF_INET6, conf.teredoPrefix)[0:4]
    return teredoPrefix == our

# returns server, flag, mapped addr and mapped port from Teredo address
def teredoAddrExtractInfo(x):
    addr = socket.inet_pton(socket.AF_INET6, x)
    server = socket.inet_ntop(socket.AF_INET, addr[4:8])
    flag = struct.unpack("!H",addr[8:10])[0]
    mappedport = struct.unpack("!H",strxor(addr[10:12],'\xff'*2))[0] 
    mappedaddr = socket.inet_ntop(socket.AF_INET, strxor(addr[12:16],'\xff'*4))
    return server, flag, mappedaddr, mappedport

def in6_iseui64(x):
    eui64 = socket.inet_pton(socket.AF_INET6, '::ff:fe00:0')
    x = in6_and(x, eui64)
    return x == socket.inet_pton(socket.AF_INET6, '::ff:fe00:0')

def in6_isanycast(x): # RFC 2526
    if in6_iseui64(x):
        s = '::fdff:ffff:ffff:ff80'
        x = in6_and(x, socket.inet_pton(socket.AF_INET6, '::ffff:ffff:ffff:ff80'))
	x = in6_and(x, socket.inet_pton(socket.AF_INET6, s)) 
        return x == socket.inet_pton(socket.AF_INET6, s)
    else:
	# not EUI-64 
	#|              n bits             |    121-n bits    |   7 bits   |
	#+---------------------------------+------------------+------------+
	#|           subnet prefix         | 1111111...111111 | anycast ID |
	#+---------------------------------+------------------+------------+
	#                                  |   interface identifier field  |
        warning('in6_isanycast(): TODO not EUI-64')
        return 0

def in6_bitops(a1, a2, operator=0):
    a1 = struct.unpack('4I', a1)
    a2 = struct.unpack('4I', a2)
    fop = [ lambda x,y: x | y,
            lambda x,y: x & y,
            lambda x,y: x ^ y
	  ]  
    ret = map(fop[operator%len(fop)], a1, a2)
    t = ''.join(map(lambda x: struct.pack('I', x), ret))
    return t

def in6_or(a1, a2):
    return in6_bitops(a1, a2, 0)

def in6_and(a1, a2):
    return in6_bitops(a1, a2, 1)

def in6_xor(a1, a2):
    return in6_bitops(a1, a2, 2)

def in6_cidr2mask(m):
  t = []
  for i in xrange(0, 4):
      t.append(max(0, 2**32  - 2**(32-min(32, m))))
      m -= 32
  mask = ''.join(map(lambda x: struct.pack('!I', x), t))
  return mask

def in6_getnsma(a): # return link-local solicited-node multicast address for given address
    r = in6_and(a, socket.inet_pton(socket.AF_INET6, '::ff:ffff'))
    r = in6_or(socket.inet_pton(socket.AF_INET6, 'ff02::1:ff00:0'), r)
    return r

def in6_getnsmac(a): # return multicast Ethernet address associated with multicast v6 destination
    a = struct.unpack('16B', a)[-4:]
    mac = '33:33:'
    mac += ':'.join(map(lambda x: '%.2x' %x, a))
    return mac

def in6_getha(a): # TODO : What does it do ?  RFC 3775
    r = in6_and(socket.inet_pton(socket.AF_INET6, a), in6_cidr2mask(64)) 
    r = in6_or(r, socket.inet_pton(socket.AF_INET6, '::fdff:ffff:ffff:fffe'))
    return socket.inet_ntop(socket.AF_INET6, r)

def in6_ptop(str): 
    """
    Normalizes IPv6 addresses provided in printable format, returning the 
    same address in printable format. (2001:0db8:0:0::1 -> 2001:db8::1)
    """
    return socket.inet_ntop(socket.AF_INET6, socket.inet_pton(socket.AF_INET6, str))

def in6_isincluded(addr, prefix, plen):
    """
    Returns True when 'addr' belongs to prefix/plen. False otherwise.
    """
    temp = socket.inet_pton(socket.AF_INET6, addr)
    pref = in6_cidr2mask(plen)
    zero = socket.inet_pton(socket.AF_INET6, prefix)
    return zero == in6_and(temp, pref)

def in6_isdocaddr(str):
    """
    Returns True if provided address in printable format belongs to
    2001:db8::/32 address space reserved for documentation (as defined 
    in RFC 3849).
    """
    return in6_isincluded(str, '2001:db8::', 32)

def in6_islladdr(str):
    """
    Returns True if provided address in printable format belongs to
    _allocated_ link-local unicast address space (fe80::/10)
    """
    return in6_isincluded(str, 'fe80::', 10)

def in6_issladdr(str):
    """
    Returns True if provided address in printable format belongs to
    _allocated_ site-local address space (fec0::/10). This prefix has 
    been deprecated, address being now reserved by IANA. Function 
    will remain for historic reasons.
    """
    return in6_isincluded(str, 'fec0::', 10)

def in6_isuladdr(str):
    """
    Returns True if provided address in printable format belongs to
    Unique local address space (fc00::/7).
    """
    return in6_isincluded(str, 'fc::', 7)

# TODO : we should see the status of Unique Local addresses against
#        global address space.
#        Up-to-date information is available through RFC 3587. 
#        We should review function behavior based on its content.
def in6_isgladdr(str):
    """
    Returns True if provided address in printable format belongs to
    _allocated_ global address space (2000::/3). Please note that,
    Unique Local addresses (FC00::/7) are not part of global address
    space, and won't match.
    """
    return in6_isincluded(str, '2000::', 3)

def in6_ismaddr(str):
    """
    Returns True if provided address in printable format belongs to 
    allocated Multicast address space (ff00::/8).
    """
    return in6_isincluded(str, 'ff00::', 8)

def in6_ismnladdr(str):
    """
    Returns True if address belongs to node-local multicast address
    space (ff01::/16) as defined in RFC 
    """
    return in6_isincluded(str, 'ff01::', 16)

def in6_ismgladdr(str):
    """
    Returns True if address belongs to global multicast address
    space (ff0e::/16).
    """
    return in6_isincluded(str, 'ff0e::', 16)

def in6_ismlladdr(str):
    """
    Returns True if address balongs to link-local multicast address
    space (ff02::/16)
    """
    return in6_isincluded(str, 'ff02::', 16)

# return True if address belongs to site local multicast (ff05::/16).
def in6_ismsladdr(str):
    """
    Returns True if address belongs to site-local multicast address
    space (ff05::/16). Site local address space has been deprecated.
    Function remains for historic reasons.
    """
    return in6_isincluded(str, 'ff05::', 16)

def in6_isaddrllallnodes(str):
    """
    Returns True if address is the link-local all-nodes multicast 
    address (ff02::1). 
    """
    return (socket.inet_pton(socket.AF_INET6, "ff02::1") ==
            socket.inet_pton(socket.AF_INET6, str))

def in6_isaddrllallservers(str):
    """
    Returns True if address is the link-local all-servers multicast 
    address (ff02::2). 
    """
    return (socket.inet_pton(socket.AF_INET6, "ff02::2") ==
            socket.inet_pton(socket.AF_INET6, str))



#############################################################################
#############################################################################
###                              IPv6 Class                               ###
#############################################################################
#############################################################################

class IP6Field(Field):
    def __init__(self, name, default):
        Field.__init__(self, name, default, "16s")
    def h2i(self, pkt, x):
        if type(x) is str:
            try:
		x = in6_ptop(x)
            except socket.error:
                x = Net6(x)
        elif type(x) is list:
            x = map(Net6, x)
        return x
    def i2m(self, pkt, x):
        return socket.inet_pton(socket.AF_INET6, x)
    def m2i(self, pkt, x):
        return socket.inet_ntop(socket.AF_INET6, x)
    def any2i(self, pkt, x):
        return self.h2i(pkt,x)
    def i2repr(self, pkt, x):
        if x is None:
	    return self.i2h(pkt,x)
	elif not isinstance(x, Net6) and not type(x) is list:
	    if in6_isaddrTeredo(x):   # print Teredo info
		server, flag, maddr, mport = teredoAddrExtractInfo(x)     
		return "%s [Teredo srv: %s cli: %s:%s]" % (self.i2h(pkt, x), server, maddr,mport)
	    elif in6_isaddr6to4(x):   # print encapsulated address
		addr = socket.inet_pton(socket.AF_INET6, x)
		vaddr = socket.inet_ntop(socket.AF_INET, addr[2:6])
		return "%s [6to4 GW: %s]" % (self.i2h(pkt, x), vaddr)
	return self.i2h(pkt, x)       # No specific information to return

class SourceIP6Field(IP6Field):
    def __init__(self, name, dstname):
        IP6Field.__init__(self, name, None)
        self.dstname = dstname
    def i2m(self, pkt, x):
        if x is None:
            dst=getattr(pkt,self.dstname)
            iff,x,nh = conf.route6.route(dst)
        return IP6Field.i2m(self, pkt, x)
    def i2h(self, pkt, x):
        if x is None:
            dst=getattr(pkt,self.dstname)
            if isinstance(dst,Gen):
                r = map(conf.route6.route, dst)
                r.sort()
                if r[0] == r[-1]:
                    x=r[0][1]
                else:
                    warning("More than one possible route for %s"%repr(dst))
                    return None
            else:
		iff,x,nh = conf.route6.route(dst)
        return IP6Field.i2h(self, pkt, x)

ipv6nh = { 0:"Hop-by-Hop Option Header",
           4:"IP",
           6:"TCP",
          17:"UDP",
          41:"IPv6",
          43:"Routing Header",
          44:"Fragment Header",
          47:"GRE",
          50:"ESP Header",
          51:"AH Header",
          58:"ICMPv6",
          59:"No Next Header",
          60:"Destination Option Header",
         135:"Mobility Header"} 

ipv6nhcls = {  0: "IPv6ExtHdrHopByHop",
               4: "IP",
               6: "TCP",
               17: "UDP",
               43: "IPv6ExtHdrRouting",
               44: "IPv6ExtHdrFragment",
              #50: "IPv6ExtHrESP",
              #51: "IPv6ExtHdrAH",
	       58: "ICMPv6Unknown", 
               59: "Raw",
               60: "IPv6ExtHdrDestOpt" }

class IP6ListField(StrField):
    islist = 1
    def i2repr(self,pkt,x):
        s = []
	if x == None:
	    return "[]"
	for y in x:
	    s.append('%s' % y)
        return "[ %s ]" % (", ".join(s))
        
    def getfield(self, pkt, s):
    	return "", self.m2i(pkt, s)
	
    def m2i(self, pkt, x):
        r = []
	while len(x) != 0:
            r.append(socket.inet_ntop(socket.AF_INET6, x[:16]))
            x = x[16:]
	return r

    def i2m(self, pkt, x):
	s = ''
        for y in x:
            try:
                y = socket.inet_pton(socket.AF_INET6, y)
            except:
                y = socket.getaddrinfo(y, None, socket.AF_INET6)[0][-1][0]
                y = socket.inet_pton(socket.AF_INET6, y)
            s += y
	return s      

class _IPv6GuessPayload:	
    name = "Dummy class that implements guess_payload_class() for IPv6"
    def default_payload_class(self,p):
        if self.nh == 58:
            if len(p) > 2:
                type = ord(p[0])
                if type == 139: # Node Info Query specific stuff
                    code = ord(p[1])
                    if code == 0:
                        return ICMPv6NIQueryIPv6
                    elif code == 1:
                        return ICMPv6NIQueryName
                    elif code == 2:
                        return ICMPv6NIQueryIPv4
                    return Raw
                elif type == 140: # Node Info Reply specific stuff
                    code = ord(p[1])
                    if code == 0:
                        if len(p) > 6:
			    qtype, = struct.unpack("!H", p[4:6])
                            return { 2: ICMPv6NIReplyName,
                                     3: ICMPv6NIReplyIPv6,
                                     4: ICMPv6NIReplyIPv4 }.get(qtype, ICMPv6NIReplyNOOP)
                    elif code == 1:
                        return ICMPv6NIReplyRefuse
                    elif code == 2:
                        return ICMPv6NIReplyUnknown
                    return Raw
		return get_cls(icmp6typescls.get(type,"Raw"), "Raw")
	elif self.nh == 60:
            if len(p) > 6:
                return IPv6ExtHdrDestOpt
	    return Raw
	elif self.nh == 135:    
	    if len(p) > 3:	    
		mhtype = ord(p[2])
            if mhtype == 5:
		return IPv6MobHdrBU
	    elif mhtype == 6:
		return IPv6MobHdrBA
	    elif mhtype == 7:
		return IPv6MobHdrBE
	    else:
		return Raw
	else:
	    return get_cls(ipv6nhcls.get(self.nh,"Raw"), "Raw")

class IPv6(_IPv6GuessPayload, Packet, IPTools):
    name = "IPv6"
    fields_desc = [ BitField("version" , 6 , 4),
                    BitField("tc", 0, 8), #TODO: IPv6, ByteField ?
		    BitField("fl", 0, 20),
		    ShortField("plen", None),
                    ByteEnumField("nh", 59, ipv6nh),
                    ByteField("hlim", 64),
                    SourceIP6Field("src", "dst"), # dst is for src @ selection
                    IP6Field("dst", "::1") ]
    def mysummary(self):
        return "%s > %s (%i)" % (self.src,self.dst, self.nh)

    def post_build(self, p, pay):
	p += pay
        if self.plen is None:
            l = len(p) - 40
            p = p[:4]+struct.pack("!H", l)+p[6:]
        return p

    def extract_padding(self, s):
        l = self.plen
        return s[:l], s[l:]

    def hashret(self):
        if self.nh == 58 and isinstance(self.payload, _ICMPv6):
            if self.payload.type < 128:
                return self.payload.payload.hashret()
            elif (self.payload.type in [133,134,135,136,144,145]):
                return struct.pack("B", self.nh)+self.payload.hashret()

	nh = self.nh
	sd = self.dst
	ss = self.src
        if self.nh == 43 and isinstance(self.payload, IPv6ExtHdrRouting):
	    # With routing header, the destination is the last 
	    # address of the IPv6 list if segleft > 0 
	    nh = self.payload.nh
	    try:
	    	sd = self.addresses[-1]
	    except IndexError:
	    	sd = '::1'
	    # TODO: big bug with ICMPv6 error messages as the destination of IPerror6
	    #       could be anything from the original list ...
	    if 1:
		sd = socket.inet_pton(socket.AF_INET6, sd)
		for a in self.addresses:
		    a = socket.inet_pton(socket.AF_INET6, a)
		    sd = strxor(sd, a)
		sd = socket.inet_ntop(socket.AF_INET6, sd)

        if self.nh == 44 and isinstance(self.payload, IPv6ExtHdrFragment):
            nh = self.payload.nh 

        if self.nh == 0 and isinstance(self.payload, IPv6ExtHdrHopByHop):
            nh = self.payload.nh 

        if self.nh == 60 and isinstance(self.payload, IPv6ExtHdrDestOpt):
            foundhao = None
            for o in self.payload.options:
                if isinstance(o, HAO):
                    foundhao = o
            if foundhao:
                nh = self.payload.nh # XXX what if another extension follows ?
                ss = foundhao.hoa

        if conf.checkIPsrc and conf.checkIPaddr:
            sd = socket.inet_pton(socket.AF_INET6, sd)
            ss = socket.inet_pton(socket.AF_INET6, self.src)
            return struct.pack("B",nh)+self.payload.hashret()
        else:
            return struct.pack("B", nh)+self.payload.hashret()

    def answers(self, other):
        if not isinstance(other, IPv6): # self is reply, other is request
            return False
        if conf.checkIPaddr: 
            ss = socket.inet_pton(socket.AF_INET6, self.src)
            sd = socket.inet_pton(socket.AF_INET6, self.dst)
            os = socket.inet_pton(socket.AF_INET6, other.src)
            od = socket.inet_pton(socket.AF_INET6, other.dst)
	    # request was sent to a multicast address (other.dst)
            # Check reply destination addr matches request source addr (i.e 
            # sd == os) except when reply is multicasted too
            # XXX test mcast scope matching ?
            if in6_ismaddr(other.dst):
                if in6_ismaddr(self.dst):
                    if ((od == sd) or 
                        (in6_isaddrllallnodes(self.dst) and in6_isaddrllallservers(other.dst))):
                         return self.payload.answers(other.payload)
                    return False
                if (os == sd): 
                    return self.payload.answers(other.payload)
                return False
            elif (sd != os): # or ss != od): <- removed for ICMP errors 
                return False
        if self.nh == 58 and isinstance(self.payload, _ICMPv6) and self.payload.type < 128:
            # ICMPv6 Error message -> generated by IPv6 packet
            # Note : at the moment, we jump the ICMPv6 specific class
            # to call answers() method of erroneous packet (over
            # initial packet). There can be cases where an ICMPv6 error
            # class could implement a specific answers method that perform
            # a specific task. Currently, don't see any use ...
            return self.payload.payload.answers(other)
        elif other.nh == 0 and isinstance(other.payload, IPv6ExtHdrHopByHop):
            return self.payload.answers(other.payload.payload) 
        elif other.nh == 44 and isinstance(other.payload, IPv6ExtHdrFragment):
            return self.payload.answers(other.payload.payload) 
        elif other.nh == 43 and isinstance(other.payload, IPv6ExtHdrRouting):
            return self.payload.answers(other.payload.payload) # Buggy if self.payload is a IPv6ExtHdrRouting
        elif other.nh == 60 and isinstance(other.payload, IPv6ExtHdrDestOpt):
            return self.payload.payload.answers(other.payload.payload)
        else:
            if (self.nh != other.nh):
                return False
            return self.payload.answers(other.payload)

import scapy 
scapy.IPv6 = IPv6

class IPerror6(IPv6):
    name = "IPv6 in ICMPv6"
    def answers(self, other):
        if not isinstance(other, IPv6):
            return False
	sd = socket.inet_pton(socket.AF_INET6, self.dst)
	ss = socket.inet_pton(socket.AF_INET6, self.src)
	od = socket.inet_pton(socket.AF_INET6, other.dst)
	os = socket.inet_pton(socket.AF_INET6, other.src)
	# Make sure that the ICMPv6 error is related to the packet scapy sent
	if isinstance(self.underlayer, _ICMPv6) and self.underlayer.type < 128:
	    #if sd == od:
	    if ss == os and sd == od:
		return self.payload.answers(other.payload)
	    #else:
	    #	return 0
	if not conf.checkIPsrc or sd != od:
	    if ss != os and self.nh != other.nh:
		return False
        return self.payload.answers(other.payload)
    def mysummary(self):
        return Packet.mysummary(self)


#############################################################################
#############################################################################
###                 Upper Layer Checksum computation                      ###
#############################################################################
#############################################################################

class PseudoIPv6(Packet): # IPv6 Pseudo-header for checksum computation
    name = "Pseudo IPv6 Header"
    fields_desc = [ IP6Field("src", "::"),
                    IP6Field("dst", "::"),
		    ShortField("uplen", None),
                    BitField("zero", 0, 24),
                    ByteField("nh", 0) ]  

def in6_chksum(nh, u, p):
    """
    Performs IPv6 Upper Layer checksum computation. Provided parameters are:

    - 'nh' : value of upper layer protocol 
    - 'u'  : upper layer instance (TCP, UDP, ICMPv6*, ). Instance must be 
             provided with all under layers (IPv6 and all extension headers, 
             for example)
    - 'p'  : the payload of the upper layer provided as a string

    Functions operate by filling a pseudo header class instance (PseudoIPv6)
    with
    - Next Header value
    - the address of _final_ destination (if some Routing Header with non
    segleft field is present in underlayer classes, last address is used.)
    - the address of _real_ source (basically the source address of an 
    IPv6 class instance available in the underlayer or the source address
    in HAO option if some Destination Option header found in underlayer
    includes this option).
    - the length is the length of provided payload string ('p')
    """

    ph6 = PseudoIPv6()
    ph6.nh = nh
    rthdr = 0
    hahdr = 0
    final_dest_addr_found = 0
    while u != None and not isinstance(u, IPv6):
	if (isinstance(u, IPv6ExtHdrRouting) and
	    u.segleft != 0 and len(u.addresses) != 0 and
            final_dest_addr_found == 0):
	    rthdr = u.addresses[-1]
            final_dest_addr_found = 1
	elif (isinstance(u, IPv6ExtHdrDestOpt) and (len(u.options) == 1) and
             isinstance(u.options[0], HAO)):
             hahdr  = u.options[0].hoa
	u = u.underlayer
    if u is None:  
	warning("No IPv6 underlayer to compute checksum. Leaving null.")
	return 0
    if hahdr:	
	ph6.src = hahdr
    else:
        ph6.src = u.src
    if rthdr:
	ph6.dst = rthdr
    else:
	ph6.dst = u.dst
    ph6.uplen = len(p)
    ph6s = str(ph6)
    return checksum(ph6s+p)


#############################################################################
#############################################################################
###                         Extension Headers                             ###
#############################################################################
#############################################################################


# Inherited by all extension header classes 
class _IPv6ExtHdr(_IPv6GuessPayload, Packet):
    name = 'Abstract IPV6 Option Header'
    aliastypes = [IPv6, IPerror6] # TODO ...

import scapy
scapy._IPv6OptionHeader = _IPv6ExtHdr


#################### IPv6 options for Extension Headers #####################

_hbhopts = { 0x00: "Pad1",
             0x01: "PadN",
             0x05: "Router Alert",
             0xc2: "Jumbo Payload",
             0xc9: "Home Address Option" }

class _OTypeField(ByteEnumField):
    """ 
    Modified BytEnumField that displays information regarding the IPv6 option
    based on its option type value (What should be done by nodes that process
    the option if they do not understand it ...)

    It is used by Jumbo, Pad1, PadN, RouterAlert, HAO options 
    """
    pol = {0x00: "00: skip",
           0x40: "01: discard",
           0x80: "10: discard+ICMP",
           0xC0: "11: discard+ICMP not mcast"}
    
    enroutechange = {0x00: "0: Don't change en-route",
                 0x20: "1: May change en-route" }

    def i2repr(self, pkt, x):
        s = self.i2s.get(x, repr(x))
        polstr = self.pol[(x & 0xC0)]
        enroutechangestr = self.enroutechange[(x & 0x20)]
        return "%s [%s, %s]" % (s, polstr, enroutechangestr)

class HBHOptUnknown(Packet): # IPv6 Hop-By-Hop Option
    name = "Scapy6 Unknown Option"
    fields_desc = [_OTypeField("otype", 0x01, _hbhopts), 
                   FieldLenField("optlen", None, "optdata", fmt="B"),
                   StrLenField("optdata", "", "optlen") ]    
    def alignment(self, curpos): # By default, no alignment requirement
        """
        As specified in section 4.2 of RFC 2460, every options has 
        an alignment requirement ususally expressed xn+y, meaning 
        the Option Type must appear at an integer multiple of x octest 
        from the start of the header, plus y octet.
        
        That function is provided the current position from the
        start of the header and returns required padding length.
        """
        return 0

class Pad1(Packet): # IPv6 Hop-By-Hop Option
    name = "Pad1"
    fields_desc = [ _OTypeField("otype", 0x00, _hbhopts) ]
    
    
    def alignment_delta(self, curpos): # No alignment requirement
        return 0

class PadN(Packet): # IPv6 Hop-By-Hop Option
    name = "PadN" 
    fields_desc = [_OTypeField("otype", 0x01, _hbhopts),
                   FieldLenField("optlen", None, "optdata", fmt="B"),
                   StrLenField("optdata", "", "optlen")]
    def alignment_delta(self, curpos): # No alignment requirement
        return 0

class RouterAlert(Packet): # RFC 2711 - IPv6 Hop-By-Hop Option
    name = "Router Alert"
    fields_desc = [_OTypeField("otype", 0x05, _hbhopts),
                   ByteField("optlen", 2), 
                   ShortEnumField("value", None, 
                                  { 0: "Datagram contains a MLD message", 
                                    1: "Datagram contains RSVP message",
                                    2: "Datagram contains an Active Network message" }) ]
    # TODO : Check IANA has not defined new values for value field of RouterAlertOption
    # TODO : now that we have that option, we should do something in MLD class that need it
    def alignment_delta(self, curpos): # alignment requirement : 2n+0
        x = 2 ; y = 0
        delta = x*((curpos - y + x - 1)/x) + y - curpos 
        return delta

class Jumbo(Packet): # IPv6 Hop-By-Hop Option
    name = "Jumbo Payload" 
    fields_desc = [_OTypeField("otype", 0xC2, _hbhopts),
                   ByteField("optlen", 4),
                   IntField("jumboplen", None) ]
    def alignment_delta(self, curpos): # alignment requirement : 4n+2
        x = 4 ; y = 2
        delta = x*((curpos - y + x - 1)/x) + y - curpos 
        return delta

class HAO(Packet): # IPv6 Destination Options Header Option
    name = "Home Address Option"
    fields_desc = [_OTypeField("otype", 0xC9, _hbhopts),
                   ByteField("optlen", 16),
                   IP6Field("hoa", "::") ]
    def alignment_delta(self, curpos): # alignment requirement : 8n+6
        x = 8 ; y = 6
        delta = x*((curpos - y + x - 1)/x) + y - curpos 
        return delta


_hbhoptcls = { 0x00: Pad1,
               0x01: PadN,
               0x05: RouterAlert,
               0xC2: Jumbo,
               0xC9: HAO }


######################## Hop-by-Hop Extension Header ########################

class _HopByHopOptionsField(PacketListField):
    islist = 1
    holds_packet = 1
    def getfield(self, pkt, s):
	l = 8*(getattr(pkt, self.fld) + 1)
        l -= self.shift
        return s[l:],self.m2i(pkt, s[:l])
        
    def i2len(self, pkt, i):
        l = (len(self.i2m(pkt, i)) + self.shift + 7)/8 - 1
        return l

    def m2i(self, pkt, x):
        opt = []
        while x:
            o = ord(x[0]) # Option type
            cls = self.cls
            if _hbhoptcls.has_key(o):
                cls = _hbhoptcls[o]
            try:
                op = cls(x)
            except:
                op = self.cls(x)
            opt.append(op)
            if isinstance(op.payload, Raw):
                x = op.payload.load
                del(op.payload)
            else:
                x = ""
	return opt

    def i2m(self, pkt, x):
        autopad = None
        try:
            autopad = getattr(pkt, "autopad") # Hack : 'autopad' phantom field
        except:
            autopad = 1
            
        if not autopad:
            return "".join(map(str, x))

        curpos = self.shift
        s = ""
        for p in x:
            d = p.alignment_delta(curpos)
            curpos += d
            if d == 1:
                s += str(Pad1())
            elif d != 0:
                s += str(PadN(optdata='\x00'*(d-2)))
            pstr = str(p)
            curpos += len(pstr)
            s += pstr
            
        # Let's make the class including our option field
        # a multiple of 8 octets long
        d = curpos % 8
        if d == 0:
            return s
        d = 8 - d
        if d == 1:
            s += str(Pad1())
        elif d != 0:
            s += str(PadN(optdata='\x00'*(d-2)))        

        return s

    def addfield(self, pkt, s, val):
        return s+self.i2m(pkt, val)

class _PhantomAutoPadField(ByteField):
    def addfield(self, pkt, s, val):
        return s

    def getfield(self, pkt, s):
        return s, 1

    def i2repr(self, pkt, x):
        if x:
            return "On"
        return "Off"


class IPv6ExtHdrHopByHop(_IPv6ExtHdr):    
    name = "IPv6 Extension Header - Hop-by-Hop Options Header"
    fields_desc = [ ByteEnumField("nh", 59, ipv6nh),
                    FieldLenField("len", None, "options", "B"), 
                    _PhantomAutoPadField("autopad", 1), # autopad activated by default
		    _HopByHopOptionsField("options", [], HBHOptUnknown, "len", shift=2) ]
    overload_fields = {IPv6: { "nh": 0 }}


######################## Destination Option Header ##########################

class IPv6ExtHdrDestOpt(_IPv6ExtHdr):    
    name = "IPv6 Extension Header - Destination Options Header"
    fields_desc = [ ByteEnumField("nh", 59, ipv6nh),
                    FieldLenField("len", None, "options", "B"), 
                    _PhantomAutoPadField("autopad", 1), # autopad activated by default
		    _HopByHopOptionsField("options", [], HBHOptUnknown, "len", shift=2) ]
    overload_fields = {IPv6: { "nh": 60 }}


############################# Routing Header ################################

# XXX : Uses "len" field of the class including it in its fields_desc
#       length field name should be made explicit
class IP6RoutingHeaderListField(IP6ListField): 
    islist=1
    def getfield(self, pkt, s):
        l = 8*getattr(pkt, "len")
        return s[l:], self.m2i(pkt, s[:l])

    def i2len(self, pkt, x):
        if x is None:
            return 0
        else:
            return 2*len(pkt.addresses)

class IPv6ExtHdrRouting(_IPv6ExtHdr):
    name = "IPv6 Option Header Routing"
    fields_desc = [ ByteEnumField("nh", 59, ipv6nh),
                    FieldLenField("len", None, "addresses", "B"),
                    ByteField("type", 0),
                    ByteField("segleft", None),
                    BitField("reserved", 0, 32), # There is meaning in this field ...
		    IP6RoutingHeaderListField("addresses", []) ]
    overload_fields = {IPv6: { "nh": 43 }}

    def post_build(self, pkt, pay):
        if self.segleft is None:
            pkt = pkt[:3]+struct.pack("B", len(self.addresses))+pkt[4:]
        return _IPv6ExtHdr.post_build(self, pkt, pay)


########################### Fragmentation Header ############################

class IPv6ExtHdrFragment(_IPv6ExtHdr):		  
    name = "IPv6 Extension Header - Fragmentation header"
    fields_desc = [ ByteEnumField("nh", 59, ipv6nh),
                    BitField("res1", 0, 8),
		    BitField("offset", 0, 13),
		    BitField("res2", 0, 2),
		    BitField("m", 0, 1),
		    IntField("id", None) ]
    overload_fields = {IPv6: { "nh": 44 }}


def defragment6(pktlist):
    """
    Performs defragmentation of a list of IPv6 packets. Packets are reordered.
    Crap is dropped. What lacks is completed by 'X' characters.
    """
    
    l = filter(lambda x: IPv6ExtHdrFragment in x, pktlist) # remove non fragments
    if not l:
        return []

    id = l[0][IPv6ExtHdrFragment].id 

    llen = len(l)
    l = filter(lambda x: x[IPv6ExtHdrFragment].id == id, l)
    if len(l) != llen:
        warning("defragment6: some fragmented packets have been removed from list")
    llen = len(l)

    # reorder fragments 
    i = 0 
    res = []
    while l:
        min_pos = 0
        min_offset  = l[0][IPv6ExtHdrFragment].offset
        for p in l:
            cur_offset = p[IPv6ExtHdrFragment].offset
            if cur_offset < min_offset:
                min_pos = 0
                min_offset  = cur_offset
        res.append(l[min_pos])
        del(l[min_pos])

    # regenerate the fragmentable part
    fragmentable = ""
    for p in res:
        q=p[IPv6ExtHdrFragment]
        offset = 8*q.offset
        if offset != len(fragmentable):
            warning("Expected an offset of %d. Found %d. Padding with XXXX" % (len(fragmentable), offset))
        fragmentable += "X"*(offset - len(fragmentable))
        fragmentable += str(q.payload)

    # Regenerate the unfragmentable part.
    q = res[0]
    nh = q[IPv6ExtHdrFragment].nh
    q[IPv6ExtHdrFragment].underlayer.nh = nh
    q[IPv6ExtHdrFragment].underlayer.payload = None
    q /= Raw(load=fragmentable)
    
    return IPv6(str(q))


def fragment6(pkt, fragSize):
    """
    Performs fragmentation of an IPv6 packet. Provided packet ('pkt') must already 
    contain an IPv6ExtHdrFragment() class. 'fragSize' argument is the expected
    maximum size of fragments (MTU). The list of packets is returned.

    If packet does not contain an IPv6OPtionHeaderFragment class, it is returned in
    result list.
    """

    pkt = pkt.copy()
    s = str(pkt) # for instantiation to get upper layer checksum right

    if len(s) <= fragSize:
        return [pkt]

    if not IPv6ExtHdrFragment in pkt:
        # TODO : automatically add a fragment before upper Layer
        #        at the moment, we do nothing and return initial packet
        #        as single element of a list
        return [pkt]

    # Fragmentable part : fake IPv6 for Fragmentable part length computation
    fragPart = pkt[IPv6ExtHdrFragment].payload
    tmp = str(IPv6(src="::1", dst="::1")/fragPart)
    fragPartLen = len(tmp) - 40  # basic IPv6 header length
    fragPartStr = s[-fragPartLen:]

    # Grab Next Header for use in Fragment Header
    nh = IPv6(tmp[:40]).nh

    # Keep fragment header
    fragHeader = pkt[IPv6ExtHdrFragment]
    fragHeader.payload = None # detach payload

    # Unfragmentable Part
    unfragPartLen = len(s) - fragPartLen - 8
    unfragPart = pkt
    pkt[IPv6ExtHdrFragment].underlayer.payload = None # detach payload

    # Cut the fragmentable part to fit fragSize. Inner fragments have 
    # a length that is an integer multiple of 8 octets. last Frag MTU
    # can be anything below MTU
    lastFragSize = fragSize - unfragPartLen - 8
    innerFragSize = lastFragSize - (lastFragSize % 8)
    
    if lastFragSize <= 0 or innerFragSize == 0:
        warning("Provided fragment size value is too low. " + 
                "Should be more than %d" % (unfragPartLen + 8))
        return [unfragPart/fragHeader/fragPart]

    remain = fragPartStr
    res = []
    fragOffset = 0     # offset, incremeted during creation
    fragId = random.randint(0,0xffffffff) # random id ...
    if fragHeader.id is not None:  # ... except id provided by user
        fragId = fragHeader.id
    fragHeader.m = 1
    fragHeader.id = fragId
    fragHeader.nh = nh

    # Main loop : cut, fit to FRAGSIZEs, fragOffset, Id ...
    while True:
        if (len(remain) > lastFragSize):
            tmp = remain[:innerFragSize] 
            remain = remain[innerFragSize:]
            fragHeader.offset = fragOffset    # update offset
            fragOffset += (innerFragSize / 8)  # compute new one
            if IPv6 in unfragPart:  
                unfragPart[IPv6].plen = None
            tempo = unfragPart/fragHeader/Raw(load=tmp)
            res.append(tempo)
        else:
            fragHeader.offset = fragOffset    # update offSet
            fragHeader.m = 0
            if IPv6 in unfragPart:
                unfragPart[IPv6].plen = None
            tempo = unfragPart/fragHeader/Raw(load=remain)
            res.append(tempo)
            break
    return res


############################### AH Header ###################################

# class _AHFieldLenField(FieldLenField):
#     def getfield(self, pkt, s):
#         l = getattr(pkt, self.fld)
#         l = (l*8)-self.shift
#         i = self.m2i(pkt, s[:l])
#         return s[l:],i        

# class _AHICVStrLenField(StrLenField):
#     def i2len(self, pkt, x):
      


# class IPv6ExtHdrAH(_IPv6ExtHdr):
#     name = "IPv6 Extension Header - AH"
#     fields_desc = [ ByteEnumField("nh", 59, ipv6nh),
#                     _AHFieldLenField("len", None, "icv"),
#                     ShortField("res", 0),
#                     IntField("spi", 0),
#                     IntField("sn", 0),
#                     _AHICVStrLenField("icv", None, "len", shift=2) ]
#     overload_fields = {IPv6: { "nh": 51 }}

#     def post_build(self, pkt, pay):
#         if self.len is None:
#             pkt = pkt[0]+struct.pack("!B", 2*len(self.addresses))+pkt[2:]
#         if self.segleft is None:
#             pkt = pkt[:3]+struct.pack("!B", len(self.addresses))+pkt[4:]
#         return _IPv6ExtHdr.post_build(self, pkt, pay)


############################### ESP Header ##################################

# class IPv6ExtHdrESP(_IPv6extHdr):
#     name = "IPv6 Extension Header - ESP"
#     fields_desc = [ IntField("spi", 0),
#                     IntField("sn", 0),
#                     # there is things to extract from IKE work 
#                     ]
#     overloads_fields = {IPv6: { "nh": 50 }}

    

#############################################################################
#############################################################################
###                           ICMPv6* Classes                             ###
#############################################################################
#############################################################################

icmp6typescls = {    1: "ICMPv6DestUnreach",
                     2: "ICMPv6PacketTooBig",
                     3: "ICMPv6TimeExceeded",
                     4: "ICMPv6ParamProblem",
                   128: "ICMPv6EchoRequest",
                   129: "ICMPv6EchoReply",
                   130: "ICMPv6MLQuery", 
                   131: "ICMPv6MLReport",
                   132: "ICMPv6MLDone",
                   133: "ICMPv6ND_RS",
                   134: "ICMPv6ND_RA",
                   135: "ICMPv6ND_NS",
                   136: "ICMPv6ND_NA",
                   137: "ICMPv6ND_Redirect",
                  #138: Do Me - RFC 2894 - Seems painful
                   139: "ICMPv6NIQuery",
                   140: "ICMPv6NIReply",
                   141: "ICMPv6ND_INDSol",
                   142: "ICMPv6ND_INDAdv",
                  #143: Do Me - RFC 3810
		   144: "ICMPv6HAADRequest", 
		   145: "ICMPv6HAADReply",
		   146: "ICMPv6MPSol",
		   147: "ICMPv6MPAdv",
                  #148: Do Me - SEND related - RFC 3971
                  #149: Do Me - SEND related - RFC 3971
                   151: "ICMPv6MRD_Advertisement",
                   152: "ICMPv6MRD_Solicitation",
                   153: "ICMPv6MRD_Termination",
		   }

icmp6types = { 1 : "Destination unreachable",  
               2 : "Packet too big", 
	       3 : "Time exceeded",
               4 : "Parameter problem",
             100 : "Private Experimentation",
             101 : "Private Experimentation",
             128 : "Echo Request",
             129 : "Echo Reply",
             130 : "MLD Query",
	     131 : "MLD Report",
	     132 : "MLD Done",
	     133 : "Router Solicitation",
	     134 : "Router Advertisement",
	     135 : "Neighbor Solicitation",
	     136 : "Neighbor Advertisement",
	     137 : "Redirect Message",
	     138 : "Router Renumbering",
	     139 : "ICMP Node Information Query", 	 
	     140 : "ICMP Node Information Response", 	 
	     141 : "Inverse Neighbor Discovery Solicitation Message",
	     142 : "Inverse Neighbor Discovery Advertisement Message",
	     143 : "Version 2 Multicast Listener Report",
	     144 : "Home Agent Address Discovery Request Message",
	     145 : "Home Agent Address Discovery Reply Message",
	     146 : "Mobile Prefix Solicitation",
	     147 : "Mobile Prefix Advertisement",
	     148 : "Certification Path Solicitation",
	     149 : "Certification Path Advertisement",
             151 : "Multicast Router Advertisement",
             152 : "Multicast Router Solicitation",
             153 : "Multicast Router Termination",
             200 : "Private Experimentation",
             201 : "Private Experimentation" }


class _ICMPv6(Packet):
    name = "ICMPv6 dummy class"
    overload_fields = {IPv6: {"nh": 58}}
    def post_build(self, p, pay):
	p += pay
        if self.cksum == None: 
	    chksum = in6_chksum(58, self.underlayer, p)
	    p = p[:2]+struct.pack("!H", chksum)+p[4:]
	return p

    def hashret(self):
        return self.payload.hashret()
    def answers(self, other):
        # isinstance(self.underlayer, _IPv6ExtHdr) may introduce a bug ...
	if isinstance(self.underlayer, IPerror6) or isinstance(self.underlayer, _IPv6ExtHdr) and isinstance(other, _ICMPv6):
	    if not ((self.type == other.type) and
		    (self.code == other.code)):
		return 0
	    return 1
	return 0


class _ICMPv6Error(_ICMPv6):
    name = "ICMPv6 errors dummy class"
    def guess_payload_class(self,p):
	return IPerror6

class ICMPv6Unknown(_ICMPv6):
    name = "Scapy6 ICMPv6 fallback class"
    fields_desc = [ ByteEnumField("type",1, icmp6types),
                    ByteField("code",0),
                    XShortField("cksum", None),
                    StrField("msgbody", "")]    


################################## RFC 2460 #################################

class ICMPv6DestUnreach(_ICMPv6Error):
    name = "ICMPv6 Destination Unreachable"
    fields_desc = [ ByteEnumField("type",1, icmp6types),
                    ByteEnumField("code",0, { 0: "No route to destination",
                                              1: "Communication with destination administratively prohibited",
                                              2: "Beyond scope of source address",
                                              3: "Address unreachable",
                                              4: "Port unreachable" }),
                    XShortField("cksum", None),
                    XIntField("unused",0x00000000)]

class ICMPv6PacketTooBig(_ICMPv6Error):
    name = "ICMPv6 Packet Too Big"
    fields_desc = [ ByteEnumField("type",2, icmp6types),
                    ByteField("code",0),
                    XShortField("cksum", None),
                    IntField("mtu",1280)]
    
class ICMPv6TimeExceeded(_ICMPv6Error):
    name = "ICMPv6 Time Exceeded"
    fields_desc = [ ByteEnumField("type",3, icmp6types),
                    ByteField("code",{ 0: "hop limit exceeded in transit",
                                       1: "fragment reassembly time exceeded"}),
                    XShortField("cksum", None),
                    XIntField("unused",0x00000000)]

# The default pointer value is set to the next header field of 
# the encapsulated IPv6 packet
class ICMPv6ParamProblem(_ICMPv6Error): 
    name = "ICMPv6 Parameter Problem"
    fields_desc = [ ByteEnumField("type",4, icmp6types),
                    ByteEnumField("code",0, {0: "erroneous header field encountered",
                                             1: "unrecognized Next Header type encountered",
                                             2: "unrecognized IPv6 option encountered"}),
                    XShortField("cksum", None),
                    IntField("ptr",6)]

class ICMPv6EchoRequest(_ICMPv6):
    name = "ICMPv6 Echo Request"
    fields_desc = [ ByteEnumField("type", 128, icmp6types),
                    ByteField("code", 0),
                    XShortField("cksum", None),
                    XShortField("id",0),
                    XShortField("seq",0),
                    StrField("data", "")]
    def mysummary(self):
        return self.sprintf("%name% (id: %id% seq: %seq%)")
    def hashret(self):
        return struct.pack("HH",self.id,self.seq)+self.payload.hashret()

    
class ICMPv6EchoReply(ICMPv6EchoRequest):
    name = "ICMPv6 Echo Reply"
    __metaclass__ = ChangeDefaultValues
    new_default_values = { "type": 129 }
    def answers(self, other):
        # We could match data content between request and reply. 
        return (isinstance(other, ICMPv6EchoRequest) and
                self.id == other.id and self.seq == other.seq and
                self.data == other.data)


############ ICMPv6 Multicast Listener Discovery (RFC3810) ##################

# tous les messages MLD sont emis avec une adresse source lien-locale
# -> Y veiller dans le post_build si aucune n'est specifiee
# La valeur de Hop-Limit doit etre de 1
# "and an IPv6 Router Alert option in a Hop-by-Hop Options
# header. (The router alert option is necessary to cause routers to
# examine MLD messages sent to multicast addresses in which the router
# itself has no interest"  
class _ICMPv6ML(_ICMPv6):
    fields_desc = [ ByteEnumField("type", 130, icmp6types),
                    ByteField("code", 0),
                    XShortField("cksum", None),
                    ShortField("mrd", 0),
                    ShortField("reserved", 0),
                    IP6Field("mladdr",None)]

# general queries are sent to the link-scope all-nodes multicast
# address ff02::1, with a multicast address field of 0 and a MRD of
# [Query Response Interval]
# Default value for mladdr is set to 0 for a General Query, and
# overloaded by the user for a Multicast Address specific query
# TODO : See what we can do to automatically include a Router Alert
#        Option in a Destination Option Header.
class ICMPv6MLQuery(_ICMPv6ML): # RFC 2710
    name = "MLD - Multicast Listener Query"
    __metaclass__ = ChangeDefaultValues
    new_default_values = {"type": 130, "mrd":10000, "mladdr": "::"} # 10s for mrd
    overload_fields = {IPv6: { "dst": "ff02::1", "hlim": 1 }} 
    def hashret(self):
        if self.mladdr != "::":
            return struct.pack("HH",self.mladdr)+self.payload.hashret()
        else:
            return self.payload.hashret()
        
    
# TODO : See what we can do to automatically include a Router Alert
#        Option in a Destination Option Header.
class ICMPv6MLReport(_ICMPv6ML): # RFC 2710
    name = "MLD - Multicast Listener Report"
    __metaclass__ = ChangeDefaultValues
    new_default_values = {"type": 131}
    overload_fields = {IPv6: {"hlim": 1}}
    # implementer le hashret et le answers
    
# When a node ceases to listen to a multicast address on an interface,
# it SHOULD send a single Done message to the link-scope all-routers
# multicast address (FF02::2), carrying in its multicast address field
# the address to which it is ceasing to listen
# TODO : See what we can do to automatically include a Router Alert
#        Option in a Destination Option Header.
class ICMPv6MLDone(_ICMPv6ML): # RFC 2710
    name = "MLD - Multicast Listener Done"
    __metaclass__ = ChangeDefaultValues
    new_default_values = {"type": 132}
    overload_fields = {IPv6: { "dst": "ff02::2", "hlim": 1}}


########## ICMPv6 MRD - Multicast Router Discovery (RFC 4286) ###############

# TODO: 
# - 04/09/06 troglocan : find a way to automatically add a router alert
#            option for all MRD packets. This could be done in a specific
#            way when IPv6 is the under layer with some specific keyword
#            like 'exthdr'. This would allow to keep compatibility with
#            providing IPv6 fields to be overloaded in fields_desc.
# 
#            At the moment, if user inserts an IPv6 Router alert option
#            none of the IPv6 default values of IPv6 layer will be set.

class ICMPv6MRD_Advertisement(_ICMPv6):
    name = "ICMPv6 Multicast Router Discovery Advertisement"
    fields_desc = [ByteEnumField("type", 151, icmp6types),
                   ByteField("advinter", 20),
                   XShortField("cksum", None),
                   ShortField("queryint", 0),
                   ShortField("robustness", 0)]
    overload_fields = {IPv6: { "nh": 58, "hlim": 1, "dst": "ff02::2"}}
                       # IPv6 Router Alert requires manual inclusion
    def extract_padding(self, s):
        return s[:8], s[8:]

class ICMPv6MRD_Solicitation(_ICMPv6):
    name = "ICMPv6 Multicast Router Discovery Solicitation"
    fields_desc = [ByteEnumField("type", 152, icmp6types),
                   ByteField("res", 0),
                   XShortField("cksum", None) ]
    overload_fields = {IPv6: { "nh": 58, "hlim": 1, "dst": "ff02::2"}}
                       # IPv6 Router Alert requires manual inclusion
    def extract_padding(self, s):
        return s[:4], s[4:]

class ICMPv6MRD_Termination(_ICMPv6):
    name = "ICMPv6 Multicast Router Discovery Termination"
    fields_desc = [ByteEnumField("type", 153, icmp6types),
                   ByteField("res", 0),
                   XShortField("cksum", None) ]
    overload_fields = {IPv6: { "nh": 58, "hlim": 1, "dst": "ff02::6A"}}  
                       # IPv6 Router Alert requires manual inclusion
    def extract_padding(self, s):
        return s[:4], s[4:]


################### ICMPv6 Neighbor Discovery (RFC 2461) ####################

icmp6ndopts = { 1: "Source Link-Layer Address",
                2: "Target Link-Layer Address",
                3: "Prefix Information",
                4: "Redirected Header",
                5: "MTU",
                6: "NBMA Shortcut Limit Option", # RFC2491
                7: "Advertisement Interval Option",
                8: "Home Agent Information Option",
                9: "Source Address List",
               10: "Target Address List",
               11: "CGA Option",            # RFC 3971
               12: "RSA Signature Option",  # RFC 3971
               13: "Timestamp Option",      # RFC 3971
               14: "Nonce option",          # RFC 3971
               15: "Trust Anchor Option",   # RFC 3971
               16: "Certificate Option",    # RFC 3971
               17: "IP Address Option",                             # RFC 4068
               18: "New Router Prefix Information Option",          # RFC 4068
               19: "Link-layer Address Option",                     # RFC 4068
               20: "Neighbor Advertisement Acknowledgement Option", 
               21: "CARD Request Option", # RFC 4065/4066/4067
               22: "CARD Reply Option",   # RFC 4065/4066/4067
               23: "MAP Option",          # RFC 4140
               24: "Route Information Option"  # RFC 4191
                }
                  
icmp6ndoptscls = { 1: "ICMPv6NDOptSrcLLAddr",
                   2: "ICMPv6NDOptDstLLAddr",
                   3: "ICMPv6NDOptPrefixInfo",
                   4: "ICMPv6NDOptRedirectedHdr",
                   5: "ICMPv6NDOptMTU",
                   6: "ICMPv6NDOptShortcutLimit",
                   7: "ICMPv6NDOptAdvInterval",
                   8: "ICMPv6NDOptHAInfo",
                   9: "ICMPv6NDOptSrcAddrList",
                  10: "ICMPv6NDOptTgtAddrList",
                  #11: Do Me,
                  #12: Do Me,
                  #13: Do Me,
                  #14: Do Me,
                  #15: Do Me,
                  #16: Do Me,
                  17: "ICMPv6NDOptIPAddr", 
                  18: "ICMPv6NDOptNewRtrPrefix",
                  19: "ICMPv6NDOptLLA",
                  #18: Do Me,
                  #19: Do Me,
                  #20: Do Me,
                  #21: Do Me,
                  #22: Do Me,
                  23: "ICMPv6NDOptMAP",
                  24: "ICMPv6NDOptRouteInfo",
                  25: "ICMPv6NDOptRDNSS"  # temporarily, till IANA assignment
                  }

class _ICMPv6NDGuessPayload:
    name = "Dummy ND class that implements guess_payload_class()"
    def guess_payload_class(self,p):
        if len(p) > 1:
            return get_cls(icmp6ndoptscls.get(ord(p[0]),"Raw"), "Raw") # s/Raw/ICMPv6NDOptUnknown/g ?


# Beginning of ICMPv6 Neighbor Discovery Options.

class ICMPv6NDOptUnknown(_ICMPv6NDGuessPayload, Packet):
    name = "ICMPv6 Neighbor Discovery Option - Scapy Unimplemented"
    fields_desc = [ ByteField("type",None),
                    FieldLenField("len",None,"data","B"),
                    StrLenField("data","","len", shift=2) ]

# NOTE: len includes type and len field. Expressed in unit of 8 bytes
# TODO: Revoir le coup du ETHER_ANY
class ICMPv6NDOptSrcLLAddr(_ICMPv6NDGuessPayload, Packet):
    name = "ICMPv6 Neighbor Discovery Option - Source Link-Layer Address"
    fields_desc = [ ByteField("type", 1),
                    ByteField("len", 1),
                    MACField("lladdr", ETHER_ANY) ]
    def mysummary(self):			
        return self.sprintf("%name% %lladdr%")

class ICMPv6NDOptDstLLAddr(ICMPv6NDOptSrcLLAddr):
    name = "ICMPv6 Neighbor Discovery Option - Destination Link-Layer Address"
    __metaclass__ = ChangeDefaultValues
    new_default_values = { 'type': 2 }

class ICMPv6NDOptPrefixInfo(_ICMPv6NDGuessPayload, Packet):
    name = "ICMPv6 Neighbor Discovery Option - Prefix Information"
    fields_desc = [ ByteField("type",3),
                    ByteField("len",4),
                    ByteField("prefixlen",None),
                    BitField("L",1,1),
                    BitField("A",1,1),
                    BitField("R",0,1),
                    BitField("res1",0,5),
                    XIntField("validlifetime",0xffffffffL),
                    XIntField("preferredlifetime",0xffffffffL),
                    XIntField("res2",0x00000000),
                    IP6Field("prefix","::") ]
    def mysummary(self):			
        return self.sprintf("%name% %prefix%")

# TODO: We should also limit the size of included packet to something
# like (initiallen - 40 - 2)
class TruncatedPacketLenField(PacketLenField):
    def getfield(self, pkt, s):
        l = getattr(pkt, self.fld)
        l = (l*8)-self.shift
        i = self.m2i(pkt, s[:l])
        return s[l:],i
    
    def m2i(self, pkt, m):
        s = None 
        try: # It can happen we have sth shorter than 40 bytes
            s = self.cls(m)
        except:
            return Raw(m)
        return s

    def i2m(self, pkt, x):
        s = str(x)
        l = len(s)
        r = (l + self.shift) % 8
        l = l - r 
        return s[:l]

    def i2len(self, pkt, i):
        return (len(self.i2m(pkt, i)) + self.shift) / 8

        
# Faire un post_build pour le recalcul de la taille (en multiple de 8 octets)
class ICMPv6NDOptRedirectedHdr(_ICMPv6NDGuessPayload, Packet):
    name = "ICMPv6 Neighbor Discovery Option - Redirected Header"
    fields_desc = [ ByteField("type",4),
                    FieldLenField("len", None, "pkt", fmt="B"),
                    XShortField("res",0),
                    TruncatedPacketLenField("pkt", "", IPv6, "len", shift=4) ]

# Voir la valeur de MTU a utiliser par defaut au lieu du 1280
class ICMPv6NDOptMTU(_ICMPv6NDGuessPayload, Packet):
    name = "ICMPv6 Neighbor Discovery Option - MTU"
    fields_desc = [ ByteField("type",5),
                    ByteField("len",1),
                    XShortField("res",0),
                    IntField("mtu",1280)]

class ICMPv6NDOptShortcutLimit(_ICMPv6NDGuessPayload, Packet): # RFC 2491
    name = "ICMPv6 Neighbor Discovery Option - NBMA Shortcut Limit"
    fields_desc = [ ByteField("type", 6),
                    ByteField("len", 1),
                    ByteField("shortcutlim", 40), # XXX
                    ByteField("res1", 0),
                    IntField("res2", 0) ]
    
class ICMPv6NDOptAdvInterval(_ICMPv6NDGuessPayload, Packet):
    name = "ICMPv6 Neighbor Discovery - Interval Advertisement"
    fields_desc = [ ByteField("type",7),
                    ByteField("len",1),
                    ShortField("res", 0),
                    IntField("advint", 0) ]
    def mysummary(self):			
        return self.sprintf("%name% %advint% milliseconds")

class ICMPv6NDOptHAInfo(_ICMPv6NDGuessPayload, Packet):	
    name = "ICMPv6 Neighbor Discovery - Home Agent Information"
    fields_desc = [ ByteField("type",8),
                    ByteField("len",1),
                    ShortField("res", 0),
                    ShortField("pref", 0),
                    ShortField("lifetime", 1)]
    def mysummary(self):			
        return self.sprintf("%name% %pref% %lifetime% seconds")

# type 9  : See ICMPv6NDOptSrcAddrList class below in IND (RFC 3122) support

# type 10 : See ICMPv6NDOptTgtAddrList class below in IND (RFC 3122) support

class ICMPv6NDOptIPAddr(_ICMPv6NDGuessPayload, Packet):	 # RFC 4068
    name = "ICMPv6 Neighbor Discovery - IP Address Option (FH for MIPv6)"
    fields_desc = [ ByteField("type",17),
                    ByteField("len", 3),
                    ByteEnumField("optcode", 1, {1: "Old Care-Of Address",
                                                 2: "New Care-Of Address",
                                                 3: "NAR's IP address" }),
                    ByteField("plen", 64),
                    IntField("res", 0),
                    IP6Field("addr", "::") ]

class ICMPv6NDOptNewRtrPrefix(_ICMPv6NDGuessPayload, Packet): # RFC 4068
    name = "ICMPv6 Neighbor Discovery - New Router Prefix Information Option (FH for MIPv6)"
    fields_desc = [ ByteField("type",18),
                    ByteField("len", 3),
                    ByteField("optcode", 0),
                    ByteField("plen", 64),
                    IntField("res", 0),
                    IP6Field("prefix", "::") ]

_rfc4068_lla_optcode = {0: "Wildcard requesting resolution for all nearby AP",
                        1: "LLA for the new AP",
                        2: "LLA of the MN",
                        3: "LLA of the NAR",
                        4: "LLA of the src of TrSolPr or PrRtAdv msg",
                        5: "AP identified by LLA belongs to current iface of router",
                        6: "No preifx info available for AP identified by the LLA",
                        7: "No fast handovers support for AP identified by the LLA" }

class ICMPv6NDOptLLA(_ICMPv6NDGuessPayload, Packet):	 # RFC 4068
    name = "ICMPv6 Neighbor Discovery - Link-Layer Address (LLA) Option (FH for MIPv6)"
    fields_desc = [ ByteField("type", 19),
                    ByteField("len", 1),
                    ByteEnumField("optcode", 0, _rfc4068_lla_optcode),
                    MACField("lla", ETHER_ANY) ] # We only support ethernet

class ICMPv6NDOptMAP(_ICMPv6NDGuessPayload, Packet):	 # RFC 4140
    name = "ICMPv6 Neighbor Discovery - MAP Option"
    fields_desc = [ ByteField("type", 23),
                    ByteField("len", 3),
                    BitField("dist", 1, 4),
                    BitField("pref", 15, 4), # highest availability
                    BitField("R", 1, 1),
                    BitField("res", 0, 7),                    
                    IntField("validlifetime", 0xffffffff),
                    IP6Field("addr", "::") ] 

class ICMPv6NDOptRouteInfo(_ICMPv6NDGuessPayload, Packet): # RFC 4191
    name = "ICMPv6 Neighbor Discovery Option - Route Information Option"
    fields_desc = [ ByteField("type",24),
                    ByteField("len",4),
                    ByteField("plen", None),
                    BitField("res1",0,3),
                    BitField("prf",0,2),
                    BitField("res2",0,3),
                    IntField("rtlifetime", 0xffffffff),
                    IP6Field("prefix", "::")]

class DNSListField(IP6ListField):
    islist=1
    def getfield(self, pkt, s):
        l = 8*(getattr(pkt, "len")-1)
        return s[l:], self.m2i(pkt, s[:l])

    def i2len(self, pkt, x):
        if x is None:
            return 1
        else:
            return 2*len(pkt.dns) + 1
    
class ICMPv6NDOptRDNSS(_ICMPv6NDGuessPayload, Packet): # RFC 4191
    name = "ICMPv6 Neighbor Discovery Option - Recusive DNS Server Option"
    fields_desc = [ ByteField("type",25),
                    FieldLenField("len", None, "dns", "B"),
                    IntField("lifetime", 0xffffffff),
                    DNSListField("dns", [])]

# End of ICMPv6 Neighbor Discovery Options.

class ICMPv6ND_RS(_ICMPv6NDGuessPayload, _ICMPv6):
    name = "ICMPv6 Neighbor Discovery - Router Solicitation"
    fields_desc = [ ByteEnumField("type", 133, icmp6types),
                    ByteField("code",0),
                    XShortField("cksum", None),
                    IntField("res",0) ]
    overload_fields = {IPv6: { "nh": 58, "dst": "ff02::2", "hlim": 255 }}

class ICMPv6ND_RA(_ICMPv6NDGuessPayload, _ICMPv6):
    name = "ICMPv6 Neighbor Discovery - Router Advertisement"
    fields_desc = [ ByteEnumField("type", 134, icmp6types),
                    ByteField("code",0),
                    XShortField("cksum", None),
                    ByteField("chlim",0),
                    BitField("M",0,1),
                    BitField("O",0,1),
                    BitField("H",0,1),
                    BitEnumField("prf",1,2, { 0: "Medium (default)",
                                              1: "High",
                                              2: "Reserved",
                                              3: "Low" } ), # RFC 4191
                    BitField("res",0,3),
                    ShortField("routerlifetime",1800),
                    IntField("reachabletime",0),
                    IntField("retranstimer",0) ]
    overload_fields = {IPv6: { "nh": 58, "dst": "ff02::1", "hlim": 255 }}

    def answers(self, other):
        return isinstance(other, ICMPv6ND_RS)

class ICMPv6ND_NS(_ICMPv6NDGuessPayload, _ICMPv6, Packet):
    name = "ICMPv6 Neighbor Discovery - Neighbor Solicitation"
    fields_desc = [ ByteEnumField("type",135, icmp6types),
                    ByteField("code",0),
                    XShortField("cksum", None),
                    BitField("R",0,1),
                    BitField("S",0,1),
                    BitField("O",0,1),
                    XBitField("res",0,29),
                    IP6Field("tgt","::") ]
    overload_fields = {IPv6: { "nh": 58, "dst": "ff02::1", "hlim": 255 }}

    def mysummary(self):
        return self.sprintf("%name% (tgt: %tgt%)")

    def hashret(self):
        return self.tgt+self.payload.hashret() 

class ICMPv6ND_NA(ICMPv6ND_NS):
    name = "ICMPv6 Neighbor Discovery - Neighbor Advertisement"
    __metaclass__ = ChangeDefaultValues
    new_default_values = { 'type': 136, 'R': 1, 'O': 1 }

    def answers(self, other):
	return isinstance(other, ICMPv6ND_NS) and self.tgt == other.tgt

# associated possible options : target link-layer option, Redirected header
class ICMPv6ND_Redirect(_ICMPv6NDGuessPayload, _ICMPv6, Packet):
    name = "ICMPv6 Neighbor Discovery - Redirect"
    fields_desc = [ ByteEnumField("type",137, icmp6types),
                    ByteField("code",0),
                    XShortField("cksum", None),
                    XIntField("res",0),
                    IP6Field("tgt","::"),
                    IP6Field("dst","::") ]
    overload_fields = {IPv6: { "nh": 58, "dst": "ff02::1", "hlim": 255 }}



################ ICMPv6 Inverse Neighbor Discovery (RFC 3122) ###############

# Developper un field specifique pour la liste d'adresse
# Voir le calcul de la longueur en fonction du nombre d'elements
# de la liste d'adresses.
# n = (len-1)/2
class _INDIP6ListField(StrLenField):
    islist = 1
    def i2repr(self,pkt,x):
        s = []
	if x == None:
	    return "[]"
	for y in x:
	    s.append('%s' % y)
        return "[ %s ]" % (", ".join(s))
        
    def m2i(self, pkt, x):
        r = []
	while len(x) != 0:
            r.append(socket.inet_ntop(socket.AF_INET6, x[:16]))
            x = x[16:]
	return r

    def i2m(self, pkt, x):
	s = ''
        for y in x:
            try:
                y = socket.inet_pton(socket.AF_INET6, y)
            except:
                y = socket.getaddrinfo(y, None, socket.AF_INET6)[0][-1][0]
                y = socket.inet_pton(socket.AF_INET6, y)
            s += y
	return s      

    def getfield(self, pkt, s):
        l = 8*getattr(pkt, self.fld) - self.shift
        return s[l:], self.m2i(pkt,s[:l])

    def i2len(self, pkt, val):
        if val is None:
            return self.shift/8
        else:
            return 2*len(val)+(self.shift/8)

class ICMPv6NDOptSrcAddrList(_ICMPv6NDGuessPayload, Packet):
    name = "ICMPv6 Inverse Neighbor Discovery Option - Source Address List"
    fields_desc = [ ByteField("type",9),
                    FieldLenField("len", None, "addrlist", fmt="B"),
                    StrFixedLenField("res","",6),
                    _INDIP6ListField("addrlist", [], "len", shift=8) ]

class ICMPv6NDOptTgtAddrList(ICMPv6NDOptSrcAddrList):
    name = "ICMPv6 Inverse Neighbor Discovery Option - Target Address List"
    __metaclass__ = ChangeDefaultValues
    new_default_values = { "type": 10 }


# RFC3122
# Options requises : source lladdr et target lladdr
# Autres options valides : source address list, MTU
# - Comme precise dans le document, il serait bien de prendre l'adresse L2
#   demandee dans l'option requise target lladdr et l'utiliser au niveau
#   de l'adresse destination ethernet si aucune adresse n'est precisee
# - ca semble pas forcement pratique si l'utilisateur doit preciser toutes
#   les options. 
# Ether() must use the target lladdr as destination
class ICMPv6ND_INDSol(_ICMPv6NDGuessPayload, _ICMPv6):
    name = "ICMPv6 Inverse Neighbor Discovery Solicitation"
    fields_desc = [ ByteEnumField("type",141, icmp6types),
                    ByteField("code",0),
                    XShortField("cksum",None),
                    XIntField("reserved",0) ]
    overload_fields = {IPv6: { "nh": 58, "dst": "ff02::1", "hlim": 255 }}

# Options requises :  target lladdr, target address list
# Autres options valides : MTU
class ICMPv6ND_INDAdv(_ICMPv6NDGuessPayload, _ICMPv6):
    name = "ICMPv6 Inverse Neighbor Discovery Advertisement"
    fields_desc = [ ByteEnumField("type",142, icmp6types),
                    ByteField("code",0),
                    XShortField("cksum",None),
                    XIntField("reserved",0) ]
    overload_fields = {IPv6: { "nh": 58, "dst": "ff02::1", "hlim": 255 }}

#############################################################################
###                           LLMNR (RFC4795)                             ###
#############################################################################
# LLMNR is based on the DNS packet format (RFC1035 Section 4)
# RFC also envisions LLMNR over TCP. Like vista, we don't support it -- arno

_LLMNR_IPv6_mcast_Addr = "FF02:0:0:0:0:0:1:3"
_LLMNR_IPv4_mcast_addr = "224.0.0.252"

class LLMNRQuery(Packet):
    name = "Link Local Multicast Node Resolution - Query"
    fields_desc = [ ShortField("id", 0),
                    BitField("qr", 0, 1),
                    BitEnumField("opcode", 0, 4, { 0:"QUERY" }),
                    BitField("c", 0, 1),
                    BitField("tc", 0, 2),
                    BitField("z", 0, 4),
                    BitEnumField("rcode", 0, 4, { 0:"ok" }),
                    DNSRRCountField("qdcount", None, "qd"),
                    DNSRRCountField("ancount", None, "an"),
                    DNSRRCountField("nscount", None, "ns"),
                    DNSRRCountField("arcount", None, "ar"),
                    DNSQRField("qd", "qdcount"),
                    DNSRRField("an", "ancount"),
                    DNSRRField("ns", "nscount"),
                    DNSRRField("ar", "arcount",0)]
    overload_fields = {UDP: {"sport": 5355, "dport": 5355 }}
    def hashret(self):
        return struct.pack("!H", id)

class LLMNRResponse(LLMNRQuery):
    name = "Link Local Multicast Node Resolution - Response"
    __metaclass__ = ChangeDefaultValues
    new_default_values = {"qr": 1}
    fields_desc = []

    def answers(self, other):
        return (isinstance(other, LLMNRQuery) and
                self.id == other.id and
                self.qr == 1 and
                other.qr == 0)

def _llmnr_dispatcher(x, *args, **kargs):
    cls = Raw
    if len(x) >= 3:
        if (ord(x[4]) & 0x80): # Response
            cls = LLMNRResponse
        else:                  # Query
            cls = LLMNRQuery
    return cls(x)

bind_bottom_up(UDP, _llmnr_dispatcher, { "dport": 5355 })
bind_bottom_up(UDP, _llmnr_dispatcher, { "sport": 5355 })

# LLMNRQuery(id=RandShort(), qd=DNSQR(qname="vista.")))



#############################################################################
#############################################################################
###                             Traceroute6                               ###
#############################################################################
#############################################################################

def _import_whois_servers(s):
    """
    internal function : constructs a dictionary of whois servers FQDN for
    every IANA assigned prefix. Dictionary is constructed from a base64 
    encoded bz2 compressed file. See below
    """
    import bz2 
    import base64
    l = bz2.decompress(base64.decodestring(s)).split('\n')
    res = {}
    for k in l[:-1]:
        prefix,server = k.split(' ')
        res[prefix.strip()] = server.strip()

_whois_servers_dict = _import_whois_servers("""
QlpoOTFBWSZTWQ3r9L0AAWRdgEAQQAX/cCoAOuXcgDABMtEElQbaEqaGmmEGgwkmqammmjQyNqb1
QGmCpSp+pP2qjJgmjBGHqW66QhK2EILOIIB6pATPxpqBwIHDgQwE5oICqEBd0gedfHfDOtiEBpNL
6Ob+DbbbbbbbbeNyCNY321iG4httttvG2r2xj3xjFUQai0gWksQWOJB7Y+q+emeHC/MEBoLcEBol
FVV27uhKZmZmar4u7und3dAhEAkvKAA7aJAbAb5znGLvOaSiqqqmW2245d+/oAHLVCXPH6IDQEB/
f6IKvEl0hmIL0Ve5BU62hMxBnRSCiSrF0F4g7EGYg9C7kinChIBvX6Xo""")

def lookup(addr):
    addr = socket.inet_pton(socket.AF_INET6, addr)
    for k in _whois_servers_dict.keys():
        prefix,plen = k.split('/')
        plen = int(plen)
        if in6_isincluded(addr, prefix, plen):
            return _whois_servers_dict[k]

class TracerouteResult6(TracerouteResult):
    def show(self):
        return self.make_table(lambda (s,r): (s.sprintf("%-42s,IPv6.dst%:{TCP:tcp%TCP.dport%}{UDP:udp%UDP.dport%}{ICMPv6EchoRequest:IER}"), # TODO: ICMPv6 !
                                              s.hlim,
                                              r.sprintf("%-42s,IPv6.src% {TCP:%TCP.flags%}"+
					                "{ICMPv6DestUnreach:%ir,type%}{ICMPv6PacketTooBig:%ir,type%}"+
							"{ICMPv6TimeExceeded:%ir,type%}{ICMPv6ParamProblem:%ir,type%}"+
							"{ICMPv6EchoReply:%ir,type%}")))

    def world_trace(self):
	warning('Not implemented for IPv6 !')

    def _hasinstance(self, p, i):
	while p:
	    if isinstance(p, i):
		return True
	    p = p.payload    
	return False

    def _get_trace_id(self, s, r):
            if s.haslayer(TCP) or s.haslayer(UDP):
                trace_id = (s.src,s.dst,s.nh,s.dport)
            elif self._hasinstance(s, _ICMPv6):
                trace_id = (s.src,s.dst,s.nh,s.type,s.code)
            else:
                trace_id = (s.src,s.dst,s.nh,0)
	    return trace_id

    def _get_trace(self, s, r, trace_id, trace, ports, ports_done):
            if not self._hasinstance(r, _ICMPv6) or r.type != 3:
                if ports_done.has_key(trace_id):
		    return None
                ports_done[trace_id] = None
                p = ports.get(r.src,[])
                if r.haslayer(TCP):
                    p.append(r.sprintf("<T%ir,TCP.sport%> %TCP.sport%: %TCP.flags%"))
                    trace[s.hlim] = r.sprintf('"%IPv6.src%":T%ir,TCP.sport%')
                elif r.haslayer(UDP):
                    p.append(r.sprintf("<U%ir,UDP.sport%> %UDP.sport%"))
                    trace[s.hlim] = r.sprintf('"%IPv6.src%":U%ir,UDP.sport%')
                elif self._hasinstance(r, _ICMPv6):
                    p.append(r.sprintf("<I%ir,type%> ICMPv6 %type%"))
                    trace[s.hlim] = r.sprintf('"%IPv6.src%":I%ir,type%')
                else:
                    p.append(r.sprintf("<P%ir,IPv6.nh%> IPv6 %IPv6.nh%"))
                    trace[s.hlim] = r.sprintf('"%IPv6.src%":P%ir,IPv6.nh%')                    
                ports[r.src] = p
            else:
                trace[s.hlim] = r.sprintf('"%IPv6.src%"')
            return (trace, ports, ports_done)

    def _get_clusters(self, ips, ASN):
        ASN_query_list = dict.fromkeys(map(lambda x:x.split("_")[0],ips)).keys()
        ASNlist = []
        if ASN == 1:
	    def parse(x):
		asn,desc = None,""
		for l in x.splitlines():
		    if not asn and l.startswith("inet6num:"):
			asn = l[9:].strip()
		    elif not asn and l.startswith("CIDR:"):
			asn = l[5:].strip()
		    if l.startswith("netname:") or l.startswith("NetName:"):
			if desc:
			    desc += r"\n"
                            desc += l[8:].strip()
		    #if l.startswith("country:") or l.startswith("Country:"):
		    #    print '%s %s' % (desc, l[9:].strip())
		    if asn is not None and desc:
			break
		return asn,desc.strip()

	    for ip in ASN_query_list:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((lookup(ip), 43))
                s.send("%s\n" % ip)
		t = s.recv(8192)
		buff = ''
		while t != '':
		    buff = buff + t 
		    t = s.recv(8192)
		s.close()
		asn, desc = parse(buff)   
		ASNlist.append((ip,asn,desc))
	else:
            ASNlist = []
	return ASNlist

    def graph(self, CL=1, padding=0, **kargs):
        """x.graph(CL=1, other args):
    CL=0 : no clustering
    CL=1 : use whois based clustering
    other args are passed to do_graph()"""
	self._graph(ASN=CL, padding=padding, **kargs)	

def traceroute6(target, dport=80, minttl=1, maxttl=30, sport=RandShort(), 
                l4 = None, timeout=2, **kargs):
    """
    Instant TCP traceroute using IPv6 :
    traceroute6(target, [maxttl=30], [dport=80], [sport=80]) -> None
    """
    if l4 is None:
        a,b = sr(IPv6(dst=target, hlim=(minttl,maxttl))/TCP(seq=RandInt(),sport=sport, dport=dport),
                 timeout=timeout, filter="icmp6 or tcp", **kargs)
    else:
        a,b = sr(IPv6(dst=target, hlim=(minttl,maxttl))/l4,
                 timeout=timeout, **kargs)

    a = TracerouteResult6(a.res)
    a.display()
    return a,b


#############################################################################
#############################################################################
###                                Sockets                                ###
#############################################################################
#############################################################################

class L3RawSocket6(L3RawSocket):
    def __init__(self, type = ETH_P_IPV6, filter=None, iface=None, promisc=None, nofilter=0):
        L3RawSocket.__init__(self, type, filter, iface, promisc)
	# NOTE: if fragmentation is needed, it will be done by the kernel (RFC 2292)
        self.outs = socket.socket(socket.AF_INET6, socket.SOCK_RAW, socket.IPPROTO_RAW)
        self.ins = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.htons(type))

def IPv6inIP(dst='203.178.135.36', src=None):
  _IPv6inIP.dst = dst
  _IPv6inIP.src = src
  if not conf.L3socket == _IPv6inIP:
    _IPv6inIP.cls = conf.L3socket
  else:
    del(conf.L3socket)
  return _IPv6inIP

class _IPv6inIP(SuperSocket):
  dst = '127.0.0.1'
  src = None
  cls = None

  def __init__(self, family=socket.AF_INET6, type=socket.SOCK_STREAM, proto=0, **args):
    SuperSocket.__init__(self, family, type, proto)
    self.worker = self.cls(**args)

  def set(self, dst, src=None):
    _IPv6inIP.src = src
    _IPv6inIP.dst = dst

  def nonblock_recv(self):
    p = self.worker.nonblock_recv()
    return self._recv(p)

  def recv(self, x):
    p = self.worker.recv(x)
    return self._recv(p, x)

  def _recv(self, p, x=MTU):
    if p is None:
      return p
    elif isinstance(p, IP):
      # TODO: verify checksum
      if p.src == self.dst and p.proto == socket.IPPROTO_IPV6:
        if isinstance(p.payload, IPv6):
          return p.payload
    return p

  def send(self, x):
    return self.worker.send(IP(dst=self.dst, src=self.src, proto=socket.IPPROTO_IPV6)/x)


#############################################################################
#############################################################################
###                          Layers binding                               ###
#############################################################################
#############################################################################

L3Types[ETH_P_IPV6] =  IPv6
LLTypes[31] = IPv6
LLNumTypes[IPv6] = 31
layer_bonds = layer_bonds + [ ( Ether,     IPv6,         { "type" : 0x86dd } ),
                              ( IPerror6,  TCPerror,     { "nh" : socket.IPPROTO_TCP } ),
                              ( IPerror6,  UDPerror,     { "nh" : socket.IPPROTO_UDP } ),
                              ( IPv6,      TCP,          { "nh" : socket.IPPROTO_TCP } ),
                              ( IPv6,      UDP,          { "nh" : socket.IPPROTO_UDP } ),
                              ( IP,        IPv6,         {"proto": socket.IPPROTO_IPV6} ),
                              ( IPv6,      IPv6,         {"nh": socket.IPPROTO_IPV6} )
	                    ]

for l in layer_bonds:
    bind_layers(*l)
del(l)


#############################################################################
###                          Conf overloading                             ###
#############################################################################

def get_working_if6():
    """
    try to guess the best interface for conf.iface by looking for the 
    one used by default route if any.
    """
    res = conf.route6.route("::/0")
    if res:
        iff, gw, addr = res
        return iff
    return get_working_if()

conf.route6 = Route6()
conf.iface = get_working_if6()

if __name__ == '__main__':
    interact(mydict=globals(), mybanner="IPv6 enabled")
else:
    import __builtin__
    __builtin__.__dict__.update(globals())
