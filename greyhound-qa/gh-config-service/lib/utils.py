import ConfigParser
import os
import yaml
import subprocess
import shlex
import random, string

def gen_secret(size = 10):
	char = string.ascii_lowercase + string.digits + string.ascii_lowercase
	return ''.join(random.choice(char) for x in range(size))
def loadIni(path):
        cfg = ConfigParser.SafeConfigParser()
        try:
                cfg.read(path)
        except Exception,e:
                return None
        config = {}
        for item in cfg.options('Greyhound'):
                value = cfg.get('Greyhound',item)
                value = value.replace('"','')
                config.update({item: value})
        return config

def loadYaml(path):
        try:
                file = open( path, 'r' )
                output = yaml.load(file)
        except Exception:
                return None
        return output

def getStorageYamlFromRemoteServer(gid, url):
	cmd = "/usr/bin/scp {0}:/apps/{1}/current/Storage.yaml /tmp/Storage.yaml".format(url,gid)
	ret, out, err = exec_cmd(shlex.split(cmd))
	if ret!=0:
		print out, err
		return False
	config = loadYaml("/tmp/Storage.yaml")
	if config:
		os.remove("/tmp/Storage.yaml")
		return config
	return False

def getGreyhoundIniFromRemoteServer(gid, url):
	cmd = "/usr/bin/scp {0}:/apps/{1}/current/greyhound.ini /tmp/greyhound.ini".format(url,gid)
	ret, out, err = exec_cmd(shlex.split(cmd))
	if ret!=0:
		print out, err
		return False
	config = loadIni("/tmp/greyhound.ini")
	if config:
		os.remove("/tmp/greyhound.ini")
		return config
	return False

def getAclFromRemoteServer(gid, url):
	cmd = "/usr/bin/scp {0}:/apps/{1}/current/ACL.yaml /tmp/ACL.yaml".format(url,gid)
	ret, out, err = exec_cmd(shlex.split(cmd))
	if ret!=0:
		print out, err
		return False
	config = loadYaml("/tmp/ACL.yaml")
	if config:
		os.remove("/tmp/ACL.yaml")
		return config
	return False


def exec_cmd(cmd):
	r = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	(std_out, std_err) = r.communicate()
	ret_code = r.wait()
	return ret_code, std_out, std_err


if __name__ == '__main__':
	print getStorageYamlFromRemoteServer("2244", "rgeorge@ghqacluster-staging-web-2.zc1.zynga.com")
	print getGreyhoundIniFromRemoteServer("2244", "ghqacluster-staging-web-2.zc1.zynga.com")
	print getAclFromRemoteServer("2244", "ghqacluster-staging-web-2.zc1.zynga.com")

