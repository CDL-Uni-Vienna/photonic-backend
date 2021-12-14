# script that fetches data from api endpoint
# translates request data to experimental setup with JSON package
# executes setup
# returns the result

import requests
# All header values must be a string, bytestring, or unicode
snek_token = 'Token 59f6d91e7cd9a14898fe2c0b4b04f7fafbae9692'


def get(id):
    """
    Returns list of JSON strings with RequestData models
    from server/api/job
    """
    url = f"http://127.0.0.1:8000/api/job/{id}/"
    token = {'Authorization': 'Token 19edc712112f74fb418960229282e1344f9cb5d2'}
    request = requests.get(
        url,
        headers=token
    )
    return request.json()


def get_job_aws(id):
    """
    Returns list of JSON strings with RequestData models
    from server/api/job
    """
    url = f"http://ec2-3-21-129-172.us-east-2.compute.amazonaws.com/api/job/{id}/"
    token = {'Authorization': 'Token 7a2d8a382030b5a52cbdadfe3944bfbc3aee88ef'}
    request = requests.get(
        url,
        headers=token
    )
    return request.json()


def get_job_snek(id):
    """
    Returns list of JSON strings with RequestData models
    from server/api/job
    """
    url = f"https://cdl.snek.at/api/job/{id}/"
    token = {'Authorization': snek_token}
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
    token = {'Authorization': 'Token 19edc712112f74fb418960229282e1344f9cb5d2'}
    # request_data['result'] = "Retrieved and executed."
    requests.post(
        f"http://127.0.0.1:8000/api/result/",
        data=payload,
        headers=token
    )


def post_result_snek(raw_result, job_id):
    """Sends back the result string"""
    payload = {'results': raw_result, 'job': job_id}
    token = {'Authorization': snek_token}
    # request_data['result'] = "Retrieved and executed."
    requests.post(
        f"https://cdl.snek.at/api/result/",
        data=payload,
        headers=token
    )
