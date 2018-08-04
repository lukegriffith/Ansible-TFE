import pytest
from mock import MagicMock
from pytest import raises
from TerraformEnterprise.tfe_workspace import api


def test_payload_format_does_not_throw():
    api('1234', 'name', 'myOrg', auto_apply=True)

    assert True

def test_payload_vcs_incomplete():

    with pytest.raises(Exception) as excinfo:
        api('1234', 'name', 'myOrg', auto_apply=True, vcs_repo='test')
    assert excinfo.value.message == 'vcs outh token needs to be specified if providing vcs_repo'

