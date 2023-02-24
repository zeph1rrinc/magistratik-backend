import json

test_player_data = {"nickname": "test_user", "status": "Активен", "rating": 100}
wrong_test_player_data = {**test_player_data, "status": "123"}
created_player_data = {}


def test_create_wrong_player(client):
    resp = client.post("/players/", data=json.dumps(wrong_test_player_data))
    assert resp.status_code == 422


def test_create_player(client):
    resp = client.post("/players", data=json.dumps(test_player_data))
    assert resp.status_code == 201
    data_from_response = resp.json()
    assert data_from_response["nickname"] == test_player_data["nickname"]
    assert data_from_response["status"] == test_player_data["status"]
    assert data_from_response["rating"] == test_player_data["rating"]
    created_player_data.update(data_from_response)


def test_get_created_player(client):
    resp = client.get(f'/players/{created_player_data["id"]}')
    assert resp.status_code == 200
    data_from_response = resp.json()
    assert data_from_response["nickname"] == created_player_data["nickname"]
    assert data_from_response["status"] == created_player_data["status"]
    assert data_from_response["rating"] == created_player_data["rating"]


def test_update_created_player(client):
    resp = client.put(
        f'/players/{created_player_data["id"]}',
        data=json.dumps({**test_player_data, "rating": 123}),
    )
    assert resp.status_code == 200
    data_from_response = resp.json()
    assert data_from_response["nickname"] == created_player_data["nickname"]
    assert data_from_response["status"] == created_player_data["status"]
    assert data_from_response["rating"] == 123


def test_delete_player(client):
    resp = client.delete(f'/players/{created_player_data["id"]}')
    assert resp.status_code == 204


def test_get_returns_404(client):
    resp = client.get(f'/players/{created_player_data["id"]}')
    assert resp.status_code == 404
