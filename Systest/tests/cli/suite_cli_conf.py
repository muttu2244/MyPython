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


### import our tests
from cli_conf_aaa  import cli_conf_aaa
from cli_conf_admn  import cli_conf_admn
#from cli_conf_clk import cli_conf_clk
#from cli_conf_cntx import cli_conf_cntx
#from cli_conf_dbug import cli_conf_dbug                  # context
from cli_conf_dot1 import cli_conf_dot1
#from cli_conf_end  import cli_conf_end
#from cli_conf_exit  import cli_conf_exit
from cli_conf_ipsc  import cli_conf_ipsc
from cli_conf_ipv6   import cli_conf_ipv6
from cli_conf_logg  import cli_conf_logg
#from cli_conf_no    import cli_conf_no
from cli_conf_ntp  import cli_conf_ntp
from cli_conf_port import cli_conf_port
from cli_conf_qos  import cli_conf_qos
#from cli_conf_show import cli_conf_show
from cli_conf_snmp import cli_conf_snmp
from cli_conf_sytm import cli_conf_sytm 
from cli_conf_tunl import cli_conf_tunl
 

# build us a log file.  Note console output is enabled.
log = buildLogger("suite_cli_conf.log", debug=True, console=True)

# build our test suite
suite = test_suite()
suite.addTest(cli_conf_aaa)
suite.addTest(cli_conf_admn)
#suite.addTest(cli_conf_clk)
#suite.addTest(cli_conf_cntx)
#suite.addTest(cli_conf_dbug)
#suite.addTest(cli_conf_dot1)  # main release (deerwood) shows "ERROR: No key generation method specified"
#suite.addTest(cli_conf_end)
#suite.addTest(cli_conf_exit)
suite.addTest(cli_conf_ipsc)
suite.addTest(cli_conf_ipv6)
suite.addTest(cli_conf_logg)
#suite.addTest(cli_conf_no)
suite.addTest(cli_conf_ntp)
suite.addTest(cli_conf_port)
#suite.addTest(cli_conf_qos)   # main release (deerwood) shows "ERROR: No key generation method specified"
#suite.addTest(cli_conf_show)
suite.addTest(cli_conf_snmp)
suite.addTest(cli_conf_sytm)
suite.addTest(cli_conf_tunl)

# now let's run our test suite
test_runner().run(suite)


