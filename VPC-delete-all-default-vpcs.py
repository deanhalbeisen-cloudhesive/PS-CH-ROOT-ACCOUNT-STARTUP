import boto3

def delete_default_vpcs():
    # Create a session using your current credentials
    session = boto3.Session()

    # Create an EC2 client
    ec2_client = session.client('ec2')

    # Get all regions that work with EC2
    regions = [region['RegionName'] for region in ec2_client.describe_regions()['Regions']]

    # Iterate over each region
    for region in regions:
        print(f"Checking region: {region}")

        # Create an EC2 client for each region
        regional_ec2 = session.client('ec2', region_name=region)

        # Find the default VPC
        vpcs = regional_ec2.describe_vpcs(Filters=[{'Name': 'isDefault', 'Values': ['true']}])
        default_vpcs = vpcs['Vpcs']

        # If a default VPC exists, delete it
        if default_vpcs:
            vpc_id = default_vpcs[0]['VpcId']
            print(f"Deleting default VPC {vpc_id} in region {region}")

            # Delete the VPC
            regional_ec2.delete_vpc(VpcId=vpc_id)
        else:
            print(f"No default VPC found in region {region}")

if __name__ == "__main__":
    delete_default_vpcs()
