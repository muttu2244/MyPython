import pymssql,os

import pandas as pd
import json
import ast #convert-a-string-representation-of-a-dictionary-to-a-dictionary
class GetDataFromDB():
    '''
    def __init__(self,recipeName,host,user,pwd,db):
        self.recipeName = str(recipeName)
        self.host = host
        self.db = db
        self.user = user
        self.pwd = pwd
        #self.db_connection = sql.connect(self.host, self.user, self.pwd, self.db)
        print "\n###########################################"
        print "The recipe Name is : \n\n %s" % self.recipeName
        print "\n###########################################"
    '''
    def readData(self,recipeName,host,user,pwd,db):
        self.recipeName = str(recipeName)
        self.host = host
        self.db = db
        self.user = user
        self.pwd = pwd
        print "\n###########################################"
        path = os.path.abspath(pymssql.__file__)
        print path
        print self.host
        print self.db
        print self.user
        print self.pwd
        print "The recipe Name is : \n\n %s" % self.recipeName
        print "\n###########################################"
        self.db_connection = pymssql.connect(self.host, self.user, self.pwd, self.db)
        #db_connection = sql.connect(host, user, pwd, db)

        self.cursor = self.db_connection.cursor()
        #self.cursor.execute("SELECT * FROM recipe_table where recipe_name=%s"%self.recipeName)
        #self.cursor.execute('SELECT * FROM recipe_table where recipe_name="RecipeAuto"')
        self.cursor.execute("SELECT recipe FROM recipe_table where recipe_name=%s", self.recipeName)
        #print self.cursor
        #self.ExeQuery = pd.read_sql("SELECT * FROM table_name" , con=self.db_connection)
        self.myData = self.cursor.fetchall()
        recipeDict = self.myData[0][0]
        dictAfterRemovingUnicode = recipeDict.decode('unicode_escape').encode('ascii', 'ignore')
        dictAfterStringtoDictConversion = ast.literal_eval(dictAfterRemovingUnicode)
        for key, value in dictAfterStringtoDictConversion.items():
            #print key
            #print value
            recipe = key
            '''
            for k, v in value.items():
                print k
                print v
            '''
            operationHeader = value['operationHeader']
            steps = value['steps'][0]
            print operationHeader
            print steps

        operationHeaderComment = operationHeader['comment']
        description = operationHeader['description']
        machineName = operationHeader['machineName']
        recipeVersion = operationHeader['recipeVersion']
        deviceId = operationHeader['deviceID']
        lastSavedBy = operationHeader['lastSavedBy']
        lastSavedOn = operationHeader['lastSavedOn']
        prodIdentification  = operationHeader['productIdentification']
        recipeName = operationHeader['recipeName']
        stepsComment = steps['comment']
        crieteria1Value = steps['criteria1Value']
        actionGroup = steps['actionGroup']
        actionDescription = steps['actionDescription']
        criteria2Operator = steps['criteria2Operator']
        criteria2Value = steps['criteria2Value']
        criteria2Code  = steps['criteria2Code']
        booleanOperator = steps['booleanOperator']
        criteria1Operator = steps['criteria1Operator']
        parameterTab = steps['parameterTab']
        label = steps['label']
        parameterScope = steps['parameterScope']
        criteria1Code = steps['criteria1Code']
        phase = steps['phase']
        actionValue = steps['actionValue']
        stepNumber = steps['stepNumber']
        
        print operationHeaderComment
        print description
        print machineName
        print recipeVersion
        print deviceId
        print lastSavedBy
        print lastSavedOn
        print prodIdentification
        print recipeName
        print stepsComment
        print crieteria1Value
        print actionGroup
        print actionDescription
        print criteria2Operator
        print criteria2Value
        print criteria2Code
        print booleanOperator
        print criteria1Operator
        print parameterTab
        print label
        print parameterScope
        print criteria1Code
        print phase
        print actionValue
        print stepNumber


        #self.df = pd.DataFrame(self.myData)
        #self.FileData = json.dumps(self.myData)
        #for item in self.cursor:
        #print type(self.FileData)
        '''
        self.recipeDataFile = 'C:\\Users\\x188694\\PycharmProjects\\RobotBasics\\Tests\\recipeData.txt'
        self.f = open(self.recipeDataFile, 'w')
        self.f.write(self.FileData)
        self.f.close()
        #return self.df
        '''
        return (machineName,recipeVersion,deviceId,recipeName,stepsComment,crieteria1Value,actionGroup,criteria2Value,booleanOperator)

if __name__ == '__main__':
    #readObj = GetDataFromDB("RecipeAuto","10.2.235.128", "sa", "Merck123!", "recipe")
    readObj = GetDataFromDB()
    readObj.readData("RecipeAuto","10.2.235.128", "sa", "Merck123!", "recipe")
    #dataFrames = readObj.readData()
    #print dataFrames
