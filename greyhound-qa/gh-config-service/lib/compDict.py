import copy
import logging

a = {'adminLog': {}, 'history-archive': {'maxsize': '300k'}, 'new-world': {}, 'transactionLog': {}, 'player': {}, 'serverUser': {}, 'game-world': {}, 'reputation': {}, 'user': {}, 'payments-meta': {}, 'thresholds': {}, 'history-current': {'maxsize': '100k'}}

b = {'adminLog': {}, 'history-archive': {'maxsize': '300k'}, '*': {'maxsize': '128k', 'pool': 'MB_OBJECTS_MASTER'}, 'new-world': {}, 'transactionLog': {}, 'player': {}, 'serverUser': {}, 'game-world': {}, 'reputation': {}, 'user': {}, 'payments-meta': {}, 'thresholds': {}, 'history-current': {'maxsize': '100k'}}


MSG = ''

#a = [{"type": "gift", "min":"4", "max":"6"},{"type":"harvest", "min":"5","max":"3"}]
#b = [{"type": "gift", "min":"2", "max":"5"},{"type":"harvest", "min":"5","max":"6"}]
def special_diff(dictA, dictB, key=None):
	global MSG
	dictA = dict([(D[key], pop(D,key)) for D in dictA])
	dictB = dict([(D[key], pop(D,key)) for D in dictB])
	dict_diff(dictA,dictB)
	ret = MSG
	MSG = ''
	return ret

def pop(x,k):
	x = copy.copy(x); del x[k]; return x


def dict_diff(a, b):
	global MSG
	if isinstance(a, dict) and isinstance(b,dict):
		for key in a.keys():
			if(not b.has_key(key)):
				MSG += "%s only in Input/Output\n"%key
			elif a[key] != b[key]:
				MSG += "%s --> "%key
				dict_diff(a[key], b[key])

		for key in b.keys():
			if (not a.has_key(key)):
				MSG += "%s only in Storage.yaml\n"%key
	else:
		MSG += "%s doesnot match %s\n" %(a,b)



if __name__ == "__main__":
	#special_diff(a,b,"name")	
	dict_diff(a,b)
	print MSG
