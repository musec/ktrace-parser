#!/bin/sh
# This script runs all of the following commands to get ktrace output from each of them.
# Note that the value of KTRACE_LOGS_PATH should be defined before run this script.
set -x 

touch /tmp/testfile.sh
echo "echo hello" > /tmp/testfile.sh
#CHMOD
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-chmod -adi -tcnisu chmod a+x /tmp/testfile.sh


#CHOWN
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-chown -adi -tcnisu chown root /tmp/testfile.sh

#FIND
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-find -adi -tcnisu find /tmp/ -name \"testfile.sh\"

#FETCH
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-fetch -adi -tcnisu fetch "https://www.google.ca"

#CP
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-cp -adi -tcnisu cp /tmp/testfile.sh /tmp/testfile2.sh

#NETSTAT  
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-netstat -adi -tcnisu netstat -n


#GREP
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-grep -adi -tcnisu grep -ri "testfile" /root/src/Capsicum/

#MAN
`ktrace -f $KTRACE_LOGS_PATH/ktrace-out-man -adi -tcnisu man passwd`

#CAT
`ktrace -f $KTRACE_LOGS_PATH/ktrace-out-cat -adi -tcnisu cat /var/ktrace-logs/ktrace-out-man`

#TAR
`ktrace -f $KTRACE_LOGS_PATH/ktrace-out-tar -adi -tcnisu tar -czvf testfile.tar.gz tmp/testfile.sh`


#CRONTAB
echo "*/10 * * * * /tmp/testfile.sh" > /tmp/cron-test
`ktrace -f $KTRACE_LOGS_PATH/ktrace-out-crontab -adi -tcnisu crontab /tmp/cron-test`

#ALIAS
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-alias -adi -tcnisu alias \"..='cd ..'\"

#EVAL
cmd="touch /tmp/testfile.txt"
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-eval -adi -tcnisu eval $cmd

#VMSTAT
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-vmstat -adi -tcnisu vmstat #check whether it's adapted with capsicum or not

#EXEC
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-exec -adi -tcnisu exec rm -rf /tmp/testfile.txt

#EXPORT
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-export -adi -tcnisu setenv country=Canada

#GZIP
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-gzip -adi -tcnisu gzip -c /tmp/testfile.sh > /tmp/testfile.gz

#LOCATE
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-locate -adi -tcnisu locate mount

#DATE
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-date -adi -tcnisu date +%D

#KILL
cron_pid=`ps ax | grep cron | awk '{print $1}'`
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-kill -adi -tcnisu kill -9 $cron_pid
service cron restart

#W
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-w -adi -tcnisu w

#--------- NETWORKING COMMANDS -------------#

#IFCONFIG
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-ifconfig -adi -tcnisu ifconfig

#nslookup ---> host command on FreeBSD
ktrace -f $KTRACE_LOGS_PATH/ktrace-out-host -adi -tcnisu host "google.com"


#
##traceroute
##ssh
##telnet
##SCP
##nmap
#
#
rm -rf /tmp/testfile*
