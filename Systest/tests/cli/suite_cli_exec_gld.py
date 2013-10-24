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
from cli_exec_boot_gld  import cli_exec_boot_gld
from cli_exec_cert_gld  import cli_exec_cert_gld
from cli_exec_clr_gld   import cli_exec_clr_gld
#from cli_exec_clk_gld  import cli_exec_clk_gld
from cli_exec_conf_gld  import cli_exec_conf_gld               
from cli_exec_cntx_gld  import cli_exec_cntx_gld			
from cli_exec_copy_gld  import cli_exec_copy_gld
from cli_exec_dbug_gld  import cli_exec_dbug_gld
from cli_exec_delt_gld  import cli_exec_delt_gld
from cli_exec_dir_gld   import cli_exec_dir_gld
from cli_exec_drve_gld  import cli_exec_drve_gld
from cli_exec_exit_gld  import cli_exec_exit_gld
from cli_exec_load_gld  import cli_exec_load_gld
from cli_exec_mdir_gld  import cli_exec_mdir_gld
from cli_exec_no_gld    import cli_exec_no_gld
#from cli_exec_ping_gld  import cli_exec_ping_gld
from cli_exec_rlod_gld  import cli_exec_rlod_gld
from cli_exec_renm_gld  import cli_exec_renm_gld
from cli_exec_rdir_gld  import cli_exec_rdir_gld
from cli_exec_save_gld  import cli_exec_save_gld
#from cli_exec_show_gld  import cli_exec_show_gld
from cli_exec_sytm_gld  import cli_exec_sytm_gld
from cli_exec_tlnt_gld  import cli_exec_tlnt_gld
from cli_exec_trml_gld  import cli_exec_trml_gld
#from cli_exec_tcrt_gld  import cli_exec_tcrt_gld
 

# build us a log file.  Note console output is enabled.
log = buildLogger("suite_reg.log", debug=True, console=True)

# build our test suite
suite = test_suite()
suite.addTest(cli_exec_boot_gld)
suite.addTest(cli_exec_cert_gld)
suite.addTest(cli_exec_clr_gld)
#suite.addTest(cli_exec_clk_gld)
suite.addTest(cli_exec_conf_gld)
suite.addTest(cli_exec_cntx_gld)
suite.addTest(cli_exec_copy_gld)
suite.addTest(cli_exec_dbug_gld)
suite.addTest(cli_exec_delt_gld)
suite.addTest(cli_exec_dir_gld)
suite.addTest(cli_exec_drve_gld)
suite.addTest(cli_exec_exit_gld)
suite.addTest(cli_exec_load_gld)
suite.addTest(cli_exec_mdir_gld)
suite.addTest(cli_exec_no_gld)
#suite.addTest(cli_exec_ping_gld)  #Contains timeing values 
suite.addTest(cli_exec_rlod_gld)
suite.addTest(cli_exec_renm_gld)
suite.addTest(cli_exec_rdir_gld)
suite.addTest(cli_exec_save_gld)
#suite.addTest(cli_exec_show_gld)  #Contains historya nd timing values
suite.addTest(cli_exec_sytm_gld)
suite.addTest(cli_exec_tlnt_gld)
suite.addTest(cli_exec_trml_gld)
#suite.addTest(cli_exec_tcrt_gld)  # Conatins timing values

# now let's run our test suite
test_runner().run(suite)


