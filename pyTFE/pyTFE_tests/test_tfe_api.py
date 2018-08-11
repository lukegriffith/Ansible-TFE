import pytest
from mock import MagicMock
from pytest import raises
from pyTFE.resources import workspace


def test_payload_format_does_not_throw():
    
    w = workspace('1234', 'name', 'myOrg', auto_apply=True)
    w.format_post_payload()

    assert True

def test_payload_vcs_incomplete():

    with pytest.raises(Exception) as excinfo:
        w = workspace('1234', 'name', 'myOrg', auto_apply=True, vcs_repo='test')
        w.format_post_payload()

    assert excinfo.value.message == 'vcs outh token needs to be specified if providing vcs_repo'

