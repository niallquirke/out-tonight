import json
from dynamodb_client import DynamoDBClient


def out_tonight_handler(event, context):
    response = {'message': 'Invalid request'}
    db_client = DynamoDBClient()

    if event['queryStringParameters']:
        if ('name' and 'out') in event['queryStringParameters']:
            name = event['queryStringParameters']['name']
            out = event['queryStringParameters']['out']
            db_client.add_person(name, out)
            response = {'message': 'Successfully added new person'}

    else:
        response = {'out-tonight': db_client.get_people()}

    return {
        "statusCode": 200,
        "body": json.dumps(response, indent=4),
    }
