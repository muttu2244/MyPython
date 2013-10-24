#!/usr/bin/python26

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/lib")
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
from mqs_api import *

# vim: ai ts=4 sts=4 et sw=4 ft=python

class mqs_unit(unittest.TestCase):  
        """ TODO : 
     	        * setUp() - will set test env
	        * tearDown() - will clean up test env
        """
	def setUp(self):
                return
		
        def validate_in_list(self, list_path, val, data):
	        tmp = data
	        for l in list_path:
		        tmp = tmp[l]
	        if val in tmp:
		        return True
		val = 1
		self.assertEqual(val, 2,msg='val is not in list')
	        return False

        def validate_not_in_list(self, list_path, val, data):
	        tmp = data
	        for l in list_path:
		        tmp = tmp[l]
	        if val not in tmp:
		        return True
		val = 1
		self.assertEqual(val, 2, msg='val is in list')
	        return False

        def validate_obj_val(self, list_path, val, data):
	        tmp = data
	        for l in list_path:
		        tmp = tmp[l]
	        if val == tmp:
		        return True

	        print "Value ", tmp, " is not same as expected value ", val, " in obj path ", list_path, " in data ", data
	        return False

        def run_validation_fn(self, validation_fn_list, data):
	        for fn in validation_fn_list:
		        if len(fn) == 1:
			        ret = fn[0](ret)
		        elif len(fn) == 2:
			        ret = fn[0](fn[1], data)
		        elif len(fn) == 3:
			        ret = fn[0](fn[1], fn[2], data)
		        elif len(fn) == 4:
			        ret = fn[0](fn[1], fn[2], fn[3], data)
		        else:
			        raise Exception("No validator defined")
		        if not ret:
			        return ret
	        return True

        def check_pass(self, fun, args, validation_fn_list = None):
	        ret = fun(*args)
	        if not ret:
		        self.assertIsNone(ret, msg= ret[ Constants.RESULT ])
            		return [ False, ret ]

	        if ret[ Constants.STATUS ][ Constants.ERROR ] == 0:
		        if ret[ Constants.RESULT ][ Constants.PARTIAL ]:
				self.assertFalse(ret, msg = ret[ Constants.RESULT ])
			        return [ False, ret ]

		        if validation_fn_list and not self.run_validation_fn(validation_fn_list, ret):
			        self.assertTrue(ret, msg = ret[ Constants.RESULT ])

		        self.assertTrue(ret, msg= ret[ Constants.RESULT ])
		        return [ True, ret ]
	        else:
			self.assertTrue(ret, msg= ret[ Constants.RESULT ])
		        return [ False, ret ]

        def check_fail(self, fun, args):
	        ret = fun(*args)
	        if not ret:
		        self.assertIsNone(ret, msg= ret[ Constants.RESULT ])
	   	        return [ False, ret ]

	        if ret[ Constants.STATUS ][ Constants.ERROR ] != 0:
			self.assertTrue(ret, msg= ret[ Constants.RESULT ])
		        return [ True, ret ]
	        else:
			self.assertFalse(ret, msg= ret[ Constants.RESULT ])
		        return [ False, ret ]

        def check_partial_fail(self, fun, args):
	        ret = fun(*args)
	        if not ret:
		        self.assertIsNone(ret, msg= ret[ Constants.RESULT ])

	        if ret[ Constants.STATUS ][ Constants.ERROR ] == 0:
		        if ret[ Constants.RESULT ][ Constants.PARTIAL ]:
		       		self.assertTrue(ret, msg= ret[ Constants.RESULT ])
 
			self.assertTrue(ret, msg= ret[ Constants.RESULT ])
	        else:
		        self.assertTrue(ret, msg= ret[ Constants.RESULT ])

        def test_meta(self):
	        meta_user_delete(1)
	        ret, result = self.check_pass(meta_user_get, [ '1' ])
	        if not ret:
		        return
	        cas = result[ Constants.RESULT ][ Constants.META_FIELD_CAS ]
	        data = result[ Constants.RESULT ][ Constants.DATA ]
    	        i = 0
	        while ret and i < 5:
		        data[ 'xp' ] += 1
	 	        ret, result = self.check_pass(meta_user_update, [ 1, data, cas ])
	   	        cas = result[ Constants.RESULT ][ Constants.META_FIELD_CAS ]
		        ret, result = self.check_pass(meta_user_get, [ '1' ])
		        n_cas = result[ Constants.RESULT ][ Constants.META_FIELD_CAS ]
		        if cas != n_cas:
			        raise Exception("Cas error")
		        i = i + 1

	        meta_user_delete(1)
	        ret, result = self.check_pass(meta_user_get, [ 1 ])
	        cas = result[ Constants.RESULT ][ Constants.META_FIELD_CAS ]
	        data = result[ Constants.RESULT ][ Constants.DATA ]
	        data[ 'xp' ] += 1
	        ret, result = self.check_pass(meta_user_update, [ 1, data, cas ])
	        ret, result = self.check_fail(meta_user_update, [ 1, data, cas ])

	def test_meta_cred(self):
        	self.check_partial_fail(meta_user_credibility_get, [ [ '3000', '3001', 3002, 3003, 3004, 4, 5, 6] ])
		self.check_pass(meta_user_credibility_get, [ [ '3000', '3001', 3002, 3003, 3004] ])
        	self.check_pass(meta_user_credibility_upgrade, [ [ '3000', '3001', 3003 ] ])
        	self.check_partial_fail(meta_user_credibility_upgrade, [ [ '30000', '30010', 30030 ] ])
       	 	self.check_pass(meta_user_credibility_upgrade, [ [ '3001', '3003', 3005 ] ])
        	self.check_partial_fail(meta_user_credibility_get, [ [ '3000', '3001', 3002, 3003, 3004, 4, 5, 6] ])
        	self.check_pass(meta_user_credibility_downgrade, [ [ '3007', '3009' ] ])
        	self.check_partial_fail(meta_user_credibility_downgrade, [ [ '3007', '3009', '48333292' ] ])

	def test_meta2(self):
	        meta_user_delete(1)
        	ret, result = self.check_pass(meta_user_get, [ '1' ])
        	if not ret:
                	return
        	cas = result[ Constants.RESULT ][ Constants.META_FIELD_CAS ]
        	data = result[ Constants.RESULT ][ Constants.DATA ]

        	data[ 'xp' ] += 1
        	ret, result = self.check_pass(meta_user_update, [ 1, data, cas ])
        	cas = result[ Constants.RESULT ][ Constants.META_FIELD_CAS ]

        	ret, result = self.check_pass(meta_user_get, [ '1' ])
        	n_cas = result[ Constants.RESULT ][ Constants.META_FIELD_CAS ]
        	if cas != n_cas:
                	raise Exception("Cas error")

	def test_meta_cred2(self):
        	self.check_partial_fail(meta_user_credibility_get, [ [ '3000', '3001', 3002, 3003, 3004, 4, 5, 6], True ])

	def test_meta_cred3(self):
        	self.check_pass(meta_user_credibility_get, [ [ '3100' ], True ])
        	self.check_pass(meta_user_credibility_downgrade, [ [ '3100' ], True ])
        	self.check_pass(meta_user_credibility_get, [ [ '3100' ], True ])
        	self.check_pass(meta_user_credibility_downgrade, [ [ '3100' ], True ])
       	 	self.check_pass(meta_user_credibility_get, [ [ '3100' ], True ])
        	self.check_pass(meta_user_credibility_downgrade, [ [ '3100' ], True ])
        	self.check_pass(meta_user_credibility_get, [ [ '3100' ], True ])
        	self.check_pass(meta_user_credibility_downgrade, [ [ '3100' ], True ])
        	self.check_pass(meta_user_credibility_get, [ [ '3100' ], True ])
        	self.check_pass(meta_user_credibility_downgrade, [ [ '3100' ], True ])
        	self.check_pass(meta_user_credibility_get, [ [ '3100' ], True ])

	def test_meta_cred4(self):
        	self.check_pass(meta_user_credibility_get, [ [ '3000', '3001', 3002, 3003, 3004 ] ])
       	 	self.check_pass(meta_user_credibility_set, [ { '3000': '0', '3001': '1', '3002': 2, '3003': 3, '3004': 0 } ])
        	self.check_pass(meta_user_credibility_get, [ [ '3000', '3001', 3002, 3003, 3004 ] ])
        	self.check_pass(meta_user_credibility_set, [ { '3000': 0, '3001': 0, '3002': '0', '3003': "0", '3004': 0 } ])
        	self.check_pass(meta_user_credibility_get, [ [ '3000', '3001', 3002, 3003, 3004 ] ])
        	self.check_partial_fail(meta_user_credibility_set, [ { '3000': 0, '3001': 1, '3002': 2, '3003': 3, '3004': 4 } ])
       	 	self.check_pass(meta_user_credibility_get, [ [ '3000', '3001', 3002, 3003, 3004 ] ])

	def test_meta_trio(self):
        	self.check_pass(meta_user_trio_get, [ [ '1001' ]] )
        	self.check_pass(meta_user_trio_get, [ [ '1003' ]] )
       	 	self.check_pass(meta_user_trio_get, [ [ 1003, 100, 1  ]] )
        	self.check_pass(meta_user_trio_get, [ [ 1, 2, 3  ]] )

	def test_meta_bulk_update(self):
        	self.check_partial_fail(meta_user_bulk_update, [ "golden", { 1005: { 'xp': 100, 'level':200 }, 1007: { 'xp':200, 'level':200 } } ])
        	self.check_fail(meta_user_bulk_update, [ "junk", { 1005: { 'xp': 111, 'level':222, 'cas':'0113b22e-cc34-11e0-bc68-000c299e9f38' }, 1007: { 'xp':200, 'level':200 } }])
        	self.check_fail(meta_user_bulk_update, [ "previous", { 1005: { 'xp': 111, 'level':222, 'cas':'0113b22e-cc34-11e0-bc68-000c299e9f38' }, 1007: { 'xp':200, 'level':200 } }])
        	self.check_partial_fail(meta_user_bulk_update, [ "golden", { 1005: { 'xp': 111, 'level':222, 'cas':'0113b22e-cc34-11e0-bc68-000c299e9f38' }, 1007: { 'xp':200, 'level':200 } }])
        	meta_user_delete(1)
       	 	ret, data = self.check_pass(meta_user_trio_get, [ [1] ])
        	if ret:
                	xp = data['result']['data'][str(1)][Constants.META_TYPE_GOLDEN]['xp']
                	cas = data['result']['data'][str(1)][Constants.META_TYPE_GOLDEN]['cas']
                	end = xp + 10
                	while xp < end:
                        	ret, data = self.check_pass(meta_user_bulk_update, [ "golden", { 1 : { 'xp': xp+1, 'cas': cas } } ])
                        	cas = data['result']['data'][str(1)]['cas']
                        	ret, data = self.check_pass(meta_user_trio_get, [ [1] ])
                        	xp = xp + 1

        	meta_user_delete(2)
        	ret, data = self.check_pass(meta_user_trio_get, [ [2] ])
        	if ret:
                	xp = data['result']['data'][str(2)][Constants.META_TYPE_CURRENT]['xp']
                	cas = data['result']['data'][str(2)][Constants.META_TYPE_CURRENT]['cas']
                	end = xp + 10
                	while xp < end:
                        	ret, data = self.check_pass(meta_user_bulk_update, [ "current", { 2: { 'xp': xp+1, 'cas': cas } } ])
                        	cas = data['result']['data'][str(2)]['cas']
                        	ret, data = self.check_pass(meta_user_trio_get, [ [2] ])
                        	xp = xp + 1

        	meta_user_delete(3)
       	 	ret, data = self.check_pass(meta_user_trio_get, [ [3] ])
        	if ret:
                	xp = data['result']['data'][str(3)][Constants.META_TYPE_CURRENT]['xp']
               	 	cas = data['result']['data'][str(3)][Constants.META_TYPE_CURRENT]['cas']
                	ret, data = self.check_pass(meta_user_bulk_update, [ "current", { 3: { 'xp': xp+1, 'cas': cas } } ])
                	#ret, data = self.check_partial_fail(meta_user_bulk_update, [ "current", { 3: { 'xp': xp+1, 'cas': cas } } ])

	def test_query(self):
        	self.check_pass(query_user_graph, [ 1001, "app-friend",  "select level,xp,zid order by level desc"])
      	 	self.check_pass(query_user_graph, [ 1002, "app-friend",  "select level,xp,zid order by level desc"])
        	self.check_pass(query_user_graph, [ 1003, "app-friend",  "select level,xp,zid order by level desc"])
        	self.check_pass(query_user_graph, [ 1004, "app-friend",  "select level,xp,zid order by level desc"])
        	self.check_pass(query_user_graph, [ 1005, "app-friend",  "select level,xp,zid order by level desc"])
        	self.check_pass(query_user_graph, [ 1006, "app-friend",  "select level,xp,zid order by level desc"])
        	self.check_pass(query_user_graph, [ 1007, "app-friend",  "select level,xp,zid order by level desc"])
        	self.check_pass(query_user_graph, [ 1008, "app-friend",  "select level,xp,zid order by level desc"])
        	self.check_pass(query_user_graph, [ 1009, "app-friend",  "select level,xp,zid order by level desc"])
        	self.check_pass(query_user_graph, [ 1010, "app-friend",  "select level,xp,zid order by level desc"])
        	self.check_pass(query_user_graph, [ 1011, "app-friend",  "select level,xp,zid order by level desc"])
        	self.check_pass(query_user_graph, [ 1012, "app-friend",  "select level,xp,zid order by level desc"])
        	self.check_pass(query_user_graph, [ 1013, "app-friend",  "select level,xp,zid order by level desc"])
       	 	self.check_pass(query_user_graph, [ 9999999, "app-friend", "select level,xp,zid"])
        	self.check_fail(query_user_graph, [ 1001, "junk-graph", "select level,xp,zid"])
        	self.check_fail(query_user_graph, [ 9999999, "junk-graph", "select level,xp,zid"])
        	self.check_fail(query_user_graph, [ 1002, "app-friend", "select NEW_FIELD,level,xp,zid"])
        	self.check_fail(query_user_graph, [ 1001, "app-friend", "select level,xp,zid from app-friend"])
        	self.check_fail(query_user_graph, [ 1001, "app-friend", "select level,xp,zid where i = 22 or j = 21 "])
        	self.check_fail(query_user_graph, [ 1001, "app-friend", "update meta set level=10,xp=20 where zid = 21 "])


	def test_graph(self):
        	self.check_pass(graph_user_get, [ 3000, [ 'app-friend'] ])
       		self.check_pass(graph_user_getwaitlist, [ 3000, [ 'app-friend'] ])
        	self.check_pass(graph_user_getconfirmlist, [ 3000, [ 'app-friend'] ])
        	self.check_pass(graph_user_getgraphlist, [ 3000, [ 1, 2, 3, 4, 5, 6 ]])
       	 	self.check_pass(graph_user_checkmembership, [ 3000, [ 'app-friend', 'test' ], [ 3001, 3002, 3003, 3004, 3006, 3007 ]])
        	self.check_pass(graph_user_checkmembership, [ 3000, [ 'fight-list', 'crew-members', 'test' ], [ 3001, 3002, 3003, 3004, 3006, 3007 ]])

	def test_graph2(self):
        	self.check_fail(graph_user_get, [ 3000, [ 'app-friend-junk'] ])
        	self.check_fail(graph_user_getwaitlist, [ 3000, [ 'app-friend-junk'] ])
        	self.check_fail(graph_user_getconfirmlist, [ 3000, [ 'app-friend-junk'] ])
        	self.check_fail(graph_user_checkmembership, [ 3000, [ 'app-friend-junk' ], [ 3001, 3002, 3003, 3004, 3006, 3007 ]])
        	self.check_fail(graph_user_add, [ 3000, 'app-friend-junk', [ 3001 ] ])
        	self.check_fail(graph_user_remove, [ 3000, 'app-friend-junk', [ 3001 ]])
       		self.check_fail(graph_user_getmembers, [ 3000, [ 'app-friend', 'app-friend-junk'] ])

	def test_graph_add(self):
       		graph_user_remove(3000, 'app-friend', [ 3001 ])
		graph_user_remove(3001, 'app-friend', [ 3000 ])
        	self.check_pass(graph_user_add, [ 3000, 'app-friend', [ 3001 ]])
        	self.check_pass(graph_user_get, [ 3000, [ 'app-friend' ] ], [ [ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ], 3001 ] ] )
        	self.check_pass(graph_user_getwaitlist, [ 3000, [ 'app-friend' ] ], [ [ self.validate_in_list, [ 'result', 'data', 'app-friend' ], 3001 ] ]  )
        	self.check_pass(graph_user_getconfirmlist, [ 3000, [ 'app-friend' ] ], [ [ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ], 3001 ]] )
      		self.check_pass(graph_user_get, [ 3001, [ 'app-friend' ] ], [ [ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
        	self.check_pass(graph_user_getwaitlist, [ 3001, [ 'app-friend' ] ], [ [ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ 3001, [ 'app-friend' ]], [ [ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ] ] )
       		self.check_pass(graph_user_add, [ 3001, 'app-friend', [ 3000 ]])
        	self.check_pass(graph_user_get, [ 3000, [ 'app-friend' ] ], [[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )
        	self.check_pass(graph_user_getwaitlist, [ 3000, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ 3000, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )
        	self.check_pass(graph_user_get, [ 3001, [ 'app-friend' ] ], [[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
        	self.check_pass(graph_user_getwaitlist, [ 3001, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ 3001, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )

	def test_graph_add2(self):
        	id1 = 3000
        	id2 = 3001
        	self.check_pass(graph_user_add, [ id1, 'app-friend', [ id2 ]])

        	self.check_pass(graph_user_get, [ id1, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , id2 ]] )
        	self.check_pass(graph_user_getwaitlist, [ id1, [ 'app-friend' ] ], [[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , id2 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ id1, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , id2 ]] )
        	self.check_pass(graph_user_get, [ id2, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , id1 ]] )
        	self.check_pass(graph_user_getwaitlist, [ id2, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , id1 ]] )
       		self.check_pass(graph_user_getconfirmlist, [ id2, [ 'app-friend' ] ], [[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , id1 ]] )

        	self.check_pass(graph_user_add, [ id2, 'app-friend', [ id1 ]])

        	self.check_pass(graph_user_get, [ id1, [ 'app-friend' ] ], [[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , id2 ]] )
       		self.check_pass(graph_user_getwaitlist, [ id1, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , id2 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ id1, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , id2 ]] )
       		self.check_pass(graph_user_get, [ id2, [ 'app-friend' ] ], [[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , id1 ]] )
        	self.check_pass(graph_user_getwaitlist, [ id2, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , id1 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ id2, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , id1 ]] )


	def test_graph_add3(self):
        	friends = [ 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010 ]
        	graph_user_remove(3000, 'app-friend', friends)
        	for f in friends:
                	self.check_pass(graph_user_get, [ f, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
                	self.check_pass(graph_user_getwaitlist, [ f, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
                	self.check_pass(graph_user_getconfirmlist, [ f, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )

                	self.check_pass(graph_user_get, [ 3000, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , f ]] )
                	self.check_pass(graph_user_getwaitlist, [ 3000, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , f ]] )
                	self.check_pass(graph_user_getconfirmlist, [ 3000, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , f ]] )

        	self.check_pass(graph_user_add, [ 3000, 'app-friend', friends ])

        	for f in friends:
                	self.check_pass(graph_user_get, [ f, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
                	self.check_pass(graph_user_getwaitlist, [ f, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
               		self. check_pass(graph_user_getconfirmlist, [ f, [ 'app-friend' ] ], [[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )

               	 	self.check_pass(graph_user_get, [ 3000, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , f ]] )
                	self.check_pass(graph_user_getwaitlist, [ 3000, [ 'app-friend' ] ], [[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , f ]] )
                	self.check_pass(graph_user_getconfirmlist, [ 3000, [ 'app-friend' ] ], [[self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , f ]] )

        	for f in friends:
                	self.check_pass(graph_user_add, [ f, 'app-friend', [ 3000 ] ])

        	for f in friends:
                	self.check_pass(graph_user_get, [ f, [ 'app-friend' ] ], [[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
                	self.check_pass(graph_user_getwaitlist, [ f, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
                	self.check_pass(graph_user_getconfirmlist, [ f, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )

                	self.check_pass(graph_user_get, [ 3000, [ 'app-friend' ] ], [[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , f ]] )
                	self.check_pass(graph_user_getwaitlist, [ 3000, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , f ]] )
               	 	self.check_pass(graph_user_getconfirmlist, [ 3000, [ 'app-friend' ] ], [[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , f ]] )

        	for f in friends:
                	self.check_pass(graph_user_add, [ f, 'app-friend', [ 3000 ] ])

	def test_graph_add4(self):
        	graph_user_remove(3000, 'app-friend', [ 3001, 3002 ])
        	graph_user_remove(3001, 'app-friend', [ 3000, 3002 ])
        	graph_user_remove(3002, 'app-friend', [ 3000, 3001 ])

        	self.check_pass(graph_user_add, [ 3000, 'app-friend', [ 3001 ] ])
        	self.check_pass(graph_user_add, [ 3001, 'app-friend', [ 3002 ] ])
        	self.check_pass(graph_user_add, [ 3002, 'app-friend', [ 3000 ] ])

        	self.check_pass(graph_user_get, [ 3000, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )
        	self.check_pass(graph_user_getwaitlist, [ 3000, [ 'app-friend' ] ], [\
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ],\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ 3000, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ], \
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )

        	self.check_pass(graph_user_get, [ 3001, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )
        	self.check_pass(graph_user_getwaitlist, [ 3001, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )
       		self.check_pass(graph_user_getconfirmlist, [ 3001, [ 'app-friend' ] ], [\
			[ self. validate_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )

        	self.check_pass(graph_user_get, [ 3002, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )
        	self.check_pass(graph_user_getwaitlist, [ 3002, [ 'app-friend' ] ], [\
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ 3002, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )
		
		# Add one to member
        	self.check_pass(graph_user_add, [ 3001, 'app-friend', [ 3000 ] ])

        	self.check_pass(graph_user_get, [ 3000, [ 'app-friend' ] ], [\
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )
        	self.check_pass(graph_user_getwaitlist, [ 3000, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ 3000, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ], \
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )

        	self.check_pass(graph_user_get, [ 3001, [ 'app-friend' ] ], [\
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )
        	self.check_pass(graph_user_getwaitlist, [ 3001, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ 3001, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )

        	self.check_pass(graph_user_get, [ 3002, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )
        	self.check_pass(graph_user_getwaitlist, [ 3002, [ 'app-friend' ] ], [\
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ 3002, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )

		# Remove members
        	self.check_pass(graph_user_remove, [ 3001, 'app-friend', [ 3000 ] ])

        	self.check_pass(graph_user_get, [ 3000, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )
        	self.check_pass(graph_user_getwaitlist, [ 3000, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ 3000, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ], \
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )

        	self.check_pass(graph_user_get, [ 3001, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )
        	self.check_pass(graph_user_getwaitlist, [ 3001, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ 3001, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3002 ]] )

        	self.check_pass(graph_user_get, [ 3002, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )
        	self.check_pass(graph_user_getwaitlist, [ 3002, [ 'app-friend' ] ], [\
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ 3002, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ], \
			[ self.validate_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )


	def test_graph_remove(self):
        	self.test_graph_add()
        	self.check_pass(graph_user_remove, [ 3000, 'app-friend', [ 3001 ] ])
        	self.check_pass(graph_user_get, [ 3000, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )
        	self.check_pass(graph_user_getwaitlist, [ 3000, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )
        	self.check_pass(graph_user_getconfirmlist, [ 3000, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3001 ]] )
       	 	self.check_pass(graph_user_get, [ 3001, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
       	 	self.check_pass(graph_user_getwaitlist, [ 3001, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
       	 	self.check_pass(graph_user_getconfirmlist, [ 3001, [ 'app-friend' ] ], [\
			[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
        	self.check_partial_fail(graph_user_remove, [ 3000, 'app-friend', [ 3000 ] ])

	def test_graph_remove2(self):
        	friends = [ 3001, 3002, 3003, 3004, 3005, 3006, 3007, 3008, 3009, 3010 ]
        	self.test_graph_add3()
        	self.check_pass(graph_user_remove, [ 3000, 'app-friend', friends ], [ \
                	[ self.validate_obj_val, [ 'result', 'data', '3001', 'graph-list' ] , 'members' ], \
                	[ self.validate_obj_val, [ 'result', 'data', '3003', 'graph-list' ] , 'members' ], \
                	[ self.validate_obj_val, [ 'result', 'data', '3006', 'graph-list' ] , 'members' ], \
                	[ self.validate_obj_val, [ 'result', 'data', '3010', 'graph-list' ] , 'members' ], \
        	] )
        	for f in friends:
                	self.check_pass(graph_user_get, [ 3000, [ 'app-friend' ] ], [\
				[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , f ]] )
                	self.check_pass(graph_user_getwaitlist, [ 3000, [ 'app-friend' ] ], [\
				[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , f ]] )
                	self.check_pass(graph_user_getconfirmlist, [ 3000, [ 'app-friend' ] ], [\
				[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , f ]] )
                	self.check_pass(graph_user_get, [ f, [ 'app-friend' ] ], [\
				[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
                	self.check_pass(graph_user_getwaitlist, [ f, [ 'app-friend' ] ], [\
				[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
                	self.check_pass(graph_user_getconfirmlist, [ f, [ 'app-friend' ] ], [\
				[ self.validate_not_in_list, [ 'result', 'data', 'app-friend' ] , 3000 ]] )
        	self.check_partial_fail(graph_user_remove, [ 3000, 'app-friend', [ 3000 ] ])


if __name__ == '__main__':
        suite0 = unittest.TestLoader().loadTestsFromTestCase(mqs_unit)
        unittest.TextTestRunner(verbosity=99).run(suite0)
