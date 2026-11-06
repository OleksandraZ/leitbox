from leitbox.domain.user import User


def test_two_users_get_different_id():
    user1 = User('user1')
    user2 = User('user2')
    assert user1.id != user2.id

def test_user_id_created_holds():
    user = User('user1', user_id = "1")
    assert user.id == "1"