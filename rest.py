#script that fetches data from api endpoint
#translates request data to experimental setup with JSON package
#executes setup
#returns the result

import requests
# All header values must be a string, bytestring, or unicode

def get(id):
    """
    Returns list of JSON strings with RequestData models
    from server/api/job
    """
    url = f"http://127.0.0.1:8000/api/job/{id}/"
    token = {'Authorization': 'Token 4d09489efd910cccae619b8381add8e2ecbfbd71'}
    request = requests.get(
        url,
        headers=token
        )
    return request.json()

def put(request_data):
    """Updates Result
     model with request_data of corresponding id"""
    id = request_data['id']
    requests.put(
        f"http://127.0.0.1:8000/api/result/{id}/",
        auth=("zilk.felix@gmail.com", "123"), data=request_data)

def is_fetched(request_data):
    """Sets status is_fetched and returns entire data string to server"""
    request_data['is_fetched'] = True
    put(request_data)

def post_result(raw_result, job_id):
    """Sends back the result string"""
    payload = {'results': raw_result, 'job': job_id}
    token = {'Authorization': 'Token 4d09489efd910cccae619b8381add8e2ecbfbd71'}
    # request_data['result'] = "Retrieved and executed."
    requests.post(
        f"http://127.0.0.1:8000/api/result/", 
        data = payload, 
        headers=token
    )
