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

import sys
from optparse import OptionParser
from time import sleep
from subprocess import Popen, PIPE
from pdb import set_trace as st

class ReturnCodeError(Exception):
    """Raised if the return code from a command line operation is not zero."""
    
    def __init__(self, value):
        self.return_code = value

    def __str__(self):
        return repr(self.return_code)

def display_error(returncode, error, output, ping):
    """Making a failure look pretty.

    XXX while this is quick and dirty, we should wrap this into some logging
    facility.
    """
    print "The following return code was recieved: %s" % returncode
    print "The error was:"
    for line in error:
	print line.strip("\n")
    print "The cmd line was: %s" % ping
    print "The output was:"
    for line in output:
        print line.strip("\n")

def status(size_range, passed):
    """Print out a status message let folks know how we're doing."""
    left = validate(passed, size_range)
    print "####################################################################"
    print "Status of Run\n"
    print "%i run, %i left, %i total" % (len(passed), len(left), len(size_range))
    print "Last icmp packet size was: %i" % passed[-1]

def traffic(cmd, size_range):
    """Generate the traffic on the command line."""

    passed = list()
    if opts.count:
        failures = int(opts.count)
        limit = True
    else:
        limit = False
        
    for size in size_range:
        try:
            # run the cmd, wait for it to finish and grab the return code.
            ping = cmd % (opts.interface, size, opts.dstip, opts.deadline)
            p = Popen([ ping ], shell=True, stdout=PIPE, stderr=PIPE)
            p.wait()
            returncode = p.returncode
            
            # check the return code
            if returncode == 0:
                passed.append(size)
            # if the return code is not 0, raise an error
            else:
                raise ReturnCodeError, returncode
        except ReturnCodeError, e:
            output = p.stdout.readlines()
            error  = p.stderr.readlines()
            display_error(returncode, error, output, ping)
            if limit:
                if failures > 0:
                    failures -= 1
                else:
                    print "\nError limit reached.  Exiting..."
                    raise KeyboardInterrupt
        except KeyboardInterrupt:
            status(size_range, passed)
            raise
    return passed

def validate(output, size_range):
    """Validate that we didn't lose anything."""
    size_range = set(size_range)
    size_range.difference_update(output)
    return size_range

def build_parser():
    """Build the command line options."""
    
    usage = "usage: %prog [options] -d host"
    parser = OptionParser(usage, add_help_option=True,)
    
    parser.add_option("-6", "--ipv6", dest="v6", action="store_true", default=None,
                      help="""Use ipv6 instead of ipv4."""
                      )
    parser.add_option("-a", "--startsize", dest="startsize", action="store", default=28,
                      help="""Start IP packet size for ping walk, defaults to 28."""
                      ) 
    parser.add_option("-c", "--count", dest="count", type="int", action="store", default=None,
                      help="""Error limit that when met will force tool to quit."""
                      )
    parser.add_option("-d", "--dstip", dest="dstip", action="store", default=None,
                      help="""IP address to send icmp traffic to."""
                      )
    parser.add_option("-i", "--interface", dest="interface", action="store", default=None,
                      help="""Outgoing interface to use."""
                      )
    parser.add_option("-z", "--endsize", dest="endsize", action="store", default=1500,
                      help="""End IP packet size for ping walk, defaults to 1500."""
                      )
    parser.add_option("-w", "--deadline", dest="deadline", action="store", default=0,
                      help="""ping waits either for deadline expire or until count probes are answered or for some error notification"""
                      )
    return parser

if __name__ == '__main__':

    parser = build_parser()
    (opts, args) = parser.parse_args()

    # validate the command line args.
    if not opts.dstip:
        print "Error: No destination IP to send traffic to.\n"
        parser.print_help()
        sys.exit(1)

    # syntax for the ping command we're going to use.
    if opts.v6:
        cmd = "ping6 -n -I %s -s %i -c 1 %s -w %s"
    else:
        cmd = "ping -n -I %s -s %i -c 1 %s -w %s"

    ping_header_len = 28

    # build the lists we need.
    size_range = range(int(opts.startsize) - ping_header_len ,
                       int(opts.endsize) - ping_header_len)

    try:
        output = traffic(cmd, size_range)
	if output:
        	whats_left = validate(output, size_range)
	        if whats_left:
        	    print "Here's what is left:"
	            for line in whats_left:
        	        print line
	else:
                raise KeyboardInterrupt
                
    except KeyboardInterrupt:
        sys.exit(1)

    

