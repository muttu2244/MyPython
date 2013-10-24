#!/usr/bin/python26
import yaml
import ConfigParser
import pdb
from zrtClient import ZrtClient
from compDict import *
from utils import *
from constants import constants


class compareFiles:

	def __init__(self, input):
		self.input = input
		self.gameId = self.input[constants.ACSKEY_GAMEID]
		self.storagePath = constants.STORAGE_PATH.format( self.gameId )
		self.greyhoundPath = constants.GREYHOUND_PATH.format(self.gameId)
		self.aclPath = constants.ACL_PATH.format(self.gameId)


	def checkStorageYaml(self, contents = None):
		status = True
		message = ''
		if contents:
			fileContents = contents
		else:
			fileContents = loadYaml(self.storagePath)
		if not fileContents:
			return False, constants.FILE_LOAD_ERROR
		
		#Checking Main Keys
		keys = fileContents.keys()
		defaultKeys = constants.DEFAULT_KEYS 
		if not set(defaultKeys).issubset(set(keys)):
			return False, constants.DEFAULT_KEYS_ERROR 
		#Collecting all blob types
		inputBlobs = []
		for blob in self.input["blobs"]:
			inputBlobs.append( blob["type"] )

		storedBlobs = []
		for blob in fileContents["Blobs"]:
			storedBlobs.append( blob["type"] )

		if "*" not in storedBlobs:
			status = False
			return False, constants.DEFAULT_TYPE_ERROR
		
		storedBlobs.remove('*')
		temp1 = set(inputBlobs) - set(storedBlobs)
                temp2 = set(storedBlobs) - set(inputBlobs)
		if temp1:
			status = False
			message +=  "The following blobs not present in Storage.yaml file "+ str(list(temp1))
		if temp2:
			status = False
			message += "\nThe following blobs were not in input/output json string but in Storage.yaml file "+str(list(temp2))

		if inputBlobs.__len__() != storedBlobs.__len__():
			status = False
			message += "\nLength of input blobs not matching"

		#compare the values defined for each blob type
		indexed = self.input["blobs"]
		"""for blob in self.input["blobs"]:
			for b in fileContents["Blobs"]:
				if b["type"] == blob["type"]:
					keys = blob.keys()
					for key in keys:
						if b[key] != blob[key]:
							return False, "%s not matching in %s"%(key, blob["type"])
		"""
		
		for item in fileContents["Blobs"]:
			if item['type'] == '*':
				fileContents["Blobs"].remove(item)
				break
		msg = special_diff( self.input["blobs"],fileContents["Blobs"], "type")
		if msg:
			return False, msg
		if status:
			return True, "Success"
		else:
			return False, message

	def checkScoreboard(self):
		fileContents = loadYaml(self.storagePath)
		if not fileContents:
			return False, constants.FILE_LOAD_ERROR
		scoreboard = self.input[constants.ACSKEY_SCOREBOARD]
		storedScore = fileContents['Scoreboard']
		for item in storedScore:
			if item['type'] == '*':
				if item.keys().__len__() != constants.DEFAULT_SCOREBOARD_KEYS.__len__():
					return False, constants.DEFAULT_TYPE_ERROR
				if set(item.keys()) != set(constants.DEFAULT_SCOREBOARD_KEYS):
					return False, constants.DEFAULT_TYPE_ERROR
				storedScore.remove(item)
				break

		msg = special_diff( scoreboard, storedScore, 'type')
		if msg:
			return False, msg
		return True, "Success"
		
	def checkDeltas(self):
		fileContents = loadYaml(self.storagePath)
		if not fileContents:
			return False, constants.FILE_LOAD_ERROR

		deltas = self.input['deltas']
		storedDeltas = fileContents['Deltas']
		for item in storedDeltas:
			if item['type'] == '*':
				if item.keys().__len__() != constants.DEFAULT_DELTA_KEYS.__len__():
					return False, constants.DEFAULT_TYPE_ERROR
				if set(item.keys()) != set(constants.DEFAULT_DELTA_KEYS):
					return False, constants.DEFAULT_TYPE_ERROR
				storedDeltas.remove(item)
				break
				
		msg = special_diff( deltas, storedDeltas, "type")
		if msg:
			return False, msg
		return True, "Success"


	def checkAclFile(self, contents = None):
		if contents:
			fileContents = contents
		else:
			fileContents = loadYaml(self.aclPath)
		if not fileContents:
			return False, constants.FILE_LOAD_ERROR
		acl = self.input['acl']
		index1 = {}
		index2 = {}
		for api in self.input["acl"]:
			temp = {}
			for t in api['api_list']:
				temp.update({t['api']:t['roles']})
			index1.update({api['blob']: temp})

		for item in fileContents['ACL']:
			index2.update({item['subject']:item['action']})

		if index1.keys() != index2.keys():
			return False, "No of subjects in ACL file not matching with input"
	
		msg = ""
		for k,v in index1.items():
			if index1[k] != index2[k]:
				for m,n in v.items():
					if m not in index2[k].keys():
						return False, m + " not in  storage.yaml"
					elif index1[k][m] != index2[k][m]:
						return False, "For " + m + " input was "+str(n)+" but stored is " + str(index2[k][m])
		return True, "Ok"

	def checkGreyhoundIni(self, contents = None):
		if contents:
			fileContents = contents
		else:
			fileContents = loadIni(self.greyhoundPath)
		msg = ""
		if fileContents['int gh_game_id'] != self.input['zlive_gameid']:
			return False, "Game id recieved is %s but stored is %s\n"%(str(self.input['zlive_gameid']),str(fileContents['int gh_game_id']))
		if fileContents['app_namespace'] != self.input['zlive_game_namespace']:
			return False, "Appname recieved is %s but stored is %s\n"%(str(self.input['zlive_game_namespace']),str(fileContents['app_namespace']))
		if fileContents['gh_app_secret'] != self.input['zlive_secret']:
			return False, "App secret recieved is %s but stored is %s\n"%(str(self.input['zlive_secret']),str(fileContents['gh_app_secret']))
		return True, "Ok"

	def checkGraphTypes(self):
		key = 'GRAPH_TYPES_' + self.input['zlive_gameid']
		zrtGraphTypes = self.getvaluesFromZrt(key)
		graphTypes = self.input['graphs']
		if zrtGraphTypes != graphTypes:
			return False, "Mis-match in the graph list. Got "+str(graphTypes)+" zrt graph types are "+str(zrtGraphTypes)
		return True, 'Ok'
	
	def checkMetaSchema(self):
		zschema = self.readMetaSchema()	
		schema = self.input['schema']
		msg = special_diff(schema, zschema, "name")
		if msg:
			return False, msg
		return True, "Success"

	def readMetaSchema(self):
		key = 'MQS_META_SCHEMA_' + self.input['zlive_gameid']
		zrtschema = self.getvaluesFromZrt(key)
		schema = []
		for item in zrtschema:
			v = item.split('|')
			schema.append({"name": v[0], "type": v[1], "default_value": v[2], "scope": v[3]})
		return schema

	def getvaluesFromZrt(self, key):
		fileContents = loadIni(self.greyhoundPath)
		zrtKey = fileContents["zruntime_product_key"]
		zrtEnv = fileContents["zruntime_namespace_key"]
		zrt = ZrtClient(zrtKey, zrtEnv)
		return zrt.getVar(key)


if __name__ == '__main__':
	import simplejson as json
	st = json.load(open("json"))
	o = compareFiles(st)
	#print o.checkStorageYaml()
	#print o.checkAclFile()
	#print o.checkGreyhoundIni()
	print o.checkGraphTypes()
