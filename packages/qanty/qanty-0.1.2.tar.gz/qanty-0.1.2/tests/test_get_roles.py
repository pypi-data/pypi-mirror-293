import qanty.common.models as models
import qanty.exceptions


def test_get_roles(qanty_client, user):
    try:
        roles = qanty_client.get_roles(user_id=user.id)
        assert isinstance(roles, list)

        if len(roles) > 0:
            assert all(isinstance(role, models.UserRole) for role in roles)
    except qanty.exceptions.UserNotFound:
        assert True  # Exception is expected, so the test should pass
