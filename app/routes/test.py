import json

dct = '{"room": "0000"}'
dct = json.loads(dct)
print(dct['room'])