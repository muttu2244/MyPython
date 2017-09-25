import pypyodbc, sys
#from xml.sax.saxutils import escape

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



def readDataFromDB():
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
    """
    #Retriving Single Row
    cursor = connection.cursor()
    SQLCommand = ("Select * from PatientInfo")
    Values = cursor.execute(SQLCommand)
    results = cursor.fetchone()
    #print("Your customer " + results[0] + " " + results[1] + " lives in " + results[2])
    print(results)
    """

    
    #Retriving Multiple Rows
    cursor = connection.cursor()
    #SQLCommand = ("Select * from PatientInfo")
    #SQLCommand = ("Select Transformed from messageQueue where QueueId=4")
    #SQLCommand = ("Select Transformed from messageQueue where QueueId=4 for xml auto")
    #SQLCommand = ("SELECT top 1 Transformed FROM MessageQueue ORDER BY QueueId DESC")
    SQLCommand = ("SELECT top 1 Transformed FROM MessageQueue ORDER BY QueueId DESC for xml auto")
    cursor.execute(SQLCommand)
    results = cursor.fetchone()

    '''
    #with open('output.xml', encoding='utf-8', mode='w') as f:
    f = open('F:\\MedicalDevices\\AlconProject\\TestAutomation\\TestAutomation\\output.xml', mode='w')
    #f.write('<?xml version="1.0" encoding="utf-8"?>\n')
    f.write('%s' %results)
    '''

    '''
    #print results
    print type(results)
    if results == None:
        sys.exit("\n\n*****GATEWAY DB DOES NOT HAVE ANY DATA INTO IT... EXITING...*****\n")
    '''

    
    mylist = results[0].split('>')
    print mylist
    for item in mylist:
        #print "\n" + item
        if item.endswith("</MSH.1"):
            FieldSepList =  item.split("</MSH.1")
            fieldSep = FieldSepList[0]
            
            continue

        if item.endswith("</MSH.2"):
            EncodingCharList =  item.split("</MSH.2")
            encodingChar = EncodingCharList[0]
            continue

        if item.endswith("EPIC</EI.1"):
            SendingApplnList =  item.split("</EI.1")
            sendingAppln = SendingApplnList[0]
            continue

        if item.endswith("EPICADT</EI.1"):
            SendingFacList =  item.split("</EI.1")
            sendingFac = SendingFacList[0]
            continue

        if item.endswith("SMS</EI.1"):
            ReceivingApplnList =  item.split("</EI.1")
            receivingAppln = ReceivingApplnList[0]
            continue

        if item.endswith("SMSADT</EI.1"):
            ReceivingFacList =  item.split("</EI.1")
            receivingFac = ReceivingFacList[0]
            #print receivingFac
            continue

        if item.endswith("</CM_MSH.1"):
            MsgTypeList =  item.split("</CM_MSH.1")
            msgType1 = MsgTypeList[0]
            continue               

        if item.endswith("</CM_MSH.2"):
            MsgTypeList =  item.split("</CM_MSH.2")
            msgType2 = MsgTypeList[0]
            #msgType = msgType1 + msgType2
            continue

        if item.endswith("</MSH.10"):
            MsgCntrlIdList = item.split("</MSH.10")
            msgCntrlId = MsgCntrlIdList[0]
            continue

        if item.endswith("</PT.1"):
            ProcessIdList = item.split("</PT.1")
            processId = ProcessIdList[0]
            continue

        if item.endswith("</MSH.12"):
            VersionIdList = item.split("</MSH.12")
            versionId = VersionIdList[0]
            continue

    #print [fieldSep, encodingChar, sendingAppln, sendingFac,  receivingAppln, receivingFac, msgType1,msgType2,msgCntrlId, processId, versionId]

        if item.endswith("</MSH.12"):
            VersionIdList = item.split("</MSH.12")
            versionId = VersionIdList[0]
            continue
##########################################################
        
        if item.endswith("</PID.1"):
            SetIdPatientIDList = item.split("</PID.1")
            SetIdPatientID = SetIdPatientIDList[0]
            continue

        if item.endswith("</XPN.1"):
            PatientLastNameList = item.split("</XPN.1")
            PatientLastName = PatientLastNameList[0]
            continue

        if item.endswith("</XPN.2"):
            PatientFirstNameList = item.split("</XPN.2")
            PatientFirstName = PatientFirstNameList[0]
            continue

        if item.endswith("</PID.7"):
            dobList = item.split("</PID.7")
            dob = dobList[0]
            continue

        if item.endswith("</PID.8"):
            GenderList = item.split("</PID.8")
            Gender = GenderList[0]
            continue

        if item.endswith("</XAD.1"):
            PatientAddList = item.split("</XAD.1")
            PatientAdd = PatientAddList[0]
            continue

##########################################################

        if item.endswith("</PV1.1"):
            PatientVisitList = item.split("</PV1.1")
            PatientVisit = PatientVisitList[0]
            continue

        if item.endswith("</PV1.2"):
            PatientClassList = item.split("</PV1.2")
            PatientClass = PatientClassList[0]
            continue

        if item.endswith("</XCN.2"):
            AttendingDocList1 = item.split("</XCN.2")
            AttendingDoc1 = AttendingDocList1[0]
            continue

        if item.endswith("</XCN.3"):
            AttendingDocList2 = item.split("</XCN.3")
            AttendingDoc2 = AttendingDocList2[0]
            continue

        if item.endswith("</XCN.4"):
            AttendingDocList3 = item.split("</XCN.4")
            AttendingDoc3 = AttendingDocList3[0]
            continue

        if item.endswith("</PV1.10"):
           HospitalServiceList = item.split("</PV1.10")
           HospitalService = HospitalServiceList[0]
           continue

        if item.endswith("</PV1.14"):
            AdmitSourceList = item.split("</PV1.14")
            AdmitSource = AdmitSourceList[0]
            continue

        if item.endswith("</PV1.15"):
            AmbulatoryStatusList = item.split("</PV1.15")
            AmbulatoryStatus = AmbulatoryStatusList[0]
            continue

        if item.endswith("</PV1.44"):
            AdmitDateTimeList = item.split("</PV1.44")
            AdmitDateTime = AdmitDateTimeList[0]
            continue

##########################################################

        if item.endswith("</EVN.1"):
            EventTypeCodeList = item.split("</EVN.1")
            EventTypeCode = EventTypeCodeList[0]
            continue

        if item.endswith("</EVN.6"):
            EventOccuredList = item.split("</EVN.6")
            EventOccured = EventOccuredList[0]
            continue
    
    '''
    print [fieldSep, encodingChar, sendingAppln, sendingFac,  receivingAppln, receivingFac, msgType1,msgType2,msgCntrlId,processId, versionId, \
            SetIdPatientID, PatientLastName, PatientFirstName, dob, Gender , PatientAdd, PatientVisit, PatientClass, AttendingDoc1, AttendingDoc2, \
            AttendingDoc3, HospitalService, AdmitSource, AmbulatoryStatus, AdmitDateTime,EventTypeCode,EventOccured]
    '''
    
    return [fieldSep, encodingChar, sendingAppln, sendingFac,  receivingAppln, receivingFac, msgType1,msgType2,msgCntrlId,processId, versionId, \
            SetIdPatientID, PatientLastName, PatientFirstName, dob, Gender , PatientAdd, PatientVisit, PatientClass, AttendingDoc1, AttendingDoc2, \
            AttendingDoc3, HospitalService, AdmitSource, AmbulatoryStatus, AdmitDateTime,EventTypeCode,EventOccured]
    


    """
    for element in results:
        #print(",".join(element))
        #print element
        #print element[50:60]
        row[0].split(',')
    """
    
    """
    while results:
        #print ("Your customer " +  str(results[0]) + " " + results[1] + " lives in " + results[2])
        results = cursor.fetchone()
        print results
    """

    
    connection.close()

if __name__ == '__main__':
    readDataFromDB()