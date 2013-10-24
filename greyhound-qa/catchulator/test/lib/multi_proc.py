#!/usr/bin/python2.6

import time
import random
import numpy
import multiprocessing
import simplejson as json
from gh_api import *
#from auth import *

USER_NOS = 10000
QUEUE_SIZE = 100

def setup():
	y = QUEUE_SIZE
	x = range(1000000, 1000000 + USER_NOS)
	s = len(x)/y
	
	#dcash = numpy.random.noncentral_chisquare(3, 20, USER_NOS)
	dcash = numpy.random.weibull(1, USER_NOS)
	dgold = numpy.random.weibull(1, USER_NOS)
	dqueue = [x[s*i:s*i+s] for i in range(y-1)] + [x[-s-(len(x)-y*s):]] 
	return dcash, dgold, dqueue

def user_blob_set_data(zid_id):
	if zid_id > 100:
		player = {}
		player['gold'] = gold[zid_id - 1000000]
		player['cash'] = cash[zid_id - 1000000]
		player['level'] = random.randint(2, 5)
		post_data = json.dumps(player)
		return user_blob_set(zid_id, "player", post_data, cas = " ")
	else:
		return user_dau_queue_update(zid_id)

def user_payment_meta_append(zid_id):
	pay = {}
	pay_cash = {}
	pay_cash['cash'] = 100
	pay['payment'] = pay_cash
	pay_fields = json.dumps(pay)
	print pay_fields
	return payment_meta_append(AuthSystem.getImpersonatedAuthToken(zid_id), pay_fields, cas = "")

def user_dau_queue_update(zid_list):
	return dau_queue_update(AuthSystem.getTrustedAuthToken(1),\
		 json.dumps({"version": 1, "uid-list": map(str, dqueue[zid_list])}))

def multi_ops(func, list):
	proc_pool = multiprocessing.Pool(processes=150)
	print '\n Populating catchulator ...'
	st = time.time()
	for i, _ in enumerate(proc_pool.imap_unordered(func, list),1):
		sys.stdout.write('\r{0}/{1} \t['.format(i, USER_NOS + QUEUE_SIZE))
		sys.stdout.write('#'* int(100 * (float(i)/float(USER_NOS + QUEUE_SIZE))))
		sys.stdout.write('] {0}%'.format(int(100 * (float(i)/float(USER_NOS + QUEUE_SIZE)))))
		sys.stdout.flush
	sys.stdout.write('\n')
	sys.stdout.flush
	proc_pool.close()
	print 'Time taken : {0} sec\n' .format(time.time()-st)


if __name__ == '__main__':
	share_cash, share_gold, share_dqueue = setup()
	manager = multiprocessing.Manager()
	cash = manager.list(share_cash)
	gold = manager.list(share_gold)
	dqueue = manager.list(share_dqueue)
	
	uid = range(1000000, (1000000 + USER_NOS)) + range(QUEUE_SIZE)
	multi_ops(user_blob_set_data, uid)

	#pay_uid = range(1000000, (1000000 + (USER_NOS/100) *2))
	pay_uid = range(1000000, (1000000 + (USER_NOS)))
	multi_ops(user_payment_meta_append, pay_uid)
