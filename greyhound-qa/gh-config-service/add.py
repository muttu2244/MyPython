#!/usr/bin/python26
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
from curl_util import *
from checkFiles import *
import pdb, time
from utils import *
#URL = "http://ghqacluster-staging-web-2.zc1.zynga.com/"
class configAdd(unittest.TestCase):

        def setUp(self):
                time.sleep(1)
                self.url = constants.URL + '/srv/get/'
                data = constants.POSTDATA_GET
                self.input = self._getDataFromServer(data)
                self.url = constants.URL + '/srv/add/'
                time.sleep(1)

        def tearDown(self):
                self.input = {}

	def test_changeSecret(self):
		secret = gen_secret()
		self.input[constants.ACSKEY_SECRET] = secret
		ob = self._processTest(self.input)
		runJobAndWait()
		status, ret = ob.checkGreyhoundIni()
		self.assertTrue(status, msg=ret)

	def test_changeAppName(self):
		appname = "2244"+gen_secret()
		self.input[constants.ACSKEY_NAMESPACE] = appname
		ob = self._processTest(self.input)
		runJobAndWait()
		status, ret = ob.checkGreyhoundIni()
		self.assertTrue(status, msg=ret)

        def test_addNormalInputForStorage(self):
                ttl = int(self.input[constants.ACSKEY_DELTAS][0]['ttl'])
		print "Original ttl of ",self.input[constants.ACSKEY_DELTAS][0]['type']," = ",ttl
                if ttl > 100:
                        ttl = 10
                else:
                        ttl = ttl + 10
                self.input[constants.ACSKEY_DELTAS][0]['ttl'] = str(ttl)
                ob = self._processTest(self.input)
                runJobAndWait()
                status, ret = ob.checkDeltas()
                self.assertTrue(status, msg=ret)
	
	def test_addNewBlobType(self):
		found = False
		for item in self.input[constants.ACSKEY_BLOBS]:
			if item['type'] == "new-world":
				found = True
				self.input[constants.ACSKEY_BLOBS].remove(item)
				break
		if not found:
			print "No new blob type"
			self.input[constants.ACSKEY_BLOBS].append({"type": "new-world", "pool": "MB_OBJECTS_MASTER_2244"})
		ob = self._processTest(self.input)
		runJobAndWait()
		status, ret = ob.checkStorageYaml()
		self.assertTrue(status, msg=ret)

	def test_addNewDelta(self):
		found = False
		for item in self.input[constants.ACSKEY_DELTAS]:
			if item['type'] == 'new-delta':
				found = True
				self.input[constants.ACSKEY_DELTAS].remove(item)
				break
		if not found:
			self.input[constants.ACSKEY_DELTAS].append({"type": "new-delta"})
		ob = self._processTest(self.input)
		runJobAndWait()
		status, ret = ob.checkDeltas()
		self.assertTrue(status, msg=ret)
			
	def test_addScoreboard(self):
		found = False
		for item in self.input[constants.ACSKEY_SCOREBOARD]:
			if item['type'] == 'new-scoreboard':
				found = True
				self.input['scoreboard'].remove(item)
				break
		if not found:
			self.input[constants.ACSKEY_SCOREBOARD].append({"type": "new-scoreboard"})
		ob = self._processTest(self.input)
		runJobAndWait()
		status, ret = ob.checkScoreboard()
		self.assertTrue(status, msg=ret)
				
			
	"""def test_addGoldenBlobType(self):
		found = False
		for item in self.input[constants.ACSKEY_GOLDEN]:
			if item['type'] == 'new-world':
				found = True
				self.input['golden'].remove(item)
				break
		if not found:
			self.input[constants.ACSKEY_GOLDEN].append({"type": "new-world"})
		ob = self._processTest(self.input)
		runJobAndWait()
		status, ret = ob.checkStorageYaml()
		self.assertTrue(status, msg=ret)"""


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
	#suite0 = unittest.TestLoader().loadTestsFromTestCase(configAdd)
        #unittest.TextTestRunner(verbosity=99).run(suite0)
	import testoob
        from testoob.reporting import HTMLReporter
        testoob.main(html='ConfigAdd.html')
