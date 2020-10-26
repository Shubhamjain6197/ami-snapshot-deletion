# ami-snapshot-deletion

Python script that deregister entered AMI and delete associated snapshot

  Script takes two inputs.

    AWS Region - any aws region (us-east-1)
    Images Ids - ami-1233,ami-3422

Note - Script will check all the running instances and and compare the images with ami's user provided as input.
       Script will only delete available amis and leave ami's associated with instance.
