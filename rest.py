#script that fetches data from api endpoint
#translates request data to experimental setup with JSON package
#executes setup
#returns the result

import requests


def get(id):
    """
    Returns list of JSON strings with RequestData models
    from server/api/job
    """
    request = requests.get(
        f"http://127.0.0.1:8000/api/job/{id}/",
        headers={'Authorization': 'Token 4d09489efd910cccae619b8381add8e2ecbfbd71'}
        )
    return request.json()

def put(request_data):
    """Updates RequestData model with request_data of corresponding id"""
    id = request_data['id']
    requests.put(
        f"http://127.0.0.1:8000/api/RequestData/{id}/",
        auth=("zilk.felix@gmail.com", "123"), data=request_data)

def is_fetched(request_data):
    """Sets status is_fetched and returns entire data string to server"""
    request_data['is_fetched'] = True
    put(request_data)

def put_result(request_data):
    """Sends back the result string"""
    id = request_data['id']
    request_data['result'] = "Retrieved and executed."
    requests.put(f"http://127.0.0.1:8000/api/RequestData/{id}/", auth=("zilk.felix@gmail.com", "123"), data=request_data)

# print(get(6))
