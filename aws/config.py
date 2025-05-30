import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_dynamodb_resource():
    # Debug: Print environment variables
    print("AWS Configuration:")
    print(f"AWS_REGION: {os.getenv('AWS_REGION')}")
    print(f"AWS_ACCESS_KEY_ID: {os.getenv('AWS_ACCESS_KEY_ID')[:5]}...")  # Only show first 5 chars for security
    print(f"AWS_SECRET_ACCESS_KEY: {'*' * 5}...")  # Hide secret key
    
    return boto3.resource(
        'dynamodb',
        region_name=os.getenv('AWS_REGION'),
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    ) 