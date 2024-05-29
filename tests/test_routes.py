import pytest 
from flask_package import routes 
from flask import session

@pytest.mark.parametrize("non_auth_routes", [
    "/welcome", 
    "/register",
    "/login",
    ])
def test_nonauthenitcated_requests(client, non_auth_routes):

    '''Test the routes that don't rely on authentication'''

    response = client.get(non_auth_routes)
    assert response.status_code == 200

def test_access_session(client):
    with client:
        response = client.get("/login")
        csrf_token = response.data.decode().split('name="csrf_token" type="hidden" value="')[1].split('"')[0]

        client.post("/login", data={
            "email": "ralph.corey.1@gmail.com", 
            "password":"test", 
            "csrf_token":csrf_token})
        # session is still accessible
        assert session["_user_id"] == "1"

@pytest.mark.parametrize("auth_routes", [
    "/feedback",
    "/index",
    "/add_chore_partial",
    "/cancel_add_chore_partial"
])
def test_authenticated_requests(auth_client, auth_routes):
    response = auth_client.get(auth_routes)
    assert response.status_code == 200 
