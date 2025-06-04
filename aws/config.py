import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_dynamodb_resource():
    # Debug: Print environment variables
    print("AWS Configuration:")
    print(f"AWS_REGION: {os.getenv('AWS_REGION')}")
    
    # Safely print AWS access key ID with null check
    aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
    if aws_access_key:
        print(f"AWS_ACCESS_KEY_ID: {aws_access_key[:5]}...")  # Only show first 5 chars for security
    else:
        print("AWS_ACCESS_KEY_ID: Not set")
    
    print(f"AWS_SECRET_ACCESS_KEY: {'*' * 5}...")  # Hide secret key
    
    return boto3.resource(
        'dynamodb',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    ) 