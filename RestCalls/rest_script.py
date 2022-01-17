import requests
import json

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


url = "https://photonq.at/api/login"

payload = json.dumps({
    # "username": "test@test.at",
    # "password": "test"
    "username": "felix.zilk@univie.ac.at",
    "password": "rHHe6PdpX8xHszYD!Wp6b.3."
})
headers = {
    'Content-Type': 'application/json',
    'Cookie': 'csrftoken=j3G9nCYFFI9TZJIFbygCkxdLfB9TzwKYXqa8F2dh7LJDzmLGbH4DM0ngA1vARG7w; sessionid=0qgcg0qct8i1sojuxzwuwsgn4miyxxyb'
}

response = requests.request(
    "POST", url, headers=headers, data=payload, verify=False)

print(response.text)
