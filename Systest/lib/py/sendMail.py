"""
DESCRIPTION             : This Script contains following APIs for SOAK                         
                           1.   getCores
                           2.   getCritErrEvts
                           3.   sendMail
                           4.   alertIfSsxNotHealthy
AUTHOR                  : Rajshekar; email :  rajshekar@primesoftsolutionsinc.com
REVIEWER                :
DEPENDENCIES            : Linux.py,device.py
"""

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
boarder = "\n" + "-" *50 + "\n"

def getCores(self,dateBefStaTestStep="") :
    """
    Description  : To Get Cores on SSX on that time
    Arguments    : dateBefStaTestStep = Give the date before you starting test step.
                   This API will be executed at the end of Test step
    Usage        : self.getCores()
    Return Value : List of core files on Success.
    """

    boarder = "\n" + "#" *50 + "\n"
    if len(dateBefStaTestStep) == 0 :
       date = self.cmd("show clock")
    else :
       date = dateBefStaTestStep
    date = date.split()
    time = date[4]
    timeInHrs = time[0]
    if  len(dateBefStaTestStep) == 0 :
        date = date[2]+date[1]+date[3]
    else :
        date = date[2]+date[1]+date[3]+" "+time[0:len(date)-1]
    slotList = ["slot0","slot1","slot2","slot3","slot4"]
    cores = ""
    for slot in slotList :
         if  len(dateBefStaTestStep) != 0 :
            out= self.cmd('dir /hd/dump/%s | begin "%s" | grep core.gz'%(slot,date))
         else :
            out= self.cmd('dir /hd/dump/%s  |  grep %s | grep core.gz'%(slot,date))
         if len(out) != 0 :
             cores = cores + boarder + "\n" + "Observed below CORES on %s"%slot + "\n"
             cores = cores + "%s"%out + boarder
    return cores

def getCritErrEvts(self,evntList=["CRIT","ERR"]) :

    """
    Description  : To Get CRIT/ERR events when CRIT,ERR observed on SSX
    Arguments    : evntList - Type of events
    Usage        : getCritErrEvts(self,evntList=["CRIT"]
                      getCritErrEvts(self,evntList=["CRIT","ERR"])
    Return Value : 0 on not successful,observed CRIT/ERR/CORE events on successful
    """

    if len(evntList) == 0 :
        log.info("Event list is empty")
        return 0
    if len(evntList) == 2 :
       if "ERR" not in evntList or "CRIT" not in evntList :
          log.info("Wrong event type entered.Please enter correct event types CRIT/ERR")
          return 0       
    nameErr = 1
    if evntList[0] == "ERR" :
            nameErr = 0
    if evntList[0] == "CRIT" :
            nameErr = 0
    if nameErr == 1 :
          log.info("Please enter correct event type CRIT/ERR but you have given %s"%evntList[0])
          return 0

    ObsEvts = []
    for evnt in evntList :
        msgList = []
        out = self.cmd('show log standard | grep \" %s\"'%evnt)
        if len(out) == 0 :
           continue
        msgs = out.split("\r")
        msgList = []
        for msg in msgs :
 
            index = int(msg.find("%s"%evnt))
            msg = "%s"%msg[index+3:].strip()
            index = "%s"%msg.find(":")
            msg = "%s"%msg[int(index)+1:].strip()
            msgList.append(msg)
        msgList = list(set(msgList))    
        #msgList = ["%s"%msg]
        #ObsEvts.append(msg)
        self.cmd("term wid infi")
        self.cmd("term len 4")
        for msg in msgList :
            if len(msg) != 0 :
                  out = self.cmd('show log standard | grep " %s" | grep -i "%s"'%(evnt,msg))
                  msgs = out.split("\r")
                  evtMsg = msgs[len(msgs)-1]
                  ObsEvts.append(evtMsg)
    return ObsEvts

def sendMail(FROM="rajshekar@stoke.com",TO=["ashu@stoke.com","tania@stoke.com"],CC = ["swqa-mgr@stoke.com"],SUBJECT="Observed ERR Or CRIT events in SOAK",TxtInBdy=""):
        TxtInBdy= TxtInBdy + "\n\n\n\n" + "THIS MAIL IS SENT FROM A SCRIPT" 
        # message
        message = """\
From: %s
To: %s
Cc: %s
Subject: %s

%s
        """ % (FROM, ", ".join(TO), ", ".join(CC), SUBJECT, TxtInBdy)

        # Send the mail
        SENDMAIL = "/usr/sbin/sendmail" # sendmail location 
        f = os.popen("which sendmail")
        sendMailLoc =  "%s" %f.readlines()[0].strip()
        p = os.popen("%s -t -i" % SENDMAIL, "w")
        p.write(message)
        status = p.close()
        if status:
            print "Sendmail exit status", status

def alertIfSsxNotHealthy(self,couBefTestStep={},couAftTestStep={},From="rajshekar@stoke.com",To=["ashu@stoke.com","tania@stoke.com","vkodali@stoke.com"],SUBJECT="SSX is not healthy : ",dateBefStaTestStep="") :


     """
       Description  : To Alert an user through mail when CRIT,CORES,ERR observed.
       Arguments    : couBefTestStep - Give Dictionary 
                      couAftTestStep - Dictionary
                      From           - Sender Mail Address
                      To             - Receiver Mail Address
       Usage        : 
                     couBef = self.ssx.get_health_stats()
                     couAft = self.ssx.get_health_stats()
                     alertIfSsxNotHealthy(self,couBefTestStep=couBef,couAftTestStep=couAft)
                     alertIfSsxNotHealthy(self,couBefTestStep=couBef,couAftTestStep=couAft,From="krao@stoke.com",To="rajshekar@stoke.com")
       Return Value : 0 on not successful
     """

     boarder = "\n" + "#" *50 + "\n"
     # Check input is valid
     if int(len(couBefTestStep.keys())) == 0 :
        log.info("Dictionary couBefTestStep is Empty.Please take look")
        return 0
     if int(len(couAftTestStep.keys())) == 0 :
        log.info("Dictionary couAftTestStep is Empty.Please take look")
        return 0

     # Get the build ID
     version = self.get_version()
     buildId = version['branch'] + "_" + version['build']

     # Get the Duration
     out = self.cmd("show version | grep -i \"Stoke uptime\"")
     dura = out[17:]
     
     # Check if any failures observed
     ErrEvntsObs = 0
     CritEvtsObs = 0
     CoreEvtObs =  0
     TEXT  = "Hi" + "\n\n\n"
     
     if couAftTestStep["Crit_logs"] >  couBefTestStep["Crit_logs"] :
         CritEvtsObs = 1
     if couAftTestStep["Err_logs"] > couBefTestStep["Err_logs"] :
         ErrEvntsObs = 1
     cores = getCores(self,dateBefStaTestStep="%s"%dateBefStaTestStep)
     if "core.gz" in cores :
         CoreEvtObs = 1     
     if CritEvtsObs | ErrEvntsObs  | CoreEvtObs :
          if CritEvtsObs :
             TEXT = TEXT + boarder + "CRIT Events observed after %s on build %s" %(dura,buildId)
             evnts = getCritErrEvts(self,evntList=["CRIT"])
             TEXT = TEXT + boarder + "CRIT Events are: " + "\n"
             for evnt in evnts :
                  if len(evnt)!=0 :          
                     evnt = evnt.strip()   
                     TEXT = TEXT + "\n" + "%s"%evnt + "\n"
             TEXT = TEXT + boarder + "\n"                     
             SUBJECT= SUBJECT + " CRITEvents "

          if ErrEvntsObs :
             TEXT = TEXT + boarder + "ERR Events observed after %s on build %s" %(dura,buildId)
             evnts = getCritErrEvts(self,evntList=["ERR"])
             TEXT = TEXT + boarder + "ERR  Events are: " + "\n"
      
             for evnt in evnts :
                  if len(evnt)!=0 :
                     evnt = evnt.strip()
                     TEXT = TEXT + "\n" + "%s"%evnt + "\n"
             TEXT = TEXT + boarder + "\n"
             SUBJECT= SUBJECT + " ERREvents "

          if CoreEvtObs :
             TEXT = TEXT + boarder + "CORE observed on build %s" %(buildId)
             cores = getCores(self)
             TEXT = TEXT + boarder + "Observed CORES are: " + "\n"
             TEXT = TEXT + "\n" + "%s"%cores
             #for core in cores :
             #     if len(core)!=0:
             #          core = core.strip()
             #          TEXT = TEXT + "\n" + "%s"%core + "\n"
                          
             TEXT = TEXT + boarder + "\n"                      
             SUBJECT= SUBJECT + " CORES"
          SUBJECT= SUBJECT + " Observed"

          # Send Mail 
          sendMail(FROM="%s"%From,TO=To,SUBJECT="%s"%SUBJECT,TxtInBdy="%s"%TEXT)

