#!/usr/bin/python

#delete the previous snapshot
#create the snapshot
#make sure the snapshot is created
import boto3
import sys
import time

def checkingSnapshot(dbname,releaseVersion):
	client = boto3.client('rds')
	timeout = 600
	starttime = 0
	step = 10
	while starttime < timeout:
		response = client.describe_db_snapshots(DBInstanceIdentifier=dbname,
		DBSnapshotIdentifier="%s-pre-%s" %(dbname,releaseVersion), 
		SnapshotType='manual')
		if response['DBSnapshots'][0]['Status'] == "available" : 
			return 0
		print "snapshoting in progress ..."
		time.sleep(step)
	return -1


def deletePreviousSnapshot(dbname,releaseVersion):
	client = boto3.client('rds')

	snapshots = client.describe_db_snapshots(
	    DBInstanceIdentifier=dbname,
	    SnapshotType='manual',
	)

	for snapshot in snapshots['DBSnapshots']:
		if snapshot['DBSnapshotIdentifier'].startswith(dbname) \
			and not snapshot['DBSnapshotIdentifier'] == "%s-pre-%s" %(dbname,releaseVersion): 
			deleteresponse = client.delete_db_snapshot(
				DBSnapshotIdentifier=snapshot['DBSnapshotIdentifier']
				)

def createPreReleaseSnapshot(dbname,releaseVersion):
	client = boto3.client('rds')
	response = client.create_db_snapshot(
		DBSnapshotIdentifier="%s-pre-%s" %(dbname,releaseVersion),
		DBInstanceIdentifier=dbname,
		Tags=[
			{
				'Key': 'purpose',
				'Value': 'Release-Pre-Snapshot'
			},
		]
	)
	return response


def usage():
	print "Usage: snapshot.py dbname releaseVersion"

def main(args):
	dbname = args[0]
	releaseVersion = args[1]
	createPreReleaseSnapshot(dbname,releaseVersion)
	if (checkingSnapshot(dbname,releaseVersion) <> 0):
		print "snapshot is not create"
		sys.exit(-2)
	deletePreviousSnapshot(dbname,releaseVersion)


if __name__ == "__main__":
	if len(sys.argv) != 3 :
		usage()
		sys.exit(-1)
	main(sys.argv[1:])
