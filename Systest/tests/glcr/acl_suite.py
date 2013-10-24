#!/usr/bin/env python2.5

""" Suite file for DoCoMo regression test cases """

### you need to make sure that the libraries are on your path.
import sys, os

mydir = os.path.dirname(__file__)
precomfile =__file__
qa_lib_dir = os.path.join(mydir, "../../../lib/py")
if qa_lib_dir not in sys.path:
    sys.path.insert(1,qa_lib_dir)

# Import topo and config information
#from topo_doc import *
#from ospf_config_doc import *

### import the libraries we need.
from log import buildLogger
from StokeTest import test_suite, test_runner
#from testopiaIf import *
from config import *
### import our tests

from GRED_ACL_TUN_FUN_001 import test_GRED_ACL_TUN_FUN_001
from GRED_ACL_TUN_FUN_002 import test_GRED_ACL_TUN_FUN_002
from GRED_ACL_TUN_FUN_003 import test_GRED_ACL_TUN_FUN_003
from GRED_ACL_TUN_FUN_004 import test_GRED_ACL_TUN_FUN_004
from GRED_ACL_TUN_FUN_005 import test_GRED_ACL_TUN_FUN_005
from GRED_ACL_TUN_FUN_006 import test_GRED_ACL_TUN_FUN_006
from GRED_ACL_TUN_FUN_007 import test_GRED_ACL_TUN_FUN_007
from GRED_ACL_TUN_FUN_008 import test_GRED_ACL_TUN_FUN_008
from GRED_ACL_TUN_FUN_009 import test_GRED_ACL_TUN_FUN_009
from GRED_ACL_TUN_FUN_010 import test_GRED_ACL_TUN_FUN_010
from GRED_ACL_TUN_FUN_012 import test_GRED_ACL_TUN_FUN_012
from GRED_ACL_TUN_FUN_013 import test_GRED_ACL_TUN_FUN_013
from GRED_ACL_TUN_FUN_014 import test_GRED_ACL_TUN_FUN_014
from ACL_Func_060 import test_ACL_Func_060
from ACL_Func_061 import test_ACL_Func_061
from ACL_Func_062 import test_ACL_Func_062
from ACL_Func_063 import test_ACL_Func_063
from ACL_Func_064 import test_ACL_Func_064
from ACL_Func_065 import test_ACL_Func_065
from ACL_Func_066 import test_ACL_Func_066
from ACL_Func_067 import test_ACL_Func_067
from ACL_Func_068 import test_ACL_Func_068
from ACL_Func_069 import test_ACL_Func_069
from ACL_Func_070 import test_ACL_Func_070
from ACL_Func_071 import test_ACL_Func_071
from ACL_Func_072 import test_ACL_Func_072
from ACL_Func_073 import test_ACL_Func_073
from ACL_Func_074 import test_ACL_Func_074
from ACL_Func_075 import test_ACL_Func_075
from ACL_Func_076 import test_ACL_Func_076
from ACL_Func_077 import test_ACL_Func_077
from ACL_Func_078 import test_ACL_Func_078
from ACL_Func_079 import test_ACL_Func_079
from ACL_Func_080 import test_ACL_Func_080
from ACL_Func_081 import test_ACL_Func_081
from ACL_Func_082 import test_ACL_Func_082
from ACL_Func_083 import test_ACL_Func_083
from ACL_Func_084 import test_ACL_Func_084
from ACL_Func_085 import test_ACL_Func_085
from ACL_Func_086 import test_ACL_Func_086
from ACL_Func_087 import test_ACL_Func_087
from ACL_Func_088 import test_ACL_Func_088
from ACL_Func_089 import test_ACL_Func_089
from ACL_Func_090 import test_ACL_Func_090
from ACL_Func_091 import test_ACL_Func_091
from ACL_Func_092 import test_ACL_FUNC_092
from ACL_Func_093 import test_ACL_FUNC_093
from ACL_Func_094 import test_ACL_FUNC_094
from ACL_Func_095 import test_ACL_FUNC_095
from ACL_Func_096 import test_ACL_FUNC_096
from ACL_Func_097 import test_ACL_FUNC_097
from ACL_Func_098 import test_ACL_FUNC_098
from ACL_Func_099 import test_ACL_FUNC_099
from ACL_Func_100 import test_ACL_FUNC_100
from ACL_Func_101 import test_ACL_FUNC_101
from ACL_Func_102 import test_ACL_FUNC_102
from ACL_Func_103 import test_ACL_FUNC_103
from ACL_Func_104 import test_ACL_FUNC_104
from ACL_Func_105 import test_ACL_FUNC_105
from ACL_Func_106 import test_ACL_FUNC_106
from ACL_Func_107 import test_ACL_FUNC_107
#from ACL_Func_060 import test_ACL_FUNC_108
#from ACL_Func_060 import test_ACL_FUNC_109
#from ACL_Func_060 import test_ACL_FUNC_110
#from ACL_Func_060 import test_ACL_FUNC_111
#from ACL_Func_060 import test_ACL_FUNC_112
from ACL_Func_119 import test_ACL_Func_119
from ACL_Func_120 import test_ACL_Func_120
from ACL_Func_121 import test_ACL_Func_121
from ACL_Func_122 import test_ACL_Func_122
from ACL_Func_123 import test_ACL_Func_123
from ACL_Func_124 import test_ACL_Func_124
from ACL_Func_125 import test_ACL_Func_125
from ACL_Func_126 import test_ACL_Func_126
from ACL_Func_127 import test_ACL_Func_127
from ACL_Func_130 import test_ACL_Func_130
from ACL_Func_131 import test_ACL_Func_131
from ACL_Func_132 import test_ACL_Func_132
from ACL_Func_138 import test_ACL_Func_138
from ACL_Func_139 import test_ACL_Func_139
from ACL_Func_144 import test_ACL_Func_144
from ACL_Func_145 import test_ACL_Func_145
from ACL_Func_151 import test_ACL_Func_151
from ACL_Func_152 import test_ACL_FUNC_152
from ACL_Func_208 import test_ACL_FUNC_208
from ACL_Func_209 import test_ACL_FUNC_209
from ACL_Func_210 import test_ACL_FUNC_210
from ACL_Func_211 import test_ACL_FUNC_211
from ACL_Func_212 import test_ACL_FUNC_212
from ACL_Func_213 import test_ACL_FUNC_213
from ACL_Func_214 import test_ACL_FUNC_214
from ACL_Func_215 import test_ACL_FUNC_215
from ACL_Func_216 import test_ACL_FUNC_216
from ACL_Func_217 import test_ACL_FUNC_217
from ACL_Func_218 import test_ACL_FUNC_218
from ACL_Func_219 import test_ACL_FUNC_219
from ACL_Func_220 import test_ACL_FUNC_220
from ACL_Func_221 import test_ACL_FUNC_221
from ACL_Func_222 import test_ACL_FUNC_222
from ACL_Func_223 import test_ACL_FUNC_223
from ACL_Func_224 import test_ACL_FUNC_224
from ACL_Func_225 import test_ACL_FUNC_225
from ACL_Func_226 import test_ACL_FUNC_226
from ACL_Func_227 import test_ACL_FUNC_227
from ACL_Func_228 import test_ACL_FUNC_228
from ACL_Func_229 import test_ACL_FUNC_229
from ACL_Func_230 import test_ACL_FUNC_230
from ACL_Func_231 import test_ACL_FUNC_231
from ACL_Func_232 import test_ACL_FUNC_232
from ACL_Func_233 import test_ACL_FUNC_233
from ACL_Func_234 import test_ACL_FUNC_234
from ACL_Func_235 import test_ACL_FUNC_235
from ACL_Func_236 import test_ACL_FUNC_236
from ACL_Func_237 import test_ACL_FUNC_237
from ACL_Func_238 import test_ACL_FUNC_238
from ACL_Func_239 import test_ACL_FUNC_239



if os.environ.has_key('TEST_LOG_DIR'):
    os.mkdir(os.environ['TEST_LOG_DIR'])
    os.chdir(os.environ['TEST_LOG_DIR'])


# build us a log file.  Note console output is enabled.
log = buildLogger("acl_SUITE.log", debug=True)


#build our test suite
suite = test_suite()
#suite.addTest(test_GRED_ACL_TUN_FUN_001)

suite.addTest(test_GRED_ACL_TUN_FUN_001)
suite.addTest(test_GRED_ACL_TUN_FUN_002)
suite.addTest(test_GRED_ACL_TUN_FUN_003)
suite.addTest(test_GRED_ACL_TUN_FUN_004)
suite.addTest(test_GRED_ACL_TUN_FUN_005)
suite.addTest(test_GRED_ACL_TUN_FUN_006)
suite.addTest(test_GRED_ACL_TUN_FUN_007)
suite.addTest(test_GRED_ACL_TUN_FUN_008)
suite.addTest(test_GRED_ACL_TUN_FUN_009)
suite.addTest(test_GRED_ACL_TUN_FUN_010)
suite.addTest(test_GRED_ACL_TUN_FUN_012)
suite.addTest(test_GRED_ACL_TUN_FUN_013)
suite.addTest(test_GRED_ACL_TUN_FUN_014)
suite.addTest(test_ACL_Func_060)
suite.addTest(test_ACL_Func_061)
suite.addTest(test_ACL_Func_062)
suite.addTest(test_ACL_Func_063)
suite.addTest(test_ACL_Func_064)
suite.addTest(test_ACL_Func_065)
suite.addTest(test_ACL_Func_066)
suite.addTest(test_ACL_Func_067)
suite.addTest(test_ACL_Func_068)
suite.addTest(test_ACL_Func_069)
suite.addTest(test_ACL_Func_070)
suite.addTest(test_ACL_Func_071)
suite.addTest(test_ACL_Func_072)
suite.addTest(test_ACL_Func_073)
suite.addTest(test_ACL_Func_074)
suite.addTest(test_ACL_Func_075)
suite.addTest(test_ACL_Func_076)
suite.addTest(test_ACL_Func_077)
suite.addTest(test_ACL_Func_078)
suite.addTest(test_ACL_Func_079)
suite.addTest(test_ACL_Func_080)
suite.addTest(test_ACL_Func_081)
suite.addTest(test_ACL_Func_082)
suite.addTest(test_ACL_Func_083)
suite.addTest(test_ACL_Func_084)
suite.addTest(test_ACL_Func_085)
suite.addTest(test_ACL_Func_086)
suite.addTest(test_ACL_Func_087)
suite.addTest(test_ACL_Func_088)
suite.addTest(test_ACL_Func_089)
suite.addTest(test_ACL_Func_090)
suite.addTest(test_ACL_Func_091)
suite.addTest(test_ACL_FUNC_092)
suite.addTest(test_ACL_FUNC_093)
suite.addTest(test_ACL_FUNC_094)
suite.addTest(test_ACL_FUNC_095)
suite.addTest(test_ACL_FUNC_096)
suite.addTest(test_ACL_FUNC_097)
suite.addTest(test_ACL_FUNC_098)
suite.addTest(test_ACL_FUNC_099)
suite.addTest(test_ACL_FUNC_100)
suite.addTest(test_ACL_FUNC_101)
suite.addTest(test_ACL_FUNC_102)
suite.addTest(test_ACL_FUNC_103)
suite.addTest(test_ACL_FUNC_104)
suite.addTest(test_ACL_FUNC_105)
suite.addTest(test_ACL_FUNC_106)
suite.addTest(test_ACL_FUNC_107)
suite.addTest(test_ACL_Func_119)
suite.addTest(test_ACL_Func_120)
suite.addTest(test_ACL_Func_121)
suite.addTest(test_ACL_Func_122)
suite.addTest(test_ACL_Func_123)
suite.addTest(test_ACL_Func_124)
suite.addTest(test_ACL_Func_125)
suite.addTest(test_ACL_Func_126)
suite.addTest(test_ACL_Func_127)
suite.addTest(test_ACL_Func_130)
suite.addTest(test_ACL_Func_131)
suite.addTest(test_ACL_Func_132)
suite.addTest(test_ACL_Func_138)
suite.addTest(test_ACL_Func_139)
suite.addTest(test_ACL_Func_144)
suite.addTest(test_ACL_Func_145)
suite.addTest(test_ACL_Func_151)
suite.addTest(test_ACL_FUNC_152)
suite.addTest(test_ACL_FUNC_208)
suite.addTest(test_ACL_FUNC_209)
suite.addTest(test_ACL_FUNC_210)
suite.addTest(test_ACL_FUNC_211)
suite.addTest(test_ACL_FUNC_212)
suite.addTest(test_ACL_FUNC_213)
suite.addTest(test_ACL_FUNC_214)
suite.addTest(test_ACL_FUNC_215)
suite.addTest(test_ACL_FUNC_216)
suite.addTest(test_ACL_FUNC_217)
suite.addTest(test_ACL_FUNC_218)
suite.addTest(test_ACL_FUNC_219)
suite.addTest(test_ACL_FUNC_220)
suite.addTest(test_ACL_FUNC_221)
suite.addTest(test_ACL_FUNC_222)
suite.addTest(test_ACL_FUNC_223)
suite.addTest(test_ACL_FUNC_224)
suite.addTest(test_ACL_FUNC_225)
suite.addTest(test_ACL_FUNC_226)
suite.addTest(test_ACL_FUNC_227)
suite.addTest(test_ACL_FUNC_228)
suite.addTest(test_ACL_FUNC_229)
suite.addTest(test_ACL_FUNC_230)
suite.addTest(test_ACL_FUNC_231)
suite.addTest(test_ACL_FUNC_232)
suite.addTest(test_ACL_FUNC_233)
suite.addTest(test_ACL_FUNC_234)
suite.addTest(test_ACL_FUNC_235)
suite.addTest(test_ACL_FUNC_236)
suite.addTest(test_ACL_FUNC_237)
suite.addTest(test_ACL_FUNC_238)
suite.addTest(test_ACL_FUNC_239)


# now let's run our test suite
test_runner().run(suite)







