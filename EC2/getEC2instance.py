#!/usr/bin/python

#delete the previous snapshot
#create the snapshot
#make sure the snapshot is created
import boto3
import sys
import datetime

def main():
	instances = ec2.instances.filter(
	    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])
	for instance in instances:
	    print(instance.id, instance.instance_type,getInstanceName(instance), getInstanceUptime(instance))

def getInstanceName(instance):
	if instance.tags is None:
		return None
	for tag in instance.tags:
		if tag['Key'] == 'Name':
			return tag['Value']

def getInstanceUptime(instance):
	launchTime = instance.launch_time
	return (datetime.datetime.now() - launchTime.replace(tzinfo=None)).days

def usage():
	print "./getEC2instance.py"

if __name__ == "__main__":
	if len(sys.argv) != 1 :
		usage()
		sys.exit(-1)
	main()