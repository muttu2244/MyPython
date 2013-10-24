#!/usr/bin/python2.5

### Import the system libraries we need.
import sys, os, re

### path.
mydir = os.path.dirname(__file__)
qa_lib_dir = mydir
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)
from logging import getLogger
# grab the root logger.
log = getLogger()


def verify_attach(self,cntxt,num):
        """Verify total number of attaches at given context"""

        self.cmd("context %s"%cntxt)
        ranap = self.cmd("show mdo counters detail ranap | grep Initial")
        ranap = ranap.splitlines()
	num1 = 0
        for j in range(1, len(ranap)):
                m = ranap[j].split(':')[-1]
                num1 = int(num1)+ int(m)
        num1 = num1/2
        count = self.cmd("show mdo session counter")
        count = count.splitlines()[-2]
        count= count.split(' ')[20]
        if (int(count) == int(num) and int(num) == num1):
                return True 
        else:
                return False , int(count), int(num), int(num1)

def verify_active_session(self,num):
	"""Verify total number of active mdo sessions in all contexts"""

	sess= self.cmd("show session | grep GTP | count")
	sess = sess.split(':')[1]
	count = self.cmd("show mdo session counter")
        count = count.splitlines()[-2]
        count= count.split(' ')[9]
	if (int(count) == int(num) and int(num) == int(sess)):
                return True, int(count) 
        else:
                return False

def verify_active_session_cntx(self,cntx,num):
        """Verify total number of active mdo sessions in all contexts"""

        sess= self.cmd("show session | grep GTP | count")
        sess = sess.split(':')[1]
        count = self.cmd("show mdo session counter")
        count = count.splitlines()[-2]
        count= count.split(' ')[9]
        if (int(count) == int(num) and int(num) == int(sess)):
                return True, int(count)
        else:
                return False


######################################################

def verify_offload_criteria(self, context="mdo123", filter_id=1, count=1):
	""" Verify the number of sessions offloaded per filter under context,
	    It needs context, filter_id and count inputs.
            On success return 0, on failure return 1 and log the number sessions offloaded for the filter.
	    Example: verify_offload_criteria(self.ssx,context="context_name", filter_id=num, count=Cnt)
        """
	
	handleList = []
	filterCnt = 0
	self.cmd("context %s"%context)
	sessHndl = self.cmd('show mdo session | grep -i "Session Handle"')
	if "ERROR" in sessHndl:
		log.error("No sessions found on any Card for the context %s"%context)
		return 1
	sessHndl = sessHndl.splitlines()
	for handleIndex in range(1,len(sessHndl)):
		#handleList = handleList + sessHndl[handleIndex].split(':')[1].strip()
		handleList.append(sessHndl[handleIndex].split(':')[1].strip())
	for handle in handleList:
		offloadOp = self.cmd('show mdo session detail handle %s | grep -i "Filter %s"'%(handle, filter_id))
		if "Filter" in offloadOp:
			filterCnt = filterCnt + 1
	if int(filterCnt) == count:
		return 0
	else:
		log.error("offload criteria for the filter %s is %s less than expected"%(filter_id, filterCnt))
		return 1


def get_count_OlFilters(self,context):
	""" Let me write API First """
	if not context:
		log.error("Please provide the context name")
		return 127
	contOp = self.cmd("context %s"%context)
	if "ERROR" in contOp:
		log.error("Cannot find context '%s'"%context)
		return 255
	# Let me go ahead 
	handleList = []
	filterList = []
	countList = []
        sessHndl = self.cmd('show mdo session | grep -i "Session Handle"')
        if "ERROR" in sessHndl:
                log.error("No sessions found on any Card for the context %s"%context)
                return 1
        sessHndl = sessHndl.splitlines()
        for handleIndex in range(1,len(sessHndl)):
                handleList.append(sessHndl[handleIndex].split(':')[1].strip())
        for handle in handleList:
		offloadOp = self.cmd('show mdo session detail handle %s'% handle)
		reOp = re.search("Offload\s+Criteria\s+:\s+Filter\s+(\d+)",offloadOp)
		if not reOp:
			log.error("Cannot find the Offload Criteria for the session handle: %s"%handle)
		if reOp:
			filterId = reOp.group(1)
			if filterId not in filterList:
				filterList.append(filterId)
				countList.append(1)
			else:
				cntIndex = filterList.index(filterId)
				countList[cntIndex] = countList[cntIndex] + 1
				
	return filterList, countList			

def get_mdo_ses_counters(self,handle=""):
	""" Let me write API first """
	lines = self.cmd("show session counters handle %s"  % handle)
	print lines
	if lines and "ERROR:" not in lines:
		if '@' in lines:
			split_lines=lines.split('@')[1].split()
			rx_pkts=split_lines[2]
			tx_pkts=split_lines[3]
           	else:
              		split_lines=lines.splitlines()[-1].split()
			rx_pkts=split_lines[-4]
                        tx_pkts=split_lines[-3]
		return int(rx_pkts), int(tx_pkts)
        else:
           return False


def get_session_list(self,handle=False,sesIp=False,sesStatus=False,localIp=False,localTEID=False,remoteIp=False,remoteTEID=False):
	""" Let me write API first """
	sessionList = []
	sesVar = ""
	sessionOp = self.cmd("show mdo session")
	if "ERROR" in sessionOp: # Exit the API, if there is no session
		return 1

	sessionOp = sessionOp.split('SLOT')
	for sessionIndex in range(1,len(sessionOp)):
		### Need to continue from here
		if handle==True:
			op = re.search("\s+Session\s+Handle\s+:\s+([xX]|[0-9a-fA-F]+)",sessionOp[sessionIndex])
			if op:
				sesVar = op.group(1)

		if sesIp==True:
			op = re.search("\s+Sess\s+IP\s+:\s+(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5]))",sessionOp[sessionIndex])
			if op:
				sesVar = sesVar + " %s"%op.group(1)

		if sesStatus==True:
			op = re.search("\s+Sess\s+Status\s+:\s+([a-zA-Z]+)",sessionOp[sessionIndex])
			if op:
				sesVar = sesVar + " %s"%op.group(1)

		if localIp==True:
			op = re.search("\s+Local\s+IP\s+:\s+(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5]))",sessionOp[sessionIndex])
			if op:
				sesVar = sesVar + " %s"%op.group(1)

		if localTEID==True:
			op = re.search("\s+Local\s+TEID\s+:\s+(0[xX][0-9a-fA-F]+)",sessionOp[sessionIndex])
			if op:
				sesVar = sesVar + " %s"%op.group(1)

                if remoteIp==True:
                        op = re.search("\s+Remote\s+IP\s+:\s+(([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5])\.([01]?\d\d?|2[0-4]\d|25[0-5]))",sessionOp[sessionIndex])
                        if op:
                                sesVar = sesVar + " %s"%op.group(1)

		if remoteTEID==True:
			op = re.search("\s+Remote\s+TEID\s+:\s+(0[xX][0-9a-fA-F]+)",sessionOp[sessionIndex])
			if op:
				sesVar = sesVar + " %s"%op.group(1)

		#Add to list
		sessionList.append(sesVar)

	if sessionList:
		return sessionList
	
	return 1

def verify_mem_leak(self):
	""" Let me write API first """

        contOp = self.cmd("show context")
        contOp = contOp.splitlines()[-1].split()[0]
        self.cmd("context local")
	self.wait4cards()
	# Get the Slot index
	slotOp = self.cmd('show card | grep GLC')
	slotOp = slotOp.splitlines()
	slotList = []
	for si in range(1,len(slotOp)):
		slotList.append(int(slotOp[si].split()[0]))

        totalSes = self.cmd("show session | grep GTP | count")
        totalSes = totalSes.split(':')[1].strip()
        ppCnt = 0
        for slotIndex in slotList:
                ppOp = self.cmd('show module mdo slot %s ma pp detail | begin "RNC Pool" | grep "Elements In Use"'%slotIndex)
                op = re.search("\s+Elements\s+In\s+Use\.*([0-9.]+)",ppOp.splitlines()[1])
                ppCnt = ppCnt + int(op.group(1))

        # Verify the Pools
        if int(ppCnt) != int(totalSes):
                #log.error("Memory leak is happened - number_of_session != number_mem_alloc")
		return 0
        else:
                #log.info("As of now, we have not seen any memory leak")
		return 1


def get_ranap_stats(self,slot):
	""" Let me write API first """
	
	regex_list=['\s*Stats\s+Ctxt\s+Id\s+:\s*(?P<context_id>\d+)',
                '\s*Stats\s+Slot\s+:\s*(?P<slot>\d+)',
                '\s*Packets\s+Sent\s+:\s*(?P<pkts_sent>\d+)',
                '\s*Packets\s+Received\s+:\s*(?P<pkts_rxed>\d+)',
                '\s*Initial\s+UE\s+Sent\s+:\s*(?P<init_ue_sent>\d+)',
                '\s*Initial\s+UE\s+Received\s+:\s*(?P<init_ue_rxed>\d+)',
                '\s*Direct\s+Transfer\s+Sent\s+:\s*(?P<direct_transfer_sent>\d+)',
                '\s*Direct\s+Transfer\s+Received\s+:\s*(?P<direct_transfer_rxed>\d+)',
                '\s*Common\s+ID\s+Sent\s+:\s*(?P<common_id_sent>\d+)',
                '\s*Common\s+ID\s+Received\s+:\s*(?P<common_id_rxed>\d+)',
                '\s*RAB\s+Assignment\s+Request\s+Sent\s+:\s*(?P<rab_req_sent>\d+)',
                '\s*RAB\s+Assignment\s+Request\s+Received\s+:\s*(?P<rab_req_rxed>\d+)',
                '\s*RAB\s+Assignment\s+Response\s+Sent\s+:\s*(?P<rab_resp_sent>\d+)',
                '\s*RAB\s+Assignment\s+Response\s+Received\s+:\s*(?P<rab_resp_rxed>\d+)',
                '\s*Connection\s+Release\s+Sent\s+:\s*(?P<conn_release_sent>\d+)',
                '\s*Connection\s+Release\s+Received\s+:\s*(?P<conn_release_rxed>\d+)']

	actual={}
	ssx_output = self.cmd("show mdo counters detail ranap slot %s"  % slot)

	for regex in regex_list:
	        obj=re.compile(regex,re.I)
	        m=obj.search(ssx_output)
	        if m:
	             dict=m.groupdict()
	             for key in dict.keys():
	                 actual[key]=dict[key]
	return actual

def get_sm_stats(self,slot):
	""" Let me write API first """
	
	regex_list=['\s*Stats\s+Ctxt\s+Id\s+:\s*(?P<context_id>\d+)',
                '\s*Stats\s+Slot\s+:\s*(?P<slot>\d+)',
                '\s*Activate\s+PDP\s+Context\s+Request\s+:\s*(?P<activate_pdp_req>\d+)',
		'\s*Activate\s+PDP\s+Context\s+Accept\s+:\s*(?P<activate_pdp_accept>\d+)',
                '\s*Activate\s+PDP\s+Context\s+Reject\s+:\s*(?P<activate_pdp_reject>\d+)',
                '\s*De-Activate\s+PDP\s+Context\s+Request\s+from\s+SGSN\s+:\s*(?P<deactivate_req_sgsn>\d+)',
                '\s*De-Activate\s+PDP\s+Context\s+Request\s+from\s+UE\s+:\s*(?P<deactivate_req_ue>\d+)',
                '\s*De-Activate\s+PDP\s+Context\s+Accept\s+from\s+SGSN\s+:\s*(?P<deactivate_accept_sgsn>\d+)',
                '\s*De-Activate\s+PDP\s+Context\s+Accept\s+from\s+UE\s+:\s*(?P<deactivate_accept_ue>\d+)',
                '\s*Modify\s+PDP\s+Context\s+Request\s+from\s+SGSN\s+:\s*(?P<modify_req_sgsn>\d+)',
                '\s*Modify\s+PDP\s+Context\s+Request\s+from\s+UE\s+:\s*(?P<modify_req_ue>\d+)',
                '\s*Modify\s+PDP\s+Context\s+Accept\s+from\s+SGSN\s+:\s*(?P<modify_accept_sgsn>\d+)',
                '\s*Modify\s+PDP\s+Context\s+Accept\s+from\s+UE\s+:\s*(?P<modify_accept_ue>\d+)',
                '\s*Modify\s+PDP\s+Context\s+Reject\s+from\s+SGSN\s+:\s*(?P<modify_reject_sgsn>\d+)',
                '\s*Modify\s+PDP\s+Context\s+Reject\s+from\s+UE\s+:\s*(?P<modify_reject_ue>\d+)']

	actual={}
	ssx_output = self.cmd("show mdo counters detail sm slot %s"  % slot)

	for regex in regex_list:
	        obj=re.compile(regex,re.I)
	        m=obj.search(ssx_output)
	        if m:
	             dict=m.groupdict()
	             for key in dict.keys():
	                 actual[key]=dict[key]
	return actual


def verify_count_mdo_context(self,count = "250"):

        """
          Description: - This API verify "show context summary" and the expected number of
                         contexts with  exact count and returns true or false
          CLI Used- CLI.s that are used for the API  <show context summary>.
          Input: -  expected context count
          Output: - returns true or false
          Author: -  Ganapathi.
          Reviewer: -                      
        """

        returnVal = "false"
        ret_str=self.cmd("sh context summary")
        log.output(ret_str)
        line_list = ret_str.split("\n")
        for line in line_list:
            if "Total number of configured context" in line:
                count = line.split(":")
                if count[1].strip() == contextCount:
                    returnVal =  "true"
                    break
        return returnVal

def verify_active_context(self,contextNamelist = ["local","InactiveContext1"]):

        """
          Description: -  This API verify "show context all" taking active context
                         names list and verifies the corresponding contexts are active or not
                         returns true or false
          CLI Used     -  CLI.s that are used for the API  <show context all>.
          Input:       -  list of active contexts lists need to be verified
          Output:      -  returns true or false
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """

        failedList  = []
        ret_str=self.cmd("sh context all")
        log.output(ret_str)
        line_list = ret_str.split("\n")
        for contextName in contextNamelist:
            status = "false"
            for line in line_list:
                if "sh context all" in line:
                    continue
                if "Index" in line:
                    continue
                if contextName in line:
                    status = "true"
                    break
                else:
                    status = "false"
            if status == "false":
                failedList.append(contextName)
            
        if len(failedList) > 0:
            log.output("Error: Following Contexts are not active %s" %str(failedList))
            return "false"
        else:
            return "true"


def verify_count_mdo_context(self,count = "250"):

        """
          Description: -  This API runs cli "sh conf | grep -i "mdo enable" | count" 
                          for verifying the number of mdo enabled contexts
          CLI Used     -  CLI.s that are used for the API  <sh conf | grep -i "mdo enable>.
          Input:       -  expected number of mdo enabled contexts 
          Output:      -  returns true or false
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """

        ret_str =self.cmd("sh conf | grep -i \"mdo enable\" | count")
        log.output(ret_str)
        line_list = ret_str.split("\n")
        status = "false"
        for line in line_list:
            if "Count" in line:
                wordList = line.split(":")
                if wordList[1].strip() == count:
                    return "true"
                else:
                    return "false"
        return status


def verify_snmp_status(self,snmpCommunityName = "snmp_com1",ssxMgmtIp = "172.16.24.16"):

        """
          Description: -  This API runs cli on Linux PC where SNMP installed
                          "snmpget -c communityName -v 2c mgmtIpOfSSX snmpEngineID.0" and
                          verifies the status of SNMP server running on SSX
          CLI Used     -  CLI.s that are used for the API  show snmp server.
          Input:       -  NONE
          Output:      -  returns true or false
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """
        ret_str = self.cmd("snmpget -c %s -v 2c %s snmpEngineID.0" %(snmpCommunityName,ssxMgmtIp))
        log.output(ret_str)
        line_list = ret_str.split("\n")
        status = "false"
        for line in line_list:
            if "SNMP-FRAMEWORK-MIB::snmpEngineID.0" in line:
                return "true"
            if "Timeout" in line:
                return "false"
        return status



def verify_ha_red_log(self,slot = "2",minTimeTowaitforLog = "4",timeStampwhenRebooted = "Tue Dec 20 2010 19:36:36 UTC"):

        """
          Description: -  This API searches the log for text  \"INFO HaMgr-REDUNDANCY_GAINED\" and 
                          confirms whether the rebooted card come back to completely redundency state
                          Here I will be searching for the above log message and also for testing the newness
                          of the message , I am comparing the timestamps ,the time when the card got rebooted and the time
                          the message arrived and difference should be less than minTimeTowaitforLog mins
          CLI Used     -  Show log | grep \"INFO HaMgr-REDUNDANCY_GAINED\" 
          Input:       -  slotNum -- Slot num of card that got rebooted
                          minTimeTowaitforLog   - time waited after reboot before calling this API
                          timeStampwhenRebooted - time stamp when the card got rebooted in above format
                                                   Tue Dec 20 2010 19:36:36 UTC                                                                                    
          Output:      -  returns true or false
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """
        
        if slot == "2":
            slotNum = "100"
        else:
            slotNum = "101"
         
        timelist = timeStampwhenRebooted.split()
        timestr = "%s %s %s %s %s" %(timelist[0],timelist[1],timelist[2],timelist[4],timelist[3])
        timetuple = time.strptime(timestr)
        timeinsec= time.mktime(timetuple) 
                

        ret_str = self.cmd("show log | grep -i \"INFO HaMgr-REDUNDANCY_GAINED\"")
        log.output(ret_str)
        line_list = ret_str.split("\n")
        status = "false"
     
        searchStr = "Grp 1 logical slot %s" %slotNum
        timeinsecList = []
        timelist1 = []
        for line in line_list:
            if searchStr in line:
                timelist1 = line.split()
                timestr  = "%s %s %s %s %s" %(timelist[0],timelist1[0],timelist1[1],timelist1[2],timelist[3])
                timetuple = time.strptime(timestr)
                timeinsec1 = time.mktime(timetuple)
                timeinsecList.append(timeinsec1)
        if len(timeinsecList) > 0:
            timeinsecList.sort()
            timediff = int(timeinsecList[-1]) - int(timeinsec)
            timediff = timediff / (60)
            if timediff < 4:
                return "true"
            else:
                log.output("Error: No New Log messages generated in HA Redundency Logs")
                return "false"
        else:
            log.output("Error: No Log messages generated in HA Redundency Logs")
            return "false"


def verify_sctp_asscociations(self,contextSlotIpList):

        """
          Description: -  This API verifies the sctp associations status in every context
          CLI Used     -  show mdo sctp-associations
          Input:       -  contextSlotIpList - This is a list of lists where each list will 
                          having following information.
                          (contextname,slotnum,rncIp,sgsnIp)
                          Eg: 
                          contextSlotIpList = [ ("mdo1","02","60.11.10.20","70.11.10.20"),
                                                ("mdo1","02","60.11.10.21","70.11.10.20"),
                                                ("mdo1","03","60.11.10.22","70.11.10.21") ]
          Output:      -  returns true or false
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """
        
            
        successList = []
        for element in contextSlotIpList:
            
            ret_str = self.cmd("context %s" %element[0])
            ret_str = self.cmd("show mdo sctp-associations")
            log.output(ret_str)
            line_list = ret_str.split("\n")
            sgsnStatus = "false"
            rncStatus  = "false"
            regex1='\s*%s\s*\d+\s+SGSN\s+%s\s*\-\s*%s(.*)' %(element[1],element[2],element[3])
            regex2='\s*%s\s*\d+\s+RNC\s+%s\s*\-\s*%s(.*)' %(element[1],element[2],element[3])

            for line in line_list:
                obj1=re.compile(regex1,re.I)
                m1=obj1.search(line)
                obj2=re.compile(regex2,re.I)
                m2=obj2.search(line)
                if m1:
                    if re.compile("\d+:\d+:\d+",re.I).search(m1.group(1)):
                        sgsnStatus = "true"
                    else:
                        sgsnStatus = "false"
                if m2:
                    if re.compile("\d+:\d+:\d+",re.I).search(m2.group(1)):
                        rncStatus = "true"
                    else:
                        print m2.group(1)
                        rncStatus = "false"
                
            if sgsnStatus == "false" or rncStatus == "false":
                log.output("Error: Following association not found %s" %str(element))
            else:
                successList.append("success")

        if len(contextSlotIpList) == len(successList):
            return "true"
        else:
            return "false" 
         


def verify_ssx_cdr_stats(self,verifyDict):

        """
          Description: -  This API verifies CDR stats counters on SSX and reports
                          whether these counters are keep on incrementing
 
          CLI Used     -  show cdr statistics all
          Input:       -  verifyDict 
                          This dictionary needs to be populated based on requirement
                          Eg:
                          If wanted to verify counters for the first time:
                          verifyDict["files_written"]  = "0"
                          verifyDict["files_uploaded"] = "0"
                          if wanted to verify increment counters with some existing counters   
                          verifyDict["files_written"]  = "15"
                          verifyDict["files_uploaded"] = "14"
          Output:      -  returns ret_dict ( dictionary ) having the following indexnames and values
                          ret_dict["files_written"]    = "15"
                          ret_dict["files_uploaded"]   = "14"
                          ret_dict["Status"]           = "false"
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """
        
            
        ret_dict = { }
        ret_str = self.cmd("show cdr statistics all")
        line_list = ret_str.split("\n")
        for line in line_list:
            if "files written" in line:
                ret_dict["files_written"] = line.split(":")[1].strip()
            if "files uploaded" in line:
                ret_dict["files_uploaded"] = line.split(":")[1].strip()
            if "files removed" in line:
                ret_dict["files_removed"] = line.split(":")[1].strip()
            if "files renamed" in line:
                ret_dict["files_renamed"] = line.split(":")[1].strip()

        if ret_dict["files_written"] == "0" and ret_dict["files_uploaded"] == 0 :
                log.out("Error:No CDR files getting generated")
        else:
            if verifyDict["files_written"] == "0" and verifyDict["files_uploaded"] == 0 :
                if int(ret_dict["files_written"])  >  0  and int(ret_dict["files_uploaded"]) > 0 :
                    ret_dict["Status"] = "true"
                else:     
                    ret_dict["Status"] = "false"
                    log.out("Error:No CDR files getting generated")
            else:
                if int(ret_dict["files_written"]) > int(verifyDict["files_written"] == "0") and int(ret_dict["files_uploaded"]) > int(verifyDict["files_uploaded"]):
                    ret_dict["Status"] = "true"
                else:
                    ret_dict["Status"] = "false"
                    log.out("Error:No New  CDR files getting generated")   
                      
        return ret_dict


def verify_ssx_rad_stats(self,serverIp,radPortList,verifyDict):

        """
          Description: -  This API verifies Radius stats counters on SSX and reports
                          whether these counters are keep on incrementing.Here I am
                          verifying only AccStart , AccStop and AccStRsp on port based
          CLI Used     -  show radius counters
          Input:       -  verifyDict 
                          This dictionary needs to be populated based on requirement
                          Eg:
                          If wanted to verify counters for the first time:
                          for portNum in portList:
                             verifyDict["%s_AccStart" %portNum]  = "0"
                             verifyDict["%s_AccStop"  %portNum]  = "0"
                             verifyDict["%s_AccStRsp" %portNum]  = "0"
                          if wanted to verify increment counters with some existing counters   
                             populate verifyDict with ret_dict returned by prev call of this API
          Output:      -  returns ret_dict ( dictionary ) having the following indexnames and values
                          ret_dict["%s_AccStart" %portNum]  =  "15"
                          ret_dict["%s_AccStop"  %portNum]   = "14"
                          ret_dict["%s_AccStRsp" %portNum]    = "0"
                          ret_dict["Status"]           = "false"
                          This ret_dict will become the argument in place of verifyDict in next
                          Call
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """
        
        ret_dict = { }
        ret_str = self.cmd("show radius counters")
        splitList = ret_str.split("%s" %serverIp)
        for portNum in radPortList:
            for element in splitList:
                element = element.strip()
                if portNum in element:
                    elementList = element.split("\n")
                    ret_dict['%s_AccStart' %portNum] = elementList[-1].strip().split()[0].strip()
                    ret_dict['%s_AccStop' %portNum] = elementList[-1].strip().split()[1].strip()
                    ret_dict['%s_AccStRsp' %portNum] = elementList[-1].strip().split()[2].strip()
                    if int(verifyDict['%s_AccStart' %portNum]) == 0 and int(verifyDict['%s_AccStop' %portNum]) == 0 and int(verifyDict['%s_AccStRsp' %portNum]) == 0:
                        if int(ret_dict['%s_AccStart' %portNum]) > 0 and int(ret_dict['%s_AccStop' %portNum]) > 0 and int(ret_dict['%s_AccStRsp' %portNum]) > 0:
                            ret_dict['Status'] = "true"
                        else:
                            ret_dict['Status'] = "false"
                            log.out("Error:No Radius messages are generated")
                            
                    else:
                        if int(ret_dict['%s_AccStart' %portNum]) > int(verifyDict['%s_AccStart' %portNum]) and int(ret_dict['%s_AccStop' %portNum]) > int(verifyDict['%s_AccStop' %portNum]) and int(ret_dict['%s_AccStRsp' %portNum]) > int(verifyDict['%s_AccStRsp' %portNum]):
                            ret_dict['Status'] = "true"
                        else:
                            ret_dict['Status'] = "false"
                            log.out("Error:No New Radius messages are generated for portNum %s" %portNum)
        return ret_dict                    


def Verify_Active_sess_count(self,contextName = "RAN1",sessionCount = "5000"):
        """
          Description: -  This API verifies no of offloaded sessions in a context and returns
                          true or false based on the expected value.
          CLI Used     -  sh sess | grep "GTP" | count

          Input:       -  contextName
                          sessionCount
          Output:      -  returns true or false
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """
        self.cmd("context %s" %contextName)
        ret_str = self.cmd("sh sess | grep \"GTP\" | count")
        lineList = ret_str.split("\n")
        for line in lineList:
            if "Count" in line:
                noOfSessions  = line.split(":")[1].strip()
                break
        if noOfSessions != sessionCount:
            return "false"
        else:
            return "true"


def verify_ssx_traffic_count(self,ueList,verifyDict):

        """
          Description: -  This API verifies session traffic counters on SSX and reports
                          whether these counters are keep on incrementing.Here I am
                          verifying only RxPkts , TxPkts on UE based
          CLI Used     -  show session counters
          Input:       -  verifyDict 
                          This dictionary needs to be populated based on requirement
                          Eg:
                          If wanted to verify counters for the first time:
                          for ue in ueList:
                             verifyDict["ContextName"]       = "local"
                             verifyDict["%s_RcvPkts" %ue]    = "0"
                             verifyDict["%s_XmitPkts"  %ue]  = "0"
                          if wanted to verify increment counters with some existing counters   
                             populate verifyDict with ret_dict returned by prev call of this API
          Output:      -  returns ret_dict ( dictionary ) having the following indexnames and values
                          ret_dict["%s_RcvPkts" %ue]  =  "15"
                          ret_dict["%s_XmitPkts"  %ue]   = "14"
                          ret_dict["Status"]           = "false"
                          This ret_dict will become the argument in place of verifyDict in next
                          Call
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """
        
        ret_dict = { }
        ret_dict['ContextName'] = verifyDict['ContextName']
        ret_str = self.cmd("context %s" %verifyDict['ContextName'])
        ret_str = self.cmd("show session counters")
        splitList = ret_str.split("\n")
        ret_dict['Status'] = "true"
        for ue in ueList:
            regex= "\s*%s\s+\w+\s+(\d+)\s+(\d+)\s+\d+\s+\d+" %ue
            for line in splitList:
                obj=re.compile(regex,re.I)
                m=obj.search(line)
                if m:
                    ret_dict['%s_RcvPkts' %ue] =  m.group(1) 
                    ret_dict['%s_XmitPkts' %ue] = m.group(2)
                    if int(verifyDict['%s_RcvPkts' %ue]) == 0 and int(verifyDict['%s_XmitPkts' %ue]) == 0:
                        if int(ret_dict['%s_RcvPkts' %ue]) > 0 and int(ret_dict['%s_XmitPkts' %ue]) > 0 :
                            ret_dict['Status'] = "true"
                        else:
                            ret_dict['Status'] = "false"
                            log.out("Error:No through UE %s" %ue)
                            
                    else:
                        if int(ret_dict['%s_RcvPkts' %ue]) > int(verifyDict['%s_RcvPkts' %ue]) and int(ret_dict['%s_XmitPkts' %ue]) > int(verifyDict['%s_XmitPkts' %ue]):
                            ret_dict['Status'] = "true"
                        else:
                            ret_dict['Status'] = "false"
                            log.out("Error:Traffic Stopped flowing through  %s" %ue)
        return ret_dict                    



def verify_redirect_traffic_count(self,verifyDict):

        """
          Description: -  This API verifies verifies ACL redirect traffic counters on SSX and reports
                          whether these counters are keep on incrementing.Here I am
                          verifying redirect traffic counters on SSX based on ACL name
          CLI Used     -  sh ip access-list  name acl1 counters 
          Input:       -  verifyDict 
                          This dictionary needs to be populated based on requirement
                          Eg:
                          If wanted to verify counters for the first time:
                          verifyDict['context']       = "CONTEXT1" 
                          verifyDict['%s_redirectPkts' %aclName]  = "0"
                          if wanted to verify increment counters with some existing counters   
                             populate verifyDict with ret_dict returned by prev call of this API
          Output:      -  returns ret_dict ( dictionary ) having the following indexnames and values
                          ret_dict['%s_redirectPkts' %aclName]  =  "15"
                          ret_dict["Status"]                    = "false"
                          This ret_dict will become the argument in place of verifyDict in next
                          Call
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """
        
        ret_dict = { }
        ret_str = self.cmd("context %s" %verifyDict['context'])
        ret_dict['ContextName'] = verifyDict['ContextName']
        ret_dict['Status'] = "false"
        ret_str = self.cmd("sh ip access-list  name %s counters" %verifyDict['acl'])
        splitList = ret_str.split("\n")
        aclName   = verifyDict['acl']
        regex= "\s*\d+\s+\d+\s+(\d+)\s+\d+\s+\d+\s+\d+"
        for line in splitList:
            obj=re.compile(regex,re.I)
            m=obj.search(line)
            if m:
                ret_dict['%s_redirectPkts' %aclName] =  m.group(1) 
                if int(verifyDict['%s_redirectPkts' %aclName]) == 0:
                    if int(ret_dict['%s_redirectPkts' %aclName]) > 0:
                        ret_dict['Status'] = "true"
                    else:
                        ret_dict['Status'] = "false"
                        #log.out("Error:No through redirect ACL  %s" %aclName)
                        print "Error:No Traffic  through redirect ACL  %s" %aclName
                else:
                    if int(ret_dict['%s_redirectPkts' %aclName]) > int(verifyDict['%s_redirectPkts' %aclName]):
                        ret_dict['Status'] = "true"
                    else:
                        ret_dict['Status'] = "false"
                        #log.out("Error:Traffic Stopped flowing through  redirect ACL  %s" %aclName)
                        print "Error:Traffic Stopped flowing through  redirect ACL  %s" %aclName 
        return ret_dict                    


def verify_ssx_ranap_rate(self,contextName,slotNum,expectedRate,tolerance):

        """
          Description: -  This API verifies SSX recieving rate based on slot Num
                          on SSX with expected rate based on tolerance in percent
          CLI Used     -  sh mdo counters detail ranap slot 2 | grep RANAP
          Input:       -  contextName   - name of the context this command need to be run
                          slotNum       - slotnum (part of the command)
                          expectedRate  - rate expected 
                          tolerance     - in percent
                          
          Output:      -  returns true or false
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """
        ret_str = self.cmd("sh mdo counters detail ranap slot %s internal | grep RANAP" %slotNum)
        splitList = ret_str.split("\n")
        currentRecieveRate = "0"
        for line in splitList:
            if "Current RANAP msg recieving rate" in line:
                currentRecieveRate = line.split(":")[1].strip()
		currentRecieveRate = int(currentRecieveRate) / 60 #converting to per sec

            
        MaxExpectedRate = int(expectedRate)  + ((int(expectedRate) *  int(tolerance)) / 100 )
        MinExpectedRate = int(expectedRate)  - ((int(expectedRate) * int(tolerance)) / 100 )
        ret_dict = { }
        if int(currentRecieveRate) > MinExpectedRate and int(currentRecieveRate) < MaxExpectedRate:
            return "true"
        else:
            print "Error: Expected Rate between %s and %s but actual is %s" %(MinExpectedRate,MaxExpectedRate,currentRecieveRate)
            return "false"


def getUeList(self,context = "CONTEXT1"):
        """
          Description: -  This API verifies SSX recieving rate based on slot Num
                          on SSX with expected rate based on tolerance in percent
          CLI Used     -  sh mdo counters detail ranap slot 2 | grep RANAP
          Input:       -  contextName   - name of the context this command need to be run
                          slotNum       - slotnum (part of the command)
                          expectedRate  - rate expected 
                          tolerance     - in percent
                          
          Output:      -  returns true or false
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """

        ret_str = self.cmd("ter len infi")
        ret_str = self.cmd("context %s" %context)
        ret_str = self.cmd("sh sess",timeout = 20000)
        lineList = ret_str.split("\n")
        regex = "\s*GTP\s+(\d+)\s+%s\s+\w+\s+\w+\s+\d+\s+\S+\d+" %context
        sessHandleList = []  
        for line in lineList:
            obj=re.compile(regex,re.I)
            m=obj.search(line)
            if m:
                sessHandleList.append(m.group(1).strip())

        return sessHandleList

def getSessionHandle(self,username="262022600060001"):

        """
          Description: - This API verify the "show session detain" and returns ip address and
                         session handle for a particular user.
          CLI Used- CLI.s that are used for the API  <show session detail>.
          Input: - User name.
          Output: - returns two elements handle and ip for that user
          Author: -  Ganapathi.
          Reviewer: -                        """

        status = "0"
        ret_str=self.cmd("sh session detail username %s  "  %(username))
        log.output(ret_str)

        regex1='\s*Session_handle:\s*\w+\s+Username:\s+\d+'

        line_list = ret_str.split("\n")
        returnList = []

        for line in line_list:
            obj=re.compile(regex1,re.I)
            m=obj.search(line)
            if m:
                handle = line.split()[1]
                return handle.strip()

def verify_ranap_counters(self,slotNum = "2"):

        """
          Description: -  This API parses the output for CLI command "show mdo counters
                          detail ranap slot <slotnum>"
          CLI Used     -  show mdo counters detail ranap slot 2
          Input:       -  slot num  
          Output:      -  returns ret_dict ( dictionary ) having the following indexnames and counter values
                          ret_dict = {'rabAssignReq_sent': '5094', 
                           'relocationrequired_sent': '0', 
                           'directTransfer_recv': '30094', 
                           'commonId_recv': '5000', 
                           'relocationComplete_sent': '0', 
                           'relocationrequired_recv': '0', 
                           'relocationCancel_recv': '0', 
                           'intial_ue_recv': '5000', 
                           'directTransfer_sent': '30188', 
                           'relocationRequest_sent': '0', 
                           'commonId_sent': '5000', 
                           'rabAssignResponse_recv': '5094', 
                           'intial_ue_sent': '5000', 
                           'relocationRequest_recv': '0', 
                           'relocationfailure_recv': '0', 
                           'relocationCommand_sent': '0', 
                           'rabAssignReq_recv': '5094', 
                           'relocationprepFail_sent': '0', 
                           'relocationfailure_sent': '0', 
                           'rabAssignResponse_sent': '5094', 
                           'relocationCancel_sent': '0', 
                           'relocationCommand_recv': '0', 
                           'relocationprepFail_recv': '0', 
                           'relocationComplete_recv': '0',
                           'relocationCancelAck_sent': '0', 
                           'relocationCancelAck_recv': '0', 
                           'relocationReqAck_recv': '0', 
                           'relocationReqAck_sent': '0'}
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """
        
        ret_str = self.cmd("show mdo counters detail ranap slot %s" %slotNum)
        splitList = ret_str.split("\n")
        ret_dict = {}
        ret_dict = {'rabAssignReq_sent': '0',
                    'relocationrequired_sent': '0',
                    'directTransfer_recv': '0',
                    'commonId_recv': '0',
                    'relocationComplete_sent': '0',
                    'relocationrequired_recv': '0',
                    'relocationCancel_recv': '0',
                    'intial_ue_recv': '0',
                    'directTransfer_sent': '0',
                    'relocationRequest_sent': '0',
                    'commonId_sent': '0',
                    'rabAssignResponse_recv': '0',
                    'intial_ue_sent': '0',
                    'relocationRequest_recv': '0',
                    'relocationfailure_recv': '0',
                    'relocationCommand_sent': '0',
                    'rabAssignReq_recv': '0',
                    'relocationprepFail_sent': '0',
                    'relocationfailure_sent': '0',
                    'rabAssignResponse_sent': '0',
                    'relocationCancel_sent': '0',
                    'relocationCommand_recv': '0',
                    'relocationprepFail_recv': '0',
                    'relocationComplete_recv': '0',
                    'relocationCancelAck_sent': '0',
                    'relocationCancelAck_recv': '0',
                    'relocationReqAck_recv': '0',
                    'relocationReqAck_sent': '0'}
        for line in splitList:
            if "Initial UE" in line:
                if "Sent" in line:
                    ret_dict['intial_ue_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['intial_ue_recv'] = line.split(":")[1].strip()
                    continue
            if "Common ID" in line:
                if "Sent" in line:
                    ret_dict['commonId_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['commonId_recv'] = line.split(":")[1].strip()
                    continue
            if "Direct Transfer" in line:
                if "Sent" in line:
                    ret_dict['directTransfer_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['directTransfer_recv'] = line.split(":")[1].strip()
                    continue
            if "RAB Assignment Request" in line:
                if "Sent" in line:
                    ret_dict['rabAssignReq_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['rabAssignReq_recv'] = line.split(":")[1].strip()
                    continue
            if "RAB Assignment Response" in line:
                if "Sent" in line:
                    ret_dict['rabAssignResponse_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['rabAssignResponse_recv'] = line.split(":")[1].strip()
                    continue
            if "RELOCATION CANCEL" in line and "RELOCATION CANCEL-ACK" not in line:
                if "Sent" in line:
                    ret_dict['relocationCancel_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['relocationCancel_recv'] = line.split(":")[1].strip()
                    continue
            if "RELOCATION CANCEL-ACK" in line:
                if "Sent" in line:
                    ret_dict['relocationCancelAck_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['relocationCancelAck_recv'] = line.split(":")[1].strip()
                    continue
            if "RELOCATION PREP-FAILURE" in line:
                if "Sent" in line:
                    ret_dict['relocationprepFail_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['relocationprepFail_recv'] = line.split(":")[1].strip()
                    continue
            if "RELOCATION FAILURE" in line:
                if "Sent" in line:
                    ret_dict['relocationfailure_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['relocationfailure_recv'] = line.split(":")[1].strip()
                    continue
            if "RELOCATION COMPLETE" in line:
                if "Sent" in line:
                    ret_dict['relocationComplete_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['relocationComplete_recv'] = line.split(":")[1].strip()
                    continue
            if "RELOCATION COMMAND" in line:
                if "Sent" in line:
                    ret_dict['relocationCommand_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['relocationCommand_recv'] = line.split(":")[1].strip() 
                    continue
            if "RELOCATION REQUEST" in line and "RELOCATION REQUEST-ACK" not in line:
                if "Sent" in line:
                    ret_dict['relocationRequest_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['relocationRequest_recv'] = line.split(":")[1].strip()
                    continue
            if "RELOCATION REQUEST-ACK" in line:
                if "Sent" in line:
                    ret_dict['relocationReqAck_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['relocationReqAck_recv'] = line.split(":")[1].strip()
                    continue
            if "RELOCATION REQUIRED" in line:
                if "Sent" in line:
                    ret_dict['relocationrequired_sent'] = line.split(":")[1].strip()
                    continue
                else:
                    ret_dict['relocationrequired_recv'] = line.split(":")[1].strip()
                    continue

        return ret_dict                    


def verify_ng40_nas_counters(self):

        """
          Description: -  This API parses the output for CLI command "stat nas"
                          run on NG40
          CLI Used     -  stat nas
          Input:       -  None  
          Output:      -  returns ret_dict ( dictionary ) having the following indexnames and counter values
                          {'Raureject_sent': '0', 
                           'PDPModifyreq_sent': '0', 
                           'AuthCiphrsp_sent': '5000', 
                           'AuthCiphreq_recv': '5000', 
                           'AuthCiphrsp_recv': '0', 
                           'Raucomplete_sent': '0', 
                           'ServiceReq_sent': '0', 
                           'Detachreq_recv': '0', 
                           'PDPActreq_recv': '0', 
                           'ServiceAcc_sent': '0', 
                           'PDPDeactacc_sent': '0', 
                           'SMstatus_recv': '0', 
                           'PDP2ndActacc_sent': '0', 
                           'PDPDeactacc_recv': '0', 
                           'PDPModifyreq_recv': '0', 
                           'Detachacc_recv': '0', 
                           'Detachreq_sent': '0', 
                           'Rauaccept_sent': '0', 
                           'PDPActacc_sent': '0', 
                           'PDPModifyacc_recv': '0', 
                           'sentAttachreqretrans': '0', 
                           'sentPDPActreqretrans': '0', 
                           'AttachAcc_sent': '0', 
                           'PDP2ndActacc_recv': '0', 
                           'sentPDPDeactreqretrans': '0', 
                           'AttachComplete_recv': '0', 
                           'Identityreq_sent': '0', 
                           'PDPDeactreq_recv': '0', 
                           'PDPActreq_sent': '0', 
                           'ServiceAcc_recv': '0', 
                           'RelocComplete_sent': '0', 
                           'sent2ndPDPActreqretrans': '0', 
                           'RelocComplete_recv': '0', 
                           'PDPDeactreq_sent': '0', 
                           'Detachacc_sent': '0', 
                           'AttachAcc_recv': '5000', 
                           'AttachReq_recv': '0', 
                           'PDPModifyacc_sent': '0', 
                           'PDPActacc_recv': '5000', 
                           'Raucomplete_recv': '0', 
                           'AuthCiphreq_sent': '0', 
                           'Identityrspbad_recv': '0', 
                           'Identityrsp_sent': '0', 
                           'AttachComplete_sent': '5000', 
                           'Identityreq_recv': '0', 
                           'Identityrsp_recv': '0', 
                           'Raureq_sent': '0', 
                           'ServiceReq_recv': '0', 
                           'AttachReq_sent': '5000', 
                           'Rauaccept_recv': '0', 
                           'SMstatus_sent': '0', 
                           'Identityrspbad_sent': '0', 
                           'Rauacc_recv': '0', 
                           'receivedIMEISVreq': '5000', 
                           'AttachReject_recv': '0', 
                           'Raureject_recv': '0', 
                           'AttachReject_sent': '0', 
                           'receivedIdentityreqdropped': '0'}
          Author:      -  Ganapathi.
          Reviewer:    -                      
        """
        for i in range(3):
            ret_str = self.cmd("stat nas")
            if "Attach req" in ret_str:
                break 
            time.sleep(1)
        
        splitList = ret_str.split("\n")
        ret_dict = {}
        ret_dict = {'Raureject_sent': '0',
                           'PDPModifyreq_sent': '0',
                           'AuthCiphrsp_sent': '0',
                           'AuthCiphreq_recv': '0',
                           'AuthCiphrsp_recv': '0',
                           'Raucomplete_sent': '0',
                           'ServiceReq_sent': '0',
                           'Detachreq_recv': '0',
                           'PDPActreq_recv': '0',
                           'ServiceAcc_sent': '0',
                           'PDPDeactacc_sent': '0',
                           'SMstatus_recv': '0',
                           'PDP2ndActacc_sent': '0',
                           'PDPDeactacc_recv': '0',
                           'PDPModifyreq_recv': '0',
                           'Detachacc_recv': '0',
                           'Detachreq_sent': '0',
                           'Rauaccept_sent': '0',
                           'PDPActacc_sent': '0',
                           'PDPModifyacc_recv': '0',
                           'sentAttachreqretrans': '0',
                           'sentPDPActreqretrans': '0',
                           'AttachAcc_sent': '0',
                           'PDP2ndActacc_recv': '0',
                           'sentPDPDeactreqretrans': '0',
                           'AttachComplete_recv': '0',
                           'Identityreq_sent': '0',
                           'PDPDeactreq_recv': '0',
                           'PDPActreq_sent': '0',
                           'ServiceAcc_recv': '0',
                           'RelocComplete_sent': '0',
                           'sent2ndPDPActreqretrans': '0',
                           'RelocComplete_recv': '0',
                           'PDPDeactreq_sent': '0',
                           'Detachacc_sent': '0',
                           'AttachAcc_recv': '0',
                           'AttachReq_recv': '0',
                           'PDPModifyacc_sent': '0',
                           'PDPActacc_recv': '0',
                           'Raucomplete_recv': '0',
                           'AuthCiphreq_sent': '0',
                           'Identityrspbad_recv': '0',
                           'Identityrsp_sent': '0',
                           'AttachComplete_sent': '0',
                           'Identityreq_recv': '0',
                           'Identityrsp_recv': '0',
                           'Raureq_sent': '0',
                           'ServiceReq_recv': '0',
                           'AttachReq_sent': '0',
                           'Rauaccept_recv': '0',
                           'SMstatus_sent': '0',
                           'Identityrspbad_sent': '0',
                           'Rauacc_recv': '0',
                           'receivedIMEISVreq': '0',
                           'AttachReject_recv': '0',
                           'Raureject_recv': '0',
                           'AttachReject_sent': '0',
                           'receivedIdentityreqdropped': '0'}
        for line in splitList:
            if "Attach req" in line  and "sent Attach req retrans" not in line and "failed Attach req" not in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['AttachReq_sent'] = Tx
                    ret_dict['AttachReq_recv'] = Rx
                    continue
            if "Attach accept" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['AttachAcc_sent'] = Tx
                    ret_dict['AttachAcc_recv'] = Rx
                    continue
            if "Attach reject" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['AttachReject_sent'] = Tx
                    ret_dict['AttachReject_recv'] = Rx
                    continue
            if "Attach complete" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['AttachComplete_sent'] = Tx
                    ret_dict['AttachComplete_recv'] = Rx
                    continue
            if "Detach req" in line and "sent Detach req retrans" not in line and "failed Detach req" not in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['Detachreq_sent'] = Tx
                    ret_dict['Detachreq_recv'] = Rx
                    continue
            if "Detach acc" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['Detachacc_sent'] = Tx
                    ret_dict['Detachacc_recv'] = Rx
                    continue
            if "RAU req" in line and "failed RAU req" not in line and "sent RAU req retrans" not in line:
                    print line
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['Raureq_sent'] = Tx
                    ret_dict['Rauacc_recv'] = Rx
                    continue
            if "RAU accept" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['Rauaccept_sent'] = Tx
                    ret_dict['Rauaccept_recv'] = Rx
                    continue
            if "RAU complete" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['Raucomplete_sent'] = Tx
                    ret_dict['Raucomplete_recv'] = Rx
                    continue
            if "RAU reject" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['Raureject_sent'] = Tx
                    ret_dict['Raureject_recv'] = Rx
                    continue
            if "Relocation complete" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['RelocComplete_sent'] = Tx
                    ret_dict['RelocComplete_recv'] = Rx
                    continue
            if "Service req" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['ServiceReq_sent'] = Tx
                    ret_dict['ServiceReq_recv'] = Rx
                    continue
            if "Service acc" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['ServiceAcc_sent'] = Tx
                    ret_dict['ServiceAcc_recv'] = Rx
                    continue
            if "AuthCiph req" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['AuthCiphreq_sent'] = Tx
                    ret_dict['AuthCiphreq_recv'] = Rx
                    continue
            if "AuthCiph rsp" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['AuthCiphrsp_sent'] = Tx
                    ret_dict['AuthCiphrsp_recv'] = Rx
                    continue
            if "Identity req" in line and "received Identity req dropped" not in line and "sent Identity req retrans" not in line and "failed Identity req " not in line:
                    print line
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['Identityreq_sent'] = Tx
                    ret_dict['Identityreq_recv'] = Rx
                    continue
            if "Identity rsp bad" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['Identityrspbad_sent'] = Tx
                    ret_dict['Identityrspbad_recv'] = Rx
                    continue
            if "PDP Act req" in line and "sent PDP Act req retrans" not in line and "sent 2nd PDP Act req retrans" not in line and "failed PDP Act req" not in line and "failed 2nd PDP Act req" not in  line:
                    print line
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['PDPActreq_sent'] = Tx
                    ret_dict['PDPActreq_recv'] = Rx
                    continue
            if "PDP Act acc" in line and "2nd PDP Act acc" not in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['PDPActacc_sent'] = Tx
                    ret_dict['PDPActacc_recv'] = Rx
                    continue
            if "2nd PDP Act req" in line and "sent 2nd PDP Act req retrans" not in line and "failed 2nd PDP Act req" not in  line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['PDP2ndActreq_sent'] = Tx
                    ret_dict['PDP2ndActreq_recv'] = Rx
                    continue
            if "2nd PDP Act acc" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['PDP2ndActacc_sent'] = Tx
                    ret_dict['PDP2ndActacc_recv'] = Rx
                    continue
            if "PDP Deact req" in line and "sent PDP Deact req retrans" not in line and "failed PDP Deact req" not in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['PDPDeactreq_sent'] = Tx
                    ret_dict['PDPDeactreq_recv'] = Rx
                    continue
            if "PDP Deact acc" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['PDPDeactacc_sent'] = Tx
                    ret_dict['PDPDeactacc_recv'] = Rx
                    continue
            if "PDP Modify acc" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['PDPModifyacc_sent'] = Tx
                    ret_dict['PDPModifyacc_recv'] = Rx
                    continue

            if "PDP Modify req" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['PDPModifyreq_sent'] = Tx
                    ret_dict['PDPModifyreq_recv'] = Rx
                    continue
            if "SM status" in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['SMstatus_sent'] = Tx
                    ret_dict['SMstatus_recv'] = Rx
                    continue
            if "Identity rsp" in line and "Identity rsp bad" not in line:
                    Rx = line.split("/")[2].strip()
                    Tx = line.split("/")[1].split("=")[1].strip()
                    ret_dict['Identityrsp_sent'] = Tx
                    ret_dict['Identityrsp_recv'] = Rx
                    continue
            if "received Identity req dropped" in line:
                    ret_dict['receivedIdentityreqdropped'] = line.split("=")[1].strip()
                    continue
            if "received IMEISV req" in line:
                    ret_dict['receivedIMEISVreq'] = line.split("=")[1].strip()
                    continue
            if "sent Attach req retrans" in line:
                    ret_dict['sentAttachreqretrans'] = line.split("=")[1].strip()
                    continue
            if "sent Detach req retrans" in line:
                    ret_dict['sentDetachreqretrans'] = line.split("=")[1].strip()
                    continue
            if "sent PDP Act req retrans" in line:
                    ret_dict['sentPDPActreqretrans'] = line.split("=")[1].strip()
                    continue
            if "sent 2nd PDP Act req retrans" in line:
                    ret_dict['sent2ndPDPActreqretrans'] = line.split("=")[1].strip()
                    continue
            if "sent PDP Deact req retrans" in line:
                    ret_dict['sentPDPDeactreqretrans'] = line.split("=")[1].strip()
                    continue
            if "sent Identity req retrans" in line:
                    ret_dict['sentIdentityreqretrans'] = line.split("=")[1].strip()
                    continue
            if "sent RAU req retrans" in line:
                    ret_dict['sentRAUreqretrans'] = line.split("=")[1].strip()
            if "failed Attach req" in line:
                    ret_dict['failedAttachreq'] = line.split("=")[1].strip()
                    continue
            if "failed Detach req" in line:
                    ret_dict['failedDetachreq'] = line.split("=")[1].strip()
                    continue
            if "failed RAU req" in line:
                    ret_dict['failedRAUreq'] = line.split("=")[1].strip()
                    continue
            if "failed PDP Act req" in line:
                    ret_dict['failedPDPActreq'] = line.split("=")[1].strip()
                    continue
            if "failed 2nd PDP Actreq" in line:
                    ret_dict['failed2ndPDPActreq'] = line.split("=")[1].strip()
                    continue
            if "failed PDP Deact req" in line:
                    ret_dict['failedPDPDeactreq'] = line.split("=")[1].strip()
                    continue
            if "failed Identity req" in line:
                    ret_dict['failedIdentityreq'] = line.split("=")[1].strip()
                    continue

        return ret_dict                    



def getProcessIdList(self,slotNum):
    """
    Description: - This API parse output  the "show process slot num" and returns list of
                         Pids
    CLI Used- CLI.s that are used for the API  <show process slot num>.
    Input: - slot num.
    Output: - returns list of process ids
    Author: -  Ganapathi.
    Reviewer: -                        
    """
    str1 = self.cmd("show process slot %s" %slotNum)
    processIdList = []
    linelist = str1.split("\n")
    obj=re.compile("\w+\:\d+",re.I)
    for line in linelist:
        m=obj.search(line)
        if m:
            processIdList.append(line.split()[1].strip())

    return processIdList


def getActiveSctpAssociationCount(self,contextName):
    """
    Description: This API parses the command "sh mdo sctp asscociatios" and returns thr number of associations present
    CLI Used- CLI.s that are used for the API <sh mdo sctp associations>
    Input:   contextname
    Output:  returns the count for number of associations present
    Author: -  Ganapathi.
    Reviewer: -                        
    """
    self.cmd("context %s" %contextName)
    str1 = self.cmd("sh mdo sctp-associations")
    linelist = str1.split("\n")
    reg = "\d+\s+\d+\s+\w+\s+\d+\.\d+\.\d+\.\d+\s*-\s*\d+\.\d+\.\d+\.\d+\s+\w+\s+\w+\s+\d+\s+\d+:\d+:\d+\s+\d+"
    obj = re.compile(reg,re.I)
    count = len(re.split(re.compile(reg,re.I),str1)) / 2
    return count

def verify_context_count(self,contextCount = "250"):

        """
          Description: - This API verify "show context summary" and the expected number of
                         contexts with  exact count and returns true or false
          CLI Used- CLI.s that are used for the API  <show context summary>.
          Input: -  expected context count
          Output: - returns true or false
          Author: -  Ganapathi.
          Reviewer: -                      
        """

        returnVal = "false"
        ret_str=self.cmd("sh context summary")
        log.output(ret_str)
        line_list = ret_str.split("\n")
        for line in line_list:
            if "Total number of configured context" in line:
                count = line.split(":")
                if count[1].strip() == contextCount:
                    returnVal =  "true"
                    break
        return returnVal

def get_mdo_activeses_count(self,cntx):
	self.cmd("context %s"%cntx)
	ret = self.cmd("show mdo ses br | grep ACTIVE | count")
	ret = ret.split(':')[-1]
	return ret

def get_sctp_count(self,cntx):
	self.cmd("context %s"%cntx)
        ret = self.cmd("show mdo sctp | grep RNC | count")
        return ret

def mdo_check_status(self):
	border ="\n" + "-" *50 + "\n"
	self.cmd("context RAN1")
	sctp = 	self.cmd("show mdo sctp | grep RNC | count")
	sctp = sctp.split(':')[-1]
	if sctp !=128:
		log.output("SCTP links have gone down RAN1 from 128 to %s"%sctp)
		scf = "False"
	else:
		log.output("SCTP links are constant in RAN1")
		scf ="True"
	self.cmd("context RAN2")
        sctp =  self.cmd("show mdo sctp | grep RNC | count")
	sctp = sctp.split(':')[-1]
        if sctp !=128:
                log.output("SCTP links have gone down RAN1 from 128 to %s"%sctp)
                scf2 = "False"
        else:
                log.output("SCTP links are constant in RAN1")
                scf2 ="True"
	if scf =="True" and scf2 =="True":
		return 1
	else:
		return 0

def coreCheck(self):
	core = self.cmd("sh syscount")
	core = core.splitlines()[6]
	ret = core.split(' ')[-1]
	if ret == 0:
		return 1
	else:
		return 0


