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
SetIdPatientID = 'None'
PatientLastName = 'None'
PatientFirstName = 'None'
dob = 'None'
Gender = 'None'
PatientAdd = 'None'
orderControl = 'None'
orcplaceOrderNumber = 'None'
quantTiming = 'None'
ordProviderLastName = 'None'
ordProviderFirstName = 'None'
obrplaceOrdNumb = 'None'
universalServiceId1 = 'None'
universalServiceId2 = 'None'
observationDateTime = 'None'
orderingProvider = 'None'
resultStatus = 'None'
quantityTiming = 'None'
setId = 'None'
valueType = 'None'
observationID = 'None'
observationValue = 'None'
observeResultStatus = 'None'
PatientVisit = 'None'
PatientClass = 'None'
AttendingDoc1 = 'None'
AttendingDoc2 = 'None'
AttendingDoc3 = 'None'
HospitalService = 'None'
AdmitSource = 'None'
AmbulatoryStatus = 'None'
AdmitDateTime = 'None'
EventTypeCode = 'None'
EventOccured = 'None'


def readDataFromDBOMG():
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
    global orderControl 
    global orcplaceOrderNumber 
    global quantTiming 
    global ordProviderLastName
    global ordProviderFirstName 
    global obrplaceOrdNumb 
    global universalServiceId1
    global universalServiceId2
    global observationDateTime 
    global orderingProvider 
    global resultStatus 
    global quantityTiming 
    global setId 
    global valueType 
    global observationID 
    global observationValue 
    global observeResultStatus
    global PatientVisit 
    global PatientClass 
    global AttendingDoc1 
    global AttendingDoc2 
    global AttendingDoc3 
    global HospitalService 
    global AdmitSource 
    global AmbulatoryStatus 
    global AdmitDateTime 
    global EventTypeCode 
    global EventOccured 



    
    connection = pypyodbc.connect('Driver={SQL Server};'
                                                  'Server=L-442000187\SQL2014;'
                                                  #'Database=EMRDB;'
                                                  'Database=GatewayDB;')
     
    
    #Retriving Multiple Rows
    cursor = connection.cursor()
    #SQLCommand = ("SELECT top 1 Transformed FROM MessageQueue ORDER BY QueueId DESC for xml auto")
    #SQLCommand = ("SELECT top 3 Transformed FROM (SELECT ROW_NUMBER() OVER (ORDER BY QueueId DESC) AS RowNumber,*FROM MessageQueue Where ProductId = 'Dev') AS foo WHERE RowNumber = 2")
    SQLCommand = ("SELECT top 4 Transformed FROM (SELECT ROW_NUMBER() OVER (ORDER BY QueueId DESC) AS RowNumber,*FROM MessageQueue Where Transformed IS NOT NULL) AS foo WHERE RowNumber = 3")
    cursor.execute(SQLCommand)
    results = cursor.fetchone()

    
    script_path = os.path.dirname(__file__)
         
    with open(script_path + "\\omgoutput.xml", mode='w') as f:
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
    tree = ET.parse(script_path + "\\omgoutput.xml")
    root = tree.getroot()


    mylist = []
    for element in root.iter():
        mylist.append(element.tag)
        mylist.append(element.text)
    


    print mylist
    print "\n\n"

    
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
    SetIdPatientID = mylist[47]
    extPatientID = mylist[51]
    intPatientID = mylist[55]
    PatientLastName = mylist[59]
    PatientFirstName = mylist[61]
    dob = mylist[63]
    #Gender = mylist[3]
    #PatientAdd = mylist[3]

    PatientVisit = mylist[73]
    PatientClass = mylist[75]
    AttendingDoc1 = mylist[79]
    AttendingDoc2 = mylist[81]
    #AttendingDoc3 = mylist[67]
    HospitalService = mylist[83]
    AdmitSource = mylist[85]
    AmbulatoryStatus = mylist[87]
    AdmitDateTime = mylist[89]



    orderControl = mylist[95]
    orcplaceOrderNumber = mylist[99]
    #quantTiming = mylist[3]
    ordProviderLastName = mylist[103]
    ordProviderFirstName = mylist[105]  # extra field added
    obrplaceOrdNumb = mylist[113]
    universalServiceId1 = mylist[117]
    universalServiceId2 = mylist[119]     # extra field added

    observationDateTime = mylist[123]
    obrOrderingProviderLastName = mylist[127]
    obrOrderingProviderFirstName = mylist[129]

    
    
    print [fieldSep, encodingChar , sendingAppln , sendingFac , receivingAppln , receivingFac , dateTimeOfMsg, msgType1 , msgType2 , msgCntrlId , processId , versionId
           , SetIdPatientID , extPatientID, intPatientID, PatientLastName , PatientFirstName , dob , Gender , PatientAdd , orderControl , orcplaceOrderNumber , quantTiming , ordProviderLastName
           , ordProviderFirstName , obrplaceOrdNumb , universalServiceId1 , universalServiceId2 , observationDateTime , orderingProvider , resultStatus , quantityTiming
           , PatientVisit , PatientClass , AttendingDoc1 , AttendingDoc2 , AttendingDoc3
           , HospitalService , AdmitSource , AmbulatoryStatus , AdmitDateTime , EventTypeCode , EventOccured]
    

    
    return [fieldSep, encodingChar , sendingAppln , sendingFac , receivingAppln , receivingFac , dateTimeOfMsg, msgType1 , msgType2 , msgCntrlId , processId , versionId
           , SetIdPatientID , extPatientID, intPatientID,PatientLastName , PatientFirstName , dob , Gender , PatientAdd , orderControl , orcplaceOrderNumber , quantTiming , ordProviderLastName
           , ordProviderFirstName , obrplaceOrdNumb , universalServiceId1 , universalServiceId2 , observationDateTime , orderingProvider , resultStatus , quantityTiming
           , PatientVisit , PatientClass , AttendingDoc1 , AttendingDoc2 , AttendingDoc3
           , HospitalService , AdmitSource , AmbulatoryStatus , AdmitDateTime , EventTypeCode , EventOccured]
    
    
    
    connection.close()

    

if __name__ == '__main__':
    readDataFromDBOMG()