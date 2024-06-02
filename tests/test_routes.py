import pytest
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

    '''Test the establishment of a session and creation of a session id'''

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

    '''Test the routes that require authentication'''

    response = auth_client.get(auth_routes)
    assert response.status_code == 200


def test_new_chore(auth_client):
    with auth_client:
        auth_client.get("/add_chore_partial")
        response = auth_client.post("/add_chore_partial", data={
            "new_chore" : "Clean Room"
        })
        assert response.status_code == 200

def test_feedback(auth_client):
    with auth_client:
        auth_client.get("/feedback")
        response = auth_client.post("/index", data={
            "feedback" : "Great app"
        })
        assert response.status_code == 200
        

    
