import boto3

TABLE_NAME = 'out-tonight-OutTonightTable-2YVAC6KD6N4N'


class DynamoDBClient:

    def __init__(self):
        self.client = boto3.client('dynamodb')

    def get_people(self):
        people = {}
        dynamo_json = self.client.scan(TableName=TABLE_NAME)

        for item in dynamo_json['Items']:
            group = self.unmarshal_dynamodb_json(item)
            people[group['out_or_not']] = group['names']

        return people

    def add_person(self, name, out):
        print(name, out)
        if out == ('true' or 'True'):
            out = 'out'
        else:
            out = 'not'
        print(out)
        group = self.get_people()[out]
        print(group)
        group.append(name)
        print(group)
        self.client.put_item(
            TableName=TABLE_NAME,
            Item=self.ddb_person(group, out)
        )

    def ddb_person(self, group, out):
        names = []

        for person in group:
            names.append({'S': person})

        return {
            'out_or_not': {'S': out},
            'names': {'L': names}
        }

    def unmarshal_dynamodb_json(self, node):
        data = dict({})
        data['M'] = node
        return self._unmarshal_value(data)

    def _unmarshal_value(self, node):
        if type(node) is not dict:
            return node
        for key, value in node.items():
            key = key.lower()
            if key == 'bool':
                return value
            if key == 'null':
                return None
            if key == 's':
                return value
            if key == 'n':
                if '.' in str(value):
                    return float(value)
                return int(value)
            if key in ['m', 'l']:
                if key == 'm':
                    data = {}
                    for key1, value1 in value.items():
                        if key1.lower() == 'l':
                            data = [self._unmarshal_value(n) for n in value1]
                        else:
                            if type(value1) is not dict:
                                return self._unmarshal_value(value)
                            data[key1] = self._unmarshal_value(value1)
                    return data
                data = []
                for item in value:
                    data.append(self._unmarshal_value(item))
                return data
