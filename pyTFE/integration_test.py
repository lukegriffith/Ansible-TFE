#!/usr/bin/env python
from pyTFE.resources import workspace, workspace_var, team, team_access
import json
import os


def main():
    #test_workspace()
    #test_workspace_var()
    #test_team()

    test_team_access()

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
        'myNewVar1',
        'MyValue'
    )

    #b = a.create_variable()
    b = a.get_variable()

    print(json.dumps(b))


def test_team():

    t = team(
        os.environ['tfe_token'],
        'NewTeam1',
        'gr-innovation'
    )

    #a = t.create_team()
    a = t.get_team()
    print(json.dumps(a))


def test_team_access():

    t = team(
        os.environ['tfe_token'],
        'NewTeam1',
        'gr-innovation'
    )

    w = workspace(
        os.environ['tfe_token'],
        'New_Workspace',
        'gr-innovation'
    )

    t_obj = t.get_team()

    w_obj = w.get_workspace()


    t_a = team_access(
        os.environ['tfe_token'],
        t_obj['id'],
        w_obj['id'],
        'read',
    )

    a = t_a.create_team_access()

    print(json.dumps(a))

main()