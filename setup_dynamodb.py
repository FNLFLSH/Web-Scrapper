import boto3
from aws.config import get_dynamodb_resource

def create_dynamodb_table():
    dynamodb = get_dynamodb_resource()
    
    try:
        table = dynamodb.create_table(
            TableName='horizon_articles',
            KeySchema=[
                {
                    'AttributeName': 'article_id',
                    'KeyType': 'HASH'  # Partition key
                },
                {
                    'AttributeName': 'category',
                    'KeyType': 'RANGE'  # Sort key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'article_id',
                    'AttributeType': 'S'  # String type
                },
                {
                    'AttributeName': 'category',
                    'AttributeType': 'S'  # String type
                },
                {
                    'AttributeName': 'scraped_at',
                    'AttributeType': 'S'  # String type
                }
            ],
            BillingMode='PAY_PER_REQUEST',  # On-demand capacity
            GlobalSecondaryIndexes=[
                {
                    'IndexName': 'CategoryIndex',
                    'KeySchema': [
                        {
                            'AttributeName': 'category',
                            'KeyType': 'HASH'
                        },
                        {
                            'AttributeName': 'scraped_at',
                            'KeyType': 'RANGE'
                        }
                    ],
                    'Projection': {
                        'ProjectionType': 'ALL'
                    }
                }
            ]
        )
        
        # Wait for table to be created
        table.meta.client.get_waiter('table_exists').wait(TableName='horizon_articles')
        print("Table 'horizon_articles' created successfully!")
        
    except dynamodb.meta.client.exceptions.ResourceInUseException:
        print("Table 'horizon_articles' already exists.")
    except Exception as e:
        print(f"Error creating table: {str(e)}")

if __name__ == "__main__":
    create_dynamodb_table() 