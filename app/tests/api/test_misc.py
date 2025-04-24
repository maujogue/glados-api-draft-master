def test_get_unexisting_resource(client):
    response = client.get("/unexisting-resource")

    assert response.status_code == 404
    assert response.json == {"error": "not_found", "message": "Resource not found."}


def test_get_version(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json == {"version": "1.0"}
