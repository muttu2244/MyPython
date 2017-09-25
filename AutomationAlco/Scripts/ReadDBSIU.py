import pypyodbc, sys,os
#from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET
import urllib2  
from xml.etree.cElementTree import parse, dump  
from xml.parsers import expat

"""
import xml.etree.ElementTree as ET
tree = ET.parse("D:\\Bayers\\German.xml")
#tree = ET.parse("D:\\MedicalDevices\\Ascensia(Bayer)\\Bayers\\German.xml")
root = tree.getroot()

def getStringfromXML(self):
        for child in root:
            for subchild in child:
                for subchild2 in subchild:
                    for node in subchild2.iter():
                        return (node.tag, node.text
        return source

"""

#MSH
fieldSep = 'None'
encodingChar = 'None'
sendingAppln = 'None'
sendingFac = 'None'
receivingAppln = 'None'
receivingFac = 'None'
msgType1 = 'None'
msgType2 = 'None'
msgCntrlId = 'None'
processId = 'None'
versionId = 'None'

#PID
SetIdPatientID = 'None'
PatientLastName = 'None'
PatientFirstName = 'None'
dob = 'None'
Gender = 'None'
PatientAdd = 'None'

#SCH
SCHPlacerAppointmentID = 'None'
SCHScheduleID = 'None'
SCHEventReason = 'None'
SCHAppointmentTimingQuantity1 = 'None'
SCHAppointmentTimingQuantity2 = 'None'
SCHEnteredByPerson = 'None'

#PV1
PatientVisit = 'None'
PatientClass = 'None'
AttendingDoc1 = 'None'
AttendingDoc2 = 'None'
AttendingDoc3 = 'None'
HospitalService = 'None'
AdmitSource = 'None'
AmbulatoryStatus = 'None'
AdmitDateTime = 'None'

#AIL
AILsetId = 'None'
AILLocResourceID = 'None'

#AIP
AIPsetId = 'None'
AIPPersonalResourceID = 'None'


def readDataFromDBSIU():
    global fieldSep 
    global encodingChar 
    global sendingAppln 
    global sendingFac 
    global receivingAppln 
    global receivingFac 
    global msgType1 
    global msgType2 
    global msgCntrlId 
    global processId 
    global versionId
    
    global SetIdPatientID 
    global PatientLastName 
    global PatientFirstName 
    global dob 
    global Gender 
    global PatientAdd
    
    global SCHPlacerAppointmentID
    global SCHScheduleID
    #quantTiming = mylist[3]
    global SCHEventReason
    global SCHAppointmentTimingQuantity1
    global SCHAppointmentTimingQuantity2
    global SCHEnteredByPerson
    
    global PatientVisit 
    global PatientClass 
    global AttendingDoc1 
    global AttendingDoc2 
    global AttendingDoc3 
    global HospitalService 
    global AdmitSource 
    global AmbulatoryStatus 
    global AdmitDateTime

    #AIL
    global AILsetId
    global AILLocResourceID

    #AIP
    global AIPsetId
    global AIPPersonalResourceID
    
    
    connection = pypyodbc.connect('Driver={SQL Server};'
                                                  'Server=L-442000187\SQL2014;'
                                                  #'Database=EMRDB;'
                                                  'Database=GatewayDB;')
     
    
    #Retriving Multiple Rows
    cursor = connection.cursor()
    #SQLCommand = ("SELECT top 1 Transformed FROM MessageQueue ORDER BY QueueId DESC for xml auto")
    #SQLCommand = ("SELECT top 3 Transformed FROM (SELECT ROW_NUMBER() OVER (ORDER BY QueueId DESC) AS RowNumber,*FROM MessageQueue Where ProductId = 'Dev') AS foo WHERE RowNumber = 3")
    #SQLCommand = ("SELECT top 3 Transformed FROM (SELECT ROW_NUMBER() OVER (ORDER BY QueueId DESC) AS RowNumber,*FROM MessageQueue Where ProductId = 'Dev') AS foo WHERE RowNumber = 3")
    SQLCommand = ("SELECT top 4 Transformed FROM (SELECT ROW_NUMBER() OVER (ORDER BY QueueId DESC) AS RowNumber,*FROM MessageQueue Where Transformed IS NOT NULL) AS foo WHERE RowNumber = 2")
    cursor.execute(SQLCommand)
    results = cursor.fetchone()

    
    script_path = os.path.dirname(__file__)
         
    with open(script_path + "\\siuoutput.xml", mode='w') as f:
        f.write('%s' %results)
    #f = open('F:\\MedicalDevices\\AlconProject\\TestAutomation\\TestAutomation\\omgoutput.xml', mode='w')
    #f.write('<?xml version="1.0" encoding="utf-8" standalone ="true"?>\n')
    #f.write('%s' %results)

    #fsock = urllib2.urlopen("http:///F:/MedicalDevices/AlconProject/TestAutomation/TestAutomation/omgoutput.xml")
    #doc = parse(fsock)  
    #dump(doc)

    #tree = ET.parse("F:\\MedicalDevices\\AlconProject\\TestAutomation\\TestAutomation\\omgoutput.xml",parser=expat.ParserCreate('UTF-8'))
    #parser = ET.XMLParser(encoding="utf-8")
    #root = tree.parse(xml_file, parser=expat.ParserCreate('UTF-8') )
    #tree = ET.fromstring("F:\\MedicalDevices\\AlconProject\\TestAutomation\\TestAutomation\\omgoutput.xml", parser=parser)
    #tree.set('SignalStrength',"100")
    tree = ET.parse(script_path + "\\siuoutput.xml")
    root = tree.getroot()

    mylist = []
    for element in root.iter():
        mylist.append(element.tag)
        mylist.append(element.text)
                        

    print "\n"                     
    print mylist
    print "\n"

    fieldSep = mylist[5]
    encodingChar = mylist[7]
    sendingAppln = mylist[11]
    sendingFac = mylist[15]
    receivingAppln = mylist[19]
    receivingFac = mylist[23]
    dateTimeOfMsg = mylist[25]
    msgType1 = mylist[29]
    msgType2 = mylist[31]
    msgCntrlId = mylist[33]
    processId = mylist[37]
    versionId = mylist[39]

    SCHPlacerAppointmentID = mylist[47]
    SCHScheduleID = mylist[51]
    #quantTiming = mylist[3]
    #SCHEventReason = mylist[95]
    SCHAppointmentTimingQuantity1 = mylist[55]  # extra field added
    SCHAppointmentTimingQuantity2 = mylist[57]
    #SCHEnteredByPerson = mylist[105]


    SetIdPatientID = mylist[67]
    #extPatientID = mylist[53]
    intPatientID = mylist[71]
    PatientLastName = mylist[75]
    PatientFirstName = mylist[77]
    dob = mylist[81]
    Gender = mylist[83]
    PatientAdd = mylist[87]


    

    #PatientVisit = mylist[91]
    PatientClass = mylist[93]
    AttendingDoc1 = mylist[97]
    AttendingDoc2 = mylist[99]
    #AttendingDoc3 = mylist[67]
    HospitalService = mylist[101]
    AdmitSource = mylist[103]
    AmbulatoryStatus = mylist[105]
    #AdmitDateTime = mylist[81]


    #AILsetId = mylist[109]
    #AILLocResourceID = mylist[111]     # extra field added

    #AIPsetId = mylist[115]
    #AIPPersonalResourceID = mylist[119]
    
    print [fieldSep, encodingChar , sendingAppln , sendingFac , receivingAppln , receivingFac , dateTimeOfMsg, msgType1 , msgType2 , msgCntrlId , processId , versionId
           , SetIdPatientID , PatientLastName , PatientFirstName , dob , Gender , PatientAdd , SCHPlacerAppointmentID , SCHScheduleID , SCHEventReason , SCHAppointmentTimingQuantity1,
           SCHAppointmentTimingQuantity2 , SCHEnteredByPerson , PatientVisit , PatientClass , AttendingDoc1 , AttendingDoc2 , AttendingDoc3, HospitalService , AdmitSource , AmbulatoryStatus , AdmitDateTime , AILsetId , AILLocResourceID,
            AIPsetId, AIPPersonalResourceID]
    
    
    return [fieldSep, encodingChar , sendingAppln , sendingFac , receivingAppln , receivingFac , dateTimeOfMsg, msgType1 , msgType2 , msgCntrlId , processId , versionId
           , SetIdPatientID , PatientLastName , PatientFirstName , dob , Gender , PatientAdd , SCHPlacerAppointmentID , SCHScheduleID , SCHEventReason , SCHAppointmentTimingQuantity1,
           SCHAppointmentTimingQuantity2 , SCHEnteredByPerson , PatientVisit , PatientClass , AttendingDoc1 , AttendingDoc2 , AttendingDoc3, HospitalService , AdmitSource , AmbulatoryStatus , AdmitDateTime , AILsetId , AILLocResourceID,
            AIPsetId, AIPPersonalResourceID]
    
       
    connection.close()

if __name__ == '__main__':
    readDataFromDBSIU()