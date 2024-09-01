# -*- coding: UTF-8 -*-


def test_qanty(qanty_client):
    assert isinstance(qanty_client.company_id, str)
    assert isinstance(qanty_client.http_client.headers.get("Authorization"), str)
