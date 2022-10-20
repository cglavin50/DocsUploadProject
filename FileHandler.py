import logging
import boto3
from botocore.exceptions import ClientError
import os
import csv


def create_bucket(bucket_name, region=None):
    """Create an S3 bucket in a specified region

    If a region is not specified, the bucket is created in the S3 default
    region (us-east-1).

    :param bucket_name: Bucket to create
    :param region: String region to create bucket in, e.g., 'us-west-2'
    :return: True if bucket created, else False
    """

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=bucket_name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


# end s3 bucket creation


# goal of this page is to reorganize the boto3 upload such that I can use it for my personal project

def newDirectory(path):
    try:
        os.mkdir(path)
    except OSError as error:
        print(error)


# end make new directory


# in readme tell user to download access key file (keep default name rootkey.csv) from aws, and keep in the active
# directory, can always add more functionality later
# after initial testing, this function works properly
def getKeys():  # could pass in location to get, again later functionality
    keyFile = open("rootkey.csv", 'r')  # creates file object, opens cwd/rootkey.csv
    # can use os.chdir to change default directory for open, or just pass in argument, useful for later functionality
    # changes

    csvreader = csv.reader(keyFile)  # create cvs file reader
    access_key_id = csvreader.__next__()[0]
    secret_access_key = csvreader.__next__()[0]

    access_key_id = access_key_id.split('=')[1]  # should split on the =, so AWSACCESS...=Key
    secret_access_key = secret_access_key.split('=')[1]

    # remember to close the file
    keyFile.close()

    return access_key_id, secret_access_key


# end getKeys

# success, everything seems to upload properly
def upload_bucket(keys):
    # first step to using boto3 is creating a session, for which you need an access key and secret access key
    # create the boto3 aws session
    session = boto3.Session(
        aws_access_key_id=keys[0],
        aws_secret_access_key=keys[1]
    )
    # next, get s3 and bucket
    bucket_name = 'document-storage-personal-project'  # customize, can get passed in as a param as well
    s3 = session.resource('s3')  # define the resource you want to use (will throw error if not accessible I assume)
    goal_bucket = s3.Bucket(bucket_name)

    files = os.listdir()  # using default location, again customize later
    types = ["txt",
             "py",
             ".csv"]  # customize later to accept what types of files the user wants to send, removing . for split
    # functions in loop

#    for file in files:
#        print(file)
#    print("End list of files in cwd")
    print("Now printing files to upload")

    for file in files:
        if '.' not in file:
            continue

        type = file.split('.')[
            1]  # each file name should only have one period by convention, and type will follow afterwards
        if type in types:
            print(file)
            # will likely need to convert from \ to /, do later!!
            # don't believe that upload_file needs it to be open according to api
            result = goal_bucket.upload_file(file, file)  # passing in the same name to upload and download
            # for logging purposes, doesn't seem to be working and causing issues, leave out for now
            # print("Upload result: " + result)
    # end for

    print("Done uploading files")


# end main


def download_bucket(keys):  # assuming downloading all files from hard-coded bucket, can add in params later
    session = boto3.Session(
        aws_access_key_id=keys[0],
        aws_secret_access_key=keys[1]
    )
    bucket_name = 'document-storage-personal-project'  # customize, can get passed in as a param as well
    s3 = session.resource('s3')  # define the resource you want to use (will throw error if not accessible I assume)
    goal_bucket = s3.Bucket(bucket_name)

    print("Printing objects in bucket")
    for file in goal_bucket.objects.all():
        print(file.key)
    print("Done listing bucket objects")

    proj = [ "main.py", "Doc.py", "FileHandler.py"]

    for temp_doc in goal_bucket.objects.all():
        filename = temp_doc.key
        if filename in proj:
            continue
        else:
            goal_bucket.download_file(filename, filename)
    # end for
# end download bucket
