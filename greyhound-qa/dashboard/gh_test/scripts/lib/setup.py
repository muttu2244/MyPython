import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../lib")
import multiprocessing
import sqlite3
import ConfigParser
import pycurl
from api_constants import *
from api_error import *
import select
import time
import simplejson as json
import memcache
import random

CONFIG = 'setup.cfg'

def encode_post(data):
	return json.dumps(data)

def decode_post(data):
	try:
		ret = json.loads(data)
	except Exception:
		return False
	return ret

class Config(object):
	@staticmethod
	def init():
		global CONFIG

		config = ConfigParser.ConfigParser()
		config.read(CONFIG)

		Config.user_id_start = config.getint('mqs', 'user_id_start')
		Config.user_id_end = config.getint('mqs', 'user_id_end')
		graph_size = config.get('mqs', 'graph_size')
		graphs = config.get('mqs', 'graph_types')
		meta_db_servers = config.get('mqs', 'meta_db_servers')
		Config.meta_db_servers = [ i for i in meta_db_servers.split(',') if i ]
		Config.meta_db_shards = config.getint('mqs', 'meta_db_shards')

		graph_db_servers = config.get('mqs', 'graph_db_servers')
		Config.graph_db_servers = [ i for i in graph_db_servers.split(',') if i ]
		Config.graph_db_shards = config.getint('mqs', 'graph_db_shards')
		Config.graph_types = [ i.strip() for i in graphs.split(',') if i ]
		Config.graph_size = [ int(i.strip()) for i in graph_size.split(',') if i ]
		Config.graph_on_membase = config.getboolean("mqs", "graph_on_membase")
		if len(Config.graph_types) != len(Config.graph_size):
			raise Exception("Mismatch in the number of graph_types and graph_size values in config")

def gen_request(api, server, params):
		url = "http://%s/services/%s" % (server, api)

		headers = [ "Expect:", "Connection: Keep-Alive", "Keep-Alive: 300", 'Content-Type: application/json', "X-Operation: %s" % (api) ]
		c = pycurl.Curl()
		c.setopt(pycurl.URL, url)
		c.setopt(pycurl.HTTPHEADER, headers)
		c.setopt(pycurl.POST, 1)
		c.setopt(pycurl.POSTFIELDS, encode_post( params ))
		return c

def wait_all(r):
	while 1:
		ret, num_handles = r.perform()
		if ret != pycurl.E_CALL_MULTI_PERFORM:
			break

	while num_handles:
		#apply(select.select, r.fdset() + (1,))
		time.sleep(1)
		while 1:
			ret, num_handles = r.perform()
			if ret != pycurl.E_CALL_MULTI_PERFORM:
				break

def gen_random_rows(pk, fields):
	row = [ ]
	random.seed(time.time())
	for k in fields:
		v = None
		if len(k) == 6:
			name, data_type, value, range1, range2, range3 = k
		elif len(k) == 7:
			name, data_type, value, range1, range2, range3, range4 = k
		else:
			raise Exception("Undefined fields - %s" % (k))

		if data_type == 'int':
			if value == 'random':
				v = random.randint(range1, range2)
			elif value == 'fixed':
				v = range1
			else:
				v = 0
		elif data_type == 'varchar':
			if value == 'random':
				v = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(range1))
			elif value == 'fixed':
				v = range1
			else:
				v = ''
		elif data_type == 'primary':
			v = pk
		elif data_type == 'list-of-int':
			if value == 'random':
				j = 0
				v1 = [ ]
				while j < range1:
					v1.append(random.randint(range2, range3))
					j += 1
				v = ",".join(str(j) for j in v1)
		elif data_type == 'graph-blob':
			v = { Constants.GRAPH_VERSION: 1, Constants.GRAPH_GRAPHS: { } }
			if value == 'random':
				for i in range(0, len(range1)):
					graph_list = range1[ i ]
					v[ Constants.GRAPH_GRAPHS ][ graph_list ] = { }
					v[ Constants.GRAPH_GRAPHS ][ graph_list ][ Constants.GRAPH_MEMBERS ] = [ ]
					v[ Constants.GRAPH_GRAPHS ][ graph_list ][ Constants.GRAPH_CONFIRM ] = [ ]
					v[ Constants.GRAPH_GRAPHS ][ graph_list ][ Constants.GRAPH_WAIT ] = [ ]
					for j in range(0, len(range2)):
						for k in range(0, range2[ j ]):
							v[ Constants.GRAPH_GRAPHS ][ graph_list ][ Constants.GRAPH_MEMBERS ].append(random.randint(range3, range4))
				v = json.dumps(v)
		else:
			raise Exception("Undefined type %s" % data_type)
		row.append(v)
	return row

def generate_rows(start, end, x_offset, x, x_limit, y, y_offset, fields):
	rows = []
	zid = start + x_offset
	j = y_offset
	while zid < end:
		i = x_offset
		zid = start + (j * x_limit) + i
		while i < x_limit and zid < end:
			rows.append(gen_random_rows(zid, fields))
			i += x
			zid = start + (j * x_limit) + i
		j += y
	return rows

def meta_populate():
	id_step = 10000 * len(Config.meta_db_servers) * 50
	meta_fields = [
		[ 'zid', 'primary', None, None, None, None ],
		[ 'flags', 'int', 'fixed', 0, None, None ],
		[ 'cas', 'varchar', 'fixed', '0000000000000000000000', None, None ],
		[ 'mtime', 'int', 'fixed', 0, None, None ],
		[ 'cred', 'int', 'fixed', 0, None, None ],
		[ 'vow', 'int', 'random', 10, 100000, None ],
		[ 'vou', 'int', 'random', 10, 1000, None ],
		[ 'cash', 'int', 'random', 10, 1000000, None ],
		[ 'coins', 'int', 'random', 10, 1000000, None ],
		[ 'level', 'int', 'random', 5, 350, None ],
		[ 'xp', 'int', 'random', 20, 10000, None ],
		[ 'gold', 'int', 'random', 5, 500000, None ],
		[ 'visitTime', 'int', 'random', 500000, 2000000, None ],
		[ 'level2', 'int', 'random', 3, 420, None ],
		[ 'xp2', 'int', 'random', 10, 23000, None ],
		[ 'level3', 'int', 'random', 21, 750, None ],
		[ 'xp3', 'int', 'random', 10, 8000, None ],
		[ 'commodity_1', 'int', 'random', 100, 250000, None ],
		[ 'commodity_2', 'int', 'random', 10000, 48239383, None ],
		[ 'commodity_3', 'int', 'random', 38239, 38293933, None ],
		[ 'commodity_4', 'int', 'random', 38, 33933, None ],
		[ 'commodity_5', 'int', 'random', 83832, 473893933, None ],
		[ 'commodity_6', 'int', 'random', 373, 99993933, None ],
		[ 'commodity_7', 'int', 'random', 9328, 338293933, None ],
		[ 'commodity_8', 'int', 'random', 3739, 78293933, None ],
	]

	id_start = Config.user_id_start
	id_end = id_start + id_step
	if id_end > Config.user_id_end:
		id_end = Config.user_id_end
	handles = [ ]
	cnt = 0
	limit = len(Config.meta_db_servers) * 30
	r = pycurl.CurlMulti()
	while True:
		for j in range(Config.meta_db_shards):
			for i in range(len(Config.meta_db_servers)):
				server = Config.meta_db_servers[ i ]
				print "id_start=%d id_end=%d i=%d j=%d server=%s" % (id_start, id_end, i, j, server)
				c = gen_request("meta.db.populate",
						server,
						{
							Constants.START: id_start,
							Constants.END: id_end,
							Constants.X_OFFSET: j,
							Constants.X: Config.meta_db_shards,
							Constants.X_LIMIT: 10000,
							Constants.Y: len(Config.meta_db_servers),
							Constants.Y_OFFSET: i,
							Constants.FIELDS: meta_fields, 
						})
				r.add_handle(c)
				handles.append(c)
				cnt += 1
				if cnt >= limit:
					wait_all(r)
					for c in handles:
						r.remove_handle(c)
					handles = [ ]
					cnt = 0
					time.sleep(1)
		if id_end == Config.user_id_end:
			break
		id_start = id_end
		id_end = id_start + id_step
		if id_end > Config.user_id_end:
			id_end = Config.user_id_end
	wait_all(r)

def graph_populate():
	id_step = 10000 * len(Config.graph_db_servers) * 50
	graph_fields = [
		[ 'zid', 'primary', None, None, None, None ],
		[ 'cas', 'varchar', 'fixed', '0000000000000000000000', None, None ],
		[ 'blob', 'graph-blob', 'random', Config.graph_types, Config.graph_size, Config.user_id_start, Config.user_id_end ]
	]

	id_start = Config.user_id_start
	id_end = id_start + id_step
	if id_end > Config.user_id_end:
		id_end = Config.user_id_end
	cnt = 0
	limit = len(Config.graph_db_servers) * 30
	if Config.graph_on_membase:
    		mc = memcache.Client(Config.graph_db_servers, debug=0)
	else:
		r = pycurl.CurlMulti()
		handles = [ ]
	while True:
		if Config.graph_on_membase:
			print "%d .. %d " % (id_start, id_end)
			rows = generate_rows(id_start, id_end, 0, 1, id_end, 1, 0, graph_fields)
			for row in rows:
				key = "graph_" + str(row[0])
				mc.set(key, row[2])
				#print row
		else:
			for j in range(Config.graph_db_shards):
				for i in range(len(Config.graph_db_servers)):
					server = Config.graph_db_servers[ i ]
					print "id_start=%d id_end=%d i=%d j=%d server=%s" % (id_start, id_end, i, j, server)
					c = gen_request("graph.db.populate",
							server,
							{
								Constants.START: id_start,
								Constants.END: id_end,
								Constants.X_OFFSET: j,
								Constants.X: Config.graph_db_shards,
								Constants.X_LIMIT: 10000,
								Constants.Y: len(Config.graph_db_servers),
								Constants.Y_OFFSET: i,
								Constants.FIELDS: graph_fields, 
							})
					r.add_handle(c)
					handles.append(c)
					cnt += 1
					if cnt >= limit:
						wait_all(r)
						for c in handles:
							r.remove_handle(c)
						handles = [ ]
						cnt = 0
						time.sleep(1)
		if id_end == Config.user_id_end:
			break
		id_start = id_end
		id_end = id_start + id_step
		if id_end > Config.user_id_end:
			id_end = Config.user_id_end
	if not Config.graph_on_membase:
		wait_all(r)

def usage():
	print "%s [ meta-populate | graph-populate ]" % sys.argv[0]
	sys.exit(0)

if __name__ == '__main__':
	if len(sys.argv) < 2:
		usage()

	Config.init()
	if sys.argv[1] == 'meta-populate':
		meta_populate()
	elif sys.argv[1] == 'graph-populate':
		graph_populate()
	else:
		usage()
	
