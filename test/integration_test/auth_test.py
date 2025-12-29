from backend.src.security import create_access_token


def test_login_access_token():

    data = {"email": "email@email.ru",
            "password": "12345678"}
    token = create_access_token(data)

    assert isinstance(token, str)