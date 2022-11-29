import logging

from botocore.exceptions import ClientError
import json
import time
import boto3


# taking the input from user where want to create internet gateway 
REGION= input("Please, Enter the region name where you want to Delete this NACL:- ")

client = boto3.client("ec2", region_name=REGION)

# setup the logger config
logger_info = logging.getLogger()

logging.basicConfig(level=logging.INFO,format=' %(message)s')

# function to describe the internet gateway to the VPC

def describe_internet_gateways(tag, value, maximum):

    try:
        # Object for describe_internet_gateways() 

        paginator = client.get_paginator('describe_internet_gateways')

        response_iterator = paginator.paginate(
            Filters=[{ 

                'Name': f'tag:{tag}',

                'Values': value
            }],

            PaginationConfig={'MaxItems': maximum})

        result = response_iterator.build_full_result()

        list = []

        for i in result['InternetGateways']:
            list.append(i)

    except ClientError:
        logger_info.exception('Sorry, We are not able to featch your Internet Gateways details.')
        raise

    else:
        return list


if __name__ == '__main__': 

    # taking input from the user for tag
    TAG_NAME = input("Please, Enter the tag")

    # tag value input
    TAG_VALUE = ['test-nacl-igw']

    #limit
    MAXIMUM = 10

    internet_gateways = describe_internet_gateways(TAG_NAME, TAG_VALUE, MAXIMUM)

    for i in range(3):
        logger_info.info(f'Please wait ......  \n We are featching  your internet gateway details....\U0001F570')
        time.sleep(3)     
    logger_info.info('Hurry, Here is your Internet Gateways Details:  \U0001F44D ')

    for internet_gateway in internet_gateways:
        
        logger_info.info(json.dumps(internet_gateway, indent=4) + '\n')