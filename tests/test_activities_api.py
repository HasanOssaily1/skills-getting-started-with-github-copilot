def test_root_redirects_to_static_index(client):
    # Arrange
    target_path = "/"

    # Act
    response = client.get(target_path, follow_redirects=False)

    # Assert
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_mapping(client):
    # Arrange
    target_path = "/activities"

    # Act
    response = client.get(target_path)
    payload = response.json()

    # Assert
    assert response.status_code == 200
    assert isinstance(payload, dict)
    assert "Chess Club" in payload
    assert "participants" in payload["Chess Club"]


def test_signup_adds_participant_when_valid(client):
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    participants_before = list(client.get("/activities").json()[activity_name]["participants"])

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})
    participants_after = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {email} for {activity_name}"
    assert email not in participants_before
    assert email in participants_after


def test_signup_returns_404_for_missing_activity(client):
    # Arrange
    missing_activity = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.post(f"/activities/{missing_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_returns_400_for_existing_participant(client):
    # Arrange
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"

    # Act
    response = client.post(f"/activities/{activity_name}/signup", params={"email": existing_email})

    # Assert
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_unregister_removes_participant_when_present(client):
    # Arrange
    activity_name = "Chess Club"
    email = "daniel@mergington.edu"
    participants_before = list(client.get("/activities").json()[activity_name]["participants"])

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})
    participants_after = client.get("/activities").json()[activity_name]["participants"]

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == f"Unregistered {email} from {activity_name}"
    assert email in participants_before
    assert email not in participants_after


def test_unregister_returns_404_for_missing_activity(client):
    # Arrange
    missing_activity = "Nonexistent Club"
    email = "student@mergington.edu"

    # Act
    response = client.delete(f"/activities/{missing_activity}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_unregister_returns_404_for_not_signed_up_student(client):
    # Arrange
    activity_name = "Chess Club"
    email = "not-signed-up@mergington.edu"

    # Act
    response = client.delete(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert
    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"
