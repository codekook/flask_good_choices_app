import pytest 
from flask_package import routes 

@pytest.mark.parametrize("non_auth_routes", [
    "/welcome", 
    "/register",
    "/login",
    ])
def test_nonauthenitcated_requests(client, non_auth_routes):

    '''Test the routes that don't rely on authentication'''

    response = client.get(non_auth_routes)
    assert response.status_code == 200
