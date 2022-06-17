from src.domain.request.userRequest import UserRequest


def test_userRequest():
    pn = UserRequest(id=1, username="pablo")

    assert pn.id == 1
    assert pn.username == 'pablo'
