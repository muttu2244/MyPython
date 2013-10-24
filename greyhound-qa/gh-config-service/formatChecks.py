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

	def test_addWithoutKeyTypeInBlob(self):
		self.input[constants.ACSKEY_BLOBS].append({'maxsize': '2k'})
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_addWithoutSecret(self):
		self.input.pop(constants.ACSKEY_SECRET)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_addWithoutGameid(self):
		self.input.pop(constants.ACSKEY_GAMEID)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_addWithoutNamespace(self):
		#self.input.pop(constants.ACSKEY_NAMESPACE)
		#status, ret = sendRequest(self.url, self.input)
		#self.assertFalse(status, msg=ret)
		#self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)
		self.assertTrue(False, msg = "Namespace has been made optional for backward compatibilty")

	def test_addWithoutKeyTypeInGolden(self):
		self.input[constants.ACSKEY_GOLDEN].append({'pool': 'MB_GOLDEN_MASTER'})
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_addWithoutKeyTypeInDeltas(self):
		self.input[constants.ACSKEY_DELTAS].append({'maxsize': '4k', 'ttl': '7'})
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_addWithoutTypeInScoreboard(self):
		self.input[constants.ACSKEY_SCOREBOARD].append({'max': '16'})
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)
		self.input[constants.ACSKEY_SCOREBOARD].append({'pool': 'MB_SECRET_MASTER', 'min': '5'})
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_addWithoutBlobInAcl(self):
		newAcl = self.input[constants.ACSKEY_ACL][0].pop('blob')
		self.input[constants.ACSKEY_ACL].append(newAcl)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_addWithoutApilistInAcl(self):
		self.input[constants.ACSKEY_ACL].append({"blob": "newBlob"})
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_addWithoutApiInApilist(self):
		newAcl = {"blob": "newWorld", "api_list": [ {"roles": ["trusted","any"]}]}
		self.input[constants.ACSKEY_ACL].append(newAcl)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)
		
		
	def test_addWithoutRolesInApilist(self):
		newAcl = {"blob": "newWorld", "api_list": [ {"api": "user.blob.get"}]}
		self.input[constants.ACSKEY_ACL].append(newAcl)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_addWithoutDefaultValueInSchema(self):
		newSchema = {"scope": "self", "type": "integer", "name": "newkey"}
		self.input[constants.ACSKEY_SCHEMA].append(newSchema)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_addWithoutScopeInSchema(self):
		newSchema = {"default_value": "0", "type": "integer", "name": "newkey"}
		self.input[constants.ACSKEY_SCHEMA].append(newSchema)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_addWithoutTypeInSchema(self):
		newSchema = {"default_value": "0", "scope": "self", "name": "newkey"}
		self.input[constants.ACSKEY_SCHEMA].append(newSchema)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_addWithoutNameInSchema(self):
		newSchema = {"default_value": "0", "scope": "self", "type": "integer"}
		self.input[constants.ACSKEY_SCHEMA].append(newSchema)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)


	#
	# Tests for Invalid Pool types ( which are not defined in the zrt )
	#

	def test_invalidPoolForBlob(self):
		#invalidPool = {"type": "newWorld", "pool": "MB_DELTAS_MASTER"}
		#self.input[constants.ACSKEY_BLOBS].append(invalidPool)
		#status, ret = sendRequest(self.url, self.input)
		#self.assertFalse(status, msg=ret)
		#self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)
		self.assertTrue(False, msg = "GH config service accepts any pool name")

	def test_invalidPoolForGolden(self):
		#invalidPool = {"type": "newWorld", "pool": "MB_OBJECTS_MASTER"}
		#self.input['golden'].append(invalidPool)
		#status, ret = sendRequest(self.url, self.input)
		#self.assertFalse(status, msg=ret)
		#self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)
		self.assertTrue(False, msg = "GH config service accepts any pool name")

	def test_invalidPoolForDeltas(self):
		#invalidPool = {"type": "newDelta", "pool": "DELTAS_MASTER"}
		#self.input[constants.ACSKEY_DELTAS].append(invalidPool)
		#status, ret = sendRequest(self.url, self.input)
		#self.assertFalse(status, msg=ret)
		#self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)
		self.assertTrue(False, msg = "GH config service accepts any pool name")

	def test_invalidPoolForScoreboard(self):
		#invalidPool = {"type": "newViral", "pool": "DELTAS_MASTER"}
		#self.input[constants.ACSKEY_SCOREBOARD].append(invalidPool)
		#status, ret = sendRequest(self.url, self.input)
		#self.assertFalse(status, msg=ret)
		#self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)
		self.assertTrue(False, msg = "GH config service accepts any pool name")
	#
	# Tests for invalid maxsize in Blobs
	#

	def test_invalidMaxSizeForBlob(self):
		# Test 1
		invalidMax = {'maxsize': 'tenk', 'type': "newWorld"}
		self.input[constants.ACSKEY_BLOBS].append(invalidMax)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)
		
		# Test 2
		invalidMax = {'maxsize': '10G', 'type': "newWorld"}
		self.input[constants.ACSKEY_BLOBS].append(invalidMax)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

		# Test 3
		invalidMax = {'maxsize': '10kk', 'type': "newWorld"}
		self.input[constants.ACSKEY_BLOBS].append(invalidMax)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	#
	# Tests for ACL Formats checks.
	# Invalid API or action in ACL
	#

	def test_invalidAclAction(self):
		invalidAction = {'api_list': [{'api': 'user.blobs.get', 'roles': ['trusted', 'impersonated']}], "blob": "adminLog"}
		self.input[constants.ACSKEY_ACL].append(invalidAction)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)
		
	#
	# Tests for invalid subject in ACL (that are not in Storage.yaml)
	#

	def test_invalidBlobName(self):
		#invalidBlob = {'api_list': [{'api': 'user.blob.get', 'roles': ['any']}], "blob": "anotherWorld"}
		#self.input[constants.ACSKEY_ACL].append(invalidBlob)
		#status, ret = sendRequest(self.url, self.input)
		#self.assertFalse(status, msg=ret)
		#self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)
		self.assertTrue(False, msg = "Checks on blob type has been removed")

	#
	# Tests for inavlid role in ACL
	#

	def test_invalidRole(self):
		invalidRole = {'api_list': [{'api': 'user.blob.get', 'roles': ['anyone']}], "blob": "game-world"}
		self.input[constants.ACSKEY_ACL].append(invalidRole)
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_invalidTTL(self):
		self.input[constants.ACSKEY_DELTAS][0]['ttl'] = '7s'
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_invalidMin(self):
		self.input[constants.ACSKEY_SCOREBOARD][0]['min'] = '12k'
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)

	def test_invalidMax(self):
		self.input[constants.ACSKEY_SCOREBOARD][0]['max'] = '12k'
		status, ret = sendRequest(self.url, self.input)
		self.assertFalse(status, msg=ret)
		self.assertTrue(ret == constants.ERROR_INTERNAL, msg=ret)
	

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
        testoob.main(html='FormatChecks.html')
