import unittest, time, os, HTMLTestRunner

from Dashboard import aDashboardStartTest
from EMRLandingPageSearch import bUILandingPageTest
#from StartBat import startBatTest
from TestADT import cMSHParseTest, dPIDParseTest, ePVParseTest, fEVNParseTest
#from StopBat import stopBatTest

from VersionInfo import getVersionInfo
ver = getVersionInfo()

'''
test_suite = unittest.TestSuite()
test_suite.addTest(unittest.makeSuite(startBatTest))
test_suite.addTest(unittest.makeSuite(DashboardStartTest))
test_suite.addTest(unittest.makeSuite(UILandingPageTest))

test_suite.addTest(unittest.makeSuite(stopBatTest))

test_suite.addTest(unittest.makeSuite(MSHParseTest))
test_suite.addTest(unittest.makeSuite(PIDParseTest))
test_suite.addTest(unittest.makeSuite(PVParseTest))
test_suite.addTest(unittest.makeSuite(EVNParseTest))

runner=unittest.TextTestRunner()
runner.run(test_suite)

'''

script_path = os.path.dirname(__file__)
print script_path
script_dir = os.path.split(script_path)[0]
print script_dir
#projDir = os.path.join(script_dir, 'V1.16' + '\\' + 'EMR' + '\\' + 'EMRApp' + '\\')
#projDir = os.path.join(script_dir, 'SRC' + '\\' + 'V1.20' + '\\' + 'V1.20' + '\\' + 'Alcon' + '\\' + 'output' + '\\' + 'EMR' + '\\' + 'EMRApp' + '\\')
projDir = os.path.join(script_dir, 'SRC' + '\\' + ver + '\\' + ver + '\\' + 'Alcon' + '\\' + 'output' + '\\' + 'EMR' + '\\' + 'EMRApp' + '\\')
print projDir

if __name__ == '__main__':
	#unittest.main()\
	test_suite = unittest.TestSuite()
	#test_suite.addTest(unittest.makeSuite(startBatTest))
	#print "Calling Dashboard\n"
	test_suite.addTest(unittest.makeSuite(aDashboardStartTest))
	#print "Calling UILandingPage\n"
	test_suite.addTest(unittest.makeSuite(bUILandingPageTest))
	#test_suite.addTest(unittest.makeSuite(stopBatTest))
	test_suite.addTest(unittest.makeSuite(cMSHParseTest))
	test_suite.addTest(unittest.makeSuite(dPIDParseTest))
	test_suite.addTest(unittest.makeSuite(ePVParseTest))
	test_suite.addTest(unittest.makeSuite(fEVNParseTest))


	#suite = unittest.TestLoader().loadTestsFromTestCase(MSHParseTest)
	#unittest.TextTestRunner(verbosity=2).run(test_suite)
	runtime = time.strftime("%Y%m%d%H%M%S")
	#outfile = open("D:\\MedicalDevices\\AlconProject\\Testing\\FinalTestScripts\\Reports\\ADTReport" + runtime + ".html", "w")
	outfile = open(script_path + "\\Reports\\EMRReport" + runtime + ".html", "w")
	runner = HTMLTestRunner.HTMLTestRunner(
				stream=outfile,
				title='EMR Test Report',
				description='This demonstrates the EMR Report run at ' + runtime
				)
	#runner.run(suite)
	#runner=unittest.TextTestRunner()
	runner.run(test_suite)
	#unittest.TestSuite.id()
	#unittest.TestCase.id()

	outfile.close()









