import sys
from api_constants import Constants
from api_error import ApiError 
import pycurl
import cStringIO
from util import Util
import time

class CurlReq(object):
	def __init__(self, api, callback, timeout):
		self.m = ConnPool.get_multi(api)
		self.callback = callback
		self.num_requests = 0
		self.s_iter = 0
		self.e_iter = 0
		self.handles = []
		self.api_error = { }
		self.api_data = { }
		self.timeout = timeout

	def add_request(self, c, callback_arg):
		if not isinstance(callback_arg, list) or len(callback_arg) == 0:
			raise Exception("callback arg list not provided")
		c.fp = cStringIO.StringIO()
		c.callback_arg = callback_arg
		c.setopt(pycurl.WRITEFUNCTION, c.fp.write)
		self.m.add_handle(c)
		self.num_requests += 1
		self.handles.append(c)

	def perform(self):
		ret = pycurl.E_CALL_MULTI_PERFORM
		while ret == pycurl.E_CALL_MULTI_PERFORM:
			ret, num_handles = self.m.perform()

	def process_response(self, success, callback, data, args):
		if success:
			retval = Util.decode_post(data)
			if not retval:
				Util.err_log("Unable to decode response: args=%s data=%s" % (str(args), data))
				self.api_error[ args[0] ] = ApiError.badData("Unable to parse data")
				return

			if not Util.status_success(retval):
				self.api_error[ args[0] ] = ApiError.internalApiError(retval[ Constants.STATUS ])
			else:
				self.api_data[ args[0] ] = retval[ Constants.RESULT ]
				if callback:
					callback(args, retval[ Constants.RESULT ])
		else:
			self.api_error[ args[0] ] = ApiError.connectionError(data)

	def wait(self):
		ret = pycurl.E_CALL_MULTI_PERFORM
		while ret == pycurl.E_CALL_MULTI_PERFORM:
			ret, num_handles = self.m.perform()

		end_time = time.time() + self.timeout
		queued = self.num_requests
		while num_handles or queued:
			timeout = end_time - time.time()
			if timeout <= 0:
				break
			ret = self.m.select(timeout)
			if ret == -1:
				break

			ret = pycurl.E_CALL_MULTI_PERFORM
			while ret == pycurl.E_CALL_MULTI_PERFORM:
				ret, num_handles = self.m.perform()

			queued, succ_list, fail_list = self.m.info_read()
			for c in succ_list:
				self.process_response(True, self.callback, c.fp.getvalue(), c.callback_arg)
				self.s_iter += 1
				self.m.remove_handle(c)
				c.fp.close()
				c.fp = None
				c.callback_arg = None
				self.handles.remove(c)
				ConnPool.put(c)

			for e in fail_list:
				self.process_response(False, self.callback, e[2], e[0].callback_arg)
				self.e_iter += 1
				self.m.remove_handle(e[0])
				e[0].fp.close()
				e[0].fp = None
				e[0].callback_arg = None
				self.handles.remove(e[0])
				ConnPool.put(e[0])

		for c in self.handles:
			self.process_response(False, self.callback, "Timeout", c.callback_arg)
			self.e_iter += 1
			self.m.remove_handle(c)
			c.fp.close()
			c.fp = None
			c.callback_arg = None
			ConnPool.put(c)
		self.handles = [ ]

		if (self.s_iter + self.e_iter) != self.num_requests:
			Util.err_log("Mismatch in the number of requests queued and result received in CurlReq")
			Util.err_log("num_requests: %d success: %d error: %d\n" % (self.num_requests, self.s_iter, self.e_iter))
		ConnPool.put_multi(self.m)
		self.m = None
		return [ self.api_data, self.api_error ]

class Request(object):
	def __init__(self, api, timeout, connect_timeout):
		self.api = api
		self.timeout = timeout
		self.connect_timeout = connect_timeout

	def gen_request(self, server, headers, post):
		headers += [ "%s: %s" % (Constants.HEADER_X_OPERATION, self.api) ]
		headers += get_common_headers()

		url = "http://%s/services/%s" % (server, self.api)
		c = ConnPool.get(url)
		c.setopt(pycurl.URL, url)
		c.setopt(pycurl.HTTPHEADER, headers)
		c.setopt(pycurl.POST, 1)
		c.setopt(pycurl.POSTFIELDS, Util.encode_post(post))
		c.setopt(pycurl.TIMEOUT, self.timeout)
		c.setopt(pycurl.CONNECTTIMEOUT, self.connect_timeout)
		return c

class ConnPool(object):
	c = { }
	m = { }
	cache_size = 5

	@staticmethod
	def init():
		ConnPool.m = { }
		ConnPool.c = { }
		ConnPool.cache_size = 5

	@staticmethod
	def get_multi(key):
		m = None
		if key in ConnPool.m:
			if ConnPool.m[ key ]:
				m = ConnPool.m[ key ].pop()
		if not m:
			m = pycurl.CurlMulti()
			m.key = key
		return m

	@staticmethod
	def put_multi(m):
		if m.key not in ConnPool.m:
			ConnPool.m[ m.key ] = [ ]
		if len(ConnPool.m[ m.key ]) > ConnPool.cache_size:
			m.key = None
			m.close()
		else:
			ConnPool.m[ m.key ].append(m)

	@staticmethod
	def get(key):
		c = None
		if key in ConnPool.c:
			if ConnPool.c[ key ]:
				c = ConnPool.c[ key ].pop()
		if not c:
			c = pycurl.Curl()
			c.key = key
		return c

	@staticmethod
	def put(c):
		if c.key not in ConnPool.c:
			ConnPool.c[ c.key ] = [ ]
		if len(ConnPool.c[ c.key ]) > ConnPool.cache_size:
			c.key = None
			c.close()
		else:
			ConnPool.c[ c.key ].append(c)

def exec_curl(version, req, args):
	s = cStringIO.StringIO()
	c = Util.fun_wrapper(req, args)
	c.setopt(pycurl.WRITEFUNCTION, s.write)
	try:
		c.perform()
	except Exception, e:
		err = c.errstr()
		ConnPool.put(c)
		return [ False, None, Util.gen_error(version, ApiError.connectionError(err)) ]
		
	if c.getinfo(pycurl.HTTP_CODE) != 200:
		err = c.errstr()
		ConnPool.put(c)
		return [ False, None, Util.gen_error(version, ApiError.connectionError(err)) ]
	ConnPool.put(c)

	ret = Util.decode_post(s.getvalue())
	if not ret:
		return [ False, None, Util.gen_error(version, ApiError.badData("Unable to parse response body")) ]
		
	if not Util.status_success(ret):
		return [ False, None, Util.gen_error(version, ApiError.internalApiError(ret[ Constants.STATUS ])) ]
	return [ True, ret[ Constants.RESULT ], None ]

def exec_curl2(version, req, args):
	s = cStringIO.StringIO()
	c = Util.fun_wrapper(req, args)
	c.setopt(pycurl.WRITEFUNCTION, s.write)
	try:
		c.perform()
	except Exception, e:
		err = c.errstr()
		ConnPool.put(c)
		return [ False, None, Util.gen_error(version, ApiError.connectionError(err)), None ]
		
	if c.getinfo(pycurl.HTTP_CODE) != 200:
		err = c.errstr()
		ConnPool.put(c)
		return [ False, None, Util.gen_error(version, ApiError.connectionError(err)), None ]
	con_type = c.getinfo(pycurl.CONTENT_TYPE)
	ConnPool.put(c)
	return [ True, [ Constants.HTTP_RESULT_200, s.getvalue() ], None, con_type ]

def gen_multi_data_succ(data, partial_flag, req_data):
	for k1 in req_data:
		if req_data[ k1 ][ Constants.PARTIAL ]:
			partial_flag = True

		# TBD: Replace this with dictionary merge
		in_data = req_data[ k1 ][ Constants.DATA ]
		for k, v in in_data.items():
			data[ k ] = v
	return [ data, partial_flag ]

def gen_multi_data_err(data, partial_flag, req_err, keys):
	# TBD: See if this can be optimized
	for i in keys:
		data[ i ] = req_err
	return [ data, True ]


def get_common_headers():
	return [ "Expect:", "Connection: Keep-Alive", "Keep-Alive: 300", "Content-Type: application/json" ]
