
import os
import re
'''
Verifies the execution of all  config commands which takes special characters
'''

cli = os.popen("perl cli-driver_specialchars.pl -l global_cli_007.ssx.log -L global_cli_007._ssx_cmd_success -f complete_list -c -u joe@local -p joe 10.3.255.103")

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
    
