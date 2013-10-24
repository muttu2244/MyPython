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

import sys, fcntl, time, os, re, string, getopt, time, pwd
from stat import *
from random import randint


#locations of resource and lock trees
#basedir = "/home/sam/perl/res"
basedir = "/auto/labtools/res/"

#handle separate resource trees
tree = os.getenv("RESOURCE_TREE")
if tree == "sw":
    treedir = "sw/locking/"
else:
    treedir = "qa/locking/"

top_level_dir = basedir + treedir
top_lock_dir = top_level_dir + "locks"
top_res_dir = top_level_dir + "resources"

#dict of lists of locks achieved (paths of resources, not lockfiles)
locked_resources = {}
test_name = ""

def add_to_taken_lock_db(type, name):
    if type not in locked_resources.keys():
        locked_resources[type] = []
    locked_resources[type].append(name)
    
def lock_res(type, name):
    filename = name + ".lock"
    filepath = lock_path(type, filename)
    if os.path.exists(filepath):
        print "Lock already exists:", filepath
        return False
    try:
        lockfd = open(filepath,"w+")
    except IOError:
        print "Couldnt open lockfile \"%s\"" % filepath
        return False
        
    try:
        fcntl.lockf(lockfd, fcntl.LOCK_EX | fcntl.LOCK_NB)
        #pump in data.. uname, pid, testname (if any), 
        print >> lockfd, "User:", os.getenv("USER")
        print >> lockfd, "PID:", os.getpid()
        print >> lockfd, "PPID:", os.getppid()
        print >> lockfd, "Host:", os.uname()[1]
        if test_name:
            print >> lockfd, "Testname:", test_name
        add_to_taken_lock_db(type, name)
        return True
    except IOError:
        print "(2) Looks like someone beat us to it with", filepath
        return False
      
def bail():
    #need clean up existing lockfiles
    remove_locks()
    sys.exit(1)

def remove_locks(interactive=False):
    for type in locked_resources.keys():
        for res in locked_resources[type]:
            res += ".lock"
            try:
                os.unlink(lock_path(type,res))
            except OSError:
                print "Warning, could not remove lock file: %s" % lock_path(type, res)
            else:
                if interactive:
                    print "Removed lock: %s/%s" % (type, res)

def getfreeones(type):
    lockreg = re.compile(".*\.lock$")

    res_dir = res_path(type,"")
    res_file_list = os.listdir(res_dir)

    lock_dir = lock_path(type,"")
    lock_file_list = os.listdir(lock_dir)

    #ignore directories and locks in resource dir
    res_name_list = filter(lambda x: os.path.isfile(res_path(type, x)), res_file_list)
    res_name_list = filter(lambda x: not re.match(lockreg, x), res_name_list)
    
    #ignore anything not a lock file in locks dir
    locklist = filter(lockreg.match, lock_file_list)

    #filter out ones already locked
    freelist = filter(lambda x: x + ".lock" not in locklist, res_name_list)

    return freelist

def locks2res(locks):
    retval = {}
    for key in locks.keys():
        retval[key] = []
        for file in locks[key]:
            retval[key].append(os.path.basename(file))
    return retval

def isnum(str):
    try:
        num = string.atoi(str)
    except ValueError:
        return False
    return True

#get args.. number of each type to lock
def get_number_locks(arg):
    types = arg.keys()
    types.sort()

    #sanity checks - make sure such resource and lock directories exist
    for thistype in types:
        res_dir_path = res_path(thistype,"")
        if not os.path.isdir(res_dir_path):
            print "Resource type \"%s\" not valid. No such resource dir: %s" % (thistype, res_dir_path)
            bail()
        lock_dir_path = lock_path(thistype,"")
        if not os.path.isdir(lock_dir_path):
            print "Lock type \"%s\" not valid. No such lock dir: %s" % (thistype, lock_dir_path)
            bail()

    #now iterate across types, grab filenames in each dir
    for thistype in types:

        num_needed = arg[thistype]
        freelist = getfreeones(thistype)
        if num_needed > len(freelist):
            print "Not enough", thistype + "'s available"
            print "Required: %d, available: %d" % (num_needed, len(freelist))
            bail()

        #now try to lock enough of these
        num_locked = 0
        for res_name in freelist:
            num = randint(0, len(freelist)-1)
            res_name = freelist[num]
            if not lock_res(thistype, res_name):
                print "Couldn't lock", res_name
            else:
                num_locked += 1
                if num_locked == num_needed:
                    break
        if num_locked != num_needed:
            print "Couldn't get enough", thistype, "locks"
            bail()

    #delay to prevent collisions
    time.sleep(2)
    return locked_resources

def res_path(type, name):
    path = "%s/%s/%s" % (top_res_dir, type, name)
    return path

def lock_path(type, name):
    path = "%s/%s/%s" % (top_lock_dir, type, name)
    return path

#get args.. number of each type to lock
def get_named_locks(args):
    types = args.keys()
    types.sort()

    #sanity checks - make sure such resource and lock directories exist
    for thistype in types:
        res_dir_path = res_path(thistype,"")
        if not os.path.isdir(res_dir_path):
            print "Resource type \"%s\" not valid. No such resource dir: %s" % (thistype, res_dir_path)
            bail()
        lock_dir_path = lock_path(thistype,"")
        if not os.path.isdir(lock_dir_path):
            print "Lock type \"%s\" not valid. No such lock dir: %s" % (thistype, lock_dir_path)
            bail()
        #verify each resource exists
        for name in args[thistype]:
            if not os.path.isfile(res_path(thistype, name)):
                print "Resource does not exist: %s/%s" % (thistype, name)
                bail()

    #now iterate across types, and try to lock each named resource
    for thistype in types:
        namelist = args[thistype]
        for name in namelist:
            if not lock_res(thistype, name):
                print "Couldn't lock %s/%s" % (thistype, name)
                bail()
                
    #delay to prevent collisions
    time.sleep(1)
    return locked_resources

#named_arg_ret is dict, entries are lists of names
#num_arg_ret is dict, entries are number of required resource
def parse_args(arglist):
    named_arg_reg = re.compile("^(\w+)[=/]([-\w]+)$")
    num_arg_reg = re.compile("^(\w+)=(\d+)$")
    named_arg_ret = {}
    num_arg_ret = {}
    for arg in arglist:
        match = num_arg_reg.match(arg)
        if match:
            (type, num) = match.groups()
            num_arg_ret[type] = string.atoi(num)
            continue
        else:
            match = named_arg_reg.match(arg)
            if match:
                (type, name) = match.groups()
                if type not in named_arg_ret.keys():
                    named_arg_ret[type] = []
                if name not in named_arg_ret[type]:
                    named_arg_ret[type].append(name)
                continue
        usage()
        sys.exit(1)
    return named_arg_ret, num_arg_ret


def usage():
    print """Usage:
    %s <type>=<number> | <type>=<name> ...""" % sys.argv[0]
  
def print_locked_resources():
    for thistype in locked_resources:
        print thistype,
        for res in locked_resources[thistype]:
            print res,
        print

def rmlocks_usage():
    print """Usage:
    %s [-f file | <type>=<name> .. ]
    Where [file] is a file containing list of locked systems of the form:
    <type> <resource name> ...
    Ex:
     ssx cayman qa-reg1
     cisco cisco1 cisco2

    If no file is specified, lines are read from stdin until control-d is pressed.
    """ % sys.argv[0]

def rmlocks():
    infile = False
    force = False
    try:
        opts, argsleft = getopt.getopt(sys.argv[1:], "kf:")
    except getopt.GetoptError:
        rmlocks_usage()
        sys.exit(1)
    
    locks_to_kill = {}

    if len(sys.argv) == 1:
        infile = sys.stdin
    else:
        for o, a in opts:
            if o == "-k":
                force = True
            if o == "-f":
                infilename = a
                try:
                    infile = open(infilename)
                except IOError:
                    print "Couldn't open file:", infilename
                    rmlocks_usage()
                    sys.exit(1)

    if infile:
        lines = infile.readlines()
        for line in lines:
            items = line.split()
            if len(items) == 0:
                continue
            type = items[0]
            if type not in locked_resources.keys():
                locked_resources[type] = []
                for item in items[1:]:
                    if item not in locked_resources[type]:
                        locked_resources[type].append(item)
    else:
        named_args, number_args = parse_args(argsleft)
        for type in named_args.keys():
            if type not in locked_resources.keys():
                locked_resources[type] = named_args[type]
    if not force:
        check_owners()
    remove_locks(interactive=True)

#check owner of lock file, if not you, complain and bail
def check_owners():
    notours = {}
    for type in locked_resources.keys():
        for res in locked_resources[type]:
            typeres = type + "/" + res
            try:
                statinfo = os.stat(lock_path(type, res + ".lock"))
            except OSError:
                continue
            uid = statinfo[ST_UID]
            pwent = pwd.getpwuid(uid)
            theuser = pwent[0]
            if theuser != os.getenv("USER"):
                notours[typeres] = theuser
    if notours:
        print "ERROR: the following resources are not locked by you:"
        for typeres in notours.keys():
            print "\t%s owned by %s" % (typeres, notours[typeres])
        sys.exit(1)
                               

def striplock(str):
    match = re.match("(.*)\.lock", str)
    return match.groups()[0]

def listlocks():
    someuser = onetype = False
    justmine = True
    lockreg = re.compile(".*\.lock$")
    try:
        opts, args = getopt.getopt(sys.argv[1:], "at:u:")
    except getopt.GetoptError:
        # print help information and exit:
        listlocks_usage()
        sys.exit(2)
    for o, a in opts:
        if o == "-a":
            if someuser:
                print "Error: -a and -u are mutually exclusive"
                listlocks_usage()
                sys.exit(1)
            justmine = False
        if o == "-u":
            someuser = a
            if not justmine:
                print "Error: -a and -u are mutually exclusive"
                listlocks_usage()
                sys.exit(1)
        if o == "-t":
            onetype = a
    
    if onetype:
        types = [onetype]
    else:
        types = os.listdir(top_lock_dir)

    locks_found = []

    #collect list of locks for each type
    for type in types:
        lock_dir = lock_path(type,"")
        lock_file_list = os.listdir(lock_dir)
        #ignore anything not a lock file in locks dir
        locklist = filter(lockreg.match, lock_file_list)
        for lockfile in locklist:
            lock_dict = {}
            lock_dict["resname"] = striplock(lockfile)
            lockfile = lock_path(type, lockfile)
            lock_dict["type"] = type
            #get time of creation
            statinfo = os.stat(lockfile)
            lock_dict["ctime"] = time.ctime(statinfo[ST_CTIME])
            uid = statinfo[ST_UID]
            pwent = pwd.getpwuid(uid)
            lock_dict["username"] = pwent[0]
            lock_dict["gecos"] = pwent[4]
            #parse contents
            infile = open(lockfile)
            for line in infile.readlines():
                match = re.match("(\S+) (.*)",line)
                if match:
                    o,a = match.groups()
                else:
                    continue
                if o == "PID:":
                    lock_dict["PID"] = a
                if o == "PPID:":
                    lock_dict["PPID"] = a
                if o == "Host:":
                    lock_dict["host"] = a
                if o == "Testname:":
                    lock_dict["testname"] = a
                if o == "Comment:":
                    lock_dict["comment"] = a
            locks_found.append(lock_dict)
    locks2show = []
    for lockinfo in locks_found:
        if someuser:
            if lockinfo["username"] == someuser:
		locks2show.append(lockinfo)
        elif justmine:
            if lockinfo["username"] == os.getenv("USER"):
		locks2show.append(lockinfo)
        else:
		locks2show.append(lockinfo)
    for lock in locks2show:
        print_lock(lock)
    if justmine and not someuser:
	print_unlock_string(locks2show)

def print_unlock_string(locks2show):
    unlockstr = ""
    for lock in locks2show:
	unlockstr += "%s=%s " % (lock["type"], lock["resname"])
    if unlockstr:
	print unlockstr
	

def print_lock(lock):
    username = lock["username"]
    ctime = lock["ctime"]
    pid = lock["PID"]
    ppid = lock["PPID"]
    host = lock["host"]
    gecos = lock["gecos"]
    type = lock["type"]
    resname = lock["resname"]
    if "testname" in lock.keys():
        namestr = " Test name: " + lock["testname"]
    else:
        namestr = ""
    if "comment" in lock.keys():
        comment = " Comment:: " + lock["comment"]
    else:
        comment = ""
    print "%s/%s: locked by %s (%s) at %s on system \"%s\". PID is %s PPID is %s%s%s" % (
        type, resname, username, gecos, ctime, host, pid, ppid, namestr, comment)
    
def listlocks_usage():
    print """Usage:
    %s [[-a] | [-u user]] [-t type]
    -a           list locks held by all users
    -u <user>    list locks held by <user>
    -t <type>    list locks of this type only
    """ % sys.argv[0]

#to be usable from perl scripts, or manually,
#need to accept command line args and return delimited list of
#resources locked
if __name__=="__main__":
    if os.path.basename(sys.argv[0]) == "rmlocks":
        rmlocks()
        sys.exit()
    if os.path.basename(sys.argv[0]) == "listlocks":
        listlocks()
        sys.exit()
    if len(sys.argv) < 2:
        usage()
        sys.exit(1)
    test_name = os.getenv("RESLOCK_TEST_NAME")
    named_args, number_args = parse_args(sys.argv[1:])
    if named_args.keys():
        get_named_locks(named_args)
    if number_args.keys():
        get_number_locks(number_args)
    print_locked_resources()
else:
    pass
