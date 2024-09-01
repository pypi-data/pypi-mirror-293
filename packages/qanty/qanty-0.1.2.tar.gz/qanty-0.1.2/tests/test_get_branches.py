# -*- coding: UTF-8 -*-

from qanty.common.models import Branch


def test_get_branches(qanty_client):
    response = qanty_client.get_branches()
    assert isinstance(response, list)
    if len(response) > 0:
        for branch in response:
            assert isinstance(branch, Branch)


def test_get_deleted_branches(qanty_client):
    response = qanty_client.get_branches(get_deleted=True)
    assert isinstance(response, list)
    if len(response) > 0:
        for branch in response:
            assert isinstance(branch, Branch)


def test_get_branches_with_filters(qanty_client):
    response = qanty_client.get_branches(filters={"branch_groups": ["group1", "group2"]})
    assert isinstance(response, list)
    if len(response) > 0:
        for branch in response:
            assert isinstance(branch, Branch)
