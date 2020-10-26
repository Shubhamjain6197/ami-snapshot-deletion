# ami-snapshot-deletion

This repo to keep the python script that deregister entered AMI and delete associated snapshot

  Script takes two inputs.

    AWS Region -
    Images Ids - ami-1233,ami-3422

Note - Script will check all the running instances and and compare the images with ami's user provided as input.
       Script will only delete available amis and leave ami's associated with instance.
