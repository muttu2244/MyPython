# -*- coding: utf-8 -*-
#from hl7 import Message, Segment, Field
  
import hl7
import unittest, os
import HTMLTestRunner
import time
import xlrd,datetime
from ReadDBADT import readDataFromDBADT


#from HL7GetInputData import GetMshInputData, GetPidInputData, GetPVInputData,GetEVNInputData
#import HL7GetInputData
from ReadUIInputData import readUIInput
from VersionInfo import getConfig

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

adtResultList = readDataFromDBADT()

uiInputData = readUIInput(script_path + '\\ADTUIInputTestData.xlsx')[0]
print uiInputData

#hl7InputData = readHL7Input()
#print hl7InputData[0]


############################################################

class cMSHParseTest(unittest.TestCase):
	#for mshData in hl7InputData[0]:
		#print mshData
	#mshData = hl7InputData[0]
	#actualMshResultsList = HL7GetInputData.GetMshInputData()
	print "**************************Test ADT MSH **************************"
	def test_3EncodingChars(self):
		#plan = hl7.create_parse_plan(sample_hl7)
		#self.assertEqual(plan.separators, [u'\r', '|', '~', '^', '&'])
		
		#self.assertEqual(mshData[2], actualMshResultsList[1])
		self.assertEqual(ver[1], adtResultList[1])

	def test_4SendingApplication(self):
		#msg = hl7.parse(sample_hl7)
		
		#self.assertEqual(mshData[3], actualMshResultsList[2])
		#self.assertEqual(ver[2], adtResultList[2])
		self.assertTrue(adtResultList[2])
		
	def test_5SendingFacility(self):
		#msg = hl7.parse(sample_hl7)
		
		#self.assertEqual(msg[0][4], [unicode(mshData[3])])
		#self.assertEqual(mshData[4], actualMshResultsList[2])
		#self.assertEqual(ver[3], adtResultList[3])
		self.assertTrue(adtResultList[3])

	def test_6ReceivingAppln(self):
		#msg = hl7.parse(sample_hl7)
		
		#self.assertEqual(msg[0][5], [unicode(mshData[4])])
		#self.assertEqual(mshData[5], actualMshResultsList[2])
		#self.assertEqual(ver[4], adtResultList[4])
		self.assertTrue(adtResultList[4])

	def test_7ReceivingFacility(self):
		#msg = hl7.parse(sample_hl7)
		
		#self.assertEqual(msg[0][6], [unicode(mshData[5])])
		#self.assertEqual(mshData[6], actualMshResultsList[2])
		#self.assertEqual(ver[5], adtResultList[5])
		self.assertTrue(adtResultList[5])
		
	def test_8DateTime(self):	#expected result from UIData.xls / actual result from gatewaydb
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[0][7], [u'199912271408'])
		#self.assertEqual(msg[0][7], [unicode(mshData[6])])
		#self.assertEqual(msg[0][7], mshData[6])
		pass

	'''
	def test_Security(self):
		msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[0][8], [u'CHARRIS'])
		self.assertEqual(msg[0][8], [unicode(mshData[8])])
	'''
	
	def test_9MessageType(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[0][9], [[[u'ADT'], [u'A04']])])
		#self.assertEqual(msg[0][9], [[[unicode(actualMshResultsList[6])],[unicode(actualMshResultsList[7])]]] )
		
		#self.assertEqual(mshData[7], actualMshResultsList[2])
		self.assertEqual([ver[6],ver[22]], [adtResultList[6],adtResultList[7]] )
		
	def test_10MessageCntrlID(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[0][10], [u'1817457'])
		
		
		#self.assertEqual(mshData[3], actualMshResultsList[2])
		self.assertTrue(len(adtResultList[8]) <= 20) 

	def test_11ProcessingID(self):		#expected result from UIData.xls / actual result from gatewaydb
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[0][11], [u'D'])
		
		
		#self.assertEqual(mshData[3], actualMshResultsList[2])
		self.assertEqual(ver[7], adtResultList[9])

	def test_12VersionID(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[0][12], [u'2.5'])
		#self.assertEqual(msg[0][12], [unicode(actualMshResultsList[10])])
		
		#self.assertEqual(mshData[3], actualMshResultsList[2])
		self.assertEqual(ver[8], adtResultList[10])



class dPIDParseTest(unittest.TestCase):
	#actualPidResultsList = HL7GetInputData.GetPidInputData()
	print "**************************Test ADT PID**************************"
	def test_13SetId(self):		
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[1][2][0][0], [u'0493575'])
		#self.assertEqual(' ', actualPidResultsList[0])
		self.assertTrue(len(adtResultList[11]) <= 4)

	def test_14PatientLastName(self):	#expected result from UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[1][2][0][0], [u'0493575'])
		self.assertEqual(uiInputData[1].encode('utf8'), adtResultList[12])
		
	def test_15PatientFirstName(self):	#expected result from UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[1][3], [u'454721'])
		self.assertEqual(uiInputData[0].encode('utf8'), adtResultList[13])

	def test_16Dob(self):			#expected result from UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual((msg[1][5][0][0],msg[1][5][0][1]), ([u'DOE'], [u'JOHN']))
		wb = xlrd.open_workbook(script_path + '\\ADTUIInputTestData.xlsx')
		dt = datetime.datetime(*xlrd.xldate_as_tuple(int(uiInputData[4].encode('utf8')), wb.datemode))
		dtOfBirth = dt.strftime("%Y%m%d")
		self.assertEqual(dtOfBirth, adtResultList[14][0:8])
		self.assertTrue(len(adtResultList[14]) <= 26)
						 

	def test_17Gender(self):	#expected result from UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual((msg[1][6][0][0],msg[1][6][0][1]), ([u'DOE'], [u'JOHN']))
		if uiInputData[3]== '0':
			gender = 'M'
		elif uiInputData[3] == '1':
			gender = 'F'
		self.assertEqual(gender, adtResultList[15])
		self.assertTrue(len(adtResultList[15]) == 1)
		
	def test_18PatientAdd(self):	#expected result from UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[1][7], [u'19480203'])
		self.assertEqual(uiInputData[7].encode('utf8'), adtResultList[16])
		self.assertTrue(len(adtResultList[16]) == 106)


class ePVParseTest(unittest.TestCase):
	#actualPVResultsList =  HL7GetInputData.GetPVInputData()
	print "**************************Test ADT PV**************************"
	def test_19SetId(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[3][2], [u'O'])
		#self.assertEqual(' ', actualPVResultsList[0])
		self.assertTrue(len(adtResultList[17]) <= 4)

	def test_20PatientClass(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[3][2], [u'O'])
		#self.assertEqual(' ', actualPVResultsList[1])
		self.assertTrue(len(adtResultList[18]) <= 1)
		
	
	def test_21AttendingDoc1(self):	#From UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[3][2][0][0], [u'0493575'])
		#self.assertEqual((msg[3][3][0][0]),  u'168 ')
		#self.assertEqual(' ',  actualPVResultsList[2])
		self.assertTrue(len(adtResultList[19]) <= 60)

	def test_21AttendingDoc2(self):	#From UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[3][2][0][0], [u'0493575'])
		#self.assertEqual((msg[3][3][0][0]),  u'168 ')
		#self.assertEqual(' ',  actualPVResultsList[2])
		self.assertTrue(len(adtResultList[20]) <= 60)
	
	def test_22HospitalService(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual((msg[3][7][0][0],msg[3][7][0][1],msg[3][7][0][2]), ([u'277'], [u'ALLEN MYLASTNAME'],[u'BONNIE']))
		self.assertEqual(ver[9], adtResultList[22])
		self.assertTrue(len(adtResultList[22]) <= 3)
	
	def test_23AdmitSource(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual((msg[1][6][0][0],msg[1][6][0][1]), ([u'DOE'], [u'JOHN']))
		self.assertEqual(ver[10], adtResultList[23])
		self.assertTrue(len(adtResultList[23]) <= 3)
	
	def test_24AmbulatoryStatus(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[3][19], [u'2688684'])
		self.assertEqual(ver[11], adtResultList[24])
		self.assertTrue(len(adtResultList[24]) <= 2)

	def test_25AdmitDateTime(self):	#UI
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[3][44], [u'199912271408'])
		#self.assertEqual(' ', adtResultList[25])
		self.assertTrue(len(adtResultList[25]) <= 26)


class fEVNParseTest(unittest.TestCase):
	#actualEVNResultsList = HL7GetInputData.GetEVNInputData()
	print "**************************Test ADT EVN**************************"
	def test_26eventTypeCode(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[3][2], [u'O'])
		self.assertEqual(ver[12], adtResultList[26])
		self.assertTrue(len(adtResultList[26]) <= 3)

	def test_27eventOccured(self):
		#msg = hl7.parse(sample_hl7)
		#self.assertEqual(msg[3][2], [u'O'])
		#self.assertEqual(' ', adtResultList[27])
		self.assertTrue(len(adtResultList[27]) <= 26)



		

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
	#unittest.main()

	
	suite = unittest.TestSuite()

	suite.addTests([
			unittest.TestLoader().loadTestsFromTestCase(cMSHParseTest),
			unittest.TestLoader().loadTestsFromTestCase(dPIDParseTest),
			unittest.TestLoader().loadTestsFromTestCase(ePVParseTest),
			unittest.TestLoader().loadTestsFromTestCase(fEVNParseTest),
			])


	#suite = unittest.TestLoader().loadTestsFromTestCase(MSHParseTest)
	unittest.TextTestRunner(verbosity=2).run(suite)
	runtime = time.strftime("%Y%m%d%H%M%S")
	#outfile = open("D:\\MedicalDevices\\AlconProject\\Testing\\FinalTestScripts\\Reports\\ADTReport" + runtime + ".html", "w")
	outfile = open(script_path + "\\Reports\\ADTReport" + runtime + ".html", "w")
	
	runner = HTMLTestRunner.HTMLTestRunner(
				stream=outfile,
				title='ADT Test Report %s'%ver[0],
				description='This demonstrates the ADT Report run at ' + runtime
				)
	runner.run(suite)
	outfile.close()
	
	#unittest.TestCase.id()

