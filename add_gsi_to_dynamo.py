import boto3

dynamodb = boto3.client('dynamodb', 
                        endpoint_url='http://localhost:8000',
                        aws_access_key_id='dummy',
                        aws_secret_access_key='dummy',
                        region_name='us-east-1')

response = dynamodb.update_table(
    TableName='Topps1989',
    AttributeDefinitions=[
        {
            'AttributeName': 'PlayerName',
            'AttributeType': 'S'  # String
        }
    ],
    GlobalSecondaryIndexUpdates=[
        {
            'Create': {
                'IndexName': 'PlayerNameIndex',
                'KeySchema': [
                    {
                        'AttributeName': 'PlayerName',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                'Projection': {
                    'ProjectionType': 'ALL'
                },
                'ProvisionedThroughput': {
                    'ReadCapacityUnits': 5,
                    'WriteCapacityUnits': 5
                }
            }
        }
    ]
)

print("GSI status:", response)
