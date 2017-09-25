import Recipe
import unittest
import requests
#import requestsSuite
import HTMLTestRunner
import time
# import requestsSuite
#import HTMLTestRunner
#import recipe
#import time
#import unittest

#import requests


#class RetrieveRecipe(unittest.TestCase):
class RetrieveRecipe(object):
    #def __init__(self, recipeName):
        #recipeName = recipeName


    def testRetrieveRecipeBasedOnName(self,recipeName ):
        # Now execute my code
        r = Recipe.Recipe()
        # status, reqId = r.get_tasks('user')

        #r.get_recipeByName('recipe/%s' % recipeName)
        #r.get_recipeByName('recipe/%s' % recipeName)
        #print "\n###########################################"
        #print "The recipe Name is : \n\n %s" % recipeName
        #print "\n###########################################"



        status, steps, operationHeader = r.get_recipeByName('recipe/%s' %recipeName)
        
        #print "\n###########################################"
        #print "The recipe Status is : \n\n %s" % status
        #print "\n###########################################"
        #print "The recipe Steps is : \n\n %s" % steps
        #print "\n###########################################"
        #print "The operationHeader is :\n\n %s" % operationHeader
        #print "\n###########################################"

        # and verify the results
        '''
        assertEqual(status, 200)

        print steps[0]["actionDescription"]
        assertEqual(steps[0]["actionDescription"], "Default Flowpath")
        print steps[0]["comment"]
        assertEqual(steps[0]["comment"], "Recipe Step 1")
        print steps[0]["actionGroup"]
        assertEqual(steps[0]["actionGroup"], "Flowpath-System")
        print steps[0]["actionValue"]
        assertEqual(steps[0]["actionValue"], "1")
        print steps[0]["stepNumber"]
        assertEqual(steps[0]["stepNumber"], "1")

        assertEqual(steps[1]["actionDescription"], "XV300 Outlet F0 Close")
        assertEqual(steps[1]["comment"], "Recipe Step 2")
        assertEqual(steps[1]["actionGroup"], "Flowpath-System")
        assertEqual(steps[1]["actionValue"], "0")
        assertEqual(steps[1]["stepNumber"], "2")
        # mocker.verify()
        '''
        #return (reqStatus, recipeSteps, recipeOperationHeader)
        return (str(status), steps, operationHeader)

    def testRetrieveAllRecipes(self):
        r = Recipe.Recipe()
        r.get_allRecipe('recipe/')


if __name__ == '__main__':
    #recipeObj = RetrieveRecipe("RecipeAuto")
    recipeObj = RetrieveRecipe()
    recipeObj.testRetrieveRecipeBasedOnName("RecipeAuto")
    recipeObj.testRetrieveAllRecipes()