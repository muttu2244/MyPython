#!/usr/bin/env python2.5

### for now we use this hack to get them there.

import sys, os
mydir = os.path.dirname(__file__)
precom_file = __file__
qa_lib_dir = os.path.join(mydir, "../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)


### import the libraries we need.
from log import buildLogger
from log import *
from StokeTest import test_suite, test_runner, test_case

#Get the configuration from a string in a config file config.py and Load it in SSX.
#os.systme("python ssx_load.py")

### import our tests
from cli_exec_boot  import cli_exec_boot
from cli_exec_cert  import cli_exec_cert
from cli_exec_clr   import cli_exec_clr
#from cli_exec_clck import cli_exec_clck                # Clock
from cli_exec_conf  import cli_exec_conf                # Configuration
from cli_exec_cntx  import cli_exec_cntx
from cli_exec_copy  import cli_exec_copy
from cli_exec_dbug  import cli_exec_dbug
from cli_exec_delt  import cli_exec_delt
from cli_exec_dir   import cli_exec_dir
from cli_exec_drve  import cli_exec_drve
from cli_exec_exit  import cli_exec_exit
from cli_exec_load  import cli_exec_load
from cli_exec_mdir  import cli_exec_mdir
from cli_exec_no    import cli_exec_no
from cli_exec_ping  import cli_exec_ping
from cli_exec_rlod  import cli_exec_rlod
from cli_exec_renm  import cli_exec_renm
from cli_exec_rdir  import cli_exec_rdir 
from cli_exec_save  import cli_exec_save
from cli_exec_show  import cli_exec_show
from cli_exec_sytm  import cli_exec_sytm
from cli_exec_tlnt  import cli_exec_tlnt
from cli_exec_trml  import cli_exec_trml
from cli_exec_tcrt  import cli_exec_tcrt
 

# build us a log file.  Note console output is enabled.
log = buildLogger("suite_cli_exec.log", debug=True, console=True)

# build our test suite
suite = test_suite()
#suite.addTest(cli_exec_boot) # changing the bootline image and config files
suite.addTest(cli_exec_cert)
suite.addTest(cli_exec_clr)
#suite.addTest(cli_exec_clck)
suite.addTest(cli_exec_conf)
suite.addTest(cli_exec_cntx)
suite.addTest(cli_exec_copy)
suite.addTest(cli_exec_dbug)
suite.addTest(cli_exec_delt)
suite.addTest(cli_exec_dir)
suite.addTest(cli_exec_drve)
#suite.addTest(cli_exec_exit) # For next commands asking for user name and password
suite.addTest(cli_exec_load)
suite.addTest(cli_exec_mdir)
suite.addTest(cli_exec_no)
#suite.addTest(cli_exec_ping)  # pinging for max values(4294967295)  
suite.addTest(cli_exec_rlod)
suite.addTest(cli_exec_renm)
suite.addTest(cli_exec_rdir)
suite.addTest(cli_exec_save)
suite.addTest(cli_exec_show)
#suite.addTest(cli_exec_sytm) # changing the baud rate
suite.addTest(cli_exec_trml)
#suite.addTest(cli_exec_tcrt) # trying for lot of time
suite.addTest(cli_exec_tlnt)

# now let's run our test suite
test_runner().run(suite)


