from flask import Flask, request, jsonify
from flask_cors import CORS
import boto3
from boto3.dynamodb.conditions import Attr

app = Flask(__name__)
CORS(app)  # This will allow requests from any origin

# Connect to local DynamoDB
dynamodb = boto3.resource('dynamodb', 
                          endpoint_url='http://localhost:8000',
                          aws_access_key_id='dummy',
                          aws_secret_access_key='dummy',
                          region_name='us-east-1',
                          use_ssl=False)

table = dynamodb.Table('Topps1989')

# Route to save a card
@app.route('/api/save-card', methods=['POST'])
def save_card():
    data = request.json
    if not all(k in data for k in ('cardNumber', 'playerName', 'teamName')):
        return jsonify({'error': 'Missing data'}), 400

    table.put_item(
        Item={
            'CardNumber': data['cardNumber'],
            'PlayerName': data['playerName'],
            'TeamName': data['teamName']
        }
    )
    return jsonify({'message': 'Card saved successfully!'}), 200

# Route to search for cards
@app.route('/api/search-card', methods=['GET'])
def search_card():
    card_number = request.args.get('cardNumber')
    player_name = request.args.get('playerName')
    
    if card_number:
        response = table.get_item(Key={'CardNumber': card_number})
        item = response.get('Item', {})
        return jsonify([item]) if item else jsonify([])
    
    if player_name:
        response = table.scan(
            FilterExpression=Attr('PlayerName').eq(player_name)
        )
        items = response.get('Items', [])
        return jsonify(items)
    
    return jsonify([]), 400

# Route to update card fields
@app.route('/api/cards/<card_number>', methods=['PUT'])
def update_card(card_number):
    data = request.json
    
    # Find the card by card_number
    response = table.get_item(Key={'CardNumber': card_number})
    card = response.get('Item')
    
    if card:
        # Update fields
        update_expression = "SET Quantity = :q, Quality = :ql, BaseCard = :bc, #p = :p"
        expression_values = {
            ':q': data.get('Quantity', card.get('Quantity', 'UNKNOWN')),
            ':ql': data.get('Quality', card.get('Quality', 'UNKNOWN')),
            ':bc': data.get('BaseCard', card.get('BaseCard', 'UNKNOWN')),
            ':p': data.get('Parallel', card.get('Parallel', 'UNKNOWN'))
        }
        
        response = table.update_item(
            Key={'CardNumber': card_number},
            UpdateExpression=update_expression,
            ExpressionAttributeNames={
                '#p': 'Parallel'  # Using placeholder for reserved keyword
            },
            ExpressionAttributeValues=expression_values,
            ReturnValues="UPDATED_NEW"
        )
        
        return jsonify({'message': 'Card updated successfully!', 'updatedAttributes': response.get('Attributes')}), 200
    else:
        return jsonify({'error': 'Card not found'}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)