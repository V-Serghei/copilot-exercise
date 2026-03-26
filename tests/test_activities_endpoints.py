def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_expected_shape_and_headers(client):
    response = client.get("/activities")

    assert response.status_code == 200
    assert "no-store" in response.headers["cache-control"]
    assert response.headers["pragma"] == "no-cache"
    assert response.headers["expires"] == "0"

    data = response.json()

    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data

    required_keys = {"description", "schedule", "max_participants", "participants"}
    for _, activity in data.items():
        assert required_keys.issubset(activity.keys())
        assert isinstance(activity["description"], str)
        assert isinstance(activity["schedule"], str)
        assert isinstance(activity["max_participants"], int)
        assert isinstance(activity["participants"], list)
