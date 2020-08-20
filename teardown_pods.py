import boto3
import os

iam_client = boto3.client('iam')

PODS_USER = os.environ['PODS_USER']
RESOURCE_NAME = f'PODS_{PODS_USER}'

iam_client.remove_user_from_group(
    GroupName=RESOURCE_NAME,
    UserName=PODS_USER
)
print(f'=== Teardown: Removed user {PODS_USER} from group {RESOURCE_NAME}')

iam_client.delete_user(
    UserName=PODS_USER
)
print('=== Teardown: Deleted user')

iam_client.delete_group_policy(
    GroupName=RESOURCE_NAME,
    PolicyName=f'LightsailFullAccessFor{PODS_USER}'
)
print('=== Teardown: Deleted group policy')

iam_client.delete_group(
    GroupName=f'PODS_{PODS_USER}',
)
print('=== Teardown: Deleted group')



lightsail_client = boto3.client('lightsail')

lightsail_client.detach_static_ip(
    staticIpName=f'{RESOURCE_NAME}_Static_IP'
)
print('=== Teardown: Detatched static ip')

lightsail_client.release_static_ip(
    staticIpName=f'{RESOURCE_NAME}_Static_IP'
)
print('=== Teardown: Released static ip')

lightsail_client.delete_instance(
    instanceName=RESOURCE_NAME,
    forceDeleteAddOns=True
)
print('=== Teardown: Deleted lightsail instance')
