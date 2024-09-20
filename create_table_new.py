import boto3

# Initialize DynamoDB client for local instance
dynamodb = boto3.resource('dynamodb', 
                          endpoint_url='http://localhost:8000',
                          aws_access_key_id='dummy',
                          aws_secret_access_key='dummy',
                          region_name='us-east-1',
                          use_ssl=False)

# Define table schema
table_name = 'Topps1989'  # Replace with your desired table name
key_schema = [
    {
        'AttributeName': 'CardNumber',
        'KeyType': 'HASH'  # Partition key
    }
]
attribute_definitions = [
    {
        'AttributeName': 'CardNumber',
        'AttributeType': 'S'
    }
]

# Create the table
table = dynamodb.create_table(
    TableName=table_name,
    KeySchema=key_schema,
    AttributeDefinitions=attribute_definitions,
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

print("Creating table...")
table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
print("Table created.")