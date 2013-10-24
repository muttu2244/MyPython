#!/usr/bin/python26
import re
import subprocess
import pdb
import sys
import os
#sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import urllib
import urllib2
from api_constants import Constants
import random
import time
from multiprocessing import Pool
import StringIO
import pycurl
import traceback
import select
import unittest
import simplejson as json
from  gh_api import *
from auth import *
from internal_api import *


class gh_unit(unittest.TestCase):
        """ TODO : 
                * setUp() - will set test env
                * tearDown() - will clean up test env
        """
        def setUp(self):
                return

	#def cleanup(self):
#		MB_DELTAS_MASTER='10.32.142.100'
#		echo "flush_all" | nc MB_DELTAS_MASTER 11211

	#	echo "flush_all" | nc MB_OBJECTS_MASTER 11211


	#class scoreboard_TC(gh_unit):

        def check_pass(self , fun, args, expected_err_code):
                ret=fun(*args)
		
		try:
			#if "'error': %s" %expected_err_code[0] in str(ret) or "'error': %s" %expected_err_code[1] in str(ret):
				#return [ True, ret ]
			for er in expected_err_code:
				if "'error': %s"%er in str(ret):
					return [ True, ret]
			return [ False, ret]

		except:
                        return  [ False, ret ]

			


        def check_fail(self, fun, args, expected_err_code):
                ret=fun(*args)

		try:
		
			if Constants.DELTA_STATUS in str(ret):
				if "%s" %expected_err_code[0] in str(ret):
					return [ True, ret]
			if "'error': %s" %expected_err_code[0] in str(ret) or "'error': %s" %expected_err_code[1] in str(ret):
                        	return [ True, ret ]
			if "'blobs': %s" %expected_err_code[0] in str(ret):
				return [ True, ret ]
			return [False, ret]	
	
		except:
			return  [ False, ret ]
