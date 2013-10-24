
import os
import re
from topo import *
'''
Executes the cli commands deleting twice and again add the config commands
'''

cli = os.popen("perl cli-driver.pl -s -l global_cli_008.log  -n -r -2 -a -f complete_list -c -u  -c -u %s -p %s %s" %(ssx['user_name'],ssx['password'],ssx['ip_addr']))


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
    
