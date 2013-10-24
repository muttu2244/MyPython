
import sys, os

mydir = os.path.dirname(__file__)
qa_lib_dir = os.path.join(mydir, "../../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

from tunnel import *

in_cntrs = verify_tunnel_counters_with_name.in_ctrs
out_cntrs =  verify_tunnel_counters_with_name.out_ctrs

print in_cntrs
print "********************\n"
print out_cntrs

