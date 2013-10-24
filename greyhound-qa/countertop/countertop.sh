#!/bin/bash
if [ $UID != 0 ]; then
	echo 'Should run as root'
	exit 0
fi
echo "Starting script.  $(date)" > $PWD/counter.log
function installServer() {
	echo 'Installing countertop-server..'
	yum install -y --enablerepo=seg-la countertop-server >> $PWD/counter.log
	if [ "$?" -ne 0 ];then
		echo 'Error in installing countertop-server'
		exit 0
	fi
	echo 'Done..'
}

function installClient() {
	echo 'Installing countertop-client...'
	yum install -y --enablerepo=seg-la countertop-client >> $PWD/counter.log
	if [ "$?" -ne 0 ];then
		echo 'Error in installing countertop-client'
		exit 0
	fi
	echo 'Done..'
}

function installModBanish() {
	echo 'Installing mod_banish ...'
	yum install -y --enablerepo=seg-la mod_banish >> $PWD/counter.log
	if [ "$?" -ne 0 ];then
                echo 'Error in installing mod_banish'
                exit 0
	fi
	echo 'Done...'
}


function addRepoFile(){
echo 'Adding repo file yum.repos.d ..'
cat > /etc/yum.repos.d/gh.repo <<EOF
[gh]
name=gh
baseurl=http://gh-test-repo-01.zc1.zynga.com/gh/current/
enabled=1
gpgcheck=0
EOF
}

function uninstall() {
	echo 'Stopping the services...'
	/sbin/service httpd stop
	/sbin/service countertopd stop
	echo 'Uninstalling countertop and mod_banish rpms..'
	yum remove -y countertop-server >> $PWD/counter.log
	yum remove -y countertop-client >> $PWD/counter.log
	yum remove -y mod_banish >> $PWD/counter.log
	echo 'Uninstallation complete...'
}

function cleanup() {
	echo 'Cleaning up the directories...'
	if [ -d /opt/zynga/countertop ]; then
		rm -rf /opt/zynga/countertop
	fi
	
	if [ -d /var/log/countertop ];then
		rm -rf /var/log/countertop
	fi
	
	if [ -d /etc/countertop ];then
		rm -rf /etc/countertop
	fi

	if [ -d /var/cache/banish ];then
		rm -rf /var/cache/banish
	fi
	echo 'Done..'

}

echo 'cleaning up yum cache..'
yum clean all

if [ -e /etc/yum.repos.d/gh.repo ];then
	echo 'gh.repo is present'
else
	echo 'Adding gh.repo file..'
	addRepoFile
fi

if [ 0 -lt $(rpm -qa|grep -c 'countertop') -o 0 -lt $(rpm -qa|grep -c 'mod_banish') ];then
	uninstall
	cleanup
fi

installServer
installClient
installModBanish
echo "See $PWD/counter.log for more.."
echo 'Done...'
exit 0
