#!/usr/bin/python

import boto3
import sys
import datetime

def main():
	getRDS()

def getRDS():
	rds = boto3.client('rds')
	dbInstances = rds.describe_db_instances()['DBInstances']
	print "%20s\t%15s\t\t%20s\t%20s" %("dbname","storage","instancetype","runningdays")
	print 93*"="
	for index in xrange(0,len(dbInstances)):
		print "%20s\t%15dG\t%20s\t%20s" %(dbInstances[index]['DBInstanceIdentifier'], \
			dbInstances[index]['AllocatedStorage'], \
			dbInstances[index]['DBInstanceClass'], \
			getInstanceUptime(dbInstances[index]['InstanceCreateTime']))

def getInstanceUptime(dateToConvert):
	return (datetime.datetime.now() - dateToConvert.replace(tzinfo=None)).days


def usage():
	print "./getEBS.py"

if __name__ == "__main__":
	if len(sys.argv) != 1 :
		usage()
		sys.exit(-1)
	main()