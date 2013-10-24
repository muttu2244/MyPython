
import os
import re
from topo import *

'''
Description : Verifies all available commands in SSX
'''

cli = os.popen("perl cli-driver.pl -l global_cli_04.ssx.log -L global_cli_04.ssx_cmd_success -f complete_list -c -u %s -p %s %s" %(ssx['user_name'],ssx['password'],ssx['ip_addr']))

prevLine = ""

f = open("ssx_cmd_unsuccess", 'w')
lineList = []
for line in cli.readlines():
    if "ERROR:" in line:
        str1 =  re.sub(r'<!>',"$",re.sub("\w+\(cfg\-\d+\)#","$",prevLine))
        str2 = re.sub(r"^H","",re.sub('\[K',"",str1))
        for command in str2.split("$"):
            line1 = command.strip()
            line1 = line1.strip("\x08\x08\x08\x1b" or "\x1b" or "\x1b\[")
            line1 = "%s\n" %line1.strip()
            if line1.strip() != '[' and len(line1) > 1:            
                f.write(line1)
    prevLine = line
    
f.close()
    
