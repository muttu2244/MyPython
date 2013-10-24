#!/usr/bin/python26
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
from curl_util import *
from checkFiles import *
import pdb, time
from constants import constants

#URL = "http://ghqacluster-staging-web-2.zc1.zynga.com/"
class configSet(unittest.TestCase):

        def setUp(self):
		time.sleep(1)
                self.url = constants.URL + '/srv/get/'
		data = constants.POSTDATA_GET
		self.input = self._getDataFromServer(data)
		self.url = constants.URL + '/srv/add/'
		time.sleep(1)

        def tearDown(self):
		self.input = {}

	def test_addNormalInputForStorage(self):
		ttl = int(self.input[constants.ACSKEY_DELTAS][0]['ttl'])
		if ttl > 100:
			ttl = 10
		else:
			ttl = ttl + 10
		self.input[constants.ACSKEY_DELTAS][0]['ttl'] = str(ttl)
		ob = self._processTest(self.input)
		runJobAndWait()
		status, ret = ob.checkDeltas()
		self.assertTrue(status, msg=ret)

	#
	#Tests for missing required attributes in input
	#
	def addItem(self, key, data):

		if key in [constants.ACSKEY_BLOBS, constants.ACSKEY_DELTAS, constants.ACSKEY_SCOREBOARD]:
			type = "type"
		elif key == constants.ACSKEY_ACL:
			type = "blob" 
		elif key == constants.ACSKEY_SCHEMA:
			type = "name"

		found = False
		for item in self.input[key]:
			if item[type] == data[type]:
				found = True
				self.input[key].remove(item)
				break
		if not found:
			self.input[key].append(data)

	

	def test_addKeyTypeInBlob(self):
		data = {'type': 'new-world', 'maxsize': '2k'}
		self.addItem(constants.ACSKEY_BLOBS, data)
		ob = self._processTest(self.input)
		runJobAndWait()
		status, ret = ob.checkStorageYaml()
		self.assertTrue(status, msg=ret)


	def test_addWithTypeInDeltas(self):
		data = {'maxsize': '4k', 'ttl': '7', 'type': 'new-delta'}
		self.addItem(constants.ACSKEY_DELTAS, data)
		ob = self._processTest(self.input)
		runJobAndWait()
		status, ret = ob.checkDeltas()
		self.assertTrue(status, msg=ret)

	def test_addWithTypeInScoreboard(self):
		data = {"max": "10", "min": "0", "maxcount": "10", "ttl": "7", "type": "new-scoreboard"}
		self.addItem(constants.ACSKEY_SCOREBOARD, data)
		ob = self._processTest(self.input)
		runJobAndWait()
		status, ret = ob.checkScoreboard()
		self.assertTrue(status, msg=ret)



	def test_addNewApiInACL(self):
		data = {"blob": "newWorld", "api_list": [ {"roles": ["trusted","any"]}, {"api": "user.blob.get"}]}
		self.addItem(constants.ACSKEY_ACL, data)
		ob = self._processTest(self.input)
		runJobAndWait()
		status, ret = ob.checkAclFile()
		self.assertTrue(status, msg=ret)		

	def test_addWithDefaultValueInSchema(self):
		data = {"scope": "self", "type": "integer", "name": "newkey", "default_value": "0" }
		self.addItem(constants.ACSKEY_SCHEMA, data)
		ob = self._processTest(self.input)
		runJobAndWait()
		status, ret = ob.checkMetaSchema()
		self.assertTrue(status, msg=ret)

        def _processTest(self, data ):
                status, ret = sendRequest(self.url, data)
                self.assertTrue(status, msg=ret)
                obj = compareFiles(self.input)
                return obj

	def _getDataFromServer(self, data):
		status, ret = sendRequest(self.url, data)
		self.assertTrue(status, msg=ret)
		return ret



if __name__ == '__main__':
        #suite0 = unittest.TestLoader().loadTestsFromTestCase(configSet)
        #unittest.TextTestRunner(verbosity=99).run(suite0)
        import testoob
        from testoob.reporting import HTMLReporter
        testoob.main(html='ConfigAdd2.html')
