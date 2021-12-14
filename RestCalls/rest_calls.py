"""Python REST Calls are used to retrieve and send data to the quco API"""

import requests

from pw import passwords


def login(useremail, userpassword):
    """Login"""
    url = f"https://quco.exp.univie.ac.at/api/login/"
    data = {"email": useremail,
            "password": userpassword}
    request = requests.post(
        url,
        data
    )
    return request.status_code, requests.Response(), request.json()


def get_experiment(token, experimentId):
    """Get Experiment"""
    url = f"https://quco.exp.univie.ac.at/api/experiments/{experimentId}/"
    token = {'Authorization': "123"}
    request = requests.get(
        url,
        headers=token
    )
    return request.json(), requests.Response()


def post_experiment(token):
    """"""
    payload = {'results': raw_result, 'job': job_id}
    token = {'Authorization': 'Token 19edc712112f74fb418960229282e1344f9cb5d2'}
    # request_data['result'] = "Retrieved and executed."
    post = requests.post(
        f"https://quco.exp.univie.ac.at/api/experiments/",
        data=payload,
        headers=token
    )
    return post.status_code


def post_result(token):
    """Post Result"""
    payload = {'results': raw_result, 'job': job_id}
    token = {'Authorization': 'Token 19edc712112f74fb418960229282e1344f9cb5d2'}
    # request_data['result'] = "Retrieved and executed."
    requests.post(
        f"https://quco.exp.univie.ac.at/api/results/",
        data=payload,
        headers=token
    )


def patch_experiment(token, experimentId):
    """Patch"""
    payload = {'results': raw_result, 'job': job_id}
    token = {'Authorization': 'Token 19edc712112f74fb418960229282e1344f9cb5d2'}
    # request_data['result'] = "Retrieved and executed."
    requests.patch(
        f"https://quco.exp.univie.ac.at/api/experiments/{experimentId}",
        data=payload,
        headers=token
    )


def delete():
    """Delete"""
