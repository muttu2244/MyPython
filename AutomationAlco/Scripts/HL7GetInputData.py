# -*- coding: utf-8 -*-
#from hl7 import Message, Segment, Field
  
import hl7
import unittest
from ReadHL7InputData import readHL7Input
#from ReadDB import readDataFromDB
import ReadDB

#DataFeederList = readHL7Input()
actualResultsList = ReadDB.readDataFromDB()
print actualResultsList

'''
for mshData in DataFeederList[0]:
    GetMshInputData(mshData)

for pidData in DataFeederList[1]:
	GetPidInputData(pidData)

for orcData in DataFeederList[2]:
	GetOrcInputData(orcData)

for obrData in DataFeederList[3]:
	GetObrInputData(obrData)

for obxData in DataFeederList[4]:
	GetObxInputData(obxData)
'''
MSHList =	[ ]
PIDList  =	  [ ]
ORCList = [ ]
OBRList = [ ]
OBXList = [ ]
PVList = [ ]
EVNList = [ ]
SCHList = [ ]
AILList = [ ]
AIPList = [ ]



def GetMshInputData():
	#print actualResultsList
	#for mshData in DataFeederList[0]:
		#print mshData
	#mshData = DataFeederList[0]
		
	print "**************************Test MSH HL7**************************"
	
	FieldSep = actualResultsList[0].encode('utf8')
	
	EncodingChar = actualResultsList[1].encode('utf8')
	
	SendingAppln = actualResultsList[2].encode('utf8')
	
	SendingFac = actualResultsList[3].encode('utf8')
	
	ReceivingAppln = actualResultsList[4].encode('utf8')

	ReceivingFac = actualResultsList[5].encode('utf8')
	
	#DateTimeMsg = actualResultsList[6].encode('utf8')
	 
	MsgType1 = actualResultsList[6].encode('utf8')

	MsgType2 = actualResultsList[7].encode('utf8')
	
	MsgCntrlId = actualResultsList[8].encode('utf8')

	ProcessingId = actualResultsList[9].encode('utf8')
	
	VersionId = actualResultsList[10].encode('utf8')
	
	
	return [FieldSep, EncodingChar, SendingAppln, SendingFac, ReceivingAppln, ReceivingFac, MsgType1,MsgType2,MsgCntrlId,ProcessingId,VersionId]
		
		

def GetPidInputData():
	print "**************************Test PID HL7**************************"
	SetId = actualResultsList[11].encode('utf8')
	PatientLastName = actualResultsList[12].encode('utf8')
	PatientFirstName = actualResultsList[13].encode('utf8')
	Dob = actualResultsList[14].encode('utf8')
	Gender = actualResultsList[15].encode('utf8')
	PatientAdd = actualResultsList[16].encode('utf8')
	return [SetId, PatientLastName, PatientFirstName, Dob,Gender, PatientAdd ]


def GetPVInputData():
	print "**************************Test PV HL7**************************"
	patientVisitSetID = actualResultsList[17].encode('utf8')
	patientClass = actualResultsList[18].encode('utf8')
	attendingDoc = actualResultsList[19].encode('utf8')
	hospitalService = actualResultsList[20].encode('utf8')
	admitSource = actualResultsList[21].encode('utf8')
	ambulatoryStatus = actualResultsList[22].encode('utf8')
	admitDateTime = actualResultsList[23].encode('utf8')
	return [ patientVisitSetID, patientClass, attendingDoc, hospitalService, admitSource, ambulatoryStatus, admitDateTime]

def GetEVNInputData():
	print "**************************Test EVN HL7**************************"
	eventTypeCode = actualResultsList[24].encode('utf8')
	eventOccured = actualResultsList[25].encode('utf8')
	return [ eventTypeCode, eventOccured]

	

def GetOrcInputData():
	for data in DataFeederList[2]:
		OrdCntrl = data[1]
		OrdNumb = data[2]
		QuantTime = data[3]
		OrdProvider = data[4]
		return ORCList[OrdCntrl, OrdNumb, QuantTime, OrdProvider]

def GetObrInputData():
	for data in DataFeederList[3]:
		PlaceOrderNumb = data[1]
		UniServiceID = data[2]
		ObservationDateTime = data[3]
		OrdProvider = data[4]
		ResultStatus = data[5]
		QuantTime = data[6]
		return OBRList[PlaceOrderNumb, UniServiceID, ObservationDateTime, OrdProvider, ResultStatus, QuantTime]

def GetObxInputData():
	for data in DataFeederList[4]:
		setID = data[1]
		valType = data[2]
		ObservationID = data[3]
		ObservationVal = data[4]
		ObserveResultStatus = data[5]
		return OBXList[ setID, valType, ObservationID, ObservationVal, ObserveResultStatus]

'''
def GetSCHInputData():
	for data in DataFeederList[7]:
		placerApptId = data[1]
		scheduleId = data[2]
		eventReason = data[3]
		appointmentTimingQuantity = data[4]
		enteredByPerson = data[5]
		return OBXList[ placerApptId, scheduleId, eventReason, appointmentTimingQuantity, enteredByPerson]


def GetAILInputData():
	for data in DataFeederList[8]:
		setID = data[1]
		locationResourceId = data[2]
		return OBXList[ setID, locationResourceId]

def GetAIPInputData():
	for data in DataFeederList[9]:
		setID = data[1]
		personalResId = data[2]
		return OBXList[ setID, personalResId]
'''


if __name__ == '__main__':
	#unittest.main()
	GetMshInputData()


    