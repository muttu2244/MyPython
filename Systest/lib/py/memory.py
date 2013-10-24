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

"""
DESCRIPTION             : This Script contains following DHCP  APIs which has
                          been used in the DHCP Testcases

TEST PLAN               : DHCP Test plan V0.3
AUTHOR                  : Rajshekar; email : Rajshekar@primesoftsolutionsinc.com
REVIEWER                :
DEPENDENCIES            : Linux.py,device.py
"""

import sys, os
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

import pexpect
import time
import string
import sys
import re
import cPickle


# Frame-work libraries
#from SSX import *
#from log import *
#from logging import getLogger
#from helpers import is_healthy
from issu import *
from pprint import pprint
#from memory import convrtToBytes 

def getProcMemoryOnSlot(self,procName,slot) :
       """
       Description  : Used to get the Memory consumed by Process on Slot.
       Arguments    : procName  - Name of the Process
                   slot - slot id
       Usage        : getProcMemoryOnSlot(self.ssx,"iked","2")
       Return Value : Size of memory consumed by Process
       """
       slot_range = [0,1,2,3,4]
       #try :
       #    int(slot)
       #except :
            
       out = self.cmd("show process mem slot %s | grep -i %s"%(slot,procName))
       if "ERROR" in "%s"%out or int(len("%s"%out)) == 0 :
          memCons = "0MB"
       else :
          memCons = out.split()[7]
       return memCons

def vrfProcMemoryLeakOnSlot(memConsBefore="",memConsAfter="") :
       """
       Description  : Used to Verify Process Memory Leak
       Arguments    : memConsBefore - Memory consumption before
                   memConsAfter - Memory consumption After
       Usage        : vrfProcMemoryLeakOnSlot(memConsBefore="27MB",memConsAfter="29MB")
       Return Value : either 1 or 0
       """
      
       memBefore = re.match("(\d*)(\w*)B","%s"%memConsBefore)
       memAfter =  re.match("(\d*)(\w*)B","%s"%memConsAfter)
       mayBeMemLeak = 0
       MemLeak = 0
       if memBefore.group(2) != memAfter.group(2) :
          mayBeMemLeak = 1
       if mayBeMemLeak == 1  :
          if memAfter.group(1) == "G" :
              MemLeak = 1
       if int(memBefore.group(1)) < int(memAfter.group(1)):
              MemLeak = 1
       if MemLeak == 1 :
          return 1
       else :
          return 0

def convrtToBytes(memsize) :
       """
       Description  : Used to convert KB or MB to bytes.
       Arguments    : memsize - Memory Size
       Usage        : convrtToBytes("27MB")
       Return Value : Return memory size in bytes
       """

       mem = re.match("(\d*)(\w*)B","%s"%memsize)
       if mem.group(2) == "M" :
           memConsInBytes = int( mem.group(1)) * 1024 * 1024
       elif mem.group(2) == "G" :
           memConsInBytes = int( mem.group(1)) * 1024 * 1024 * 1024
       else :
           memConsInBytes = int( mem.group(1)) * 1024
       return int(memConsInBytes)

def exeMemComands(self) :
        """
        Description  : Used to Execute the commands related to Memory
        Arguments    :
        Usage        : exeMemComands(self.ssx)
        Return Value : Return the output of all commands.
        """

        boarder = "\n" + "-" *50 + "\n"
        shClock = self.cmd("show clock")
        memo = self.cmd("show memory")
        procMemConsOnSlot0 = self.cmd("show proce mem slot 0")
        procMemConsOnSlot1 = self.cmd("show proce mem slot 1") 
        procMemConsOnSlot2 = self.cmd("show proce mem slot 2")
        procMemConsOnSlot3 = self.cmd("show proce mem slot 3")
        procMemConsOnSlot4 = self.cmd("show proce mem slot 4")

        modIpMa = self.cmd("show module ip ma")
        modIpMaPools = self.cmd("show module ip ma pools")
        
        ikedProcconsOnSlot2 = self.cmd("sh module iked slot 2 ma")
        ikedProcconsOnSlot3 = self.cmd("sh module iked slot 3 ma")
        ikedProcconsOnSlot4 = self.cmd("sh module iked slot 4 ma")

        modIkedSlot2_pool = self.cmd("sh module iked slot 2 ma pool")
        modIkedSlot3_pool = self.cmd("sh module iked slot 3 ma pool")
        modIkedSlot4_pool = self.cmd("sh module iked slot 4 ma pool")

        modIkedSlot2_pp = self.cmd("sh module iked slot 2 ma pp")
        modIkedSlot3_pp = self.cmd("sh module iked slot 3 ma pp")
        modIkedSlot4_pp = self.cmd("sh module iked slot 4 ma pp")
        modIplcma = self.cmd("sh module iplc slot 2 ma") + self.cmd("sh module iplc slot 3 ma") + self.cmd("sh module iplc slot 4 ma") 
        modIplcmapool = self.cmd("sh module iplc slot 2 ma pool") + self.cmd("sh module iplc slot 3 ma pool") + self.cmd("sh module iplc slot 4 ma pool")
        modIplcmapp = self.cmd("sh module iplc slot 2 ma pp") + self.cmd("sh module iplc slot 3 ma pp") + self.cmd("sh module iplc slot 4 ma pp")     
        modIpLcma = self.cmd("sh module nsemgr slot 2 ma") + self.cmd("sh module nsemgr slot 3 ma") + self.cmd("sh module nsemgr slot 4 ma")
        modIpLcmapool = self.cmd("sh module nsemgr slot 2 ma pool") + self.cmd("sh module nsemgr slot 3 ma pool") + self.cmd("sh module nsemgr slot 4 ma pool")
        modIpLcmapp = self.cmd("sh module nsemgr slot 2 ma pp") + self.cmd("sh module nsemgr slot 3 ma pp") + self.cmd("sh module nsemgr slot 4 ma pp")
        modAaadma = self.cmd("sh module aaad slot 0 ma") + self.cmd("sh module aaad slot 1 ma")
        modAaadmapool = self.cmd("sh module aaad slot 0 ma pool") + self.cmd("sh module aaad slot 1 ma pool")
        modAaadmapp = self.cmd("sh module aaad slot 0 ma pp") + self.cmd("sh module aaad slot 1 ma pp")
        modipMcma = self.cmd("sh module ip slot 0 ma") + self.cmd("sh module ip slot 1 ma")
        modipMcmapool = self.cmd("sh module ip slot 0 ma pool") + self.cmd("sh module ip slot 1 ma pool")
        modipMcmapp = self.cmd("sh module ip slot 0 ma pp") + self.cmd("sh module ip slot 1 ma pp")
 
        ssxMemStats = ""
        ssxMemStats = boarder + "SSX MEMORY STATISTICS:" + "SHOW CLOCK" + shClock + boarder + "MEM" + memo + boarder + "PROC MEM ON SLOT 0" + procMemConsOnSlot0 + boarder + "PROC MEM ON SLOT 1" + procMemConsOnSlot1 + boarder + "PROC MEM ON SLOT 1" + procMemConsOnSlot1 + boarder + "PROC MEM ON SLOT 2" + procMemConsOnSlot2 + boarder + "PROC MEM ON SLOT 3" + procMemConsOnSlot3 + "PROC MEM ON SLOT 4" + procMemConsOnSlot4 + boarder + "show module ip ma" + modIpMa + "show module ip ma pools" + modIpMaPools + "sh module iked slot 2 ma" + ikedProcconsOnSlot2  + boarder +  "sh module iked slot 3 ma" + ikedProcconsOnSlot3 + boarder + "sh module iked slot 4 ma" + ikedProcconsOnSlot4  + boarder + "sh module iked slot 2 ma pool" + modIkedSlot2_pool + boarder + "sh module iked slot 3 ma pool"  + modIkedSlot3_pool + boarder + "sh module iked slot 4 ma pool" + modIkedSlot4_pool  + boarder + "sh module iked slot 2 ma pp" + modIkedSlot2_pp + boarder + "sh module iked slot 3 ma pp" + modIkedSlot3_pp + "sh module iked slot 4 ma pp" + modIkedSlot4_pp + boarder + "sh module iplc slot <2/3/4> ma" + modIplcma + boarder  + "sh module iplc slot <2/3/4> ma pool" + modIplcmapool + boarder + "sh module iplc slot <2/3/4> ma pp" + modIplcmapp  + boarder + "sh module nsemgr slot <2/3/4> ma" + modIpLcma + boarder  + "sh module nsemgr slot <2/3/4> ma pool" + modIpLcmapool + boarder + "sh module nsemgr slot <2/3/4> ma pp" + modIpLcmapp  + boarder + "sh module aaad slot <0/1> ma" + modAaadma + boarder  + "sh module aaad slot <0/1> ma pool" + modAaadmapool + boarder + "sh module aaad slot <0/1> ma pp" + modAaadmapp  + boarder + "sh module ip slot <0/1> ma" + modipMcma + boarder  + "sh module ip slot <0/1> ma pool" + modipMcmapool + boarder + "sh module ip slot <0/1> ma pp" + modipMcmapp  + boarder




        return ssxMemStats

"""
This section is added by Anthony Ton
"""

def printDiff(self,diffDict,level=-1):
    """
        Description  : This proc takes the different ditionary and print out in a readable form
        Arguments    : diffDict, which was created by calling findDiff
                     : level - by default -1.  Should not have passed in this paramemter.  Only
		     : uses by the proc itself during recursive call
        Usage        : printDiff(curDict)
        Return Value : None
    """
    debug = False
    level += 1

    for key in diffDict.keys():
	tabchar = "\t" * level
	val = diffDict[key]
	if level == 0:
	    # rinfo level, skip printing
	    pass
	elif level == 1:
	    # slot level
	    #self.myLog.info("\n%sSlot: %s" %(tabchar,key)),
	    self.myLog.info("%sSlot: %s" %(tabchar,key)),
	else:
	    # any level bellow slot
	    self.myLog.info("%s%s" %(tabchar,key)),
	
    	if isinstance(val,dict):
	    # if is a dictionary, recursive call to traverse down to leaves
	    printDiff(self,val,level)
	else:
	    # is is the list of different values, print them
	    #self.myLog.info("\t%s\t%s" %(val[0],val[1])), 
	    self.myLog.info("%s%s\t%s" %(tabchar,val[0],val[1])), 
    
    if level == 0:
        if diffDict.keys() == []:
	    self.myLog.info("There is no difference") 
	self.myLog.info("\n\n\n") 




def findDiff(val1,val2,prevkey='ignore',data1={},data2={}):
    """
        Description  : This proc accept two values (either dictionaries or values) and compare.
    		     : If dictionary, recursive check for keys and vals until reaching to the leaves.
        Arguments    : val1: a dictionary generated by calling getcounters
                     : val2: a dictionary generated by calling getcounters
                     : prevkey - by default ignore.  Should not have passed in this paramemter.  Only
		     : uses by the proc itself during recursive call
        Usage        : findDiff(curDict,oldDict)
        Return Value : An dictionary which contains the differences between curDict and oldDict
	Sample Output:
	{   'rinfo': {   '0': {   'sh mem': {   'bytes used': [   '662,376,448',
                                                          '662,364,160']}},
                 	 '2': {   'sh mod proc ma': {   'Count': {   'Default VarPool': {   'Allocs': [   '176',
                        	                                                                          '171'],
                                                                                    'Frees': [   '65',
                                                                                                 '60']},
                                                             'Pools': {   'Allocs': [   '725',
                                                                                        '714'],
                                                                          'Frees': [   '388',
                                                                                       '377']},
                                                             'Shared Pools': {   'Allocs': [   '1,198,292',
                                                                                               '1,198,166'],
                                                                                 'Frees': [   '1,185,998',
                                                                                              '1,185,875'],
                                                                                 'Usage': [   '60,812,352',
                                                                                              '60,805,920']},
                                                             'VarPool Fixed Pools': {   'Allocs': [   '181',
                                                                                                      '176'],
                                                                                        'Frees': [   '129',
                                                                                                     '124']}},
                                                'DHCPdLC': {   'Default VarPool': {   'Allocs': [   '140',
                                                                                                    '135'],
                                                                                      'Frees': [   '64',
                                                                                                   '59']},
                                                               'Pools': {   'Allocs': [   '491',
                                                                                          '480'],
                                                                            'Frees': [   '259',
                                                                                         '248']},
                                                               'Shared Pools': {   'Allocs': [   '1,198,292',
                                                                                                 '1,198,169'],
                                                                                   'Frees': [   '1,186,001',
                                                                                                '1,185,878']},
                                                               'VarPool Fixed Pools': {   'Allocs': [   '116',
                                                                                                        '111'],
                                                                                          'Frees': [   '92',
                                                                                                       '87']}}}
    """
    debug = False
    finalDiffDict = {}
    if (isinstance(val1,dict) and isinstance(val2,dict)):
	# vals are dictionaries. Get the list of keys
	key1List = val1.keys()
	key2List = val2.keys()
	if debug:
	    print("key1List='%s'" %key1List) 
	    print("key2List='%s'" %key2List) 
	# create a set from list of keys
	s1 = set(key1List)
	s2 = set(key2List)
	# find list of the same keys
	intersectList = list(s1.intersection(s2))
	if debug:
	    print("intersectList='%s'" %intersectList) 
	if (intersectList == []):
	    # no match key, do nothing
	    pass
	else:
	    # work of each key 
	    for key in intersectList:
		# get the value of each key
		nval1 = val1[key]
	   	nval2 = val2[key]
		data1 = val1
		data2 = val2	
		if debug:
	    	    print("nval1='%s'" %nval1) 
	    	    print("nval2='%s'" %nval2) 
	    	    print("prevkey='%s'" %prevkey) 
	    	    print("data1='%s'" %data1) 
	    	    print("data2='%s'" %data2) 
		# recursive call through the list
		diffDict = findDiff(nval1,nval2,key,data1,data2)
		if debug:
	    	    print("diffDict") 
    		    pprint(diffDict,indent=4,width=20,depth=20)
		if diffDict != {}:
		    # get the difference, now insert it into exisiting dict
		    if prevkey in finalDiffDict.keys():
			# insert into exisint dict
			# get the current dict
			tmpDict = finalDiffDict[prevkey]
			tDict = {}
			# put the existing dict and new dict together
			for k in tmpDict.keys():
			    tDict[k] = tmpDict[k]
			for k in diffDict.keys():
			    tDict[k] = diffDict[k]
			# insert back to existing dict
			finalDiffDict[prevkey] = tDict
		    else:
			# insert to new dict
			if prevkey != "ignore":
		    	    finalDiffDict[prevkey] = diffDict
			else:
			    # top of the tree, just get the list
		    	    finalDiffDict = diffDict
		    if debug:
	    	        print("finalDiffDict 1") 
    		        pprint(finalDiffDict,indent=4,width=20,depth=20)
		    #if prevkey != 'rinfo':
		    #    finalDiffDict.insert(0,prevkey)
		    #    if debug:
	    	    #	    print("finalDiffDict='%s'" %finalDiffDict) 
    else:
	# vals are values
	# first check if they are digit and then convert into bytes if necessary
	if debug:
	    print("value val1= '%s'" %val1) 
	    print("value val2= '%s'" %val2) 
	    print("prevkey = '%s'" %prevkey) 
	suffix = ('MB','B','GB','KB')
	if val1.endswith(suffix):
	    val1  = str(convrtToBytes(val1))
	if val2.endswith(suffix):
	    val2 = str(convrtToBytes(val2))
	if val1 != val2:
	    # two vals are not the same
	    if re.search('alloc|free',prevkey,re.I) == None:
		if debug:
	    	    print("prevkey is NOT alloc or free") 
	        # add to the dict if the diff is not for key alloc or free
	        finalDiffDict[prevkey] = [val1,val2]
	        if debug:
	            print("finalDiffDict 2") 
    	            pprint(finalDiffDict,indent=4,width=20,depth=20)
	    else:
		# alloc and free differences, then we need to see if the difference between alloc - free
		# for both snapshot and the same or not.  If the same, it is OK; otherwise, add to diffDict
		if debug:
	    	    print("prevkey is alloc or free") 
    	            pprint(data1,indent=4,width=20,depth=20)
    	            pprint(data2,indent=4,width=20,depth=20)
	 	alloc1 = alloc2 = free1 = free2 = '0'
		use1 = use2 = 0	
		for dkey in data1.keys():
	    	    if re.search('alloc',dkey,re.I) != None:
			alloc1 = data1[dkey]
			if alloc1.endswith(suffix):
	    		    alloc1  = str(convrtToBytes(alloc1))
			alloc2 = data2[dkey]
			if alloc2.endswith(suffix):
	    		    alloc2  = str(convrtToBytes(alloc2))
	    	    elif re.search('free',dkey,re.I) != None:
			free1 = data1[dkey]
			if free1.endswith(suffix):
	    		    free1  = str(convrtToBytes(free1))
			free2 = data2[dkey]
			if free2.endswith(suffix):
	    		    free2  = str(convrtToBytes(free2))
		if debug:
	    	    print("alloc1 = %s, free1 = %s, alloc2 = %s, free2 = %s" %(alloc1,free1,alloc2,free2)) 
		use1 = abs(int(alloc1.replace(',','')) - int(free1.replace(',','')))	
		use2 = abs(int(alloc2.replace(',','')) - int(free2.replace(',','')))	
		if use1 != use2:
	            # add to the dict if the diff off alloc minus free
	            finalDiffDict['allocminusfree'] = [str(use1),str(use2)]
	            if debug:
	                print("finalDiffDict 2") 
    	           	pprint(finalDiffDict,indent=4,width=20,depth=20)



    return finalDiffDict
 

def getcounters(self,slotList=[],portList=[]):
    """
        Description  : This proc accept three values self, slot and port list and collect memory counters
    		       for these slots and ports
        Arguments    : self: a class object that have ssx object to access dut
                     : slotList: default empty.  List of slots to collect data
                     : portList: default empty.  List of ports to collect data
        Usage        : myDict = getcounters(self,slotList=['2','3'],portList=['2/0','2/1','3/0'])
        Return Value : An dictionary which contains the memory counters using these commands:
                      'show mem','show process mem','show module proc slot ma'
		      'show module slot ma shared','show module slot ma pp'
		      'show module slot ma pool' 
	Sample Output:
	{'rinfo':{'0':{'show mem':{'ike': 12, \
                                   'cli': [35,46]}, \
                       'show mod sl ma':{'info': 31, \
                                         'test': 32}}, \
                  '1':{'show mem':{'ike': 10, \
                                   'cli': 30}, \
                       'show mod sl ma':{'info': 30, \
                                         'test': 30}}}} 

    """

    self.myLog.info("================================================")
    self.myLog.info("======= Start collecting memory counters =======")
    self.myLog.info("================================================")

    databasedict = {}

    globalSlotDict = {}
    tmpSlotDict = {}
    curDict = {}

    #SHOW MEMORY
    #shMemory_dict = show_mem(self.ssx)
    shMemory_dict = getshowmemcounters(self)
    for slot in shMemory_dict.keys():
	if slot in globalSlotDict.keys():
	    curDict = globalSlotDict[slot]
	else:
	    curDict = {}
	# add new data
	curDict['sh mem'] = shMemory_dict[slot]

	# save back to globalSlotDict			
	globalSlotDict[slot] = curDict

    #SHOW PROCESS MEMORY (ONLY FOR SLOT FROM 2-4)
    #pprint(globalSlotDict,indent=4,width=20,depth=20)
    tmpDict = {}
    for slot in slotList:
        processMemory_dict = show_process_memory(self.ssx,slot)
	# get the current value from the globalSlotDict 
	if slot in globalSlotDict.keys():
	    curDict = globalSlotDict[slot]
	else:
	    curDict = {}
	# add new data
	curDict['sh proc mem'] = processMemory_dict
	# save back to globalSlotDict			
	globalSlotDict[slot] = curDict

    #SHOW MODULE PROCESS SLOT MA 
    tmpDict = {}
    for slot in slotList:
        modprocma_dict = showmoduleprocessma(self.ssx,slot)
	# get the current value from the globalSlotDict 
	if slot in globalSlotDict.keys():
	    curDict = globalSlotDict[slot]
	else:
	    curDict = {}
	# add new data
	curDict['sh mod proc ma'] = modprocma_dict
	# save back to globalSlotDict			
	globalSlotDict[slot] = curDict

    #SHOW MODULE PROCESS SLOT MA SHARED 
    tmpDict = {}
    for slot in slotList:
        modprocmashared_dict = showmoduleprocessmashared(self.ssx,slot)
	# get the current value from the globalSlotDict 
	if slot in globalSlotDict.keys():
	    curDict = globalSlotDict[slot]
	else:
	    curDict = {}
	# add new data
	curDict['sh mod proc ma shared'] = modprocmashared_dict
	# save back to globalSlotDict			
	globalSlotDict[slot] = curDict
	

    #SHOW MODULE PROCESS SLOT MA PP
    tmpDict = {}
    for slot in slotList:
        modprocmapp_dict = showmoduleprocessmapp(self.ssx,slot)
	# get the current value from the globalSlotDict 
	if slot in globalSlotDict.keys():
	    curDict = globalSlotDict[slot]
	else:
	    curDict = {}
	# add new data
	curDict['sh mod proc ma pp'] = modprocmapp_dict
	# save back to globalSlotDict			
	globalSlotDict[slot] = curDict


    #SHOW MODULE PROCESS SLOT MA POOL
    tmpDict = {}
    for slot in slotList:
        modprocmapool_dict = showmoduleprocessmapool(self.ssx,slot)
	# get the current value from the globalSlotDict 
	if slot in globalSlotDict.keys():
	    curDict = globalSlotDict[slot]
	else:
	    curDict = {}
	# add new data
	curDict['sh mod proc ma pool'] = modprocmapool_dict
	# save back to globalSlotDict			
	globalSlotDict[slot] = curDict

    #SHOW MODULE PROCESS SLOT MA PP-SLAB
    tmpDict = {}
    for slot in slotList:
        modprocmappslab_dict = showmoduleprocessmappslab(self.ssx,slot)
	# get the current value from the globalSlotDict 
	if slot in globalSlotDict.keys():
	    curDict = globalSlotDict[slot]
	else:
	    curDict = {}
	# add new data
	curDict['sh mod proc ma pp-slab'] = modprocmappslab_dict
	# save back to globalSlotDict			
	globalSlotDict[slot] = curDict

    #SHOW MODULE PROCESS SLOT MA SLAB
    tmpDict = {}
    for slot in slotList:
        modprocmaslab_dict = showmoduleprocessmaslab(self.ssx,slot)
	# get the current value from the globalSlotDict 
	if slot in globalSlotDict.keys():
	    curDict = globalSlotDict[slot]
	else:
	    curDict = {}
	# add new data
	curDict['sh mod proc ma slab'] = modprocmaslab_dict
	# save back to globalSlotDict			
	globalSlotDict[slot] = curDict

    databasedict['rinfo'] = globalSlotDict

    return databasedict

def getcountersforcmd(self,cmdList,slotList=[],portList=[]):
    """
        Description  : This proc accept four parameter, self, commandList, slot and port list 
		       and collect memory counters for these slots and ports
        Arguments    : self: a class object that have ssx object to access dut
                     : cmdList:  List of commands to collect data
                     : slotList: default empty.  List of slots to collect data
                     : portList: default empty.  List of ports to collect data
        Usage        : myDict = getcountersforcmd(self,['show process mem','show mem'],slotList=['2','3'],portList=['2/0','2/1','3/0'])
        Return Value : An dictionary which contains the memory counters.
		       Supported commands are:
                      'show mem','show process mem','show module proc slot ma',
		      'show module slot ma shared','show module slot ma pp',
		      'show module slot ma pool', 'show module slot ma pp-slab',
		      'show module slot ma slab'
	Sample Output:
       {'rinfo':{'0':{'show mem':{'ike': 12, \
                                   'cli': [35,46]}, \
                       'show mod sl ma':{'info': 31, \
                                         'test': 32}}, \
                  '1':{'show mem':{'ike': 10, \
                                   'cli': 30}, \
                       'show mod sl ma':{'info': 30, \
                                         'test': 30}}}} 

    """
    debug = False
    databasedict = {}

    globalSlotDict = {}
    tmpSlotDict = {}
    curDict = {}

    supportCmdList = ['show mem','show process mem','show module proc slot ma', \
		      'show module slot ma shared','show module slot ma pp', \
		      'show module slot ma pool','show module slot ma pp-slab',
		      'show module slot ma slab']
    # check against support commands
    invalidCmdList = [i for i in cmdList if i not in supportCmdList]
    if invalidCmdList != []: 
	self.myLog.info("Command list '%s' is not supported" %invalidCmdList)
	self.myLog.info("List of suppored commands are %s" %supportCmdList)
	return databasedict

    for cmd in cmdList:
    	self.myLog.info("==================================================================================")
   	self.myLog.info("======= Start collecting memory counters for command %s =======" %cmd)
    	self.myLog.info("==================================================================================")

        if cmd == 'show mem':	
    	    #SHOW MEMORY
    	    shMemory_dict = getshowmemcounters(self)
    	    for slot in shMemory_dict.keys():
	        if slot in globalSlotDict.keys():
	            curDict = globalSlotDict[slot]
	        else:
	            curDict = {}
	        # add new data
	        curDict['sh mem'] = shMemory_dict[slot]

	        # save back to globalSlotDict			
	        globalSlotDict[slot] = curDict
	elif cmd == 'show process mem':
    	    #SHOW PROCESS MEMORY (ONLY FOR SLOT FROM 2-4)
            #pprint(globalSlotDict,indent=4,width=20,depth=20)
            tmpDict = {}
            for slot in slotList:
                processMemory_dict = show_process_memory(self.ssx,slot)
	        # get the current value from the globalSlotDict 
	        if slot in globalSlotDict.keys():
	            curDict = globalSlotDict[slot]
	        else:
	            curDict = {}
	        # add new data
	        curDict['sh proc mem'] = processMemory_dict
	        # save back to globalSlotDict			
	        globalSlotDict[slot] = curDict
	elif cmd == 'show module proc slot ma':
            #SHOW MODULE PROCESS SLOT MA 
            tmpDict = {}
            for slot in slotList:
                modprocma_dict = showmoduleprocessma(self.ssx,slot)
	        # get the current value from the globalSlotDict 
	        if slot in globalSlotDict.keys():
	            curDict = globalSlotDict[slot]
	        else:
	            curDict = {}
	        # add new data
	        curDict['sh mod proc ma'] = modprocma_dict
	        # save back to globalSlotDict			
	        globalSlotDict[slot] = curDict
	elif cmd == 'show module slot ma shared':
            #SHOW MODULE SLOT MA SHARED
            tmpDict = {}
            for slot in slotList:
                modprocmashared_dict = showmoduleprocessmashared(self.ssx,slot)
	        # get the current value from the globalSlotDict 
	        if slot in globalSlotDict.keys():
	            curDict = globalSlotDict[slot]
	        else:
	            curDict = {}
	        # add new data
	        curDict['sh mod proc ma shared'] = modprocmashared_dict
	        # save back to globalSlotDict			
	        globalSlotDict[slot] = curDict
        elif cmd == 'show module slot ma pp':    
            #SHOW MODULE PROCESS SLOT MA PP
            tmpDict = {}
            for slot in slotList:
                modprocmapp_dict = showmoduleprocessmapp(self.ssx,slot)
		if debug:
	    	    print("modprocmapp_dict") 
    		    pprint(modprocmapp_dict,indent=4,width=20,depth=20)
	        # get the current value from the globalSlotDict 
	        if slot in globalSlotDict.keys():
	            curDict = globalSlotDict[slot]
	        else:
	            curDict = {}
	        # add new data
	        curDict['sh mod proc ma pp'] = modprocmapp_dict
	        # save back to globalSlotDict			
	        globalSlotDict[slot] = curDict
        elif cmd == 'show module slot ma pp-slab':    
            #SHOW MODULE PROCESS SLOT MA PP-SLAB
            tmpDict = {}
            for slot in slotList:
                modprocmappslab_dict = showmoduleprocessmappslab(self.ssx,slot)
		if debug:
	    	    print("modprocmappslab_dict") 
    		    pprint(modprocmappslab_dict,indent=4,width=20,depth=20)
	        # get the current value from the globalSlotDict 
	        if slot in globalSlotDict.keys():
	            curDict = globalSlotDict[slot]
	        else:
	            curDict = {}
	        # add new data
	        curDict['sh mod proc ma pp-slab'] = modprocmappslab_dict
	        # save back to globalSlotDict			
	        globalSlotDict[slot] = curDict
        elif cmd == 'show module slot ma slab':    
            #SHOW MODULE PROCESS SLOT MA SLAB
            tmpDict = {}
            for slot in slotList:
                modprocmaslab_dict = showmoduleprocessmaslab(self.ssx,slot)
		if debug:
	    	    print("modprocmaslab_dict") 
    		    pprint(modprocmaslab_dict,indent=4,width=20,depth=20)
	        # get the current value from the globalSlotDict 
	        if slot in globalSlotDict.keys():
	            curDict = globalSlotDict[slot]
	        else:
	            curDict = {}
	        # add new data
	        curDict['sh mod proc ma slab'] = modprocmaslab_dict
	        # save back to globalSlotDict			
	        globalSlotDict[slot] = curDict
        elif cmd == 'show module slot ma pool':    
            #SHOW MODULE PROCESS SLOT MA POOL
            tmpDict = {}
            for slot in slotList:
                modprocmapool_dict = showmoduleprocessmapool(self.ssx,slot)
	        # get the current value from the globalSlotDict 
	        if slot in globalSlotDict.keys():
	            curDict = globalSlotDict[slot]
	        else:
	            curDict = {}
	        # add new data
	        curDict['sh mod proc ma pool'] = modprocmapool_dict
	        # save back to globalSlotDict			
	        globalSlotDict[slot] = curDict

    databasedict['rinfo'] = globalSlotDict

    return databasedict

def checkmemoryhighwatermark(self,diffDict,highwatermark,prevkey=''):
    """
        Description  : This proc accepts four paramters self, diffDict, highwatermark and previous key
    		       and print any difference that is bigger than the specified watermark
        Arguments    : self: a class object that have ssx object to access dut
                     : diffDict:  the dictionary that is returned by calling diffDict
                     : highwatermark (string): limit of how much the difference is allowed
                     : prevkey: default is empty.  Should not pass in this parameter.  Only use by the proc itself
        Usage        : myDict = getcountersforcmd(self,['show process mem','show mem'],slotList=['2','3'],portList=['2/0','2/1','3/0'])
        Return Value : True: if some values are higher that watermark and print to the log
		       False: if no value is higher that watermark
    """
    rc = False
    debug = False
    suffix = ('MB','B','GB','KB')
    if highwatermark.endswith(suffix):
        maxlimit  = convrtToBytes(highwatermark)
    for key in diffDict.keys():
    	keyStr = "%s-%s-" %(prevkey,key)
	if debug:
	    print "keyStr = %s" %keyStr
	val = diffDict[key]
	if debug:
	   print "key %s, val = %s" %(key,val)
    	if isinstance(val,dict):
	    # if is a dictionary, recursive call to traverse down to leaves
	    if checkmemoryhighwatermark(self,val,highwatermark,keyStr):
		rc = True
	else:
	    # is is the list of different values, print them
	    valDiff = abs(int(val[0].replace(",","")) - int(val[1].replace(",","")))
	    if debug:
		print "val0 = %s, val1 = %s, valDiff = %s, maxlimit = %s" %(val[0], val[1], valDiff, maxlimit)
	    if valDiff > maxlimit: 
    	        self.myLog.info("== WARNING - Difference exceeds watermark of %s ==" %maxlimit)
    	        self.myLog.info("'%s' - diff amount %s" %(keyStr,valDiff))
		rc = True
    #print "rc ='%s'" %rc 
    return rc


def elapsetime(t1,t2):
    eltime = int((time.mktime(t2) - time.mktime(t1)) / 3600)
    return eltime

def saveDictToFile(sDict,sFileName):
    """
        Description  : This proc accepts two parameters, sDict the dictionary to save and sFilename
    		       is the file name to save the sDict to
        Arguments    : sDict: dictionary to save
                     : sFilename:  the file name to save the dictionary to
        Usage        : saveDictToFile(oneBaseLineDict,'test1')
        Return Value : none
    """
    fout = open(sFileName, "wb")
    cPickle.dump(sDict,fout)
    fout.close()

def readDictFromFile(sFileName):
    """
        Description  : This proc accepts one parameters, sFilename is the file name to read the dictionary
		       data from
        Arguments    : sFilename:  the file name to read the dictionary data from
        Usage        : rDict = {}
         	       rDict = readDictFromFile('test1')
        Return Value : dictionary read from file
    """
    fout = open(sFileName, "rb")
    rDict = cPickle.load(fout)
    pprint(rDict,indent=4,width=20,depth=20)
    fout.close()
    return rDict

# End section added by Anthony Ton
