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
from cli_cntx_aaa   import cli_cntx_aaa
from cli_cntx_cdr   import cli_cntx_cdr
from cli_cntx_cmap  import cli_cntx_cmap
#from cli_cntx_dbug import cli_cntx_dbug
from cli_cntx_domn  import cli_cntx_domn
#from cli_cntx_end  import cli_cntx_end
#from cli_cntx_exit import cli_cntx_exit
from cli_cntx_intf  import cli_cntx_intf           
from cli_cntx_ip    import cli_cntx_ip
from cli_cntx_ipsc  import cli_cntx_ipsc
from cli_cntx_ipv6  import cli_cntx_ipv6
#from cli_cntx_logg import cli_cntx_logg
#from cli_cntx_no   import cli_cntx_no
from cli_cntx_ntp   import cli_cntx_ntp
from cli_cntx_plcy  import cli_cntx_plcy
from cli_cntx_pmap  import cli_cntx_pmap
from cli_cntx_rdis  import cli_cntx_rdis
from cli_cntx_rand  import cli_cntx_rand
from cli_cntx_rmap  import cli_cntx_rmap
from cli_cntx_rmon  import cli_cntx_rmon
from cli_cntx_rotr  import cli_cntx_rotr
from cli_cntx_rtid  import cli_cntx_rtid 
from cli_cntx_sesn  import cli_cntx_sesn
#from cli_cntx_show import cli_cntx_show
from cli_cntx_user  import cli_cntx_user
 

# build us a log file.  Note console output is enabled.
log = buildLogger("suite_cli_cntx.log", debug=True, console=True)

# build our test suite
suite = test_suite()
suite.addTest(cli_cntx_aaa)
suite.addTest(cli_cntx_cdr)   # Not available at 3.0R1 and below
#suite.addTest(cli_cntx_cmap) # main release(deerwood) shows err "ERROR: No key generation method specified"
#suite.addTest(cli_cntx_dbug)
#suite.addTest(cli_cntx_domn)  # A single commnad 
#suite.addTest(cli_cntx_end)
#suite.addTest(cli_cntx_exit)
suite.addTest(cli_cntx_intf)
suite.addTest(cli_cntx_ip)
suite.addTest(cli_cntx_ipsc)
suite.addTest(cli_cntx_ipv6)
#suite.addTest(cli_cntx_logg)
#suite.addTest(cli_cntx_no)
suite.addTest(cli_cntx_ntp)
suite.addTest(cli_cntx_plcy)  # main release(deerwood) shows err "ERROR: No key generation method specified"
suite.addTest(cli_cntx_pmap)  # main release(deerwood) shows err "ERROR: No key generation method specified"
suite.addTest(cli_cntx_rdis)
suite.addTest(cli_cntx_rand)  # main release(deerwood) shows err "ERROR: No key generation method specified"	
suite.addTest(cli_cntx_rmap)
suite.addTest(cli_cntx_rmon)
suite.addTest(cli_cntx_rotr) 
suite.addTest(cli_cntx_rtid)  # A single command
suite.addTest(cli_cntx_sesn)
#suite.addTest(cli_cntx_show)
suite.addTest(cli_cntx_user)

# now let's run our test suite
test_runner().run(suite)


