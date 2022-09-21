from email import header
from os import getcwd
from fastapi import FastAPI
from fastapi.testclient import TestClient
from sql_app.main import app
import uuid

teacher_jwt = ''
test_assignment_id = ''
test_file_path = ''
test_file_name = ''

teacher_data = {

    "first_name": "Test",
    "last_name": "User",
    "password": "123456",
    "email": "test_teacher@mail.com",
    "role": "Teacher"

}

student_data = {

    "first_name": "Test",
    "last_name": "User",
    "password": "123456",
    "email": "test_student@mail.com",
    "role": "Teacher"

}

assignment_data = {
    "name": "Test Assignment",
    "description": "This is the first assignment created in app."
}


def test_initiate_app_test_user():
    # Create Teacher Test User
    response = client.post("/users/user", json=teacher_data)
    if (not response.status_code == 200):
        payload = response.json()
        assert payload['detail'] == 'User email already exists'
    else:
        assert response.status_code == 200
        payload = response.json()
        data_less_password = teacher_data
        del data_less_password['password']
        del payload['hashed_password'], payload['created_date'], payload['id']
        assert payload == data_less_password

    # Create Student Test User
    response = client.post("/users/user", json=student_data)
    if (not response.status_code == 200):
        payload = response.json()
        assert payload['detail'] == 'User email already exists'
    else:
        assert response.status_code == 200
        payload = response.json()
        data_less_password = student_data
        del data_less_password['password']
        del payload['hashed_password'], payload['created_date'], payload['id']
        assert payload == data_less_password


def test_login():
    print({"username": teacher_data['email'],
          "password": teacher_data['password']})
    response = client.post(
        "/users/token", data={"username": teacher_data['email'], "password": teacher_data['password']})
    assert response.status_code == 200
    payload = response.json()
    global teacher_jwt
    teacher_jwt = payload['access_token']


def test_initiate_app_test_assignment():
    # Create first Assignment
    global test_assignment_id
    response = client.post("/assignments/assignment", json=assignment_data, headers={
                           "content-type": "application/json", "Authorization": f'Bearer {teacher_jwt}'})
    assert response.status_code == 200
    payload = response.json()
    test_assignment_id = payload['id']
    del payload['id']
    assert payload == assignment_data


{
    "assignment_id": "string",
    "file_path": "string",
    "filename": "string"
}


def test_homework_creation():
    # UPload home work file
    response = client.post('/homeworks/upload', files={"file": ("download.jpg", open(
        f'{getcwd()}/sql_app/download.jpeg', "rb"), "image/jpeg")}, headers={"content-type": None, "Authorization": f'Bearer {teacher_jwt}'})
    payload = response.json()
    global test_file_name, test_file_path
    test_file_name = payload['filename']
    test_file_path = payload['file_path']
    assert response.status_code == 200
    res = client.post('homeworks/homework', json={"assignment_id": test_assignment_id,
                                                  "file_path": test_file_path,
                                                  "filename": test_file_name}, headers={
        "content-type": "application/json", "Authorization": f'Bearer {teacher_jwt}'})

    assert res.status_code == 200


client = TestClient(app)
