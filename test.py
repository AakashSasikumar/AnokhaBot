import json

with open('context.json') as jsonData:
    context = json.load(jsonData)

strr = "inc-asdfasdf"

print(strr[3:])