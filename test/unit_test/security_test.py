from backend.src.security import pwd_context


def test_hash_password():
    password = "12345678"
    hashed =  pwd_context.hash(password)

    assert password != hashed
    assert len(hashed) > 50
    assert isinstance(hashed, str)


def test_verify_password():
    plain_password = "12345678"
    hashed_password =  pwd_context.hash(plain_password)
    result = pwd_context.verify(plain_password, hashed_password)
    wrong_result = pwd_context.verify("plain_password", hashed_password)

    assert isinstance(result, bool)
    assert result is True

    assert isinstance(wrong_result, bool)
    assert wrong_result is False



