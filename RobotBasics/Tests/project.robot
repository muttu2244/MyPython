*** Settings ***
Documentation                                       This is a basic test
#Extrnal Library  for UI
Library                                             Selenium2Library

#Extrnal Library  for GUI Automation / KeyPress Simulator Library
Library                                             ImageHorizonLibrary

#Custom Libraries  for Backend
Library                                             RetrieveRecipe.py
Library                                             Recipe.py

#Extrnal Library  for Backend
Library                                             RequestsLibrary

#Custom Library  for Database
Library                                             GetDataFromDB.py
Library                                             DatabaseLibrary

#Inbuilt Library  for handling python Lists and Dictionaries
Library                                             Collections

#Standard Libraries
Library                                             String
Library                                             BuiltIn

#Library                                             MyMaths  10  20
#Library                                             GetDataFromDB.py  ${recipeName}  "10.2.235.128"  "recipe"  "sa"  "Merck123!" WITH NAME GD1


*** Variables ***
${Browser}                                          chrome
#${URL}                                             https://www.airbnb.co.nz
${FrontEndURL}                                      http://localhost:5000
${recipeName}                                       RecipeAuto
${BackEndURL}                                       http://localhost:8133/recipe/
${NewRecipeName}

#${SYSLOG}                                          %{TEMPDIR}${/}syslog.txt
#${versionNum}                                      Evaluate                    random.sample(range(1, 9), 1)  random
#$RecipeBackEndObj                                  RetrieveRecipe()
#set global variable                                ${recipeName}
#${recipeName}                                      Generate Random String      8       [LOWER]




*** Test Cases ***
Testing Recipe Front End
    [Documentation]                                 As a user i can test the Recipe Editor
    #Set Environment Variable                        ROBOT_SYSLOG_FILE    ${SYSLOG}
    #open browser                                    https://www.airbnb.co.nz   chrome
    [Tags]                                          Recipe FrontEnd
    open browser                                    ${FrontEndURL}      ${Browser}

    #set selenium timeout                            6
    maximize browser window
    wait until page contains                        Recipe Editor
    #close browser
    click element                                   xpath=//select[@id="actionDropDown"]
    click element                                   xpath=//*[@id="actionDropDown"]/option[3]
    click element                                   xpath=//*[@id="row1col2"]
    click element                                   xpath=//*[@id="criteriaList"]
    click element                                   xpath=//*[@id="criteriaList"]/option[2]
    click element                                   xpath=//*[@id="containerButtons"]/button[1]
    click element                                   xpath=//*[@id="row1col3"]
    click element                                   xpath=//*[@id="row1col3"]/select/option[2]
    click element                                   xpath=//*[@id="row1col4"]
    click element                                   xpath=//*[@id="criteriaList"]/option[2]
    click element                                   xpath=//*[@id="containerButtons"]/button[1]
    click element                                   xpath=//*[@id="row1col8"]
    click element                                   xpath=/html/body/div[2]/div/div[2]/div/form/input[2]
    input text                                      xpath=/html/body/div[2]/div/div[2]/div/form/input[2]  Automated
    click element                                   xpath=//*[@id="buttonContainer"]/button[1]
    click element                                   xpath = //*[@id="root"]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/input
    set selenium implicit wait                      2
    #close window
    #CHOOSE OK ON NEXT CONFIRMATION
    #dismiss alert
    #Click Button    css=input[type="submit"]
    #Alert Should Be Present
    #Get Alert Message
    #set selenium timeout                            6
    #pyautogui.keyDown                               "Alt"
    press combination                               Key.alt
    press combination                               Key.space
    press combination                               Key.c
    set selenium implicit wait                      2
    press combination                               Key.c
    press combination                               Key.space
    press combination                               Key.alt


    #input text                                      xpath = //*[@id="root"]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/input  "RecipeAuto"
    #set selenium timeout                            5
    #input text                                      xpath=//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/input     1
    #set selenium timeout                            5
    #click element                                   xpath=//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div/button

    set selenium timeout                            10
    press combination                               Key.esc

    set selenium timeout                            10
    press combination                               Key.esc



    ${recipeName}                                   Generate Random String      8       [LOWER]
    Log To Console                                  "This is the recipe Name: ${recipeName}"
    set global variable                             ${NewRecipeName}            ${recipeName}

    input text                                      xpath = //*[@id="root"]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[1]/input  ${recipeName}
    set selenium timeout                            5
    #${versionNum}  generate random and unique numbers
    #call method                                      print  ${versionNum}

    set selenium timeout                            10
    press combination                               Key.esc


    input text                                      xpath=//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div/div[1]/div[2]/div[2]/input  1
    set selenium timeout                            5
    click element                                   xpath=//*[@id="root"]/div/div/div[2]/div[2]/div[2]/div/button


Testing RetrieveRecipeBasedOnName
    [Documentation]                                         User can test the RetrieveRecipeBasedOnName
    [Tags]                                                  Recipe Backend

    open browser                                            ${BackEndURL}${NewRecipeName}       ${Browser}
    #import library                                  RetrieveRecipe.py  ${NewRecipeName}
    #import library                                 RetrieveRecipe.py   ${recipeName}   WITH NAME   RR2
    #RR2.Test Retrieve Recipe Based On Name
    #${RetrieveRecipe}=  Get Library Instance  RetrieveRecipe
    #reload library  RetrieveRecipe.py
    #${status}   ${steps}    ${operationHeader}      returnOneRecipe
    ${status}   ${steps}    ${operationHeader}              testRetrieveRecipeBasedOnName       ${NewRecipeName}
    should be equal             ${status}                   200

    ${stepsValuesDict}          get from list               ${steps}                            0
    ${comment}                  get from dictionary         ${stepsValuesDict}                  comment
    should be equal             ${comment}                  Automated

    ${criteria1Value}           get from dictionary         ${stepsValuesDict}                  criteria1Value
    should be equal             ${criteria1Value}           130

    ${actionGroup}              get from dictionary         ${stepsValuesDict}                  actionGroup
    should be equal             ${actionGroup}              Analog Alarm

    ${actionDescription}        get from dictionary         ${stepsValuesDict}                  actionDescription
    should be equal             ${actionDescription}        T1001 Temperature HI Alarm

    ${criteria2Value}           get from dictionary         ${stepsValuesDict}                  criteria2Value
    should be equal             ${criteria2Value}           130

    ${criteria2Code}            get from dictionary         ${stepsValuesDict}                  criteria2Code
    should be equal             ${criteria2Code}            TI001 Temperature

    ${booleanOperator}          get from dictionary         ${stepsValuesDict}                  booleanOperator
    should be equal             ${booleanOperator}          OR

    ${criteria1Code}            get from dictionary         ${stepsValuesDict}                  criteria1Code
    should be equal             ${criteria1Code}            TI001 Temperature

    ${actionValue}              get from dictionary         ${stepsValuesDict}                  actionValue
    should be equal             ${actionValue}              130

    ${stepNumber}               get from dictionary         ${stepsValuesDict}                  stepNumber
    should be equal             ${stepNumber}               1

    ${description}              get from dictionary         ${operationHeader}                  description
    should be equal             ${description}              Sample recipe for system demo

    ${machineName}              get from dictionary         ${operationHeader}                  machineName
    should be equal             ${machineName}              XMO4

    ${recipeVersion}            get from dictionary         ${operationHeader}                  recipeVersion
    should be equal             ${recipeVersion}            V1

    ${deviceID}                 get from dictionary         ${operationHeader}                  deviceID
    should be equal             ${deviceID}                 1001

    #${lastSavedOn}             get from dictionary     ${operationHeader}
    #should be equal            ${lastSavedOn}

    ${productIdentification}    get from dictionary         ${operationHeader}                  productIdentification
    should be equal             ${productIdentification}    System Demo

    ${recipeName}               get from dictionary         ${operationHeader}                  recipeName
    should be equal             ${recipeName}               ${NewRecipeName}


Testing Retrieving All Recipes
    [Documentation]                                         User can test the Retrieving All Recipes
    [Tags]                                                  Recipe Backend

    open browser                ${BackEndURL}               ${Browser}
    testRetrieveAllRecipes
    #testAdd

Testing the DataBase
    [Documentation]                                         User can test the database
    [Tags]                                                  DataBase
    #import library  GetDataFromDB.py  ${NewRecipeName}  "10.2.235.128"  "recipe"  "sa"  "Merck123!"
    readData                                                ${NewRecipeName}  10.2.235.128  sa  Merck123!   recipe
    #connect to database         "MySQLdb"    "recipe"    "sa"    "Merck123!"     "10.2.235.128"   8133    "None"
    #connect to database     "pymssql"       "recipe"    "sa"    "Merck123!"     "10.2.235.128"   1433    "None"
    #connect to database using custom params  database, user, Password, host and port
#Testing the simple http requests
#    [Documentation]                                 User can test the database
#    [Tags]                                          Recipe Backend

    #${result} =                                     get  http://echo.jsontest.com/framework/robot-framework/api/rest
    #Should Be Equal                                 ${result.status_code}          ${200}

*** Keywords ***
    #test Add

    #testRetrieveRecipeBasedOnName
    #testRetrieveAllRecipes
    #set global variable                                  ${recipeName}
#returnOneRecipe
#    ${v1}   testRetrieveRecipeBasedOnName                   ${NewRecipeName}
#    ${v2}   testRetrieveRecipeBasedOnName                   ${NewRecipeName}
#    ${v3}   testRetrieveRecipeBasedOnName                   ${NewRecipeName}

#    [Return]                                                ${v1}   ${v2}   ${v3}

