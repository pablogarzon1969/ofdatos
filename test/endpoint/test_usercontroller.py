from typing import Any
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_executeUserSSIS():
    response = client.get("/user/user/user/ssis/")
    assert response.status_code == 200
    assert {'body': {'re...error': None}} != {'body': {'result': 1}}


def test_getAllUser():
    response = client.get("/user/user/")
    assert response.status_code == 200
    assert {'body': {'re...error': None}} == {'body': {'re...error': None}}


def test_getUserById():
    response = client.get("/user/user/user/3")
    assert response.status_code == 200
    assert {'body': "Error Negocio"}


def test_postUserCreate():
    data = {
        'id': 1,
        'username': "pablo"
    }
    response = client.post("/user/user/user/", json=data)
    assert response.status_code == 200
    assert {'body': "Error Negocio"}
