const express = require('express');
const AWS = require('aws-sdk');
const app = express();
const port = 3000;

// Configure AWS SDK for DynamoDB
AWS.config.update({
  region: 'us-east-1',
  endpoint: 'http://localhost:8000',
  accessKeyId: 'dummy',
  secretAccessKey: 'dummy'
});

const dynamodb = new AWS.DynamoDB.DocumentClient();

// Serve static files (like HTML, CSS, and JS)
app.use(express.static('public'));

// API endpoint to retrieve card data based on search criteria
app.get('/api/cards', (req, res) => {
  const { cardNumber, playerName } = req.query;

  if (cardNumber) {
    const params = {
      TableName: 'Topps1989',
      Key: { CardNumber: cardNumber }
    };

    dynamodb.get(params, (err, data) => {
      if (err) {
        console.error('Error retrieving data:', err);
        res.status(500).send('Error retrieving data.');
        return;
      }
      res.json(data.Item ? [data.Item] : []);
    });
  } else if (playerName) {
    const params = {
      TableName: 'Topps1989',
      IndexName: 'PlayerNameIndex',
      KeyConditionExpression: 'PlayerName = :playerName',
      ExpressionAttributeValues: {
        ':playerName': playerName
      }
    };

    dynamodb.query(params, (err, data) => {
      if (err) {
        console.error('Error retrieving data:', err);
        res.status(500).send('Error retrieving data.');
        return;
      }
      console.log('Query Result:', data.Items); // Add this line for debugging
      res.json(data.Items);
    });
  } else {
    res.status(400).send('Invalid query parameters.');
  }
});

// Start the server
app.listen(port, () => {
  console.log(`Server is running on http://localhost:${port}`);
});
