import random
import string

import qanty.exceptions


def test_create_user(qanty_client, user):
    # Generate a random user_id
    role_id = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(16))
    doc_id = "".join(random.choice(string.digits) for _ in range(10))

    try:
        new_user = qanty_client.create_user(
            user_id=user.id,
            email="test@domain.com",
            doc_id=doc_id,
            name="test",
            role_id=role_id,
            branches=["*"],
            debug=True,
        )
    except qanty.exceptions.UserNotFound:
        assert True
    else:
        assert isinstance(new_user, str)
