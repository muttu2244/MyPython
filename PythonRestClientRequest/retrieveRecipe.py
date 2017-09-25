import recipe
import unittest
import requests
#import requestsSuite
import HTMLTestRunner
import time

from mocker import Mocker, MockerTestCase


'''
resp = todo.add_task("/transform/collection?from=5&to=6","Take out trash", "This description is to take out trash")
if resp.status_code != 201:
    raise ApiError('Cannot create task: {}'.format(resp.status_code))
print('Created task. ID: {}'.format(resp.json()["id"]))


resp = todo.get_tasks("transform/collection?from=5&to=6")
if resp.status_code != 200:
    raise ApiError('Cannot fetch all tasks: {}'.format(resp.status_code))
#for todo_item in resp.json():
#    print('{} {}'.format(todo_item['id'], todo_item['summary']))

else:
	print "The Response is %s" %resp

	
'''



#class MyReqTests(MockerTestCase):
class MyReqTests(unittest.TestCase):
        
        """	
        def testSomething(self):
	
                # Create a mock result for the requests.get call
                result = self.mocker.mock()
                result.headers
                self.mocker.result({'content-type': 'mytest/pass'})

                # Use mocker to intercept the call to requests.get
                myget = self.mocker.replace("requests.get")
                #myget('https://api.github.com', auth=('user', 'pass'))
                myget('https://api.github.com', auth=('muttu2244', 'June2017*'))
                self.mocker.result(result)

                self.mocker.replay()
		
		# Now execute my code
		r = recipe.MyRecipe()
		status, reqId = r.doSomething()
		print "\n###########################################"
                print "The status is : \n\n %s" %status
                print "\n###########################################"
                print "The reqId is : \n\n %s" %reqId
                print "\n###########################################" 
		# and verify the results
		self.assertEqual(status, '200 OK')
		#self.assertEqual(reqId, 'C935:1DA22:211A19:492829:59772F8B')
		
		#self.mocker.verify()
		
	"""
	def testRetrieveRecipeBasedOnName(self):
		# Now execute my code
		r = recipe.MyRecipe()
		#status, reqId = r.get_tasks('user')

                status,steps,operationHeader  = r.get_recipeByName('recipe/RecipeAuto')
                
                print "\n###########################################"
                print "The recipe Status is : \n\n %s" %status
		print "\n###########################################"
                print "The recipe Steps is : \n\n %s" %steps
                print "\n###########################################"
                print "The operationHeader is :\n\n %s" %operationHeader
                print "\n###########################################"
                

                
		# and verify the results

                self.assertEqual(status, 200)
		
                print steps[0]["actionDescription"]
                self.assertEqual(steps[0]["actionDescription"], "Default Flowpath")
		print steps[0]["comment"]
		self.assertEqual(steps[0]["comment"],"Recipe Step 1")
		print steps[0]["actionGroup"]
		self.assertEqual(steps[0]["actionGroup"], "Flowpath-System")
		print steps[0]["actionValue"]
		self.assertEqual(steps[0]["actionValue"], "1")
		print steps[0]["stepNumber"]
		self.assertEqual(steps[0]["stepNumber"], "1")

		self.assertEqual(steps[1]["actionDescription"], "XV300 Outlet F0 Close")
		self.assertEqual(steps[1]["comment"],"Recipe Step 2")
		self.assertEqual(steps[1]["actionGroup"], "Flowpath-System")
		self.assertEqual(steps[1]["actionValue"], "0")
		self.assertEqual(steps[1]["stepNumber"], "2")
		#self.mocker.verify()
                
	def testRetrieveAllRecipes(self):
		r = recipe.MyRecipe()
		r.get_allRecipe('recipe/')
		
	def testRetrieveRecipeBasedOnID(self):
		pass
        
	

if __name__ == '__main__':
        
	unittest.main()

	
        suite0 = unittest.TestLoader().loadTestsFromTestCase(MyReqTests)
        unittest.TextTestRunner(verbosity=99).run(suite0)

        import testoob
        from testoob.reporting import HTMLReporter
        testoob.main(html='D:\\PI2.2Iteration\\PythonRestClientRequest\\restRequests.html',xml='D:\\PI2.2Iteration\\PythonRestClientRequest\\restRequests.xml')
        #testoob.main(suite0)


	"""
	suite.addTests([
			unittest.TestLoader().loadTestsFromTestCase(cMSHParseTest),
			unittest.TestLoader().loadTestsFromTestCase(dPIDParseTest),
			unittest.TestLoader().loadTestsFromTestCase(ePVParseTest),
			unittest.TestLoader().loadTestsFromTestCase(fEVNParseTest),
			])

        """


        """
        suite = unittest.TestSuite()
	suite = unittest.TestLoader().loadTestsFromTestCase(MyReqTests)
	unittest.TextTestRunner(verbosity=2).run(suite)
	runtime = time.strftime("%Y%m%d%H%M%S")
	#outfile = open("D:\\MedicalDevices\\AlconProject\\Testing\\FinalTestScripts\\Reports\\ADTReport" + runtime + ".html", "w")
	#outfile = open(script_path + "\\Reports\\ADTReport" + runtime + ".html", "w")
	outfile = open("D:\\PI2.2Iteration\\PythonRestClientRequest\\restRequests.html", "w")
	
	runner = HTMLTestRunner.HTMLTestRunner(
				stream=outfile,
				title='Retrieve Recipe Test Report ',
				description='This demonstrates the Retrieve Recipe Report run at ' + runtime
				)
	runner.run(suite)
	outfile.close()
        """










        
	
	
