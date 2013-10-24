
"""
A series of helper functions that don't have a home.  When a grouping of these
functions share a common use case, they should be grouped together in a seperate
module.
"""

from logging import getLogger
from os.path import normpath
from time import localtime
import time, datetime
import re, string

def timestamp(filename):
    """Take a string representing a filename and add a timestamp to it.

    timestamp sequence is year, month, day, hour, minute.
    """
    timestr = str()
    for i in localtime()[:-4]:
        timestr += str(i)
        
    name, suffix = filename.split(".")
    name = "%s-%s" % (name, timestr)
    return ".".join([name, suffix])

def is_healthy(pd, IMC_Switch=0,Card_Reset=0, Card_Restart=0, Core_Files=0,
               Proc_Exits=0, Proc_Restarts=0, Crit_logs=0, Err_logs=0,
               Warn_logs=0):
    """Take a platform dictionary returned from SSX.get_health_stats
    and ensure the values are all zero. *Most* tests will use function
    to verify the system health. In cases where non-zero health counters
    are expected, this function should not be used."""
    #
    mylog = getLogger()
    if ('IMC_Switch' in pd and
        pd['IMC_Switch'] > IMC_Switch):
        mylog.info("The number of IMC switches is %d" % pd['IMC_Switch'])
        return False
    if ('Card_Reset' in pd and
        pd['Card_Reset'] > Card_Reset):
        mylog.info("The number of card resets is %d" % pd['Card_Reset'])
        return False
    if ('Card_Restart' in pd and
        pd['Card_Restart'] > Card_Restart):
        mylog.info("The number of card restarts is %d" % pd['Card_Restart'])
        return False
    if ('Core_Files' in pd and
        pd['Core_Files'] > Core_Files):
        mylog.info("The number of core files is %d" % pd['Core_Files'])
        return False
    if ('Proc_Exits' in pd and
        pd['Proc_Exits'] > Proc_Exits):
        mylog.info("The number of process restarts is %d" % pd['Proc_Exits'])
        return False
    if ('Proc_Restarts' in pd and
        pd['Proc_Restarts'] > Proc_Restarts):
        mylog.info("The number of process restarts is %d" % pd['Proc_Restarts'])
        return False
    if ('Crit_logs' in pd and
        pd['Crit_logs'] > Crit_logs):
        mylog.info("The number of CRITICAL log events is %d" % pd['Crit_logs'])
        return False
    if ('Err_logs' in pd and
        pd['Err_logs'] > Err_logs):
        mylog.info("The number of ERROR log events is %d" % pd['Err_logs'])
        return False
    if ('Warn_logs' in pd and
        pd['Warn_logs'] > Warn_logs):
        mylog.info("The number of WARN log events is %d" % pd['Warn_logs'])
        return True
    return True


def write_to_file(data, filename, location=None):
    """Writes the contents of data to a file.  The data and filename arguements are
    required.  Location is optional.  Data can be either a string or a list of strings.
    """
    if location:
        filename = normpath("%s/%s" % (location, filename))

    f = open(filename, "w")
    if type(data) == str():
        f.write(data)
    else:
        f.writelines(data)
    f.close()

def diff_in_time(hour1, min1, sec1, hour2, min2, sec2, year1=1, month1=1, day1=1, year2=1, month2=1, day2=1):
        """Gives the difference in time in hours , minutes and seconds"""
        old_time = datetime.datetime(year2,month2,day2,hour2,min2,sec2)
        new_time = datetime.datetime(year1,month1,day1,hour1,min1,sec1)
        difference = new_time-old_time
        week,days = divmod(difference.days,7)
        minutes,seconds = divmod(difference.seconds,60)
        hours,minutes = divmod(minutes,60)
        return hours,minutes,seconds

def diff_in_hours(hour1, min1, sec1, hour2, min2, sec2,  year1=1, month1=1, day1=1, year2=1, month2=1, day2=1):
        """Gives the difference in time in hours only"""
        (x,y,z) = diff_in_time(hour1, min1, sec1, hour2, min2, sec2, year1, month1, day1, year2, month2, day2)
        return x

def diff_in_minutes(hour1, min1, sec1, hour2, min2, sec2, year1=1, month1=1, day1=1, year2=1, month2=1, day2=1):
        """Gives the difference in time in minutes only"""
        (x,y,z) = diff_in_time(hour1, min1, sec1, hour2, min2, sec2, year1, month1, day1, year2, month2, day2)
        return y

def diff_in_seconds(hour1, min1, sec1, hour2, min2, sec2, year1=1, month1=1, day1=1, year2=1, month2=1, day2=1):
        """Gives the difference in time in seconds only"""
        (x,y,z) = diff_in_time(hour1, min1, sec1, hour2, min2, sec2, year1, month1, day1, year2, month2, day2)
        return z


def diff_in_time_ssx(time_str1,time_str2):
        """ Gives the difference int time in seconds, the arguments can be show clock output strings/ SA time strings/ Linux date string """
        time_regex ='(\d+):(\d+):(\d+)'
        obj = re.compile(time_regex,re.I)
        m = obj.search(time_str1)
        n = obj.search(time_str2)

        hr1 = int(m.group(1))
        min1 = int(m.group(2))
        sec1 = int(m.group(3))

        hr2 = int(n.group(1))
        min2 = int(n.group(2))
        sec2 = int(n.group(3))

        hr=hr2-hr1
        min=min2-min1
        sec=sec2-sec1

        if hr:
          hr=hr*3600
        if min:
          min=min*60
        diff = hr+min+sec
        return diff

def dec_to_any_base(num, base):
        """Returns the converted decimal number to any base as a string. It takes the integer input 'number' and 'base' to which it has to convert""" 
        if not num: return '0'
        digits=[]
        minus=''
        if num < 0:
           minus='-'
           num=-num
        while num:
           num, digit = divmod(num, base)
           digits.append(str(digit))
        if minus: digits.append(minus)
        digits.reverse()
        return string.join(digits,'')

def compare2ipv4(ip1="1.1.1.1",ip2="1.1.1.2",index=3):
	if index == 1:
		ip1_diff=ip1.split('.')[0]
		ip2_diff=ip2.split('.')[0]

	if index == 2:
		ip1_diff="%s.%s"%(ip1.split('.')[0],ip1.split('.')[1])
		ip2_diff="%s.%s"%(ip2.split('.')[0],ip2.split('.')[1])
	
	if index == 3:
		ip1_diff="%s.%s.%s"%(ip1.split('.')[0],ip1.split('.')[1],ip1.split('.')[2])
		ip2_diff="%s.%s.%s"%(ip2.split('.')[0],ip2.split('.')[1],ip2.split('.')[2])

	if index == 4:
		ip1_diff="%s.%s.%s.%s"%(ip1.split('.')[0],ip1.split('.')[1],ip1.split('.')[2],ip1.split('.')[3])
		ip2_diff="%s.%s.%s.%s"%(ip2.split('.')[0],ip2.split('.')[1],ip2.split('.')[2],ip2.split('.')[3])
		
	if ip1_diff == ip2_diff:
		return 0
	else:
		return 1
def verify_null_string(nullStr = "\n\n"):
	"""Matches any whitespace character; this is equivalent to the class [ \t\n\r\f\v].
           retunrs 0 if it is null, else 1
	"""
	op1 = re.search("\s",nullStr)
	#op2 = re.search("\w",nullStr)
	if not op1:
		return 1
	else:
		return 0

def insert_char_to_string(Originalstr,pos,insChar):
	""" Let me write API first
	"""
	modifiedStr = ""
	posIndex = pos
	while (posIndex <= len(Originalstr)):
	        testStr = Originalstr[:posIndex]
	        testStr = testStr[-pos:]
        	modifiedStr = modifiedStr + testStr + insChar
        	posIndex = posIndex + pos

	modifiedStr = modifiedStr.strip(insChar)
	return modifiedStr
