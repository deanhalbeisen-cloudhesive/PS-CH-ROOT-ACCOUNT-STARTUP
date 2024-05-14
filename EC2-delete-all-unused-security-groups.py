import boto3

def delete_unused_security_groups():
    # Create a Boto3 session using your current credentials
    session = boto3.Session()

    # Initialize an EC2 client to list all regions
    ec2_client = session.client('ec2')

    # Retrieve all AWS regions where EC2 is available
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    # Loop through each region to handle security groups regionally
    for region in regions:
        print(f"Processing region: {region}")
        regional_ec2 = session.client('ec2', region_name=region)

        # Gather all security groups in the region
        all_sgs = regional_ec2.describe_security_groups()['SecurityGroups']
        used_sg_ids = set()

        # Collect IDs of security groups used by EC2 instances
        instances = regional_ec2.describe_instances()
        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                for sg in instance['SecurityGroups']:
                    used_sg_ids.add(sg['GroupId'])

        # Collect IDs of security groups used by network interfaces
        network_interfaces = regional_ec2.describe_network_interfaces()
        for ni in network_interfaces['NetworkInterfaces']:
            for sg in ni['Groups']:
                used_sg_ids.add(sg['GroupId'])

        # Attempt to delete each security group that is not used
        for sg in all_sgs:
            if sg['GroupId'] not in used_sg_ids and not sg['GroupName'] == 'default':
                try:
                    print(f"Deleting unused security group: {sg['GroupId']} ({sg['GroupName']})")
                    regional_ec2.delete_security_group(GroupId=sg['GroupId'])
                except Exception as e:
                    print(f"Could not delete security group {sg['GroupId']}: {e}")

if __name__ == "__main__":
    delete_unused_security_groups()
