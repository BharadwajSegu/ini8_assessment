from tests.helpers import get_auth_token

def test_file_upload_validation(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/documents/upload", data={}, headers=headers)
    assert response.status_code == 400

def test_list_documents_empty(client):
    token = get_auth_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/documents", headers=headers)
    assert response.status_code == 200
    assert response.get_json() == []
