import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert isinstance(data["Chess Club"], dict)

def test_signup_for_activity_success():
    response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up newstudent@mergington.edu for Chess Club" in response.json()["message"]

    # Clean up: remove the test participant
    client.post("/unregister", json={"participant": "newstudent@mergington.edu", "activity": "Chess Club"})

def test_signup_for_activity_already_signed_up():
    # Use an existing participant
    response = client.post("/activities/Chess Club/signup", params={"email": "michael@mergington.edu"})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up for this activity"

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_participant_success():
    # Add a participant to remove
    client.post("/activities/Chess Club/signup", params={"email": "temp@mergington.edu"})
    response = client.post("/unregister", json={"participant": "temp@mergington.edu", "activity": "Chess Club"})
    assert response.status_code == 200
    assert response.json()["success"] is True

def test_unregister_participant_not_found():
    response = client.post("/unregister", json={"participant": "notfound@mergington.edu", "activity": "Chess Club"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"

def test_unregister_from_nonexistent_activity():
    response = client.post("/unregister", json={"participant": "someone@mergington.edu", "activity": "Nonexistent"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
