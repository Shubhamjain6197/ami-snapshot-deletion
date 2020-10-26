'''
Author - @Shubham Jain
Description - This scripts delates the ami and associated snapshots with it.
Inputs - Please pass region name and ami ids(n) as inputs.
'''

import boto3
import sys
import json
from botocore.exceptions import ClientError

region=input("\nPlease enter AWS region name : ")
images=input("\nPlease enter Image Ids : ").split(',')

def info():
    ec2 = boto3.client('ec2', region_name=region)
    print("\n\nGething Details -: \n\nGot {count} images to deregister {images} from {region} as input\n".format(images=images,count=len(images),region=region))
    response = ec2.describe_instances()
    inuse_image_list=[]
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            inuseimages=instance["ImageId"]
            inuse_image_list.append(inuseimages)
        
    inuse_image_list = list(dict.fromkeys(inuse_image_list))
    print("Fount {count} Inuse Images :-\n\n".format(count=len(inuse_image_list)),inuse_image_list,"\n\n")

    global unused_image_list
    unused_image_list = (set(images).difference(inuse_image_list))
    print("Found {count} Unused Images that can be deleted :-\n\n".format(count=len(unused_image_list)),unused_image_list,"\n\n")
    print("Describing Unused Images and Associated snapshots :-\n")
    for image in unused_image_list:
        try:
            response = ec2.describe_images(ImageIds=[image])
            response_dump=json.dumps(response)
            responses=json.loads(response_dump)
            for response in responses["Images"]: 
                for snapshots in response["BlockDeviceMappings"]:
                    snapshots_id= snapshots["Ebs"]["SnapshotId"]
                    snapshots_id=snapshots_id.split(" ")
                    print("Found {image} and {snapcount} associated {snapshots_id}\n".format(snapshots_id=snapshots_id,image=image,snapcount=len(snapshots_id)))
        except ClientError as e:
            print("Opps!!",e,"\n")
    return unused_image_list

def delt():
    print("\n-----------------------------\n\n")
    print("List of Images to Deregister :- \n\n",unused_image_list)
    ec2 = boto3.client('ec2', region_name=region)
    print("\n\nDeletion Started :-\n")
    for image in unused_image_list:
        try:
            response = ec2.describe_images(ImageIds=[image])
            response_dump=json.dumps(response)
            responses=json.loads(response_dump)
            for response in responses["Images"]: 
                for snapshots in response["BlockDeviceMappings"]:
                    snapshots_id= snapshots["Ebs"]["SnapshotId"]
                    snapshots_id=snapshots_id.split(" ")
                    for snapshot in snapshots_id:
                        amiResponse = ec2.deregister_image(DryRun=False,ImageId=image)
                        snap = ec2.delete_snapshot(SnapshotId=snapshot,DryRun=False)
                        print("Deregistering {image} and associated {snapshot}\n".format(image=image,snapshot=snapshot))
        except ClientError as e:
            print("Opps!!",e,"\n")     

#funtions
                   
info()  #funtion will provide details of all the ami and associated snapshots
delt()  #funtion will deregister/delete all the ami and associated snapshots

