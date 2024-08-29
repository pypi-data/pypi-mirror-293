import boto3

def is_instance_running(instance_id, profile_name, region_name):
    session = boto3.Session(region_name=region_name, profile_name=profile_name)
    ec2 = session.client('ec2')
    response = ec2.describe_instance_status(InstanceIds=[instance_id])
    return len(response['InstanceStatuses']) != 0 and response['InstanceStatuses'][0]['InstanceState']['Name'] == "running"

def start_instance(instance_id, profile_name, region_name):
    session = boto3.Session(region_name=region_name, profile_name=profile_name)
    ec2 = session.client('ec2')
    response = ec2.start_instances(InstanceIds=[instance_id])
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])