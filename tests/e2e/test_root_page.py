from fastapi.testclient import TestClient

def test_root_page(client: TestClient):
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

    html = response.text
    assert "<title>DoDoes API" in html
    assert "Swagger Docs" in html
    assert "Redoc Docs" in html
    assert "OpenAPI JSON" in html
