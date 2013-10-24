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
DESCRIPTION             : This Script contains following SIP APIs which has been used in the MBC-SIP test cases
			  get_pid
			  cmp_sip_parameters
			  cmp_sip_parameters_option
			  verify_sip_call_detail
			  verify_sip_session
			  verify_sip_session_detail
			   
TEST PLAN               : MBC-SIP Test plan V04
AUTHOR                  : Raja Rathnam; email:rathnam@primesoftsolutionsinc.com
REVIEWER                :
DEPENDENCIES            : Linux.py,SSX.py
"""

import sys, os
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)



from StokeTest import test_case
import pexpect
import time
import misc
import string
import sys
import re
import glob
import calendar
from stat import *

from logging import getLogger
log = getLogger()

#from Host import ConsoleServer
from Linux import *
from SSX import *




class sip_linux(test_case):

    def get_pid(string_one = "none",string_two = "none"):
        """ DESCRIPTION:
            Gets the PID(Process ID) of the running instance using givem strings as filter keywords 
                 
	    usage: get_pid("./sipp","uac")
	"""


	# Grepping for PID according to received  parameters
        if string_two  == "none":
                pid_strg = self.cmd("ps ax | grep %s"%string_one)
        else:
                pid_strg = self.cmd("ps ax | grep %s |grep %s"% (string_one,string_two))
	
	# After excuting the command expecting the promet
        self.ses.expect("[\$\#]")
        pid = self.ses.before
        split_pid = pid.split('\n')
        is_grep = re.findall('grep',split_pid[1])
        if is_grep:
            self.failUnless(is_grep == "grep","Test fail as no SIPp instance found")
        pattern = re.compile('^\d+')
        current_pid = pattern.findall(pid)
        log.debug ("Process id of  Current SIPp process", current_pid[0])

	return current_pid[0]


    def cmp_sip_parameters(self,file_name = "none",sip_type = "none"):

        """ DESCRIPTION:
            The API does the following things
	    1. Catch the SIPp PID                  
	    2. Search for error log along with the PID
	    3. If error log exist test is fail and exit else search for sip log along with PID
            4. Compares the SIP parameters in the sip log and declares Pass/Fail 
   
            usage : cmp_sip_parameters(file_name="msip_ete_001.log",sip_type="uac")
        """



        if sip_type == "none":
               pid_strg =  self.cmd("ps ax | grep ./sipp")
        else:
               pid_strg =  self.cmd("ps ax |grep ./sipp |grep %s"% sip_type)
       
	pid = self.ses.before
        self.cmd("\n")
        self.ses.expect("[\$\#]")
	split_pid = pid.split('\n')
	is_grep = re.findall('grep',split_pid[1]) 
	if is_grep:
	    self.failUnless(is_grep == "grep","test fail due to wrong pid")
        pattern = re.compile('\d+')
        cpid = pattern.findall(pid)
        log.debug ("Please wait, Sleeping for 8 seconds for catching the error log") 
        #Wait to get the errorfile
	time.sleep(8)
        result = self.cmd("ls |grep %s |grep error" % cpid[0])
        result1 = result.split("\n")
	self.failUnless(result1[1] == '',"test fail due to error log file")
        
        if file_name == "none":
                pass
        else:
                resultfile=self.cmd("ls |grep %s" % file_name)
                resultfile1=resultfile.split("\r\n")

                if resultfile[1]:
 	            catOp = self.cmd("cat %s"% file_name)
		
		    no_file = re.findall("No such file or directory",catOp,re.I)	
	            self.failUnless(not no_file,"Failed because log file not found")
                    readFile = catOp
                    mesSent = [];mesReceived = [];sentAllParameters = []
                    actualSent = {};actualReceived = {}

                    splitOp = readFile.split('\n')
                    for line in splitOp:
                                s = line.find('Sent')
                                if s !=  -1:
                                        mesSent.append(line)
                                else:
                                        mesReceived.append(line)
                    for i in range(0,len(mesSent)):
                        index = mesSent[i].find("Sent_")
                        index = index+5
                        mes = mesSent[i][index:]
                        index1 = mes.find("=")
                        sentAllParameters.append(mes[:index1])
                        index2 = index1+1
                        actualSent[mes[:index1]] = mes[index2:]

                    for j in range(0,len(mesReceived)):
                        index = mesReceived[j].find("Recv_")
                        index = index+5
                        me = mesReceived[j][index:]
                        index1 = me.find("=")
                        index2 = index1+1
                        actualReceived[me[:index1]] = me[index2:]

                    for i in range(0,len(sentAllParameters)):


			self.failUnlessEqual(actualSent[sentAllParameters[i]],actualReceived[sentAllParameters[i]],"TESTFAIL due to miss match in sent and recived parameters")





    def cmp_sip_parameters_option(self,file_name = "none",sip_type = "none",option = "yes"):

        """ DESCRIPTION:
            The API does the following things
            1. Catch the SIPp PID
            2. Search for error log along with the PID
            3. With option = yes, if error log exist test is Pass and exit else option = no test is fail.

            usage : cmp_sip_parameters_option(file_name="msip_ete_001.log",sip_type="uac",option="yes")
        """
        

        if sip_type =="none":
                self.cmd("ps ax | grep ./sipp ")
        else:
                self.cmd("ps ax |grep ./sipp |grep %s"% sip_type)
        pid = self.ses.before
        self.cmd("\n")
        self.ses.expect("[\$\#]")
        pattern = re.compile('\d+')
        cpid = pattern.findall(pid)
        log.debug ("Please wait, Sleeping for 8 seconds for catching the error log") 
	#To get errorfile
	time.sleep(8)
        result = self.cmd("ls |grep %s |grep error" % cpid[0])
        result1 = result.split("\n")
	
	if option!="none":

		if option == "yes":
        		self.failUnless(result1[1]!='',"test pass due to error log file")
		elif  option == "no":
			self.failUnless(result1[1] == '',"test fail due to error log file")

#	self.failUnless(result1[1] == '',"test fail due to error log file")
	else:

       	 if file_name == "none":
                	pass
         else:
                resultfile = self.cmd("ls |grep %s" % file_name)
                resultfile1 = resultfile.split("\r\n")

                if resultfile[1]:
                    catOp = self.cmd("cat %s"% file_name)
                    readFile = catOp
                    mesSent = []
                    mesReceived = []
                    sentAllParameters = []
                    actualSent = {}
                    actualReceived = {}
                    splitOp = readFile.split('\n')
                    for line in splitOp:
                                s = line.find('Sent')
                                if s!=-1:
                                        mesSent.append(line)
                                else:
                                        mesReceived.append(line)
                    for i in range(0,len(mesSent)):
                        index = mesSent[i].find("Sent_")
                        index = index+5
                        mes = mesSent[i][index:]
                        index1 = mes.find("=")
                        sentAllParameters.append(mes[:index1])
                        index2 = index1+1
                        actualSent[mes[:index1]] = mes[index2:]

                    for i in range(0,len(mesReceived)):
                        index = mesReceived[i].find("Recv_")
                        index = index+5
                        me = mesReceived[i][index:]
                        index1 = me.find("=")
                        index2 = index1+1
                        actualReceived[me[:index1]] = me[index2:]


	 for i in range(0,len(sentAllParameters)):


                        self.failUnlessEqual(actualSent[sentAllParameters[i]],actualReceived[sentAllParameters[i]],"TESTFAIL due to miss match in sent and recived parameters")







class sip_ssx(test_case):

    def verify_sip_call_detail(self,callee="none",caller="none",call_status="none",handover_state="none",
                        session_handle="none",call_type="none",transferred_to="none",transferred_from="none",
                        rtp_ip_address="none",rtp_port="none"):


                
	""" DESCRIPTION:
	    
	    1.  Executes the Command 'show sip call detail' at SSX
            2.  Pass or fail based on given argument/s is/are available or not in the DETAILS

            usage : verify_sip_call_detail(callee="uac1",caller="uac2",call_status="ACTIVE")
        """

 

        #ssx_output=self.cmd("show sip call detail\n")
        ssx_output=self.cmd("show sip call detail")
        found_error=re.compile("session handle",re.I).findall(ssx_output)

        # Fail the testcase if there is error in out put of the CLI
        if found_error:
            self.failUnless(found_error!="Session Handle","failed due to error in cli \"show sip call detail\"")

        split_output=ssx_output.split("------------------------")
        list=[]
        # Here is the twofold searching of the callee and the caller

        for line in split_output:
            s=line.find(callee)
            if s!=-1:
                 s=line.find(caller)
                 if s!=-1:
                     list.append(line)
                     if call_type!="none":
                         s=line.find(call_type)
                         if s!=1:
                             list.append(line)



        # the Expected values are stired in the dictionray named expected

        expected={'call_type' : call_type,
                  'call_status' : call_status,
                  'callee' : callee,
                  'session_handle': session_handle,
                  'caller': caller,
                  'handover_state': handover_state,'transferred_to':transferred_to,
                  'transferred_from':transferred_from,
                  'rtp_ip_address':rtp_ip_address,'rtp_port':rtp_port
                 }

        #Searching for the details in the ssx output and keeping them in the actual named dictionary
        
        for index in range(0,len(list)):

            handover_state_actual = re.search(r"handover state(\s*):(\s*)(.*)(\r)",list[index],re.I)
	    if handover_state_actual:
	        handover_state_actual=handover_state_actual.group(3)	
            caller_actual = re.search(r"caller(\s*):(\s*)(.*)(\r)",list[index],re.I)
	    if caller_actual :
	        caller_actual = caller_actual.group(3)
            call_type_actual = re.search(r"call type(\s*):(\s*)(.*)(\r)",list[index],re.I)
	    if call_type_actual :
	        call_type_actual = call_type_actual.group(3) 
            call_status_actual = re.search(r"call status(\s*):(\s*)(\w*)(.*)(\r)",list[index],re.I)
	    if call_status_actual :
	        call_status_actual = call_status_actual.group(3) 
            callee_actual = re.search(r"callee(\s*):(\s*)(.*)(\r)",list[index],re.I)
	    if callee_actual :
	        callee_actual = callee_actual.group(3)
            session_handle_actual =re.search(r"session handle(\s*):(\s*)(.*)(\r)",list[index],re.I)
	    if session_handle_actual :
	        session_handle_actual = session_handle_actual.group(3)
            transferred_to_actual =re.search(r"transferred-to(\s*):(\s*)(.*)(\r)",list[index],re.I)
	    if transferred_to_actual :
	        transferred_to_actual = transferred_to_actual.group(3)
            transferred_from_actual  = re.search(r"transferred-from(\s*):(\s*)(.*)(\r)",list[index],re.I)
	    if transferred_from_actual :
	        transferred_from_actual = transferred_from_actual.group(3)
            rtp_ip_address_actual = re.search(r"rtp ip address(\s*):(\s*)(.*)(\r)",list[index],re.I)
	    if rtp_ip_address_actual :
	        rtp_ip_address_actual = rtp_ip_address_actual.group(3)
            rtp_port_actual = re.search(r"rtp port(\s*):(\s*)(.*)",list[index],re.I)
	    if rtp_port_actual :
	        rtp_port_actual = rtp_port_actual.group(3)

            #Adding to the actual dictionary
            actual={index:{'call_type' : call_type_actual,'call_status' : call_status_actual,
                           'callee' : callee_actual,'session_handle' : session_handle_actual,
                           'caller': caller_actual,'transferred_to' : transferred_to_actual,
                           'transferred_from':transferred_from_actual,
                           'rtp_ip_address':rtp_ip_address_actual,'rtp_port':rtp_port_actual,
                           'handover_state': handover_state_actual}}


            #comparing the actual and expected parameters
            for key in actual[index].keys():
                if expected[key]!="none":
                    self.failUnlessEqual(expected[key],actual[index][key],"TESTFAIL due to missmatch in\
                                                                         expected and actual parameters")




    def verify_sip_session(self,service_profile="none",
                       registration_state="none",expires="none",
                       address_of_record="none",domain="none",imsi="none",
                       connection_id="none",handover_state="none",msisdn="none",contact_address="none"):

        """ DESCRIPTION:

            1.  Executes the Command 'show sip session detail imsi ' at SSX
            2.  Pass or fail based on given argument/s is/are available or not in the DETAILS

            usage : verify_sip_session(imsi="uac1",domain="default",registration_state="ACTIVE")
        """


        ssx_output=self.cmd("show sip session detail imsi sipp")

        found_error=re.compile("session handle",re.I).findall(ssx_output)

        # Fail the testcase if there is error in out put of the CLI
        if found_error:
            self.failUnless(found_error!="Session Handle","failed due to error in cli \"show sip call detail\"")


        #the Expected values are stored in the dictionray named expected
        expected={'service_profile': service_profile,
                  'registration_state' : registration_state,
                  'expires' : expires,
                  'address_of_record' : address_of_record,
                  'domain': domain,
                  'imsi': imsi,
                  'msisdn':msisdn
                 }

        #Searching for the details in the ssx_output that is the cli output and keeping them in the actual,named dictionary
        imsi_actual = re.search(r"imsi(\s*):(\s*)(\w*)(.*)",ssx_output,re.I)
	if imsi_actual:
	    imsi_actual = imsi_actual.group(3)		
        msisdn_actual = re.search(r"msisdn(\s*):(\s*)(\w*)(.*)",ssx_output,re.I)
	if msisdn_actual:
	    msisdn_actual = msisdn_actual.group(3)
        domain_actual = re.search(r"domain(\s*):(\s*)(.*)(\r)",ssx_output,re.I)
	if domain_actual:
	    domain_actual = domain_actual.group(3)
        service_profile_actual=re.search(r"service(\s*)profile(\s*):(\s*)(.*)",ssx_output,re.I)
	if service_profile_actual:
	    service_profile_actual = service_profile_actual.group(4)
        registration_state_actual = re.search(r"registration(\s*) state(\s*):(\s*)(\w*)(.*)",ssx_output,re.I)
	if registration_state_actual:
	    registration_state_actual = registration_state_actual.group(4)
        expires_actual=re.search(r"expires(\s*):(\s*)(\w*)(.*)",ssx_output,re.I)
	if expires_actual:
	    expires_actual = expires_actual.group(3)
        address_of_record_actual=re.search(r"address-of-record(\s*):(\s*)(.*)(\r)",ssx_output,re.I)
	if address_of_record_actual:
	    address_of_record_actual = address_of_record_actual.group(3)

        #Adding to the actual dictionary
        actual={'service_profile' : service_profile_actual,
                'registration_state' : registration_state_actual,
                'expires' : expires_actual,
                'address_of_record' : address_of_record_actual,
                'domain': domain_actual,
                'imsi': imsi_actual,
                'msisdn':msisdn_actual
               }


        #comparing the actual and expected parameters
        for key in actual.keys():
            if expected[key]!="none":
                self.failUnlessEqual(expected[key],actual[key],"TESTFAIL due to missmatch in expected and actual parameters")




    def verify_sip_session_detail(self,service_profile="none",registration_state="none",expires="none",
				address_of_record="none",domain="none",imsi="none",connection_id="none",
				handover_state="none",msisdn="none",contact_address="none"):

        """ DESCRIPTION:

            1.  Executes the Command 'show sip session detail ' at SSX
            2.  Pass or fail based on given argument/s is/are available or not in the DETAILS

            usage : verify_sip_session_detail(imsi="uac1",domain="default",registration_state="ACTIVE")
        """


        ssx_output=self.cmd("show sip session detail imsi %s"%imsi)
        found_error=re.compile("error",re.I).findall(ssx_output)

        # Fail the testcase if there is error in out put of the CLI
        if found_error:
            self.failUnless(found_error=="ERROR","failed due to error in cli \"show sip call detail\"")



	# the Expected values are stored in the dictionray named expected
        expected={'service_profile' : service_profile,
                 'registration_state' : registration_state,
                 'expires' : expires,
                 'address_of_record' : address_of_record,
                 'domain': domain,
		 'imsi': imsi,
                 'msisdn':msisdn
                }

	#Searching for the details in the ssx_output that is the cli output and keeping them in the actual,named dictionary
        

        imsi_actual = re.search(r"imsi(\s*):(\s*)(\w*)(.*)",ssx_output,re.I)
        if imsi_actual:
            imsi_actual = imsi_actual.group(3)
        msisdn_actual = re.search(r"msisdn(\s*):(\s*)(\w*)(.*)",ssx_output,re.I)
        if msisdn_actual:
            msisdn_actual = msisdn_actual.group(3)
        domain_actual = re.search(r"domain(\s*):(\s*)(.*)(\r)",ssx_output,re.I)
        if domain_actual:
            domain_actual = domain_actual.group(3)
        service_profile_actual=re.search(r"service(\s*)profile(\s*):(\s*)(.*)",ssx_output,re.I)
        if service_profile_actual:
            service_profile_actual = service_profile_actual.group(4)
        registration_state_actual = re.search(r"registration(\s*) state(\s*):(\s*)(\w*)(.*)",ssx_output,re.I)
        if registration_state_actual:
            registration_state_actual = registration_state_actual.group(4)
        expires_actual=re.search(r"expires(\s*):(\s*)(\w*)(.*)",ssx_output,re.I)
        if expires_actual:
            expires_actual = expires_actual.group(3)
        address_of_record_actual=re.search(r"address-of-record(\s*):(\s*)(.*)(\r)",ssx_output,re.I)
        if address_of_record_actual:
            address_of_record_actual = address_of_record_actual.group(3)

        #Adding to the actual dictionary
        actual={'service_profile' : service_profile_actual,
                'registration_state' : registration_state_actual,
                'expires' : expires_actual,
                'address_of_record' : address_of_record_actual,
                'domain': domain_actual,
                'imsi': imsi_actual,
                'msisdn':msisdn_actual
               }

	#comparing the actual and expected parameters
        for key in actual.keys():
                if expected[key]!="none":

                        self.failUnlessEqual(expected[key],actual[key],"TESTFAIL due to miss match in expected and actual parameters the expected is = %s  actual is = %s "%(expected[key],actual[key]))


	
