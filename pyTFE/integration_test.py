#!/usr/bin/env python
from pyTFE.resources import workspace, workspace_var
import json
import os


def main():
    #test_workspace()
    test_workspace_var()
    pass


def test_workspace():
    a = workspace(
        os.environ['tfe_token'],
        'New_Workspace',
        'gr-innovation'
    )

    b = a.get_workspace()

    print(json.dumps(b))

def test_workspace_var():
    a = workspace_var(
        os.environ['tfe_token'],
        'New_Workspace',
        'gr-innovation',
        'myNewVar',
        'MyValue'
    )

    #b = a.create_variable()
    b = a.get_variable()

    print(json.dumps(b))

main()