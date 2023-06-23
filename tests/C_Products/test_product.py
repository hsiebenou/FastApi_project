from app.routers.login import create_acces_token
from conf_test_db import app
from starlette.testclient import TestClient

client = TestClient(app)


def test_product():

    # get token
    user_access_token = create_acces_token(
        {
            "sub": "xavier@princinhup.net",
        },
    )

    # get one sku
    response = client.get(
        "/product/10",
        headers={
            "Authorization": f"Bearer {user_access_token}",
        }
    )
    assert response.status_code == 200

    # all sku
    response = client.get(
        "/product",
        headers={
            "Authorization": f"Bearer {user_access_token}",
        },
    )
    assert response.status_code == 200


    # Wrong token
    response = client.get(
        "/product",
        headers={
            "Authorization": f"Bearer bsljgrokirzoknnkjrnvbzlncflkjb",
        },
    )
    assert response.status_code == 401
    assert response.json()["detail"] == "Couldn't validate credentials"


    # get difference price
    response = client.post(
        "/product",
        headers={
            "Authorization": f"Bearer {user_access_token}",
        },
        json=[10, 12]
    )
    assert response.status_code == 200
    assert response.json() == {'10': 2.0, '12': 4.0}