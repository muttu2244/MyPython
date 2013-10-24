#!/usr/bin/python26
import sys,os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
import random
from auth import *
from internal_api import *

def get_threshold_data(version,level,uidlist):
	data = {"version": version, "level": level, "thresholds": {"measures": {}, "computed-measures": {}} }
        for id in uidlist:
		value = {"play-time": random.randrange(100), "cash": random.randrange(1000), "time": random.randrange(1000)}
		data["thresholds"]["measures"].update({str(id): value})
		data["thresholds"]["computed-measures"].update({str(id): value})
	return data
	

class thresholds_update(unittest.TestCase):

	def check_pass(self, zauth, data):
		#data = get_threshold_data(version, level, uidlist)
		ret = threshold_update_api(zauth, data)
		try:
			if ret["status"]["error"] == 0:
				return [True, ret]

			else:
				return [False, ret]
		except:
			return [False, ret]

	def check_fail(self, zauth, data, err_code):
		#data = get_threshold_data(version, level, uidlist)
		ret = threshold_update_api(zauth, data)
		try:
			if ret["status"]["error"] == err_code:
				return [True, ret]
			else:
				return [False, ret]
		except:
			return [False, ret]

	def test_threshold_update_functional(self):
                zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		uidlist = [random.randint(100,200) for x in range(10)]
		data = get_threshold_data(Constants.VERSION,Constants.LEVEL, uidlist)
		ret, result = self.check_pass(zauth,data) 
		self.assertTrue(ret,msg=result)


	def test_threshold_update_wrong_version(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
                uidlist = [random.randint(100,200) for x in range(10)]
		data = get_threshold_data(Constants.VERSION + 1, Constants.LEVEL, uidlist)
                ret, result = self.check_fail(zauth, data, 3)
                self.assertTrue(ret,msg=result)

	def test_threshold_update_empty_level(self):
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID )
		level = " "
		uidlist = [random.randint(100,200) for x in range(10)]
		data = get_threshold_data(Constants.VERSION, level, uidlist)
		ret, result = self.check_fail(zauth, data, 403)
		self.assertTrue(ret,msg="Refer Jira defect SEG-9263")

	def test_threshold_update_incorrect_input(self):              # Empty level should not give error 0
		zauth = AuthSystem.getTrustedAuthToken(Constants.ZID ) # Refer jira BUG SEG-9263
		uidlist = []
		data = get_threshold_data(Constants.VERSION, Constants.LEVEL, uidlist)
		ret, result = self.check_fail(zauth, data, 403)
		self.assertTrue(ret,msg="Refer Jira defect SEG-9277")

	


if __name__ == '__main__':
	suite0 = unittest.TestLoader().loadTestsFromTestCase(thresholds_update)
        unittest.TextTestRunner(verbosity=99).run(suite0)
