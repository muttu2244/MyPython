import yaml
from api_constants import Constants

class ACL:
	
	@staticmethod
	def getACLValues():
		try:
			path = "/apps/%s/current/ACL.yaml" % (Constants.APP_NAMESPACE)
			f = open(path)
			aclObj = yaml.load(f.read())
			#print aclObj
			f.close()
			return aclObj
		except:
			return None

	@staticmethod
	def getGraphTypes(action, subject):
		aclObj = ACL.getACLValues()
		ACLArray = aclObj['ACL']
		defaultGraphTypeArray = []
		graphTypeArray = []	
		for Acl in ACLArray:
			_subject = Acl['subject']
			if _subject == subject:
				actionList = Acl['action'].keys()
				i = 0
				for _graphList in Acl['action']:
					if actionList[i] == 'default-action':
						defaultGraphTypeArray = Acl['action'][_graphList]
					if  actionList[i] == action:
						graphTypeArray =  Acl['action'][_graphList]
						break
					i += 1
					del _graphList
				del actionList
				break
			del Acl

		if graphTypeArray.__len__() == 0:
			if defaultGraphTypeArray.__len__() != 0:
				graphTypeArray = defaultGraphTypeArray
			else:
				if subject != 'default-subject':
					return ACL.getGraphTypes(action, 'default-subject')
				else:
					return None

		mqsGraphTypeArray = []
		
		for _graph in graphTypeArray:
			if _graph == 'none' or _graph == 'trusted' or _graph == 'impersonated' or _graph == 'self' or _graph == 'any':
				mqsGraphTypeArray.append(_graph)
			else:
				mqsGraphTypeArray.append(_graph)
		
		if mqsGraphTypeArray.__len__() != 0:
			return mqsGraphTypeArray
		return None


