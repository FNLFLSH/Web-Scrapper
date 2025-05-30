#!/bin/bash
echo "[1/5] Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "[2/5] Installing requirements..."
pip install -r requirements.txt

echo "[3/5] Creating DynamoDB table..."
python setup_dynamodb.py

echo "[4/5] Running scraper..."
python main.py

echo "[5/5] Done. Check your DynamoDB table!" 