import boto3

# Initialize a DynamoDB resource
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')

# List all tables
tables = dynamodb.tables.all()
for table in tables:
    print(table.name)