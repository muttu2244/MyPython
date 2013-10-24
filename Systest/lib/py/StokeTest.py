#!/usr/bin/env python2.5
#######################################################################
#
# Copyright (c) Stoke, Inc.
# All Rights Reserved.
#
# This code is confidential and proprietary to Stoke, Inc. and may only
# be used under a license from Stoke.
#
#######################################################################

### std python
from logging import getLogger
import sys
import re
import os
import time
import datetime
import traceback
from unittest import makeSuite, TestCase, TestSuite, TextTestRunner
from unittest import _TextTestResult, TestResult, _WritelnDecorator
### local libs
from helpers import timestamp
import pexpect	#Venkat
from log import  *
import commands

log = getLogger()

class text_test_result(_TextTestResult):
    """A test result class that can print formatted text results to a stream.  This is
    a subclass of _TextTestResult to alter result output.

    Used by test_runner.
    """
    #print wasSuccessful()
    def ssxVersion(self, test):
	self.stream.writeln("SSX_VERSION")

    def addSuccess(self, test):
        """When a successful result is written in the superclass, it's result
        is described as ok.  Here we're altering it to write out 'PASS'.
        """
        TestResult.addSuccess(self, test)
        if self.showAll:
            self.stream.writeln("PASS")
        elif self.dots:
            self.stream.write('.')
        log.result("#" * 50)
        log.result("%s: PASS" % test._testMethodName)
        print "%s: PASS" % test._testMethodName
        log.result("#" * 50)

    def addError(self, test, err):
        TestResult.addError(self,test, err)
        file_name =  getattr(self.stream,"name")
        if self.showAll:
            self.stream.writeln("ERROR")
        elif self.dots:
            self.stream.write('E')
        error = TestResult._exc_info_to_string(self,err,test)
        log.error("#" * 50)
        log.error("%s errored out." % test._testMethodName)
        if "setUp" in test._testMethodName:
            print "Testsuite  aborted in setUp itself."
        log.error("#" * 50)
        if "stdout" not in file_name:
                log.error("\n\n%s"%error)

    def addFailure(self, test, err):
        TestResult.addFailure(self,test, err)
        file_name =  getattr(self.stream,"name")
        if self.showAll:
            self.stream.writeln("FAIL")
        elif self.dots:
            self.stream.write('F')
        failure = TestResult._exc_info_to_string(self,err,test)
        log.result("#" * 50)
        log.result("%s: FAIL" % test._testMethodName)
        print "%s: FAIL" % test._testMethodName
        log.result("#" * 50)
        if "stdout" not in file_name:
                log.result("\n\n%s"%failure)

class test_case(TestCase):
    """Our subclass for unittest's TestCase."""
    suite = None
    

    def run(self, result=None):
        log.test("#" * 50)	#Venkat
	python_version=pexpect.run('python -V')	#Venkat
        log.test("Python Version: %s" % python_version.strip())#Venkat
        log.test("#" * 50)	#Venkat
        log.test("#" * 50)
        log.test(self._testMethodName)
        log.test("#" * 50)
        TestCase.run(self, result)


def _strclass(cls):
    return "%s.%s" % (cls.__module__, cls.__name__)

class test_suite(TestSuite):
    """A test suite is a composite test consisting of a number of test cases.

    For use, create an instance of test_suite, then add test case instances.
    When all tests have been added, the suite can be passed to a test
    runner, such as test_runner. It will run the individual test cases
    in the order in which they were added, aggregating the results. When
    subclassing, do not forget to call the base class constructor.
    """
    main_dict = {}
    pass_count = 0
    fail_count = 0
    error_count = 0
    total_time = 0
    suite_start_time = 0
    suite_end_time = 0
    def __init__(self, tests=()):
	self.flags = {}
        if tests:
            TestSuite.__init__(self, tests)
        else:
            TestSuite.__init__(self)

    def setUp(self):
        """Hook method for setting up the test suite environment before
        executing it.
        """
        #Vself.suite_start_time = str(time.asctime().split(" ")[3]) 
        self.suite_start_time = str(str(time.time()).split(".")[0])
        pass

    def tearDown(self):
        """Hook method for deconstructing the test suite environment after
        testing it.
        """
        #Vself.suite_end_time = str(time.asctime().split(" ")[3])
        try:
            self.suite_end_time = str(str(time.time()).split(".")[0])
            self.total_time = self.difftime(self.suite_end_time, self.suite_start_time) 
            pass_percent = (float(self.pass_count) / len(self.main_dict)) * 100 
            suite_name = sys.argv[0].split(".")[0].strip()
            mail_file = sys.argv[0].split("/")[-1].replace('.py','-%s.mail'%str(time.time()).split(".")[0])
            try:
                mail_fd = open(mail_file, 'w')
            except:
                return
    
            mail_fd.write("\n")
            mail_fd.write("=" * 150)
            mail_fd.write("\n\n")
            hr,min,sec = self.total_time.split(":")
            mail_fd.write("Total test time: %s Hours %s Minutes %s seconds\n\n"% (hr,min,sec))
            mail_fd.write("Test Pass/Fail/Error summary:\n")
            mail_fd.write("\t%-30s%+5s\n"%("Total Test Case Run:",len(self.main_dict)))
            mail_fd.write("\t%-30s%+5s\n"%("Total Test Case Passed:",self.pass_count))
            mail_fd.write("\t%-30s%+5s\n"%("Total Test Case Failed:",self.fail_count))
            mail_fd.write("\t%-30s%+5s\n"%("Total Test Case Errored:",self.error_count))
            mail_fd.write("\t%-30s%+5s%%\n"%("Test pass percentage:",pass_percent))
            pwd = commands.getoutput("pwd")
            pwd = pwd.strip("\r")
            mail_fd.write("\t%-30s%s/%s\n\n"%("Execution logs:",pwd,get_log_file()))
            build = commands.getoutput("grep -ria \"StokeOS release\" %s | tail -1"%get_log_file())
            build = build.strip("\r")
            py_version = commands.getoutput("grep -ari \"python version\" %s | tail -1"%get_log_file())
            py_version = py_version.split(":")[-1].strip("\r")
            mail_fd.write("\t%-30s%+5s\n"%("Build Tested:",build))
            mail_fd.write("\t%-30s%+5s\n\n"%("Python Version:",py_version))
            print("-" * 150)
            mail_fd.write("-" * 150)
            mail_fd.write("\n")
            mail_fd.write("%50s"%"Individual Test Results Summary")
            mail_fd.write("\n")
            mail_fd.write("-" * 150)
            mail_fd.write("\n")
            mail_fd.write("%-35s\t%-80s\t\t%-12s\t%-5s\n\n"%("Test Name","Test Summary","Exec.Time","P/F/E"))
            for (mKey, mVal) in self.main_dict.iteritems():
                temp_desc = mVal['tc_desc']
                mail_fd.write("%-35s\t%-80s\t\t%-12s\t%-5s\n\n"%(mVal['tc_name'],temp_desc[:80],mVal['tc_run_time'],mVal['tc_result']))
            mail_fd.write("\n")
            mail_fd.write("-" * 150)
            mail_fd.close()
            os.system("/bin/mail -s \"Execution Status for Suite: %s\" -c krao@stoke.com %s@stoke.com < %s"%(suite_name,os.environ['USER'],mail_file))
        except:
            #Probably we're running suite.
            pass
        pass

    def addTest(self, test):
        """Add a test to the test suite object."""
        self._tests.append(makeSuite(test))
	test.suite = self

    def addTests(self, tests):
        """Add a series of tests to a test suite object.  Requires a list
        or tuple.
        """
        for test in tests:
            self._tests.append(makeSuite(test))
	    test.suite = self
    def printCases(self):
        print self._tests

    def difftime(self,eTime,sTime):
        diff_seconds = int(eTime) - int(sTime)
        hms  = str(datetime.timedelta(seconds=diff_seconds))
        hr0,min0,sec0 = hms.split(":")
        hr0,min0,sec0 = int(hr0),int(min0),int(sec0)
        return "%02d:%02d:%02d"%(hr0,min0,sec0)



    def run(self, result):
        """First run the setUp method.  Then execute the tests.  Then run
        the tearDown method.
        """
        try:
            try:
                self.setUp()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, self._exc_info())
                return
            failures = 1
            errors = 1
            for test in self._tests:
                
                if result.shouldStop:
                    break
                if isinstance(test, test_case):
                    log.test(str(test))
                suit_dict = {}
                #print "Executing the Test %s"%test
                str_test = str(test)
                try:
                    tc_name = re.search("\[\<([0-9A-Za-z_]+)\.",str_test)
                    tc_name = tc_name.group(1)
                    if tc_name == "__main__":
                        tc_name = sys.argv[0].split("/")[-1].split(".")[0]
                    suit_dict['tc_name'] = tc_name
                    current_path = str(os.getcwd())
                    if current_path.split("/")[-1] == "Logs":
                        file_1 = "/".join(current_path.split("/")[0:-1])
                        file_2 = "/".join(sys.argv[0].split("/")[0:-1])
                        file = file_1 + "/" + file_2 + "/" + tc_name + '.py'
                    else:
                        file = sys.argv[0]

                    desc = pexpect.run('grep -ri -m 1 "Description\s*:" %s' %file)
                    #print("desc = %s"%desc)
                    if len(desc):
                        desc = desc.split(":")[1].strip("\n").strip("\r").strip()
                    else:
                        desc = "No Description Specified"
                    suit_dict['tc_desc'] = desc
                    start_time = str(str(time.time()).split(".")[0])
                    suit_dict['tc_start_time'] = start_time
                    res = test(result)
                    end_time = str(str(time.time()).split(".")[0])
                    suit_dict['tc_end_time'] = end_time
                    tc_run_time = self.difftime(end_time, start_time)
                    suit_dict['tc_run_time'] = tc_run_time
                    res = str(res)
                    temp_result = re.search("failures=([0-9]+)", res)
                    temp_error =  re.search("errors=([0-9]+)", res)
                    temp_result = int(temp_result.group(1))
                    temp_error = int(temp_error.group(1))
                    if (temp_result == failures) :
                        tc_result = "F"
                        failures = failures + 1
                        self.fail_count = self.fail_count + 1
                    elif (temp_error == errors) :
                        tc_result = "E"
                        errors = errors + 1
                        self.error_count = self.error_count + 1
                    else:
                        tc_result = "P"
                        self.pass_count = self.pass_count + 1
                    suit_dict['tc_result'] = tc_result
                    self.main_dict[tc_name] = suit_dict
                except:
                    #Some Issue and we cannot generate mail file
                    pass 
            try:
                self.tearDown()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, self._exc_info())
                ok = False
        finally:
            result.stopTest(self)
        return result



class test_suite_failfast(TestSuite):
    """A test suite is a composite test consisting of a number of test cases.

    For use, create an instance of test_suite, then add test case instances.
    When all tests have been added, the suite can be passed to a test
    runner, such as test_runner. It will run the individual test cases
    in the order in which they were added, aggregating the results. When
    subclassing, do not forget to call the base class constructor.
    Execution will stopped if one testcase fails in between
    """

    def __init__(self, tests=()):
        self.flags = {}
        if tests:
            TestSuite.__init__(self, tests)
        else:
            TestSuite.__init__(self)

    def setUp(self):
        """Hook method for setting up the test suite environment before
        executing it.
        """
        pass

    def tearDown(self):
        """Hook method for deconstructing the test suite environment after
        testing it.
        """
        test_variable = 1
        pass

    def addTest(self, test):
        """Add a test to the test suite object."""
        self._tests.append(makeSuite(test))
        test.suite = self

    def addTests(self, tests):
        """Add a series of tests to a test suite object.  Requires a list
        or tuple.
        """
        for test in tests:
            self._tests.append(makeSuite(test))
            test.suite = self

    def run(self, result):
        """First run the setUp method.  Then execute the tests.  Then run
        the tearDown method.
        """
        try:
            try:
                self.setUp()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, self._exc_info())
                return

            for test in self._tests:

                if result.shouldStop:
                    break
                if isinstance(test, test_case):
                    log.test(str(test))
                res = test(result)
                if not res.wasSuccessful():
                    res.shouldStop = True
                    res.stop()
                    break
                #print result.wasSuccessful()
            try:
                self.tearDown()
            except KeyboardInterrupt:
                raise
            except:
                result.addError(self, self._exc_info())
                ok = False
        finally:
            result.stopTest(self)
        return result


class run_all_cases_failfast(TestSuite):
    """
    Description -       1. This class is to be used when user wants to run either all of the testcases or set of
                           testcases written in a single testcase class.
                        2. Testcase function names should start with "test_".
                        3. Run method starts with the setUp() and ends with tearDown() by default and hence expects the defs
                           for setUp and tearDown inside the testcase class.
                        4. When no list is provided it runs all the testcases.
                        5. Execution will be stopped if one testcase fails in between

    Arguments -         test case class and list of tests to run

    Examples -          1. To run all the test cases.
                           suite = run_all_cases(test_case_calss)
                           test_runner().run(suite)
                        2. To run set of  test cases.
                           test_case_list = ('test_FUN_001','test_FUN_002','test_FUN_003')
                           suite = run_all_cases(test_case_calss,test_case_list)
                           test_runner().run(suite)

    """

    failureException = AssertionError
    testMethodPrefix = 'test'
    sortTestMethodsUsing = cmp
    suiteClass = TestSuite
    testMethodPrefix = 'test'
    sortTestMethodsUsing = cmp
    suiteClass = TestSuite


    def __init__(self,test_class,test_case_list = None):
        self.flags = {}
        self._test_class = test_class
        if test_case_list:
                self._tests = test_case_list
        else:
                self._tests = self.getTestCaseNames(test_class)

    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """
        def isTestMethod(attrname, testCaseClass=testCaseClass, prefix=self.testMethodPrefix):
            return attrname.startswith(prefix) and callable(getattr(testCaseClass, attrname))
        testFnNames = filter(isTestMethod, dir(testCaseClass))
        for baseclass in testCaseClass.__bases__:
            for testFnName in self.getTestCaseNames(baseclass):
                if testFnName not in testFnNames:  # handle overridden methods
                    testFnNames.append(testFnName)
        if self.sortTestMethodsUsing:
            testFnNames.sort(self.sortTestMethodsUsing)
        return testFnNames

    def setUp(self):
        """Hook method for setting up the test suite environment before
        executing it.
        """
        pass

    def tearDown(self):
        """Hook method for deconstructing the test suite environment after
        testing it.
        """
        pass

    def addTest(self, test):
        """Add a test to the test suite object."""
        self._tests.append(test)
        test.suite = self

    def addTests(self, tests):
        """Add a series of tests to a test suite object.  Requires a list
        or tuple.
        """
        for test in tests:
            uest.suite = self

    def shortDescription(self):
        """Returns a one-line description of the test, or None if no
        description has been provided.
        """
        pass

    def _exc_info(self):
        """Return a version of sys.exc_info() with the traceback frame
           minimised; usually the top level of the traceback frame is not
           needed.
        """
        exctype, excvalue, tb = sys.exc_info()
        if sys.platform[:4] == 'java': ## tracebacks look different in Jython
            return (exctype, excvalue, tb)
        return (exctype, excvalue, tb)

    def run(self, result):
        """First run the setUp method.  Then execute the tests.  Then run
        the tearDown method.
        """
        try:
            try:
                instance = self._test_class("setUp")
                setup_method = getattr(instance,"setUp")
                self._testMethodName = "setUp"
                setup_method()
            except KeyboardInterrupt:
                raise
            except self.failureException:
                result.addFailure(self, self._exc_info())
            except:
                result.addError(self, self._exc_info())
                return
            for test in self._tests:
                try:
                        log.test(str(test))
                        if not result.wasSuccessful():
                            result.stop()
                            break
                        result.startTest(test)
                        test_method = getattr(instance,test)
                        self._testMethodName = test
                        test_method()
                        result.addSuccess(self)
                        if not result.wasSuccessful():
                            result.stop()
                            break
                except KeyboardInterrupt:
                        raise
                except self.failureException:
                        result.addFailure(self, self._exc_info())
                except:
                        result.addError(self, self._exc_info())
            try:
                tear_down = getattr(instance,"tearDown")
                self._testMethodName = "tearDown"
                tear_down()
            except KeyboardInterrupt:
                raise
            except self.failureException:
                result.addFailure(self, self._exc_info())
            except:
                result.addError(self, self._exc_info())
                ok = False
        finally:
            result.stopTest(self)









     
class run_all_cases(TestSuite):
    """
    Description -       1. This class is to be used when user wants to run either all of the testcases or set of
                           testcases written in a single testcase class.
                        2. Testcase function names should start with "test_".
                        3. Run method starts with the setUp() and ends with tearDown() by default and hence expects the defs
                           for setUp and tearDown inside the testcase class.
                        4. When no list is provided it runs all the testcases.

    Arguments -         test case class and list of tests to run

    Examples -          1. To run all the test cases.
                           suite = run_all_cases(test_case_calss)
                           test_runner().run(suite)
                        2. To run set of  test cases.
                           test_case_list = ('test_FUN_001','test_FUN_002','test_FUN_003')
                           suite = run_all_cases(test_case_calss,test_case_list)
                           test_runner().run(suite)

    """

    failureException = AssertionError
    testMethodPrefix = 'test'
    sortTestMethodsUsing = cmp
    suiteClass = TestSuite
    testMethodPrefix = 'test'
    sortTestMethodsUsing = cmp
    suiteClass = TestSuite


    def __init__(self,test_class,test_case_list = None):
        self.flags = {}
        self._test_class = test_class
        if test_case_list:
                self._tests = test_case_list
        else:
                self._tests = self.getTestCaseNames(test_class)

    def getTestCaseNames(self, testCaseClass):
        """Return a sorted sequence of method names found within testCaseClass
        """
        def isTestMethod(attrname, testCaseClass=testCaseClass, prefix=self.testMethodPrefix):
            return attrname.startswith(prefix) and callable(getattr(testCaseClass, attrname))
        testFnNames = filter(isTestMethod, dir(testCaseClass))
        for baseclass in testCaseClass.__bases__:
            for testFnName in self.getTestCaseNames(baseclass):
                if testFnName not in testFnNames:  # handle overridden methods
                    testFnNames.append(testFnName)
        if self.sortTestMethodsUsing:
            testFnNames.sort(self.sortTestMethodsUsing)
        return testFnNames

    def setUp(self):
        """Hook method for setting up the test suite environment before
        executing it.
        """
        pass

    def tearDown(self):
        """Hook method for deconstructing the test suite environment after
        testing it.
        """
        pass

    def addTest(self, test):
        """Add a test to the test suite object."""
        self._tests.append(test)
        test.suite = self

    def addTests(self, tests):
        """Add a series of tests to a test suite object.  Requires a list
        or tuple.
        """
        for test in tests:
            uest.suite = self

    def shortDescription(self):
        """Returns a one-line description of the test, or None if no
        description has been provided.
        """
        pass

    def _exc_info(self):
        """Return a version of sys.exc_info() with the traceback frame
           minimised; usually the top level of the traceback frame is not
           needed.
        """
        exctype, excvalue, tb = sys.exc_info()
        if sys.platform[:4] == 'java': ## tracebacks look different in Jython
            return (exctype, excvalue, tb)
        return (exctype, excvalue, tb)

    def run(self, result):
        """First run the setUp method.  Then execute the tests.  Then run
        the tearDown method.
        """
        try:
            try:
                instance = self._test_class("setUp")
                setup_method = getattr(instance,"setUp")
                self._testMethodName = "setUp"
                setup_method()
            except KeyboardInterrupt:
                raise
            except self.failureException:
                result.addFailure(self, self._exc_info())
            except:
                result.addError(self, self._exc_info())
                return
            for test in self._tests:
                try:
                        log.test(str(test))
                        result.startTest(test)
                        test_method = getattr(instance,test)
                        self._testMethodName = test
                        test_method()
                        result.addSuccess(self)
                except KeyboardInterrupt:
                        raise
                except self.failureException:
                        result.addFailure(self, self._exc_info())
                except:
                        result.addError(self, self._exc_info())
            try:
                tear_down = getattr(instance,"tearDown")
                self._testMethodName = "tearDown"
                tear_down()
            except KeyboardInterrupt:
                raise
            except self.failureException:
                result.addFailure(self, self._exc_info())
            except:
                result.addError(self, self._exc_info())
                ok = False
        finally:
            result.stopTest(self)

class test_runner(TextTestRunner):
    """A test runner class that displays results in textual form.

    It writes out to a file the names of tests as they are run, errors
    as they occur, and a summary of the results at the end of the test
    run.
    """


    def __init__(self,stream=None):
	if not stream:
            file_prefix = os.path.basename(sys.argv[0]).split(".")[0].replace("test_", "")
            filename = timestamp("%s_results.txt" % file_prefix)
            self.stream = _WritelnDecorator(open(filename, "a+"))
	else:
	    self.stream = _WritelnDecorator(stream)
        self.descriptions = 0
        self.verbosity = 2
    def _makeResult(self):
        
        return text_test_result(self.stream, self.descriptions, self.verbosity)

    #def run(self, suite):
    #    TextTestRunner().run(suite)
    #    self.stream.close()
