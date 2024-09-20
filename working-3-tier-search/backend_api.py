from flask import Flask, jsonify, request
from flask_cors import CORS
import boto3
from boto3.dynamodb.conditions import Key

app = Flask(__name__)
CORS(app)  # This will allow all origins by default

# Connect to local DynamoDB
dynamodb = boto3.resource('dynamodb', 
                          endpoint_url='http://localhost:8000',
                          aws_access_key_id='dummy',
                          aws_secret_access_key='dummy',
                          region_name='us-east-1',
                          use_ssl=False)

table = dynamodb.Table('Topps1989')

@app.route('/api/cards', methods=['GET'])
def get_cards():
    player_name = request.args.get('playerName')
    card_number = request.args.get('cardNumber')

    response_data = []

    if player_name:
        print(f"Searching by player name: {player_name}")
        try:
            response = table.query(
                IndexName='PlayerNameIndex',
                KeyConditionExpression=Key('PlayerName').eq(player_name)
            )
            response_data = response['Items']
        except Exception as e:
            print(f"Error querying by player name: {e}")

    elif card_number:
        print(f"Searching by card number: {card_number}")
        try:
            response = table.query(
                KeyConditionExpression=Key('CardNumber').eq(card_number)
            )
            response_data = response['Items']
        except Exception as e:
            print(f"Error querying by card number: {e}")

    return jsonify(response_data)

if __name__ == '__main__':
    app.run(debug=True, port=5001)
