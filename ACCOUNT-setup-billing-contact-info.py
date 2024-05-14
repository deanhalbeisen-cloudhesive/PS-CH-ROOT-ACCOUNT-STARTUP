import boto3

# Initialize a boto3 client
client = boto3.client('account')

def update_contact(contact_type, name, title, email, phone_number):
    try:
        response = client.put_alternate_contact(
            AccountId='123456789012',  # Specify the AWS Account ID
            AlternateContactType=contact_type,  # 'BILLING', 'OPERATIONS', or 'SECURITY'
            Name=name,
            Title=title,
            EmailAddress=email,
            PhoneNumber=phone_number
        )
        print(f'Successfully updated {contact_type} contact:', response)
    except Exception as e:
        print(f'Failed to update {contact_type} contact:', e)

# Example usage
update_contact(
    contact_type='BILLING',
    name='Cloudhesive Managed Services',
    title='Account Owner',
    email='msp@cloudhesive.com',
    phone_number='18008602040'
)
