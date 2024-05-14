import boto3
import json

def create_cloudhesive_role():
    iam = boto3.client('iam')
    
    # Assume role policy document (trust relationship)
    assume_role_policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {
                    "AWS": "arn:aws:iam::632958987962:root"
                },
                "Action": "sts:AssumeRole"
            }
        ]
    }

    # Inline policy document
    policy_document = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Action": "*",
                "Resource": "*",
                "Effect": "Allow",
                "Sid": "CloudHesiveCrossAccountRolev1"
            }
        ]
    }

    # Create the IAM role with the assume role policy
    try:
        role = iam.create_role(
            Path='/',
            RoleName='CloudHesive-Management',
            AssumeRolePolicyDocument=json.dumps(assume_role_policy_document),
            Description='Cross account role for "CloudHesive"'
        )
        print(f"Role created successfully: {role['Role']['Arn']}")

        # Put the inline policy
        iam.put_role_policy(
            RoleName='CloudHesive-Management',
            PolicyName='CloudHesiveAccessPolicy',
            PolicyDocument=json.dumps(policy_document)
        )
        print("Inline policy added successfully.")
        
        return role['Role']['Arn']
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Create the role and output the ARN
role_arn = create_cloudhesive_role()
if role_arn:
    print(f"The ARN of the created role is: {role_arn}")
