import rest_calls_prod
import json

# returns KeyError: 'experimentId' if no experiment is in Queue
task = rest_calls_prod.getexp_fromqueue(
    "01a9b596c1b165fa4f15fbccad4092428dc47db76ad4e5dfe3bfee24b66bb434")
# if "detail":"Invalid token." or {"detail":"Invalid token header. No credentials provided."}

print(task)

if "detail" in task:
    credentials = rest_calls_prod.login("zilk.felix@gmail.com", "123")
    token = credentials["token"]
