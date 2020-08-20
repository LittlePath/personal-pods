# If user is going to be running this on their own or from some User Interface...
# it might be easier to create something that is easily runnable from an API
# like a python script? rather than cloudformation/terraform which is more suited
# for pipeline environments/ machine users

# terraform is for things you want to keep the same? (like a database)
# rather than things you want to dynamically change (like the database content)

# Q: will user group - pods_user already exist? or is that something that is created for every user?

import boto3
import os
import time

PODS_USER = os.environ['PODS_USER']
RESOURCE_NAME = f'PODS_{PODS_USER}'

iam_client = boto3.client('iam')

# create group
group = iam_client.create_group(
    GroupName=RESOURCE_NAME
)

# add policy inline to group
response = iam_client.put_group_policy(
    GroupName=group['Group']['GroupName'],
    PolicyName=f'LightsailFullAccessFor{PODS_USER}',
    PolicyDocument='{ "Version": "2012-10-17","Statement": [{ "Effect": "Allow", "Action": [ "lightsail:*" ], "Resource": "*"}]}',
)

print('===Create PODS: Created group', group['Group']['GroupName'])

# create user
user = iam_client.create_user(
    UserName=PODS_USER,
    Tags=[
        {
            'Key': 'zoompp',
            'Value': 'True'
        },
    ]
)
print('===Create PODS: Created user', user['User']['UserName'])

response = iam_client.add_user_to_group(
    GroupName=group['Group']['GroupName'],
    UserName=PODS_USER
)

print(f'===Create PODS: Added user to group', group['Group']['GroupName'])


lightsail_client = boto3.client('lightsail')
#parameterize with script
availability_zone = 'us-east-1a' 
blueprint_id = 'ubuntu_18_04'
bundle_id = 'nano_2_0'

instance = lightsail_client.create_instances(
    instanceNames=[
        RESOURCE_NAME,
    ],
    availabilityZone=availability_zone,
    blueprintId=blueprint_id,
    bundleId=bundle_id,
    userData='echo "deb [trusted=yes] https://apt.fury.io/caddy/ /" | sudo tee -a /etc/apt/sources.list.d/caddy-fury.list && sudo apt update && sudo apt install caddy && sudo groupadd --system caddy && sudo useradd --system --gid caddy  --create-home --home-dir /var/lib/caddy --shell /usr/sbin/nologin --comment "Caddy web server" caddy',
    tags=[
        {
            'key': 'zoompp',
            'value': 'True'
        },
    ]
)

print('===Create PODS: Created lightsail instance')

# # set firewall port
# response = lightsail_client.put_instance_public_ports(
#     portInfos=[
#         {
#             'fromPort': 123,
#             'toPort': 123,
#             'protocol': 'tcp'|'all'|'udp'|'icmp',
#             'cidrs': [
#                 'string',
#             ],
#             'cidrListAliases': [
#                 'string',
#             ]
#         },
#     ],
#     instanceName='string'
# )

# provision static ip 
response = lightsail_client.allocate_static_ip(
    staticIpName=f'{RESOURCE_NAME}_Static_IP'
)
ip_name = response['operations'][0]['resourceName']
print(f'===Create PODS: Created static ip: {ip_name}')

print('===Create PODS: !!! Waiting for instance to be in a "Running" state in order to attach the static IP !!!')
time.sleep(10) #wait for lightsail intance to have status 'Running'. TODO: Implement exponention backoff
print('===Create PODS: !!! Waiting for instance to be in a "Running" state in order to attach the static IP !!!')
time.sleep(10) #wait for lightsail intance to have status 'Running'. TODO: Implement exponention backoff

response = lightsail_client.attach_static_ip(
    staticIpName=f'{RESOURCE_NAME}_Static_IP',
    instanceName=RESOURCE_NAME
)

static_ip= lightsail_client.get_static_ip( 
    staticIpName=f'{RESOURCE_NAME}_Static_IP'
)
static_ip_address = static_ip['staticIp']['ipAddress']
static_ip_address_instance = static_ip['staticIp']['attachedTo']

print(f'===Create PODS: Attached static ip {static_ip_address} to lightsail instance: {static_ip_address_instance}. Give it a few seconds for caddy to come up.')
