from app.routers.login import create_acces_token
from conf_test_db import app
from starlette.testclient import TestClient


client = TestClient(app)


def test_user():

    # Inactive user
    user_not_access_token = create_acces_token(
        {
            "sub": "xavier2@princinhup.net",
        },
    )

    response = client.get(
        "/user",
        headers={
            "Authorization": f"Bearer {user_not_access_token}",
        },
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "inactive user"


    user_access_token = create_acces_token(
        {
            "sub": "xavier@princinhup.net",
        },
    )

    # Get all current user(s)
    response = client.get(
        "/user",
        headers={
            "Authorization": f"Bearer {user_access_token}",
        },
    )
    assert response.status_code == 200
    assert len(response.json()) == 2


    # Get a current user
    response = client.get(
        "/user/3",
        headers={
            "Authorization": f"Bearer {user_access_token}",
        },
    )
    assert response.status_code == 200
    assert len(response.json()) == 4

    # User creation
    response = client.post(
        "/user",
        headers={
            "Authorization": f"Bearer {user_access_token}",
        },
        json={
            "login": "xavier3@princinhup.net",
            "password": "0000",
            "admin": False,
        }
    )
    assert response.status_code == 200


    # User update
    response = client.put(
        "/user/3",
        headers={
            "Authorization": f"Bearer {user_access_token}",
        },
        json={
            "admin": "true",
        },
    )
    assert response.status_code == 200

    # User deletion
    response = client.delete(
        "/user/3",
        headers={
            "Authorization": f"Bearer {user_access_token}",
        },
    )
    assert response.status_code == 200


    # Wrong inquired token
    response = client.get(
        "/user",
        headers={
            "Authorization": "Bearer bsljgrokirzoknnkjrnvbzlncflkjb"
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Couldn't validate credentials"
