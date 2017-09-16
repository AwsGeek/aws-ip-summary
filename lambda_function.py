from __future__ import print_function

import os
import json
import boto3
import urllib

def count_ipv4_addresses(ranges):
    count = 0
    for range in ranges:
        count += (1<<(32-int(range.split("/")[-1])))
        
    return count

def get_ipv4_ranges(data):
    ranges = [] 
    response = json.loads(data)
    for k in response['prefixes']:
        ranges.append(k['ip_prefix'])

    return ranges

def get_ipv4_info(data):
    ranges = get_ipv4_ranges(data)
    range_count = len(ranges)
    address_count = count_ipv4_addresses(ranges)
    return {'ranges': ranges, 'range_count': range_count, 'address_count': address_count}
    
def lambda_handler(event, context):
    
    current_data = urllib.request.urlopen('https://ip-ranges.amazonaws.com/ip-ranges.json').read()
    current_info  = get_ipv4_info(current_data)
    
    s3 = boto3.resource('s3')
    previous_data = s3.Object(os.environ['s3_bucket'], os.environ['s3_key']).get()['Body'].read()
    previous_info  = get_ipv4_info(previous_data)

    s3.Bucket(os.environ['s3_bucket']).put_object(Key=os.environ['s3_key'], Body=current_data)

    message = "AWS IPv4 Address Summary: "
    message += "Ranges: %s, " % current_info['range_count']
    message += "Addresses: %s, " % current_info['address_count']
    
    added = len(list(set(current_info['ranges']) - set(previous_info['ranges'])))
    message += "Added: %s, " % added
    
    removed = len(list(set(previous_info['ranges']) - set(current_info['ranges'])))
    message += "Removed: %s" % removed

    sns = boto3.client('sns')
    sns.publish(
        TargetArn=os.environ['sns_topic'],
        Message=message
    )
        
    return message