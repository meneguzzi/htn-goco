#!/bin/sh
if [ $# -lt 3 ]
	then echo "Usage ${0} <domain-name> <problem-name> <gui|nogui> [a|<0..n>]"
	exit 1
else
	# echo $CLASSPATH
	export CLASSPATH=./jshop2/antlr.jar:./jshop2/bin.build/JSHOP2.jar:.
	export PARS="-Xms8g -Xmx12g"
	# echo $CLASSPATH
	# DOMAIN=${1}
# 	PROBLEM=${2}
#
# 	if [ -e ${1}.jshop ]
# 	then
# 		DOMAIN=${1}.jshop
# 	elif [ -e ${1}.ujshop ]
# 	then
# 		DOMAIN=${1}.ujshop
# 	fi
#
# 	if [ -e ${2}.jshop ]
# 	then
# 		PROBLEM=${2}.jshop
# 	elif [ -e ${2}.ujshop ]
# 	then
# 		PROBLEM=${2}.ujshop
# 	fi
	
	java -cp $CLASSPATH JSHOP2.InternalDomain ${1}.jshop #${DOMAIN}
	java -cp $CLASSPATH JSHOP2.InternalDomain -r${4} ${2}.jshop #${PROBLEM}
	javac *.java
	if [ $3 = "gui" ]; then
		java ${PARS} gui $2
	else
		java ${PARS} run $2
	fi
	rm *.class
	rm ${1}.java ${2}.java ${1}.txt
fi