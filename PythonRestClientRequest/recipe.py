import requests



class MyRecipe(object):
    def doSomething(self):
        r = requests.get('https://api.github.com/user', auth=('muttu2244', 'June2017*'))
        #print r.headers['content-type']
        print "###########################################"
        print "The header is %s" %r.headers
        print "###########################################"
        return (r.headers['status'], r.headers['X-GitHub-Request-Id'])
    def _url(self,path):
        #return 'https://api.github.com/' + path
        return 'http://localhost:8133/' + path
    def get_recipeByName(self,path):
        #r = requests.get('http://localhost:9010/recipe/recipename')
        r = requests.get(self._url(path))
	#r = requests.get('https://api.github.com/user', auth=('muttu2244', 'June2017*'))
		print "###########################################"
        print "The header is %s" %r.headers
        print "###########################################"
	#return (r.headers['status'], r.headers['X-GitHub-Request-Id'])
	text = r.json()
	#print "Type of text is %s" %type(text)
	reqStatus = r.status_code
        recipeSteps = text['recipe']['steps']
	recipeOperationHeader = text['recipe']['operationHeader']
	return (reqStatus,recipeSteps, recipeOperationHeader)
	#return text
	

    def get_allRecipe(self,path):
        r = requests.get(self._url(path))
        print "###########################################"
        print "The header is %s" %r.headers
        print "###########################################"
	#return (r.headers['status'], r.headers['X-GitHub-Request-Id'])
	text = r.json()
	print "Type of text is %s" %text



	'''
	def describe_task(path, task_id):
		return requests.get(self._url(path.format(task_id)))

	def add_task(path, summary, description=""):
		return requests.post(_url(path), json={
			'summary': summary,
			'description': description,
			})

	def task_done(path, task_id):
		return requests.delete(_url(path.format(task_id)))

	def update_task(path, task_id, summary, description):
		url = _url(path.format(task_id))
		return requests.put(url, json={
			'summary': summary,
			'description': description,
			})
	'''
