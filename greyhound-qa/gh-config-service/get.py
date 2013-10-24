#!/usr/bin/python26
import os,sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import unittest
from curl_util import *
from checkFiles import *
from constants import * 
import pdb

class configGet(unittest.TestCase):

        def setUp(self):
                self.url = constants.URL + '/srv/get/'
        def tearDown(self):
                pass

        def test_getStorageYaml(self):
                data = constants.POSTDATA_GET
                ob = self._processTest(data)
                status, ret = ob.checkStorageYaml()
                self.assertTrue(status, msg=ret)

        def test_getAclFiles(self):
                data = constants.POSTDATA_GET
                ob = self._processTest(data)
                status, ret = ob.checkAclFile()
                self.assertTrue(status, msg=ret)

        def test_getGreyhoundIni(self):
                data = constants.POSTDATA_GET
                ob = self._processTest(data)
                status, ret = ob.checkGreyhoundIni()
                self.assertTrue(status, msg=ret)

	def test_getDeltas(self):
		data = constants.POSTDATA_GET
		ob = self._processTest(data)
		status, ret = ob.checkDeltas()
		self.assertTrue(status, msg=ret)
	
	def test_getScoreboard(self):
		data = constants.POSTDATA_GET
		ob = self._processTest(data)
		status, ret = ob.checkScoreboard()
		self.assertTrue(status, msg=ret)
	
        def test_graphTypes(self):
                data = constants.POSTDATA_GET
                ob = self._processTest(data)
                status, ret = ob.checkGraphTypes()
                self.assertTrue(status, msg=ret)

	def test_metaschema(self):
		data = constants.POSTDATA_GET
		ob = self._processTest(data)
		status, ret = ob.checkMetaSchema()
		self.assertTrue(status, msg=ret)

        def _processTest(self, data ):
                status, ret = sendRequest(self.url, data)
                self.assertTrue(status, msg=ret)
                obj = compareFiles(ret)
                return obj




if __name__ == '__main__':
        #suite0 = unittest.TestLoader().loadTestsFromTestCase(configGet)
        #unittest.TextTestRunner(verbosity=99).run(suite0)
        import testoob
        from testoob.reporting import HTMLReporter
        testoob.main(html='ConfigGet.html')
