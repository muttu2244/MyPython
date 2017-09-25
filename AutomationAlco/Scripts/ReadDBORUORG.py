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


def readDataFromDBORU():
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
    SQLCommand = ("SELECT top 1 Transformed FROM MessageQueue ORDER BY QueueId DESC ")
    #SQLCommand = ("SELECT top 4 Transformed FROM (SELECT ROW_NUMBER() OVER (ORDER BY QueueId ASC) AS RowNumber,*FROM MessageQueue Where ProductId = 'Dev') AS foo WHERE RowNumber = 2")
    cursor.execute(SQLCommand)
    results = cursor.fetchone()

    script_path = os.path.dirname(__file__)
         
    with open(script_path + "\\oruoutput.xml", mode='w') as f:
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
    #tree = ET.parse("F:\\MedicalDevices\\AlconProject\\TestAutomation\\TestAutomation\\omgoutput.xml")
    tree = ET.parse(script_path + "\\oruoutput.xml")
    root = tree.getroot()

    
    mylist = []
    '''
    mydict = {'MSH.1':None,'MSH.2':None,'MSH.3':None,'MSH.4':None,'MSH.6':None,'MSH.7':None,'MSH.9':None,'MSH.10':None,'MSH.11':None,'MSH.12':None,
              'PID.1':None,'PID.2':None,'PID.3':None,'PID.5':None,'PID.7':None,'PID.8':None,'PID.11':None,'ORC.1':None,'ORC.2':None,'ORC.7':None,'ORC.12':None,
               'OBR.2':None,'OBR.4':None,'OBR.7':None,'OBR.16':None,'OBR.25':None,'OBR.27':None}
    '''        
                                  
    for child in root:
            for subchild in child:
                for subchild2 in subchild:
                    for node in subchild2.iter():
                        mylist.append(node.tag)
                        mylist.append(node.text)
                        
                            
                            
                        
                        
    print mylist

    fieldSep = mylist[3]
    encodingChar = mylist[5]
    sendingAppln = mylist[9]
    sendingFac = mylist[13]
    receivingAppln = mylist[17]
    receivingFac = mylist[21]
    msgType1 = mylist[25]
    msgType2 = mylist[27]
    msgCntrlId = mylist[29]
    processId = mylist[33]
    versionId = mylist[35]
    SetIdPatientID = mylist[41]
    extPatientID = mylist[53]
    intPatientID = mylist[57]
    PatientLastName = mylist[61]
    PatientFirstName = mylist[63]
    dob = mylist[65]
    #Gender = mylist[3]
    #PatientAdd = mylist[3]
    orderControl = mylist[87]
    orcplaceOrderNumber = mylist[91]
    #quantTiming = mylist[3]
    ordProviderLastName = mylist[95]
    ordProviderFirstName = mylist[97]  # extra field added
    obrplaceOrdNumb = mylist[105]
    universalServiceId1 = mylist[109]
    universalServiceId2 = mylist[111]     # extra field added

    observationDateTime = mylist[115]
    obrOrderingProviderLastName = mylist[119]
    obrOrderingProviderFirstName = mylist[121]


    #resultStatus = mylist[3]
    #quantityTiming = mylist[3]
    #obxsetId = mylist[3]
    #obxvalueType = mylist[3]
    #obxobservationID = mylist[3]
    #obxobservationValue = mylist[3]
    #obxobserveResultStatus = mylist[3]
    PatientVisit = mylist[67]
    #PatientClass = mylist[67]
    AttendingDoc1 = mylist[71]
    AttendingDoc2 = mylist[73]
    #AttendingDoc3 = mylist[67]
    HospitalService = mylist[75]
    AdmitSource = mylist[77]
    AmbulatoryStatus = mylist[79]
    AdmitDateTime = mylist[81]
    

    '''
    ['MSH', None, 'MSH.1', '|', 'MSH.2', '^~\\&', 'MSH.3', None, 'EI.1', 'EPIC', 'MSH.4', None, 'EI.1', 'EPICADT', 'MSH.5', None, 'EI.1', 'SMS',
     'MSH.6', None, 'EI.1', 'SMSADT', 'MSH.9', None, 'CM_MSH.1', 'OMG', 'CM_MSH.2', 'O19', 'MSH.10', '1817457', 'MSH.11', None, 'PT.1', 'D', 'MSH.12',
     '2.3', 'ORMO19.PATIENT', None, 'PID', None, 'PID.1', '10122', 'PID.2', None, 'CX.1', 'PC98592212', 'PID.3', None, 'CX.1', 'PC98592212', 'PID.5', None,
     'XPN.1', 'chopra', 'XPN.2', 'priyanka', 'PID.7', '20160727120000', 'PID.11', None, 'PID.19', '984487127', 'ORMO19.PATIENT_VISIT', None, 'PV1', None,
     'PV1.1', '10122', 'PV1.7', None, 'XCN.2', 'Madhu', 'XCN.3', 'Kiran', 'PV1.10', 'SUR', 'PV1.14', 'ADM', 'PV1.15', 'AO', 'PV1.44', '20160923051933',
     'ORMO19.ORDER', None, 'ORC', None, 'ORC.1', 'NW', 'ORC.2', None, 'EI.1', 'BPE4804637', 'ORC.12', None, 'XCN.2', 'Kiran', 'XCN.3', 'Madhu', 'OBR', None,
     'OBR.1', '1', 'OBR.2', None, 'EI.1', 'BPE4804637', 'OBR.4', None, 'CE.1', '101', 'CE.2', 'Visual field Test', 'OBR.6', '20160923000000',
     'OBR.7', '20160915000000', 'OBR.16', None, 'XCN.2', 'Kiran', 'XCN.3', 'Madhu']
    '''

    '''
    #print results
    print type(results)
    if results == None:
        sys.exit("\n\n*****GATEWAY DB DOES NOT HAVE ANY DATA INTO IT... EXITING...*****\n")
    '''

    '''
    
    print [fieldSep, encodingChar , sendingAppln , sendingFac , receivingAppln , receivingFac , msgType1 , msgType2 , msgCntrlId , processId , versionId
           , SetIdPatientID , PatientLastName , PatientFirstName , dob , Gender , PatientAdd , orderControl , orcplaceOrderNumber , quantTiming , ordProviderLastName
           , ordProviderFirstName , obrplaceOrdNumb , universalServiceId1 , universalServiceId2 , observationDateTime , orderingProvider , resultStatus , quantityTiming
           , setId , valueType , observationID , observationValue , observeResultStatus, PatientVisit , PatientClass , AttendingDoc1 , AttendingDoc2 , AttendingDoc3
           , HospitalService , AdmitSource , AmbulatoryStatus , AdmitDateTime , EventTypeCode , EventOccured]
    '''
    
    return [fieldSep, encodingChar , sendingAppln , sendingFac , receivingAppln , receivingFac , msgType1 , msgType2 , msgCntrlId , processId , versionId
           , SetIdPatientID , PatientLastName , PatientFirstName , dob , Gender , PatientAdd , orderControl , orcplaceOrderNumber , quantTiming , ordProviderLastName
           , ordProviderFirstName , obrplaceOrdNumb , universalServiceId1 , universalServiceId2 , observationDateTime , orderingProvider , resultStatus , quantityTiming
           , setId , valueType , observationID , observationValue , observeResultStatus, PatientVisit , PatientClass , AttendingDoc1 , AttendingDoc2 , AttendingDoc3
           , HospitalService , AdmitSource , AmbulatoryStatus , AdmitDateTime , EventTypeCode , EventOccured]
    
       
    connection.close()

if __name__ == '__main__':
    readDataFromDBORU()