"""
log.py

Simple wrapper for the logging module.  Simply a place holder for
larger things to come.
"""
### std python
import sys, os
from subprocess import Popen, PIPE, call
from os.path import normpath
import logging
from string import strip
from optparse import OptionParser

### local libs
from helpers import timestamp

## Global variables
PATH_LOG_SANITY  = "/auto/labtools/test_logs/sanity"
PATH_LOG_REGRESSION = "/auto/labtools/test_logs/regression"
PATH_LOG_SOAK = "/auto/labtools/test_logs/soak"
PATH_BUILDS = "/auto/build/builder"
LOG_DIR_ENVVAR = "TEST_LOG_DIR"
log_file_name = ""

def help_message():
        print """ 
Logging Path Command Line Options:  
	--sanity 	Save log files to sanity log repository	
	--regr 		Save log files to regression log repository	
	--soak 		Save log files to soak log repository	
 	--branch=BRANCH	Type branch name. 
        --build=BUILD   Type build id. 
	--dir=DIR	Save logs to DIR. 

If the script is executed from sanity or soak directory, log files will be saved to sanity or soak repository unless specific option --dir or --reg is used. 

If no options are provided, log files will be saved to 
	1) the directory specified in the environment variable "TEST_LOG_DIR" 
	2) "Logs" under the current direcotry if ENVVAR is not set (default) 

--branch and --build are required if testlogdir is in the repository. 

Example:
	./ospf_regression_suite.py --re --br 4.6B2 
	(Build unspecified. Assuming the latest build is being used.)
	Logs files can be found in
	/auto/labtools/test_logs/regression/4.6B2/2011021901
	"""
        sys.exit(0)


def path_error(path):
	"""
	Helper function to print an error and exit when branch and/or build passed in cannot be verified exists. 
	"""
	print "ERROR: " + path + " does not exist. Please verify that you have entered the correct branch or build id." 
#	help_message()
	sys.exit(0)

def get_latest_build(branch):
	"""
	Helper function. Takes branch as the parameter, finds the latest build in the branch passed-in, and returns the build-id.
	"""
	p = Popen('ls -ltr ' + PATH_BUILDS+ '/' +branch+ '| tail -1', shell=True, stdout=PIPE)
	for line in p.stdout:
		build = strip(line.split(' ')[-1])	
	return build	

parser = OptionParser()	
parser.add_option("--sanity", action="store_true", dest="sanity", help="Save log files to sanity log repository")	
parser.add_option("--soak", action="store_true", dest="soak", help="Save log files to soak log repository")	
parser.add_option("--regression", action="store_true", dest="regression", help="Save log files to regression log repository")	
parser.add_option("--branch", action="store", type="str", dest="branch", help="Type branch name  e.g: --br 4.6B2")
parser.add_option("--build", action="store", type="str", dest="build", help="Type build ID  e.g: --bu 2011022802")
parser.add_option("--dir", dest="dir", help="Save logs to DIR. e.g: --d fridayLogs")

def frameworkOptionParser(usage):
	parser.usage = usage
	return parser

def setLogDir():
	""" 
	Set testlogdir in the following order (pri hi to lo): 
	1. Log Repository if --sanity, --regr, or --soak is used
	   Repository path: 
		/auto/labtools/test_logs/sanity/<branch>/<build-id>
		/auto/labtools/test_logs/regression/<branch>/<build-id>
		/auto/labtools/test_logs/soak/<branch>/<build-id>
	2. DIR in --dir DIR
		If --branch or --build option is used after --dir, 
                then set path to DIR/BRANCH or DIR/BUILD 
	3. Log Repository if script path is in /systest/tests/sanity or .../soak
	4. ENVVAR TEST_LOG_DIR 
	5. Default: Logs in current working directory
	"""
	(options, args) = parser.parse_args()
	

	# 1. If --sanity, --regression, or --soak are used, send logs to the repository
	if options.sanity or options.regression or options.soak:
		if not options.branch:
			print "ERROR: branch is missing"
			print "Please enter the branch name. e.g: --br 4.6B2"
			exit(0)
		
		br = options.branch	
		print "Branch: " + br 
		brpath = os.path.join(PATH_BUILDS, br)

		## Check if the branch passed in is valid	
		if not os.path.exists(brpath):
			path_error(brpath)	
		
		## Get build-id from the argument in --build option
		if options.build:	
			bld = options.build 
		## Use lastest build if --build option is not used 
		else: 
			print "(Build unspecified. Assuming the latest build is being used.)"
			bld = get_latest_build(br)
		print "Build:  " + bld
		bldpath = os.path.join(brpath,bld)

		## Check if the build is valid
		if not os.path.exists(bldpath):
			path_error(bldpath)
		
		## Build log path	
		if parser.has_option("--sanity"):
			cdDir(PATH_LOG_SANITY)
			cdDir(br)
			cdDir(bld)
		elif parser.has_option("--regr"):
			cdDir(PATH_LOG_REGRESSION)
			cdDir(br)
			cdDir(bld)
		elif parser.has_option("--soak"):
			cdDir(PATH_LOG_SOAK)
			cdDir(br)
			cdDir(bld)
		testlogdir = os.getcwd()
		return testlogdir
	
	# 2. If --dir DIR is used, save logs to DIR    
	#    Since it's user defined directory, branch and build are optional and not validated 
	elif options.dir:
		## mkdir or cd DIR
		cdDir(options.dir)
		
		## If --dir DIR --branch BRANCH, save logs to DIR/BRANCH
		if options.branch:
			br = options.branch	
			print "Branch: " + br 
			cdDir(br)

		## If --dir DIR --build BUILD, save logs to DIR/BUILD or DIR/BRANCH/BUILD
		if options.build:	
			bld = options.build 
			print "Build:  " + bld
			cdDir(bld)
	
		testlogdir = os.getcwd()
		return testlogdir
	
	# 3. If neither test type is specified nor --dir are used,  
	#    check if the script path is in systest/tests/sanity or .../soak. 
	elif os.path.basename(os.getcwd())=='sanity' or os.path.basename(os.getcwd())=='soak':
		# --branch is required if destination is in repository	
		if not options.branch:
			print "ERROR: branch is missing"
			print "Please enter the branch name. e.g: --br 4.6B2"
			exit(0)

		br = options.branch	
		print "Branch: " + br 
		brpath = os.path.join(PATH_BUILDS, br)

		## Check if the branch passed in is valid	
		if not os.path.exists(brpath):
			path_error(brpath)	
		
		## Get build-id from the argument in --build option
		if options.build:	
			bld = options.build 
		## Use lastest build if --build option is not used 
		else: 
			print "(Build unspecified. Assuming the latest build is being used.)"
			bld = get_latest_build(br)
		print "Build:  " + bld
		bldpath = os.path.join(brpath,bld)

		## Check if the build is valid
		if not os.path.exists(bldpath):
			path_error(bldpath)
		
		## cd log path	
		if os.path.basename(os.getcwd()) == 'sanity':
			cdDir(PATH_LOG_SANITY)
			cdDir(br)
			cdDir(bld)
		elif os.path.basename(os.getcwd()) == 'soak':
			cdDir(PATH_LOG_SOAK)
			cdDir(br)
			cdDir(bld)
		
		testlogdir = os.getcwd()
		return testlogdir
		
	
	# 4. Else, if ENVVAR exists, use the ENVVAR
	#    Branch and build options are optional and not validated 
	elif os.environ.has_key(LOG_DIR_ENVVAR):
		cdDir(os.environ[LOG_DIR_ENVVAR])
	
		## If --dir DIR --branch BRANCH, save logs to DIR/BRANCH
		if options.branch:
			br = options.branch	
			print "Branch: " + br 
			cdDir(br)

		## If --dir DIR --build BUILD, save logs to DIR/BUILD or DIR/BRANCH/BUILD
		if options.build:	
			bld = options.build 
			print "Build:  " + bld
			cdDir(bld)
	
		testlogdir = os.getcwd()
		return testlogdir

	# 5. Lastly, Default log directory: Logs 
	#    Branch and build options are optional and not validated 
	else: 
		cdDir('Logs')
		
		## If --dir DIR --branch BRANCH, save logs to DIR/BRANCH
		if options.branch:
			br = options.branch	
			print "Branch: " + br 
			cdDir(br)

		## If --dir DIR --build BUILD, save logs to DIR/BUILD or DIR/BRANCH/BUILD
		if options.build:	
			bld = options.build 
			print "Build:  " + bld
			cdDir(bld)
		
		testlogdir = os.getcwd()
		return testlogdir
		
def get_log_file():
    return log_file_name

def cdDir(d):
	try:
               	if os.path.exists(d):
                       	#print "directory " + d + " exits"
                       	os.chdir(d) 
               	else:
                       	#print "creating directory: " + d
			os.mkdir(d)
                       	os.chdir(d)
	except OSError, e:
		print "ERROR: failed to create " + d + " under current directory " + os.getcwd()
		print OSError, e 
		exit(0)


def buildLogger(filename, **kwds):
    """Build the basic logging facility.

    A typical call would be:

    buildLogger("somename.log")

    To enable debug logging:

    buildLogger("somename.log", debug=True)
    
    """
    global log_file_name
    testlogdir = setLogDir()
    #print "Test logs will be created in " + testlogdir
    datefmt='%H:%M:%S'
    logformat = '%(asctime)s : %(levelname)-7s : %(message)s'

    try:
        # build a new instance of the logger and add the general
        # format
        log = logging.getLogger()
        formatter = logging.Formatter(logformat, datefmt)

        # add a couple of high level log levels for other purposes
        ### log.output: for logging the output from a command
        logging.output = 51
        log.output = lambda msg, self=log, level=logging.output: self.log(level, msg)
        logging.addLevelName(logging.output, "OUTPUT")
        
        ### log.cmd: for logging the command send on a cli
        logging.cmd = 52
        log.cmd = lambda msg, self=log, level=logging.cmd: self.log(level, msg)
        logging.addLevelName(logging.cmd, "CMD")

        ### log.test: for logging the command send on a cli
        logging.test = 53
        log.test = lambda msg, self=log, level=logging.test: self.log(level, msg)
        logging.addLevelName(logging.test, "TEST")
        
        ### log.result: for logging the command send on a cli
        logging.result = 54
        log.result = lambda msg, self=log, level=logging.result: self.log(level, msg)
        logging.addLevelName(logging.result, "RESULT")

		
        # build the logfile handler
        filename = timestamp(filename)
        log_file_name = filename
        fh = logging.FileHandler(normpath(filename), "w")
        fh.setFormatter(formatter)
        log.addHandler(fh)

        # build the stdout handler
        try:
            if kwds['console']:            
                sh = logging.StreamHandler()
                sh.setFormatter(formatter)
                log.addHandler(sh)
        except KeyError:
            pass
            
        # set the log level
        try:
            if kwds['debug']:
                log.setLevel(logging.DEBUG)
            elif kwds['info']:
                log.setLevel(logging.INFO)
        except KeyError:
            log.setLevel(logging.WARN)

        return log

    except:
        raise
