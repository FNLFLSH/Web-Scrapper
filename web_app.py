from flask import Flask, render_template, request
from aws.config import get_dynamodb_resource
from config.categories import CATEGORIES
import boto3
from boto3.dynamodb.conditions import Key

app = Flask(__name__)
dynamodb = get_dynamodb_resource()
table = dynamodb.Table('horizon_articles')

@app.route('/')
def index():
    # Get all categories
    categories = CATEGORIES
    
    # Get selected category from query parameter
    selected_category = request.args.get('category', 'all')
    
    # Query articles
    if selected_category == 'all':
        response = table.scan(Limit=50)
    else:
        response = table.query(
            IndexName='CategoryIndex',
            KeyConditionExpression=Key('category').eq(selected_category),
            Limit=50
        )
    
    articles = response.get('Items', [])
    
    return render_template('index.html', 
                         articles=articles,
                         categories=categories,
                         selected_category=selected_category)

if __name__ == '__main__':
    app.run(debug=True, port=5000) 