#!/usr/bin/python26
import ConfigParser
import os, sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/config")

class constants:
	
	cfg = ConfigParser.SafeConfigParser()
	try:
		cfg.read("config/ghconfig.conf")
	except:
		print "Couldnt parse config file"
		sys.exit(1)

	URL = cfg.get("gh-config", "url")
	GAMEID = cfg.get("gh-config" , "gameid")
	
	STORAGE_PATH = "/apps/{0}/current/Storage.yaml"
	GREYHOUND_PATH = "/apps/{0}/current/greyhound.ini"
	ACL_PATH = "/apps/{0}/current/ACL.yaml"

	ZRT_USERNAME = cfg.get("gh-config", "zrtUser")
	ZRT_PASSWORD = cfg.get("gh-config", "zrtPass")

	
	#Storage.yaml
	DEFAULT_KEYS = ["Blobs","Deltas","Scoreboard"]
	DEFAULT_DELTA_KEYS = ['keep', 'maxcount', 'maxsize', 'pool', 'ttl', 'type']
	DEFAULT_BLOB_KEYS = ['maxsize','pool','type']
	DEFAULT_SCOREBOARD_KEYS = ['max','min','maxcount','pool','ttl','type']
	
	#
	#Error messages
	#
	ERROR_INTERNAL = "Internal server error occured"
	HTTP_ERROR = "Error occured. HTTP {0}"
	HTTP_FAILED = "Couldnot send the request"
	DECODE_FAILED = "JSON decode failed"
	FILE_LOAD_ERROR = "Couldnot load file"

	DEFAULT_KEYS_ERROR = "Default keys are not present in Storage.yaml file"
	DEFAULT_TYPE_ERROR = "Default type * not present in Storage.yaml or doesnot have all the default keys" 

	#
	#Input data
	#
	POSTDATA_GET = {"appid": GAMEID}
	
	#
	#KEYs in ACS input json string
	#
	ACSKEY_SECRET = "zlive_secret"
	ACSKEY_GAMEID = "zlive_gameid"
	ACSKEY_NAMESPACE = "zlive_game_namespace"

	ACSKEY_BLOBS = "blobs"
	ACSKEY_GOLDEN = "golden"
	ACSKEY_DELTAS = "deltas"
	ACSKEY_SCOREBOARD = "scoreboard"
	ACSKEY_ACL = "acl"
	ACSKEY_GRAPHS = "graphs"
	ACSKEY_SCHEMA = "schema"

	
	

if __name__ == '__main__':
	print constants.URL
	print constants.POSTDATA_GET
