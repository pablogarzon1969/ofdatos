
from src.domain.response.userResponse import UserResponse


def test_userResponse():
    userResponse = UserResponse(
        id=1,
        firstName="pablo",
        lastName="garzon",
        userName="parzon",
        password="123",
        address="p@prueba.com",
        token="123"
    )

    assert userResponse.id == 1
    assert userResponse.firstName == "pablo"
    assert userResponse.lastName == "garzon"
    assert userResponse.userName == "parzon"
    assert userResponse.password == "123"
    assert userResponse.address == "p@prueba.com"
    assert userResponse.token == "123"
