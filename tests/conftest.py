import pytest

from app.database.DPredictORM import ApiUser


@pytest.fixture(autouse=True)
def create_dummy_user():
    """Fixture to execute asserts before and after a test is run"""

    # Setup: fill with any logic you want
    from conf_test_db import override_get_db

    database = next(override_get_db())
    new_user = ApiUser(
        login="xavier@princinhup.net",
        password="1234",
        admin=True,
    )
    database.add(new_user)
    database.commit()
    new_user = ApiUser(
        login="xavier2@princinhup.net",
        password="1234",
        admin=False,
    )
    database.add(new_user)
    database.commit()

    yield  # this is where the testing happens

    # Teardown : fill with any logic you want
    database.query(ApiUser).delete()
    database.commit()
