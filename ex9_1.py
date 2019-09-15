import requests
from sys import argv
import json

url = 'https://api.github.com/users/pymivn/repos'

resp = requests.get(url)
data = json.loads(resp.text)
imput_cmd = argv
result = []
for username in imput_cmd[1:]:
    for d in data:
        if d['name'].strip().lower() == username.strip().lower():
            try:
                notification = username + ': '+ d['owner']['repos_url']
                result.append(notification)
            except KeyError:
                notification = username + " doesn't have any repo "
                result.append(notification)
        else:
            notification = username + ': ' + 'is not match'
            
print(result)