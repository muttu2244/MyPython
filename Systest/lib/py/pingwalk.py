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

import sys, os
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

#import sys
#qa_lib_dir = "/auto/labtools/systest/lib/py"
#if qa_lib_dir not in sys.path:
#    sys.path.insert(1,qa_lib_dir)

import scapy, thread, os, cPickle, getopt, time
from scapy import *

#unchanged globals
packet_cache_dir = "/a/pktcache/"
pingwalk_cache_dir = packet_cache_dir + "pingwalk/"

#globals that need to reinit'd to be reentrant
received = []
received_frames = []
exitmutexes = [0] * 2


def gen_pad(len):
    retstr = ""
    for i in range(0,len):
        octetval = i % 255
        retstr += "%c" % octetval 
    return retstr

padstr = gen_pad(65536)

def cache_read(filename):
    #check dirs
    if not os.path.isdir(pingwalk_cache_dir):
	os.makedirs(pingwalk_cache_dir)
    pfile_fullpath = pingwalk_cache_dir + filename
    if os.path.isfile(pfile_fullpath):
        #unpickle it
        pfile = os.popen("bzip2 -dc %s" % pfile_fullpath, "r")
        retlist = cPickle.load(pfile)
        del(pfile)
        return retlist
    else:
	return []

def cache_write(data, filename):
    pfile_fullpath = pingwalk_cache_dir + filename
    pfile = os.popen("bzip2 -1 -c >%s" % pfile_fullpath, "w")
    cPickle.dump(data, pfile)
    del(pfile)


def reset_received():
    global received
    received = []
    for i in range(0,65535):
	received.append(False)

def gen_packets(srcip,dstip,startsize,endsize):
    global received

    beforetime=time.ctime()
    must_pickle = False
    #construct hashed filename and try the cache
    l = [srcip,dstip,startsize,endsize]
    frozen = frozenset(l)
    thehash = hash(frozen)
    pfile_name = "pingwalk.ip.%x" % abs(thehash)
    send_packets = cache_read(pfile_name)
    if not send_packets:
	must_pickle = True
    else:      #got what we needed via the cache, we are done
	print "Read packets from cachefile: %s%s" %(pingwalk_cache_dir, pfile_name)
	return send_packets

    send_packets = {}
    print "Generating packets.."
    id = 0
    #iterate across icmp PAYLOAD sizes
    for size in range(startsize, endsize+1):
        this_size = []
        pad = padstr[:size]
        p_ip = IP(src=srcip, dst=dstip, id=id)/ICMP(type=8)/Raw(load=pad)
	id += 1
        if size > 1472:
            fraglist_ip = fragment(p_ip)
            for i in fraglist_ip:
                this_size.append(str(i))
        else:
            this_size.append(str(p_ip))
        send_packets[size+28]=this_size
        sys.stdout.write("%s " % size)        
        sys.stdout.flush()
    print "done"
    aftertime=time.ctime()
    print "before: %s after: %s" % (beforetime, aftertime)
    cache_write(send_packets, pfile_name)
    print "Wrote packets to cachefile: %s%s" %(pingwalk_cache_dir, pfile_name)
    return send_packets

numfrags = 0
num_nonfrags = 0
num_recvd = 0
ids = {}
received = []

def catcher(tid, count, timeout, myaddr, intf):
    global received_frames
    global received
    global num_recvd
    global ids
    global numfrags
    global num_nonfrags

    num_recvd = 0
    ids = {}
    numfrags = 0
    num_nonfrags = 0
    
    def ping4me(x):
        if x.type == 0x800 and x.payload.proto == 1 and x.payload.dst==myaddr:
            return True
        else:
            return False
        
    def pkt4me(x):
	if x.payload.dst==myaddr:
	    return True
	else:
		return False
    def rt_reass(frame):
	global num_recvd
	global ids
	global numfrags
	global num_nonfrags
	global received

	if ping4me(frame):
	    received_packet = frame.payload
	    if not isfrag(received_packet):
		received[received_packet.len] = True
		num_recvd += 1
		num_nonfrags += 1
	    else:  #tack this sucker on the frags lists and try to reass
		numfrags += 1
		id = received_packet.id
		if id not in ids.keys():
		    ids[id] = []
		ids[id].append(received_packet)
		#attempt a reass
		full_pkt = reass_one_pkt(ids[id])
		if full_pkt:
		    received[full_pkt.len] = True
		    num_recvd += 1
	    if num_recvd == count:
		exitmutexes[tid] = 1
		return True
	    else:
		return False

	
    retlist = sniff(iface=intf,timeout=timeout,lfilter=rt_reass)
    exitmutexes[tid] = 1


def sender(tid,intf, delay, frames):

    print time.ctime()
    sendpraw(frames, iface=intf,inter=delay)
    print time.ctime()
    exitmutexes[tid] = 1

def get_intf_mac(intf):
    return get_if_hwaddr(intf)

def get_intf_ip(intf):
    return get_if_addr(intf)


def reassemble(pktlist):
    print "entering reassemble %s" % time.ctime()
    retlist = []
    #collect list of ids
    ids = {}
    for pkt in pktlist:
        id = pkt.id
	print id
        if id not in ids.keys():
            ids[id] = []
        ids[id].append(pkt)
    for id in ids.keys():
        retlist.append(reass_one_pkt(ids[id]))
    print "leaving reassemble %s" % time.ctime()
    print len(retlist)
    return retlist

def reass_one_pkt(pktlist):
    reassed_pkt = None
    #clone first packet's header
    for pkt in pktlist:
        if pkt.frag == 0:
            reassed_packet = pkt.copy()
            reassed_packet.payload = ""
            break
    notdone = True
    offset = 0
    while notdone:
        got_it = False
        for pkt in pktlist:
            if pkt.frag * 8 == offset:
                got_it = True
                #merge packet data onto our new packet
                payload_len = pkt.len - 20
                reassed_packet.payload.load += str(pkt.payload)[:payload_len]
                offset += payload_len
                if pkt.flags == 0:
                    notdone = False
                    break
        if not got_it:
            return None
    reassed_packet.len = len(reassed_packet.payload.load) + 20
    reassed_packet.flags = 0
    return reassed_packet

def isfrag(pkt):
    if pkt.flags == 1 or pkt.frag != 0:
        return True
    else:
        return False



def dosome(frames, intf, delay, srcip):
    global received_frames
    global exitmutexes
    global numfrags
    global num_nonfrags
    global num_recvd

    #reset to make reentrant for use in scripts
    received_packets = []
    exitmutexes = [0,0]

    count = len(frames)
    timeout = int(10 + delay * float(count))

    thread.start_new(catcher, (0, count, timeout, srcip, intf))
    thread.start_new(sender,(1,intf, delay, frames))

    while 0 in exitmutexes: time.sleep(.5)


def myrun(dstmac, dstip, intf, startsize=28, endsize=1500, srcmac="", srcip="", delay=0.0 ):
    global received_frames
    global exitmutexes
    global received
    global num_nonfrags
    global numfrags
    global num_recvd
    
    if not srcmac:
	srcmac = get_intf_mac(intf)
    if not srcip:
	srcip = get_intf_ip(intf)

    #fixup for icmp payload size
    icmp_start_size = startsize - 28
    icmp_end_size = endsize - 28

    send_sizes = range(startsize, endsize+1)
    
    count = (endsize - startsize) + 1
    packets = gen_packets(srcip,dstip,icmp_start_size,icmp_end_size)
    eth_hdr = str(Ether(dst=dstmac, src=srcmac, type = 0x800))
    pkt_list = []
    for pkt_size in packets.keys():
        pkt_list.extend(packets[pkt_size])
    frames = map(lambda x: eth_hdr + x, pkt_list)

    ## reset array of received sizes
    reset_received()
    dosome(frames, intf, delay, srcip)

    lost_sizes = check_received(send_sizes)

    if lost_sizes:
        success = False
        print "MISSING PACKET(s) of size:",
        for i in lost_sizes:
            print "%d" % i,
        print 
    else:
        success = True
    print "number of recvd nonfrags: %d, number of recvd frags: %d" % (num_nonfrags, numfrags)
    print "Sent %d packets, in %d frames" % (count, len(frames))
    print "received %d out of %d packets sent, %s packets were lost" % (num_recvd, count, count - num_recvd)

    #try one more time, if some were lost
    if not success:
        print "WARNING: Some packets were lost, trying again with those sizes"

        pkt_list = []
        for pkt_size in lost_sizes:
            pkt_list.extend(packets[pkt_size])
        frames = map(lambda x: eth_hdr + x, pkt_list)
        count = len(lost_sizes)
        
        ## reset array of received sizes
        received=[]
        reset_received()
        dosome(frames, intf, delay, srcip)

	success = True
        for i in lost_sizes:
	    if not received[i]:
		success = False
		print "STILL MISSING packet of size %d" % i
	print "number of recvd nonfrags: %d, number of recvd frags: %d" % (num_nonfrags, numfrags)
	print "Sent %d packets, in %d frames" % (count, len(frames))
	print "received %d out of %d packets sent, %s packets were lost" % (num_recvd, count, count - num_recvd)
    return success

def check_received(send_sizes):
    global received
    lost_sizes = []
    for pktlen in send_sizes:
        if not received[pktlen]:
	    lost_sizes.append(pktlen)
    return lost_sizes

def usage(retcode):
    print """Usage:
    %s [-a startsize] [-z endsize] [-S srcmac] -D dstmac
                 [-s srcip] -d dstip [-w delay] -i interface
    -a           start IP packet size for ping walk, defaults to 28.
    -z           end IP packet size for ping walk, defaults to 1500.
    -S <srcmac>  source mac address to use for packets, if omitted,
                 defaults to the mac address of the outgoing interface.
    -D <dstmac>  Mac address of destination or next hop.
    -s <srcip>   source ip address to use, defaults to address of
                 outgoing intf.
    -w <delay>   inter-packet delay, defaults to zero.
                 (ie as fast as script can send)
    -i <intf>    Outgoing interface to use.
    """ % sys.argv[0]
    sys.exit(retcode)

#    [-a startsize] [-z endsize] [-S srcmac] -D dstmac
#                 [-s srcip] -d dstip [-w delay] -i interface
if __name__ == "__main__":
    #set up defaults and nulls to pass, dorun() will fill in dynamic defaults
    startsize = 28
    endsize = 1500
    delay = 0.0
    srcmac = ""
    srcip = ""
    intf = ""
    dstmac = ""
    dstop = ""

    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:z:S:D:s:d:w:i:h")
    except getopt.GetoptError:
        # print help information and exit:
        usage(1)

    for o, a in opts:
	if o == "-a":
	    startsize = int(a)
	if o == "-z":
	    endsize = int(a)
	if o == "-S":
	    srcmac = a
	if o == "-D":
	    dstmac = a
	if o == "-s":
	    srcip = a
	if o == "-d":
	    dstip = a
	if o == "-w":
	    delay = float(a)
	if o == "-i":
	    intf = a
	if o == "-h":
	    usage(0)

    #required arguments
    if not dstmac:
	usage(1)
    if not dstip:
	usage(1)
    if not intf:
	usage(1)

    retval = 0
    success = myrun(dstmac, dstip, intf,startsize=startsize, endsize=endsize, srcmac=srcmac, srcip=srcip, delay=delay)
    if not success:
	retval=1
    sys.exit(retval)

