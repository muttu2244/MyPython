import pypyodbc, sys,os
#from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET

"""
import xml.etree.ElementTree as ET
tree = ET.parse("D:\\Bayers\\German.xml")
#tree = ET.parse("D:\\MedicalDevices\\Ascensia(Bayer)\\Bayers\\German.xml")
root = tree.getroot()

def getStringfromXML(self, validationStr):
        self.validationStr = validationStr
        for t in root.findall('trans-unit'):
            id = t.get('id')
            if id == self.validationStr:
                source = t.find('source').text
                break
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



def readDataFromDBADT():
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
                                                  'Database=GatewayDB;'
                                                  'uid=sa;pwd=Admin@123' )
    #Retriving Multiple Rows
    cursor = connection.cursor()
    #SQLCommand = ("SELECT top 1 Transformed FROM MessageQueue ORDER BY QueueId DESC")
    #SQLCommand = ("SELECT top 3 Transformed FROM (SELECT ROW_NUMBER() OVER (ORDER BY QueueId DESC) AS RowNumber,*FROM MessageQueue Where ProductId = 'Dev') AS foo WHERE RowNumber = 1")
    SQLCommand = ("SELECT top 4 Transformed FROM (SELECT ROW_NUMBER() OVER (ORDER BY QueueId DESC) AS RowNumber,*FROM MessageQueue Where Transformed IS NOT NULL) AS foo WHERE RowNumber = 4")
    cursor.execute(SQLCommand)
    results = cursor.fetchone()

    
    script_path = os.path.dirname(__file__)
         
    with open(script_path + "\\adtoutput.xml", mode='w') as f:
        f.write('%s' %results)

      
    tree = ET.parse(script_path + "\\adtoutput.xml")
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
    EventTypeCode = mylist[45]
    EventOccured = mylist[49]

    SetIdPatientID = mylist[53]
    InternalPatientId = mylist[57]
    PatientLastName = mylist[61]
    PatientFirstName = mylist[63]
    dob = mylist[67]
    Gender = mylist[69]
    PatientAdd  = mylist[73]
    PatientVisit = mylist[79]
    PatientClass = mylist[81]
    AttendingDoc1 = mylist[85]
    AttendingDoc2 = mylist[87]
    AttendingDoc3 = mylist[89]
    HospitalService = mylist[91]
    AdmitSource = mylist[93]
    AmbulatoryStatus = mylist[95]
    AdmitDateTime = mylist[97]
    


    
    print [fieldSep, encodingChar, sendingAppln, sendingFac,  receivingAppln, receivingFac, dateTimeOfMsg, msgType1,msgType2,msgCntrlId,processId, versionId, \
            SetIdPatientID, PatientLastName, PatientFirstName, dob, Gender , PatientAdd, PatientVisit, PatientClass, AttendingDoc1, AttendingDoc2, \
            AttendingDoc3, HospitalService, AdmitSource, AmbulatoryStatus, AdmitDateTime,EventTypeCode,EventOccured]
    
    
    return [fieldSep, encodingChar, sendingAppln, sendingFac,  receivingAppln, receivingFac, msgType1,msgType2,msgCntrlId,processId, versionId, \
            SetIdPatientID, PatientLastName, PatientFirstName, dob, Gender , PatientAdd, PatientVisit, PatientClass, AttendingDoc1, AttendingDoc2, \
            AttendingDoc3, HospitalService, AdmitSource, AmbulatoryStatus, AdmitDateTime,EventTypeCode,EventOccured]
    


    connection.close()

if __name__ == '__main__':
    readDataFromDBADT()