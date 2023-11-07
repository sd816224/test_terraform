import json
from pprint import pprint
f=open('mock_json/address.json')
content=json.load(f)
for row in content['address']:

    print(row['address_line_2'],type(row['address_line_2']))
