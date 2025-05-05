from fastapi.testclient import TestClient
from main import app, verify_firebase_token

client = TestClient(app)

# ✅ mock UID returned by Firebase
app.dependency_overrides[verify_firebase_token] = lambda: "test_uid"

auth_header = {"Authorization": "FAKE_ID_TOKEN"}

def test_create_profile():
    res = client.post("/profile", json={"name": "Test User", "email": "test@example.com"}, headers=auth_header)
    assert res.status_code in (200, 201)

def test_get_profile():
    res = client.get("/profile", headers=auth_header)
    assert res.status_code in (200, 404)

def test_update_profile():
    res = client.put("/profile", json={"name": "Updated"}, headers=auth_header)
    assert res.status_code in (200, 204)

def test_delete_profile():
    res = client.delete("/profile", headers=auth_header)
    assert res.status_code in (200, 204)
