Software Requirements:

1) Windows OS

2) Python 2.7.12

3) USB Drivers for all the Android Devices 

4) SeeTest Automation tool 10.3.71

5) pycharm-edu-3.0.1 (Editor)

6) ITunes 12.5.3.16 for the IOS Devices

7) XDEF Profile files for the IOS Devices

8) Contour App Ver: 1.9.44r

Initial Setup:

1) Make sure that the Host PC with Windows OS has USB ports as well as Admin access.

2) Install SeeTest Automation tool on the Host PC.

3) Install Python, PyCharm and ITunes on the Host PC.

4) Install USB drivers on the PC for all the required devices.

5) Connect the DUT using USB dongle to Host PC via USB port.

6) For the IOS Devices do the “IOS Code Signing Configuration” using the IOS Profile Management on the “SeeTest---- > Tools ---- > IOS Profile Management”

7) Update the language.ini with "english" language

8) Select English language from Settings--> Country and Language (Script to auto select the language is under implementation)

9) Once the Suite is complete, replace "english" in the language.ini with "german" language

10) Select German language from Settings--> Country and Language (Script to auto select the language is under implementation)

11) If a new language is (other than english and german) has been introduced/supported completely, we need to update all the language xml files present in the LTPScripts folder. Example - CountryLTP.xml. Currently the language xml files only have English and German strings. To add new language strings run the script "ExtractStringFromXML.py". This script is present under LTP_package/Misc_scripts/.

Usage: 
	a. Open the script in any editor, uncomment the language inside "dump1" method(English and German are already uncommented)
	b. Modify the "system_map" variable to point to the location of the language xml file.
	c. Modify the "path" to point to the location where the Master string xml is present.
	d. Modify the line "tree.write("D:\\LTP-2.0\\" + file_name + "String.xml")" to a location where you need to have a generated xml.
	e. Rename the master string xml files as "English.xml", "German.xml", Spanish.xml" etc before the script is executed

Run: python <path to ExtractStringFromXML script>\ExtractStringFromXML.py 

Output: This script generates an xml file with the language strings that user wanted. Using the id, copy the language xml tags to the language xml files(example - CountryLTP.xml) that are present in LTPScripts folder.

Steps to run LTP script:
 	1) Unzip the folder to Target, which creates the 	"LTP_suite_integrated" Folder.
 
	2) Check python path is in Environment Variable.
	
	3) Please use below link for that.
	(http://stackoverflow.com/questions/3701646/how-to-add-	  to-the-pythonpath-in-windows-7

 	4) Open command Prompt and navigate to 		 		 	"LTP_suite_integrated/LTPScripts" Folder.

 	5) Run the suite using "python LTPTestSuite.py" command/Select the LTPTestSuite.py in Pycharm project and run(Using Pycharm preferred as command prompt does not support few unicode characters.


	6)  To run individual scripts: Type python scriptname.py
		eg. 	python EditEntry.py
	    		python SmartRemindersLTP.py
	    		
	
	7) Logs will be generated in Logs folder having with format --> <scriptname><language><timestamp>.log.
	
	8) Reports will be generated in Reports folder with test 		folder name locate index.html in test folder having 		highest number.
	
To view UML class Diagrams:

1. Unzip "pyNsource-1.61-win32-standalone.zip" from the package
2. Launch "pyNsourceGui.exe" 
3. Click File --> Open and select the ".pyns" file from "LTP_package\uml_diagrams" location.
