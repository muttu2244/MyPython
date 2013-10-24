#!/usr/bin/python26

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
import urllib
import urllib2
from api_constants import Constants
from multiprocessing import Pool
import StringIO
import traceback
import select

class mqs_check(object):
	
	@staticmethod
	def check_pass(fun, args, validation_fn_list=None):
		ret = fun(*args) 
		if ret == None:
			return [False, 'Failed to get data from server']
		
		if not type(ret) is dict:
			return [False, "Type recieved is not a json. Result = %s" % ret]

		try:
			if ret[ Constants.STATUS][Constants.ERROR] == 0:
				if ret[ Constants.RESULT][Constants.PARTIAL]:
					return [False, 'Partial "True", expected "False"\n'+str(ret)]
				else:
					return [True, ret]
			else:
				return [False, ret]
		except NameError:
			return [False, ret]
	@staticmethod
	def check_fail(fun,args):
		ret = fun(*args)
		if ret == None:
			return [False, 'Failed to get data from server']

		if not type(ret) is dict:
			return [False, ret]

		try:
			if ret[Constants.STATUS][Constants.ERROR] != 0:
				return [True, ret]
			else:
				return [False, ret]

		except NameError:
			return [False, ret]


	
			
