from curl_util import *

class ZrtClient:
	zrtUser = constants.ZRT_USERNAME 
	zrtPass = constants.ZRT_PASSWORD
	def __init__(self, zrtKey, zrtEnv):
		self.zrtKey = zrtKey
		self.zrtEnv = zrtEnv

	def _call(self, revision):
		url = "https://api.runtime.zynga.com:8994/%s/%s/%s" % (self.zrtKey, self.zrtEnv, revision)
		cred = "%s:%s" % (self.zrtUser, self.zrtPass)
		status, response = sendRequest(url, None, None, cred)
		if status:
			if response['status'] == 0:
				return response
		return {}

	def getVar(self,key):
		response = self._call('current')
		if response:
			return response.get("output", {}).get(key)
		return None

if __name__ == "__main__":
	zrt = ZrtClient("greyhound-mt","dev")
	#zrt = ZrtClient("greyhound", "prod")
	print zrt.getVar("MQS_META_SCHEMA_2244")
	print zrt.getVar("GRAPH_TYPES_2244")

		
