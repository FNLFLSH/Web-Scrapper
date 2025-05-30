from aws.config import get_dynamodb_resource
import uuid
from datetime import datetime

dynamodb = get_dynamodb_resource()
table = dynamodb.Table('horizon_articles')

def save_article(article):
    try:
        article['article_id'] = str(uuid.uuid4())
        article['scraped_at'] = datetime.utcnow().isoformat()
        print(f"\nSaving article to DynamoDB:")
        print(f"Title: {article['title']}")
        print(f"Category: {article['category']}")
        print(f"Article ID: {article['article_id']}")
        
        response = table.put_item(Item=article)
        print(f"Successfully saved article to DynamoDB")
        return True
    except Exception as e:
        print(f"Error saving article to DynamoDB: {str(e)}")
        return False

def save_bulk(articles):
    success_count = 0
    for a in articles:
        if save_article(a):
            success_count += 1
    
    print(f"\nSaved {success_count} out of {len(articles)} articles to DynamoDB") 