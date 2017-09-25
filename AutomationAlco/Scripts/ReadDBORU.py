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
dateTimeOfMsg = 'None'
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

obxsetId1  = 'None'
obxvalueType1  = 'None'
obxobservationID1_1  = 'None'
obxobservationID1_2  = 'None'
obxobservationValue1 = 'None'
obxobserveResultStatus1= 'None'

obxsetId2  = 'None'
obxvalueType2  = 'None'
obxobservationID2_1  = 'None'
obxobservationID2_2  = 'None'
obxobservationValue2 = 'None'
obxobserveResultStatus2= 'None'

obxsetId3  = 'None'
obxvalueType3  = 'None'
obxobservationID3_1  = 'None'
obxobservationID3_2  = 'None'
obxobservationValue3 = 'None'
obxobserveResultStatus3= 'None'

obxsetId4  = 'None'
obxvalueType4  = 'None'
obxobservationID4_1  = 'None'
obxobservationID4_2  = 'None'
obxobservationValue4 = 'None'
obxobserveResultStatus4= 'None'

obxsetId5 = 'None'
obxvalueType5  = 'None'
obxobservationID5_1  = 'None'
obxobservationID5_2  = 'None'
obxobservationValue5 = 'None'
obxobserveResultStatus5= 'None'

obxsetId6  = 'None'
obxvalueType6  = 'None'
obxobservationID6_1  = 'None'
obxobservationID6_2  = 'None'
obxobservationValue6 = 'None'
obxobserveResultStatus6= 'None'

obxsetId7  = 'None'
obxvalueType7  = 'None'
obxobservationID7_1  = 'None'
obxobservationID7_2  = 'None'
obxobservationValue7 = 'None'
obxobserveResultStatus7= 'None'

obxsetId8  = 'None'
obxvalueType8  = 'None'
obxobservationID8_1  = 'None'
obxobservationID8_2  = 'None'
obxobservationValue8 = 'None'
obxobserveResultStatus8= 'None'

obxsetId9  = 'None'
obxvalueType9  = 'None'
obxobservationID9_1  = 'None'
obxobservationID9_2  = 'None'
obxobservationValue9 = 'None'
obxobserveResultStatus9= 'None'

obxsetId10  = 'None'
obxvalueType10  = 'None'
obxobservationID10_1  = 'None'
obxobservationID10_2  = 'None'
obxobservationValue10 = 'None'
obxobserveResultStatus10= 'None'
           
obxsetId11  = 'None'
obxvalueType11  = 'None'
obxobservationID11_1  = 'None'
obxobservationID11_2  = 'None'
obxobservationValue11 = 'None'
obxobserveResultStatus11= 'None'

obxsetId12  = 'None'
obxvalueType12  = 'None'
obxobservationID12_1  = 'None'
obxobservationID12_2  = 'None'
obxobservationValue12 = 'None'
obxobserveResultStatus12= 'None'
           
obxsetId13  = 'None'
obxvalueType13  = 'None'
obxobservationID13_1  = 'None'
obxobservationID13_2  = 'None'
obxobservationValue13 = 'None'
obxobserveResultStatus13= 'None'

obxsetId14  = 'None'
obxvalueType14  = 'None'
obxobservationID14_1  = 'None'
obxobservationID14_2  = 'None'
obxobservationValue14 = 'None'
obxobserveResultStatus14= 'None'




def readDataFromDBORU():
    global fieldSep 
    global encodingChar 
    global sendingAppln 
    global sendingFac 
    global receivingAppln 
    global receivingFac
    global dateTimeOfMsg
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
    
    global obxsetId1  
    global obxvalueType1  
    global obxobservationID1_1  
    global obxobservationID1_2  
    global obxobservationValue1 
    global obxobserveResultStatus1

    global obxsetId2  
    global obxvalueType2  
    global obxobservationID2_1  
    global obxobservationID2_2  
    global obxobservationValue2 
    global obxobserveResultStatus2

    global obxsetId3  
    global obxvalueType3  
    global obxobservationID3_1  
    global obxobservationID3_2  
    global obxobservationValue3 
    global obxobserveResultStatus3

    global obxsetId4  
    global obxvalueType4  
    global obxobservationID4_1  
    global obxobservationID4_2  
    global obxobservationValue4 
    global obxobserveResultStatus4

    global obxsetId5 
    global obxvalueType5  
    global obxobservationID5_1  
    global obxobservationID5_2  
    global obxobservationValue5 
    global obxobserveResultStatus5

    global obxsetId6  
    global obxvalueType6  
    global obxobservationID6_1  
    global obxobservationID6_2  
    global obxobservationValue6 
    global obxobserveResultStatus6

    global obxsetId7  
    global obxvalueType7  
    global obxobservationID7_1  
    global obxobservationID7_2  
    global obxobservationValue7 
    global obxobserveResultStatus7

    global obxsetId8  
    global obxvalueType8  
    global obxobservationID8_1  
    global obxobservationID8_2  
    global obxobservationValue8 
    global obxobserveResultStatus8

    global obxsetId9  
    global obxvalueType9  
    global obxobservationID9_1  
    global obxobservationID9_2  
    global obxobservationValue9 
    global obxobserveResultStatus9

    global obxsetId10  
    global obxvalueType10  
    global obxobservationID10_1  
    global obxobservationID10_2  
    global obxobservationValue10 
    global obxobserveResultStatus10
               
    global obxsetId11  
    global obxvalueType11  
    global obxobservationID11_1  
    global obxobservationID11_2  
    global obxobservationValue11 
    global obxobserveResultStatus11

    global obxsetId12  
    global obxvalueType12  
    global obxobservationID12_1  
    global obxobservationID12_2  
    global obxobservationValue12 
    global obxobserveResultStatus12
               
    global obxsetId13  
    global obxvalueType13  
    global obxobservationID13_1  
    global obxobservationID13_2  
    global obxobservationValue13 
    global obxobserveResultStatus13

    global obxsetId14  
    global obxvalueType14  
    global obxobservationID14_1  
    global obxobservationID14_2  
    global obxobservationValue14 
    global obxobserveResultStatus14
    
    
    connection = pypyodbc.connect('Driver={SQL Server};'
                                                  'Server=L-442000187\SQL2014;'
                                                  #'Database=EMRDB;'
                                                  'Database=GatewayDB;')
     
    
    #Retriving Multiple Rows
    cursor = connection.cursor()
    #SQLCommand = ("SELECT top 1 Transformed FROM MessageQueue ORDER BY QueueId DESC")
    #SQLCommand = ("SELECT top 3 Transformed FROM (SELECT ROW_NUMBER() OVER (ORDER BY QueueId ASC) AS RowNumber,*FROM MessageQueue Where ProductId = 'Dev') AS foo WHERE RowNumber = 2")
    SQLCommand = ("SELECT top 4 Transformed FROM (SELECT ROW_NUMBER() OVER (ORDER BY QueueId DESC) AS RowNumber,*FROM MessageQueue Where Transformed IS NOT NULL) AS foo WHERE RowNumber = 1")
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
    tree = ET.parse(script_path + "\\oruoutput.xml")
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
    dateTimeOfMsg = mylist[25]      #######
    msgType1 = mylist[29]
    msgType2 = mylist[31]
    msgCntrlId = mylist[33]
    processId = mylist[37]
    versionId = mylist[39]
    SetIdPatientID = mylist[45]
    extPatientID = mylist[49]
    intPatientID = mylist[53]
    PatientLastName = mylist[63]
    PatientFirstName = mylist[61]
    dob = mylist[65]
    Gender = mylist[67]
    PatientAdd = mylist[71]
    orderControl = mylist[85]
    orcplaceOrderNumber = mylist[89]
    #quantTiming = mylist[3]
    ordProviderLastName = mylist[95]
    ordProviderFirstName = mylist[97]  # extra field added
    obrplaceOrdNumb = mylist[107]
    universalServiceId1 = mylist[113]
    universalServiceId2 = mylist[115]     # extra field added

    observationDateTime = mylist[119]
    obrOrderingProviderLastName = mylist[123]
    obrOrderingProviderFirstName = mylist[125]


    resultStatus = mylist[131]
    #quantityTiming = mylist[3]


    obxsetId1 = mylist[138]
    obxvalueType1 = mylist[140]
    obxobservationID1_1 = mylist[144]
    obxobservationID1_2 = mylist[146]
    obxobservationValue1 = mylist[150]
    obxobserveResultStatus1 = mylist[152]


    obxsetId2 = mylist[156]
    obxvalueType2 = mylist[158]
    obxobservationID2_1 = mylist[162]
    obxobservationID2_2 = mylist[164]
    obxobservationValue2 = mylist[168]
    #obxobserveResultStatus2 = mylist[168]

    obxsetId3 = mylist[176]
    obxvalueType3 = mylist[178]
    obxobservationID3_1 = mylist[182]
    obxobservationID3_2 = mylist[184]
    obxobservationValue3 = mylist[188]
    #obxobserveResultStatus3 = mylist[186]

    obxsetId4 = mylist[196]
    obxvalueType4 = mylist[198]
    obxobservationID4_1 = mylist[202]
    obxobservationID4_2 = mylist[204]
    obxobservationValue4 = mylist[208]
    #obxobserveResultStatus4 = mylist[204]

    obxsetId5 = mylist[216]
    obxvalueType5 = mylist[218]
    obxobservationID5_1 = mylist[222]
    obxobservationID5_2 = mylist[224]
    obxobservationValue5 = mylist[228]
    #obxobserveResultStatus5 = mylist[222]

    obxsetId6 = mylist[236]
    obxvalueType6 = mylist[238]
    obxobservationID6_1 = mylist[242]
    obxobservationID6_2 = mylist[244]
    obxobservationValue6 = mylist[248]
    #obxobserveResultStatus6 = mylist[240]

    obxsetId7 = mylist[256]
    obxvalueType7 = mylist[258]
    obxobservationID7_1 = mylist[262]
    obxobservationID7_2 = mylist[264]
    obxobservationValue7 = mylist[268]
    #obxobserveResultStatus7 = mylist[258]

    obxsetId8 = mylist[276]
    obxvalueType8 = mylist[278]
    obxobservationID8_1 = mylist[282]
    obxobservationID8_2 = mylist[284]
    obxobservationValue8 = mylist[288]
    #obxobserveResultStatus8 = mylist[276]

    obxsetId9 = mylist[292]
    obxvalueType9 = mylist[294]
    obxobservationID9_1 = mylist[298]
    obxobservationID9_2 = mylist[300]
    obxobservationValue9 = mylist[304]
    #obxobserveResultStatus9 = mylist[294]

    obxsetId10 = mylist[308]
    obxvalueType10 = mylist[310]
    obxobservationID10_1 = mylist[314]
    obxobservationID10_2 = mylist[316]
    obxobservationValue10 = mylist[320]
    #obxobserveResultStatus10 = mylist[312]

    obxsetId11 = mylist[324]
    obxvalueType11 = mylist[326]
    obxobservationID11_1 = mylist[330]
    obxobservationID11_2 = mylist[332]
    obxobservationValue11 = mylist[336]
    #obxobserveResultStatus11 = mylist[330]

    obxsetId12 = mylist[340]
    obxvalueType12 = mylist[342]
    obxobservationID12_1 = mylist[346]
    obxobservationID12_2 = mylist[348]
    obxobservationValue12 = mylist[352]
    #obxobserveResultStatus12 = mylist[348]

    obxsetId13 = mylist[356]
    obxvalueType13 = mylist[358]
    obxobservationID13_1 = mylist[362]
    obxobservationID13_2 = mylist[364]
    obxobservationValue13 = mylist[367]
    #obxobserveResultStatus13 = mylist[366]

    obxsetId14 = mylist[371]
    obxvalueType14 = mylist[373]
    obxobservationID14_1 = mylist[377]
    obxobservationID14_2 = mylist[379]
    obxobservationValue14 = mylist[383]
    #obxobserveResultStatus14 = mylist[385]




    '''
    #PatientVisit = mylist[69]
    #PatientClass = mylist[67]
    #AttendingDoc1 = mylist[73]
    AttendingDoc2 = mylist[75]
    #AttendingDoc3 = mylist[67]
    HospitalService = mylist[77]
    AdmitSource = mylist[79]
    AmbulatoryStatus = mylist[81]
    AdmitDateTime = mylist[83]
    
    
    #print results
    print type(results)
    if results == None:
        sys.exit("\n\n*****GATEWAY DB DOES NOT HAVE ANY DATA INTO IT... EXITING...*****\n")
    '''

    
    
    print [fieldSep, encodingChar , sendingAppln , sendingFac , receivingAppln , receivingFac , dateTimeOfMsg, msgType1 , msgType2 , msgCntrlId , processId , versionId
           , SetIdPatientID , extPatientID, intPatientID, PatientLastName , PatientFirstName , dob , Gender , PatientAdd , orderControl , orcplaceOrderNumber , quantTiming , ordProviderLastName
           , ordProviderFirstName , obrplaceOrdNumb , universalServiceId1 , universalServiceId2 , observationDateTime , orderingProvider , resultStatus , quantityTiming
           , obxsetId1 , obxvalueType1 , obxobservationID1_1 , obxobservationID1_2 , obxobservationValue1, obxobserveResultStatus1,obxsetId2 , obxvalueType2 , obxobservationID2_1 , obxobservationID2_2 , obxobservationValue2, obxobserveResultStatus2,
           obxsetId3 , obxvalueType3 , obxobservationID3_1 , obxobservationID3_2 , obxobservationValue3, obxobserveResultStatus3,obxsetId4 , obxvalueType4 , obxobservationID4_1 , obxobservationID4_2 , obxobservationValue4, obxobserveResultStatus4,
           obxsetId5 , obxvalueType5 , obxobservationID5_1 , obxobservationID5_2 , obxobservationValue5, obxobserveResultStatus5,obxsetId6 , obxvalueType6 , obxobservationID6_1 , obxobservationID6_2 , obxobservationValue6, obxobserveResultStatus6,
           obxsetId7 , obxvalueType7 , obxobservationID7_1 , obxobservationID7_2 , obxobservationValue7, obxobserveResultStatus7,obxsetId8 , obxvalueType8 , obxobservationID8_1 , obxobservationID8_2 , obxobservationValue8, obxobserveResultStatus8,
           obxsetId9 , obxvalueType9 , obxobservationID9_1 , obxobservationID9_2 , obxobservationValue9, obxobserveResultStatus9,obxsetId10 , obxvalueType10 , obxobservationID10_1 , obxobservationID10_2 , obxobservationValue10, obxobserveResultStatus10,
           obxsetId11 , obxvalueType11 , obxobservationID11_1 , obxobservationID11_2 , obxobservationValue11, obxobserveResultStatus11,obxsetId12 , obxvalueType12 , obxobservationID12_1 , obxobservationID12_2 , obxobservationValue12, obxobserveResultStatus12,
           obxsetId13 , obxvalueType13 , obxobservationID13_1 , obxobservationID13_2 , obxobservationValue13, obxobserveResultStatus13,obxsetId14 , obxvalueType14 , obxobservationID14_1 , obxobservationID14_2 , obxobservationValue14, obxobserveResultStatus14]
    

    
    return [fieldSep, encodingChar , sendingAppln , sendingFac , receivingAppln , receivingFac , dateTimeOfMsg, msgType1 , msgType2 , msgCntrlId , processId , versionId
           , SetIdPatientID , extPatientID, intPatientID,PatientLastName , PatientFirstName , dob , Gender , PatientAdd , orderControl , orcplaceOrderNumber , quantTiming , ordProviderLastName
           , ordProviderFirstName , obrplaceOrdNumb , universalServiceId1 , universalServiceId2 , observationDateTime , orderingProvider , resultStatus , quantityTiming
           , obxsetId1 , obxvalueType1 , obxobservationID1_1 , obxobservationID1_2 , obxobservationValue1, obxobserveResultStatus1,obxsetId2 , obxvalueType2 , obxobservationID2_1 , obxobservationID2_2 , obxobservationValue2, obxobserveResultStatus2,
           obxsetId3 , obxvalueType3 , obxobservationID3_1 , obxobservationID3_2 , obxobservationValue3, obxobserveResultStatus3,obxsetId4 , obxvalueType4 , obxobservationID4_1 , obxobservationID4_2 , obxobservationValue4, obxobserveResultStatus4,
           obxsetId5 , obxvalueType5 , obxobservationID5_1 , obxobservationID5_2 , obxobservationValue5, obxobserveResultStatus5,obxsetId6 , obxvalueType6 , obxobservationID6_1 , obxobservationID6_2 , obxobservationValue6, obxobserveResultStatus6,
           obxsetId7 , obxvalueType7 , obxobservationID7_1 , obxobservationID7_2 , obxobservationValue7, obxobserveResultStatus7,obxsetId8 , obxvalueType8 , obxobservationID8_1 , obxobservationID8_2 , obxobservationValue8, obxobserveResultStatus8,
           obxsetId9 , obxvalueType9 , obxobservationID9_1 , obxobservationID9_2 , obxobservationValue9, obxobserveResultStatus9,obxsetId10 , obxvalueType10 , obxobservationID10_1 , obxobservationID10_2 , obxobservationValue10, obxobserveResultStatus10,
           obxsetId11 , obxvalueType11 , obxobservationID11_1 , obxobservationID11_2 , obxobservationValue11, obxobserveResultStatus11,obxsetId12 , obxvalueType12 , obxobservationID12_1 , obxobservationID12_2 , obxobservationValue12, obxobserveResultStatus12,
           obxsetId13 , obxvalueType13 , obxobservationID13_1 , obxobservationID13_2 , obxobservationValue13, obxobserveResultStatus13,obxsetId14 , obxvalueType14 , obxobservationID14_1 , obxobservationID14_2 , obxobservationValue14, obxobserveResultStatus14]
    
    
    
    connection.close()

    

if __name__ == '__main__':
    readDataFromDBORU()