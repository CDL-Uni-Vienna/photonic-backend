import requests
import json

url = "https://quco.exp.univie.ac.at/api/login"

payload = json.dumps({
    "username": "test@test.at",
    "password": "test"
})
headers = {
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=j3G9nCYFFI9TZJIFbygCkxdLfB9TzwKYXqa8F2dh7LJDzmLGbH4DM0ngA1vARG7w; sessionid=0qgcg0qct8i1sojuxzwuwsgn4miyxxyb'
}

response = requests.request(
    "POST", url, headers=headers, data=payload, verify=False)

print(response.text)
