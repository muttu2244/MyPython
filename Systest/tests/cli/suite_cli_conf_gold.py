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
from cli_conf_aaa_gld  import cli_conf_aaa_gld
from cli_conf_admn_gld  import cli_conf_admn_gld
#from cli_conf_clk_gld import cli_conf_clk_gld
#from cli_conf_cntx_gld import cli_conf_cntx_gld
#from cli_conf_dbug_gld import cli_conf_dbug_gld                  # context
from cli_conf_dot1_gld import cli_conf_dot1_gld
#from cli_conf_end_gld  import cli_conf_end_gld
#from cli_conf_exit_gld  import cli_conf_exit_gld
from cli_conf_ipsc_gld  import cli_conf_ipsc_gld
from cli_conf_ipv6_gld   import cli_conf_ipv6_gld
from cli_conf_logg_gld  import cli_conf_logg_gld
#from cli_conf_no_gld    import cli_conf_no_gld
from cli_conf_ntp_gld  import cli_conf_ntp_gld
from cli_conf_port_gld import cli_conf_port_gld
from cli_conf_qos_gld  import cli_conf_qos_gld
#from cli_conf_show_gld import cli_conf_show_gld
from cli_conf_snmp_gld import cli_conf_snmp_gld
from cli_conf_sytm_gld import cli_conf_sytm_gld
from cli_conf_tunl_gld import cli_conf_tunl_gld
 

# build us a log file.  Note console output is enabled.
log = buildLogger("suite_reg.log", debug=True, console=True)

# build our test suite
suite = test_suite()
suite.addTest(cli_conf_aaa_gld)
suite.addTest(cli_conf_admn_gld)
#suite.addTest(cli_conf_clk_gld)
#suite.addTest(cli_conf_cntx_gld)
#suite.addTest(cli_conf_dbug_gld)
suite.addTest(cli_conf_dot1_gld)
#suite.addTest(cli_conf_end_gld)
#suite.addTest(cli_conf_exit_gld)
suite.addTest(cli_conf_ipsc_gld)
suite.addTest(cli_conf_ipv6_gld)
suite.addTest(cli_conf_logg_gld)
#suite.addTest(cli_conf_no_gld)
suite.addTest(cli_conf_ntp_gld)
suite.addTest(cli_conf_port_gld)
suite.addTest(cli_conf_qos_gld)
#suite.addTest(cli_conf_show_gld)
suite.addTest(cli_conf_snmp_gld)
suite.addTest(cli_conf_sytm_gld)
suite.addTest(cli_conf_tunl_gld)

# now let's run our test suite
test_runner().run(suite)

# FOLLOWING CODE WILL TAR ALL THE SIPp LOG FILE AVAILABLE IN THE SIPp DIR
#os.system("python sip_log_tar.py")

