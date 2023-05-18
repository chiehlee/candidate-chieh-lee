from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from fastapi import HTTPException
from webapp.src.app import app

client = TestClient(app)

# To mock exception when service is not available
def mocked_requests_get(*args, **kwargs):
    raise HTTPException(status_code=503, detail="Service Unavailable")

def test_get_star_wars_data():
    client = TestClient(app)
    response = client.get("/data")
    assert response.status_code == 200
    assert "name" in response.json()

# Additional test cases can be added by the candidate

def test_get_star_wars_data_bad_input():
    # Test error case: invalid ID
    response = client.get("/data?id=invalid")
    assert response.status_code == 500

    # Test edge case: large ID
    response = client.get("/data?id=10000")
    assert response.status_code == 500


@patch('fastapi.testclient.TestClient.get', new=mocked_requests_get)
def test_get_star_wars_data_service_not_available():
    # Test error case: Service not available
    with pytest.raises(HTTPException):
        response = client.get("/data?id=1")
        assert response.status_code == 503
        assert response.json()['detail'] == "Service Unavailable"


def test_top_people_by_bmi():
    # Test normal case
    response = client.get("/top-people-by-bmi")
    results = response.json()

    # Test response code: Normal
    assert response.status_code == 200

    # Test that the result contains no more than 20 people
    assert len(results) <= 20

    # Test that the 'bmi' key is not present in the results
    for person in results:
        assert 'bmi' not in person


def test_non_existed_endpoint():
    # Test normal case
    response = client.get("/i-dont-know-who-i-am")
    results = response.json()

    # Test response code: Normal
    assert response.status_code == 404
