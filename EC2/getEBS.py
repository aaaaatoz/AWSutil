#!/usr/bin/python

import boto3
import sys
import datetime

def main():
	print "in-use volumes:"
	print "create date\t\tvolume name"
	getVolumes('in-use')
	print "available volumes:"
	print "create date\t\tvolume name"
	getVolumes('available')

def getVolumes(status):
	ec2 = boto3.resource('ec2')
	volumes = ec2.volumes.filter(
    	Filters=[{'Name': 'status', 'Values': [status]}])
	for volume in volumes:
		print "%s\t%s" %(volume.create_time.strftime("%Y-%m-%D"), volume.volume_id)


def usage():
	print "./getEBS.py"

if __name__ == "__main__":
	if len(sys.argv) != 1 :
		usage()
		sys.exit(-1)
	main()