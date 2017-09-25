# -*- coding: utf-8 -*-
#from hl7 import Message, Segment, Field
  
import hl7
import unittest, os
import HTMLTestRunner
import time
import xlrd


#from HL7GetInputData import GetMshInputData, GetPidInputData, GetOrcInputData, GetObrInputData, GetObxInputData
from ReadUIInputData import readUIInput
from VersionInfo import getConfig
from ReadDBOMG import readDataFromDBOMG

## Sample message from HL7 Normative Edition
## http://healthinfo.med.dal.ca/hl7intro/CDA_R2_normativewebedition/help/v3guide/v3guide.htm#v3gexamples

############################################################
'''
hl7Data = open('D:\MedicalDevices\AlconProject\Testing\FinalTestScripts\\sample.hl7.txt', 'r')
sample_hl7 = []
for line in hl7Data:
	sample_hl7.append(line)

hl7Data.close()
sample_hl7 = '\r'.join(sample_hl7)
'''

ver = getConfig()

script_path = os.path.dirname(__file__)
print script_path
script_dir = os.path.split(script_path)[0]
print script_dir
#projDir = os.path.join(script_dir, 'V1.16' + '\\' + 'EMR' + '\\' + 'EMRApp' + '\\')
#projDir = os.path.join(script_dir, 'SRC' + '\\' + 'V1.20' + '\\' + 'V1.20' + '\\' + 'Alcon' + '\\' + 'output' + '\\' + 'EMR' + '\\' + 'EMRApp' + '\\')
projDir = os.path.join(script_dir, 'SRC' + '\\' + ver[0] + '\\' + 'Alcon' + '\\' + 'output' + '\\' + 'EMR' + '\\' + 'EMRApp' + '\\')
print projDir

#oruResultList = GetMshInputData()
#actualPidResultsList = GetPidInputData()
#actualOrcResultsList = GetOrcInputData()
#actualObrResultsList = GetObrInputData()
#actualObxResultsList = GetObxInputData()

omgResultList = readDataFromDBOMG()

uiInputData = readUIInput(script_path + '\\ADTUIInputTestData.xlsx')[0] # CHANGE THIS INPUT FILE FOR ORM DATA
print uiInputData

#hl7InputData = readHL7Input()
#print hl7InputData[0]


############################################################

class cMSHParseTest(unittest.TestCase):
	#for mshData in hl7InputData[0]:
		#print mshData
	#mshData = hl7InputData[0]
	#omgResultList = readDataFromDBOMG()
	print "**************************Test ADT MSH **************************"
	def test_3EncodingChars(self):
		#plan = hl7.create_parse_plan(sample_hl7)
		#self.assertEqual(plan.separators, [u'\r', '|', '~', '^', '&'])
		
		#self.assertEqual(mshData[2], oruResultList[1])
		self.assertEqual(ver[1], omgResultList[1])

	def test_4SendingApplication(self):
		#msg = hl7.parse(sample_hl7)
		
		#self.assertEqual(mshData[3], oruResultList[2])
		#self.assertEqual(ver[2], omgResultList[2])
		self.assertTrue(omgResultList[2])
		
	def test_5SendingFacility(self):
		#msg = hl7.parse(sample_hl7)
		
		#self.assertEqual(msg[0][4], [unicode(mshData[3])])
		#self.assertEqual(mshData[4], oruResultList[2])
		#self.assertEqual(ver[3], omgResultList[3])
		self.assertTrue(omgResultList[3])

	def test_6ReceivingAppln(self):
		#msg = hl7.parse(sample_hl7)
		
		#self.assertEqual(msg[0][5], [unicode(mshData[4])])
		#self.assertEqual(mshData[5], oruResultList[2])
		#self.assertEqual(ver[4], omgResultList[4])
		self.assertTrue(omgResultList[4])

	def test_7ReceivingFacility(self):
		#msg = hl7.parse(sample_hl7)
		
		#self.assertEqual(msg[0][6], [unicode(mshData[5])])
		#self.assertEqual(mshData[6], oruResultList[2])
		#self.assertEqual(ver[5], omgResultList[5])
		self.assertTrue(omgResultList[5])
		
	def test_8DateTime(self):	#expected result from UIData.xls / actual result from gatewaydb
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[0][7], [u'199912271408'])
		#self.assertEqual(msg[0][7], [unicode(mshData[6])])
		#self.assertEqual(msg[0][7], mshData[6])
		self.assertTrue(len(omgResultList[6]) <= 26)

	'''
	def test_Security(self):
		msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[0][8], [u'CHARRIS'])
		self.assertEqual(msg[0][8], [unicode(mshData[8])])
	'''
	
	def test_9MessageType(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[0][9], [[[u'ADT'], [u'A04']])])
		#self.assertEqual(msg[0][9], [[[unicode(oruResultList[6])],[unicode(oruResultList[7])]]] )
		
		#self.assertEqual(mshData[7], oruResultList[2])
		#self.assertEqual(ver[14], [omgResultList[6],omgResultList[7]] )
		self.assertEqual([ver[14],ver[23]], [omgResultList[7],omgResultList[8]] )
		
		
	def test_10MessageCntrlID(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[0][10], [u'1817457'])
		
		
		#self.assertEqual(mshData[3], oruResultList[2])
		#self.assertTrue(len(omgResultList[8]) <= 20)
		self.assertTrue(len(omgResultList[9]) <= 20)

	def test_11ProcessingID(self):		#expected result from UIData.xls / actual result from gatewaydb
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[0][11], [u'D'])
		
		
		#self.assertEqual(mshData[3], oruResultList[2])
		#self.assertEqual(ver[7], omgResultList[9])
		self.assertEqual(ver[7], omgResultList[10])

	def test_12VersionID(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[0][12], [u'2.5'])
		#self.assertEqual(msg[0][12], [unicode(oruResultList[10])])
		
		#self.assertEqual(mshData[3], oruResultList[2])
		#self.assertEqual(ver[8], omgResultList[10])
		self.assertEqual(ver[8], omgResultList[11])



class dPIDParseTest(unittest.TestCase):
	#omgResultList = readDataFromDBOMG()
	print "**************************Test ADT PID**************************"
	def test_SetId(self):		
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[1][2][0][0], [u'0493575'])
		#self.assertEqual(' ', omgResultList[11])
		self.assertTrue(len(omgResultList[12]) <= 4)		#GET the LENGTH
		

	def test_extPatientID(self):	#expected result from UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[1][2][0][0], [u'0493575'])
		#self.assertEqual('', omgResultList[12])
		self.assertTrue(len(omgResultList[13]) <= 20)

	def test_intPatientID(self):	#expected result from UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[1][2][0][0], [u'0493575'])
		#self.assertEqual('', omgResultList[13])
		self.assertTrue(len(omgResultList[14]) <= 20)

	def test_PatientLastName(self):	#expected result from UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[1][2][0][0], [u'0493575'])
		self.assertEqual(uiInputData[1].encode('utf8'), omgResultList[15])
		
	def test_15PatientFirstName(self):	#expected result from UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[1][3], [u'454721'])
		self.assertEqual(uiInputData[0].encode('utf8'), omgResultList[16])

	def test_16Dob(self):			#expected result from UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual((msg[1][5][0][0],msg[1][5][0][1]), ([u'DOE'], [u'JOHN']))
		wb = xlrd.open_workbook(script_path + '\\ADTUIInputTestData.xlsx')
		dt = xlrd.xldate.xldate_as_datetime(int(uiInputData[4].encode('utf8')), wb.datemode)
		#self.assertEqual(dt, actualPidResultsList[3][0:8])
		dtOfBirth = dt.strftime("%Y%m%d")
		self.assertEqual(dtOfBirth, omgResultList[17][0:8])
		self.assertTrue(len(omgResultList[17]) <= 26)
						 

	def test_17Gender(self):	#expected result from UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual((msg[1][6][0][0],msg[1][6][0][1]), ([u'DOE'], [u'JOHN']))
		if uiInputData[3]== '0':
			gender = 'M'
		elif uiInputData[3] == '1':
			gender = 'F'
		self.assertEqual(gender, omgResultList[18])
		self.assertTrue(len(actualPidResultsList[18]) == 1)
		
	def test_18PatientAdd(self):	#expected result from UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[1][7], [u'19480203'])
		self.assertEqual(uiInputData[7].encode('utf8'), omgResultList[19])
		


class ORCParseTest(unittest.TestCase):
	#omgResultList = readDataFromDBOMG()
	def test_OrderControl(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual((msg[2][2][0][0],msg[2][2][0][1]), ([u'ROE'], [u'MARIE']))
		#self.assertEqual(' ', omgResultList[19])
		self.assertTrue(len(omgResultList[20]) <= 2)
		
	def test_PlacerOrderNumber(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[2][3], [u'SPO'])
		#self.assertEqual(' ', omgResultList[20])
		self.assertTrue(len(omgResultList[21]) <= 22)

	def test_QuantityTiming(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[2][5], [u'(216)123-4567'])
		#self.assertEqual(' ', omgResultList[21])
		self.assertTrue(len(omgResultList[22]) <= 200)

	def test_OrderingProvider(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[2][7], [u'EC'])
		self.assertEqual([uiInputData[13].encode('utf8').upper(), uiInputData[12].encode('utf8').upper()], [omgResultList[23].upper(),omgResultList[24].upper()])
		#self.assertEqual(uiInputData[13].encode('utf8'), siuResultList[13])
		



class OBRParseTest(unittest.TestCase):
	#omgResultList = readDataFromDBOMG()
	def test_PlaceOrderNumb(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual((msg[2][2][0][0],msg[2][2][0][1]), ([u'ROE'], [u'MARIE']))
		#self.assertEqual(' ', omgResultList[19])
		self.assertTrue(len(omgResultList[25]) <= 26)
		
	def test_universalServiceId1(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[2][3], [u'SPO'])
		#self.assertEqual(' ', omgResultList[25])
		self.assertTrue(len(omgResultList[26]) <= 200)

	def test_universalServiceId2(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[2][3], [u'SPO'])
		#self.assertEqual(' ', omgResultList[26])
		self.assertTrue(len(omgResultList[27]) <= 200)

	def test_ObservationDateTime(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[2][5], [u'(216)123-4567'])
		#self.assertEqual(' ', omgResultList[27])
		self.assertTrue(len(omgResultList[28]) <= 26)

	def test_OrderingProvider(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[2][7], [u'EC'])
		#self.assertEqual(' ', omgResultList[28])
		self.assertTrue(len(omgResultList[29]) <= 120)

	def test_ResultStatus(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[2][5], [u'(216)123-4567'])
		#self.assertEqual(' ', omgResultList[29])
		self.assertTrue(len(omgResultList[30]) <= 1)

	def test_QuantityTiming(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[2][5], [u'(216)123-4567'])
		#self.assertEqual(' ', omgResultList[30])
		self.assertTrue(len(omgResultList[31]) <= 200)


class OBXParseTest(unittest.TestCase):
	#omgResultList = readDataFromDBOMG()
	def test_SetId(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual((msg[2][2][0][0],msg[2][2][0][1]), ([u'ROE'], [u'MARIE']))
		#self.assertEqual(' ',  omgResultList[31])
		self.assertTrue(len(omgResultList[32]) <= 4)

	def test_ValueType(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[2][3], [u'SPO'])
		#self.assertEqual(' ', omgResultList[32])
		self.assertTrue(len(omgResultList[33]) <= 4)

	def test_ObservationID(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[2][5], [u'(216)123-4567'])
		#self.assertEqual(' ', omgResultList[33])
		self.assertTrue(len(omgResultList[34]) <= 80)

	def test_ObservationValue(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[2][7], [u'EC'])
		#self.assertEqual(' ', omgResultList[34])
		self.assertTrue(len(omgResultList[35]) <= pow(655363,3))

	def test_ObserveResultStatus(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[2][7], [u'EC'])
		#self.assertEqual(' ', omgResultList[35])
		self.assertTrue(len(omgResultList[36]) <= 1)

		

"""
'''
class NKParseTest(unittest.TestCase):

	def test_NameOfKin(self):
		msg = hl7.parse(sample_hl7)
		self.assertEqual((msg[2][2][0][0],msg[2][2][0][1]), ([u'ROE'], [u'MARIE']))
		
	def test_Relationship(self):
		msg = hl7.parse(sample_hl7)
		self.assertEqual(msg[2][3], [u'SPO'])

	def test_PhoneNum(self):
		msg = hl7.parse(sample_hl7)
		self.assertEqual(msg[2][5], [u'(216)123-4567'])

	def test_MothersMaidenName(self):
		msg = hl7.parse(sample_hl7)
		self.assertEqual(msg[2][7], [u'EC'])
		
'''


'''
class IsHL7Test(unittest.TestCase):
    def test_ishl7(self):
        self.assertTrue(hl7.ishl7(sample_hl7))
  
    def test_ishl7_empty(self):
        self.assertFalse(hl7.ishl7(''))
  
    def test_ishl7_None(self):
        self.assertFalse(hl7.ishl7(None))
  
    def test_ishl7_wrongsegment(self):
        message = 'NK1||ROE^MARIE^^^^|SPO||(216)123-4567||EC|||||||||||||||||||||||||||\r'
        self.assertFalse(hl7.ishl7(message))
  
  
class ContainerTest(unittest.TestCase):
    def test_unicode(self):
        msg = hl7.parse(sample_hl7)
        self.assertEqual(unicode(msg), sample_hl7.strip())
        self.assertEqual(unicode(msg[3][2]),u'O')
        #self.assertEqual(msg[3][2],'ROE^MARIE^^^^')
    def test_container_unicode(self):
        c = hl7.Container('|')
        c.extend(['1', 'b', 'data'])
        self.assertEqual(unicode(c), '1|b|data')

'''
"""
if __name__ == '__main__':
	#unittest.main()\
	suite = unittest.TestSuite()

	suite.addTests([
			unittest.TestLoader().loadTestsFromTestCase(cMSHParseTest),
			unittest.TestLoader().loadTestsFromTestCase(dPIDParseTest),
			unittest.TestLoader().loadTestsFromTestCase(ORCParseTest),
			unittest.TestLoader().loadTestsFromTestCase(OBRParseTest),
			unittest.TestLoader().loadTestsFromTestCase(OBXParseTest),
			])


	#suite = unittest.TestLoader().loadTestsFromTestCase(MSHParseTest)
	unittest.TextTestRunner(verbosity=2).run(suite)
	runtime = time.strftime("%Y%m%d%H%M%S")
	#outfile = open("D:\\MedicalDevices\\AlconProject\\Testing\\FinalTestScripts\\Reports\\ADTReport" + runtime + ".html", "w")
	outfile = open(script_path + "\\Reports\\OMGReport" + runtime + ".html", "w")
	runner = HTMLTestRunner.HTMLTestRunner(
				stream=outfile,
				title='OMG Test Report %s'%ver[0],
				description='This demonstrates the OMG Report run at ' + runtime
				)
	runner.run(suite)
	outfile.close()

	#unittest.TestCase.id()

