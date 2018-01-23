#!/bin/sh 
#set -x 

KDUMP_LOGS_PATH="/var/kdump-logs"
KTRACE_LOGS_PATH="/var/ktrace-logs"
PARSER_OUT_PATH="/var/parser-output"

if [ -d "$KTRACE_LOGS_PATH" -a -d "$KDUMP_LOGS_PATH" -a -d "$PARSER_OUT_PATH" ]
then
	rm -r $KTRACE_LOGS_PATH/*
	rm -r $KDUMP_LOGS_PATH/*
	rm -r $PARSER_OUT_PATH/*
else

	mkdir $KTRACE_LOGS_PATH
	mkdir $KDUMP_LOGS_PATH
	mkdir $PARSER_OUT_PATH
fi 

. ./commands.sh

logfiles=$(basename `ls -l $KTRACE_LOGS_PATH/ktrace-out-* | awk '{print $9}'`)

for file in $logfiles
do
	echo $file
	command_str=$(echo $file | tr "-" "\n" | tail -1)
	kdump -f $KTRACE_LOGS_PATH/$file > $KDUMP_LOGS_PATH/kdump-$command_str.txt 
	python2 ./parser.py $KDUMP_LOGS_PATH/kdump-$command_str.txt > $PARSER_OUT_PATH/parsed_$command_str.txt

done

exit 0 

