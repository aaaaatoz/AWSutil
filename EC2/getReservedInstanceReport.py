#!/usr/bin/python

import boto3
import sys
import ConfigParser

"""
check the reservedInstances to see if they are used
"""

def main():
	isUsedUp = True
	Config = ConfigParser.ConfigParser()
	Config.read(r"./conf/aws.conf")
	for region, vpconly in Config.items("regions"):
		print "\n\n" + 20 * "=" + "Region %s information" %(region) + 20 * "="		
		reservedInstances = getReservedInstance(region,vpconly=="True")
		runningInstances = getRunningInstance(region,vpconly=="True")
		print 25 * "=" + "Reseved Instances Status" + 25 * "="
		for instance, count in reservedInstances.iteritems():
			if count > runningInstances[instance]:
				print "%2d Reseved Instance type %12s in AZ %s in VPC(%6s) is not used up. %d not used" %(count, instance[1],instance[0], instance[2],count - runningInstances[instance])
				runningInstances[instance] = 0
				isUsedUp = False
			else:
				print "%2d Reseved Instance type %12s in AZ %s in VPC(%6s) is used up" %(count,instance[1],instance[0], instance[2])
				runningInstances[instance] = runningInstances[instance] - count
		print 25 * "=" + "On Demand Instances Status" + 25 * "="
		ondemandInstances = (instance for instance, count in runningInstances.iteritems() if count > 0)
		for instance in ondemandInstances:
			print "%2d Instance type %12s in AZ %s in VPC(%6s) is running on demand mode" %(runningInstances[instance],instance[1],instance[0], instance[2])
	return isUsedUp

def getRunningInstance(region,vpconly=True):
	client = boto3.client('ec2',region_name=region)
	runningInstanceCounter = dict()
	instances = client.describe_instances(
	    Filters=[{'Name': 'instance-state-name', 'Values': ['running']}])['Reservations']
	for instance in instances:
		instanceTypeAndAZ = (instance['Instances'][0]['Placement']['AvailabilityZone'],instance['Instances'][0]['InstanceType'],  vpconly or "VpcId" in instance['Instances'][0])
		runningInstanceCounter[instanceTypeAndAZ] = runningInstanceCounter.get(instanceTypeAndAZ,0) + 1
	return runningInstanceCounter


def getReservedInstance(region,vpconly=True):
	client = boto3.client('ec2',region_name=region)
	reservedInstances = client.describe_reserved_instances()['ReservedInstances']
	reservedInstancesCounter = dict()
	for instances in reservedInstances:
		reservedTypeAndAZ = (instances['AvailabilityZone'],instances['InstanceType'], vpconly or "VPC" in instances['ProductDescription'] )
		reservedInstancesCounter[reservedTypeAndAZ] = reservedInstancesCounter.get(reservedTypeAndAZ,0) + instances['InstanceCount']
	return reservedInstancesCounter

def usage():
	print "./getReservedInstanceReport.py"

if __name__ == "__main__":
	if len(sys.argv) != 1 :
		usage()
		sys.exit(-1)
	if main():
		sys.exit(0)
	else:
		sys.exit(-100)