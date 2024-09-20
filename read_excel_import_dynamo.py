import boto3
import pandas as pd

# Initialize DynamoDB client for local instance (no credentials needed)
dynamodb = boto3.resource('dynamodb', 
                          endpoint_url='http://localhost:8000',
                          aws_access_key_id='dummy',
                          aws_secret_access_key='dummy',
                          region_name='us-east-1',
                          use_ssl=False)

tables = dynamodb.tables.all()
table_names = [table.name for table in tables]
print("Existing tables:", table_names)


table = dynamodb.Table('Topps1989')  # Adjust based on your table name

# Read the CSV file
df = pd.read_csv('dynamo_topps1989.csv')  # Use the actual path to your CSV file

# Iterate through each row in the dataframe
for index, row in df.iterrows():
    # Dynamically handle empty cells (e.g., for team name)
    card_number = str(row['Card Number']) if pd.notna(row['Card Number']) else 'UNKNOWN'
    player_name = row['Player Name'] if pd.notna(row['Player Name']) else 'UNKNOWN'
    first_name = row['First Name'] if pd.notna(row['First Name']) else 'UNKNOWN'
    last_name = row['Last Name'] if pd.notna(row['Last Name']) else 'UNKNOWN'
    team_name = row['Team Name'] if pd.notna(row['Team Name']) else 'UNKNOWN'
    quantity = str(row['Quantity']) if pd.notna(row['Quantity']) else 'UNKNOWN'
    quality = row['Quality'] if pd.notna(row['Quality']) else 'UNKNOWN'
    base_card = row['Base Card'] if pd.notna(row['Base Card']) else 'UNKNOWN'

    # Check if the 'Parallel' column exists before accessing it
    if 'Parallel' in df.columns:
        parallel = row['Parallel'] if pd.notna(row['Parallel']) else 'UNKNOWN'
    else:
        parallel = 'UNKNOWN'

    # Insert each row into DynamoDB
    table.put_item(
        Item={
            'CardNumber': card_number,
            'PlayerName': player_name,
            'FirstName': first_name,
            'LastName': last_name,
            'TeamName': team_name,
            'Quantity': quantity,
            'Quality': quality,
            'BaseCard': base_card,
            'Parallel': parallel
        }
    )
    print(f"Inserted card {card_number} for player {player_name} into DynamoDB")

print("CSV import complete.")