from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
# some standart checking if endpoint are working

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_start_game():
    response = client.post("/start_game", json={"player1": "Alice", "mode": "computer", "player2": None})
    assert response.status_code == 200
    assert "message" in response.json()

def test_play():
    response = client.post("/play", json={"player": "player1", "choice": "rock"})
    assert response.status_code == 200
    assert "result" in response.json() or "message" in response.json()

def test_save_game():
    response = client.post("/save_game")
    assert response.status_code == 200
    assert "message" in response.json()

def test_game_history():
    response = client.get("/game_history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# TODO I would add some tests to check parameters that go into the endpoints
#  and how it will behave with this parameters but I would spent more than 3 hours on that