from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_signup_and_unregister():
    # choose an activity with known participants
    activity = "Chess Club"
    email = "test_student@mergington.edu"

    # ensure email not already in participants
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    # sign up
    response = client.post(f"/activities/{activity}/signup?email={email}")
    assert response.status_code == 200
    assert email in activities[activity]["participants"]

    # unregister
    response = client.delete(f"/activities/{activity}/participants?email={email}")
    assert response.status_code == 200
    assert email not in activities[activity]["participants"]


def test_unregister_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/participants?email=foo")
    assert response.status_code == 404


def test_unregister_not_signed_up():
    activity = "Gym Class"
    email = "nobody@mergington.edu"
    # ensure not present
    if email in activities[activity]["participants"]:
        activities[activity]["participants"].remove(email)

    response = client.delete(f"/activities/{activity}/participants?email={email}")
    assert response.status_code == 400
