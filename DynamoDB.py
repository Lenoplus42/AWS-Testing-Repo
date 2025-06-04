import boto3

# Create a DynamoDB resource
session = boto3.Session(profile_name="LenoDev")
dynamodb = session.resource('dynamodb')
sts = session.client("sts")

identity = sts.get_caller_identity()
print("AWS Identity:", identity)

# Create a table
table_name = 'HelloWorldTable'
try:
    table = dynamodb.create_table(
        TableName=table_name,
        KeySchema=[
            {'AttributeName': 'id', 'KeyType': 'HASH'}  # Partition key
        ],
        AttributeDefinitions=[
            {'AttributeName': 'id', 'AttributeType': 'S'}
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 1,
            'WriteCapacityUnits': 1
        }
    )
    print("Creating table...")
    table.meta.client.get_waiter('table_exists').wait(TableName=table_name)
except dynamodb.meta.client.exceptions.ResourceInUseException:
    table = dynamodb.Table(table_name)
    print("Table already exists.")

# Put item
table.put_item(
    Item={
        'id': '123',
        'message': 'Hello, DynamoDB!'
    }
)

# Get item
response = table.get_item(Key={'id': '123'})
item = response.get('Item')
print("Retrieved item:", item)
