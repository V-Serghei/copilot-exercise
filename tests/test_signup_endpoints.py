def test_signup_adds_new_participant(client):
    email = "newstudent@mergington.edu"

    response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for Chess Club"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Chess Club"]["participants"]
    assert email in participants


def test_signup_rejects_duplicate_participant(client):
    email = "duplicate@mergington.edu"

    first_response = client.post("/activities/Chess Club/signup", params={"email": email})
    second_response = client.post("/activities/Chess Club/signup", params={"email": email})

    assert first_response.status_code == 200
    assert second_response.status_code == 400
    assert second_response.json()["detail"] == "Student already signed up for this activity"


def test_signup_unknown_activity_returns_not_found(client):
    response = client.post("/activities/Unknown Activity/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_removes_participant(client):
    email = "remove-me@mergington.edu"
    client.post("/activities/Gym Class/signup", params={"email": email})

    response = client.delete("/activities/Gym Class/signup", params={"email": email})

    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from Gym Class"

    activities_response = client.get("/activities")
    participants = activities_response.json()["Gym Class"]["participants"]
    assert email not in participants


def test_unregister_unknown_activity_returns_not_found(client):
    response = client.delete("/activities/Unknown Activity/signup", params={"email": "student@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_missing_participant_returns_not_found(client):
    response = client.delete("/activities/Chess Club/signup", params={"email": "not-registered@mergington.edu"})

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not signed up for this activity"


def test_unregister_then_signup_again_succeeds(client):
    email = "cycle@mergington.edu"

    signup_response = client.post("/activities/Tennis Club/signup", params={"email": email})
    assert signup_response.status_code == 200

    unregister_response = client.delete("/activities/Tennis Club/signup", params={"email": email})
    assert unregister_response.status_code == 200

    signup_again_response = client.post("/activities/Tennis Club/signup", params={"email": email})
    assert signup_again_response.status_code == 200
    assert signup_again_response.json()["message"] == f"Signed up {email} for Tennis Club"
