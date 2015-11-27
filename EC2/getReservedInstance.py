#!/usr/bin/python

import boto3
import sys
from collections import Counter

def main():
	getReservedInstance()

def getReservedInstance():
	client = boto3.client('ec2')
	reservedInstances = client.describe_reserved_instances()['ReservedInstances']
	instanceType = Counter([ instance.get('InstanceType') for instance in reservedInstances ])
	for i in instanceType.iteritems():
		print "Instance type %15s\tcounter%3d" %(i[0],i[1])


def usage():
	print "./getReservedInstance.py"

if __name__ == "__main__":
	if len(sys.argv) != 1 :
		usage()
		sys.exit(-1)
	main()