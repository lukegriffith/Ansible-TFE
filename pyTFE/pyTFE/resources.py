import requests
import json
from api import base, ResourceNotFoundException

class workspace(base):
    def __init__(self, token, workspace_name, organization, **kwargs):

        base.__init__(self, token, organization, 'workspaces')

        self.workspace_name = workspace_name
        self.kwargs = kwargs

    def format_post_payload(self):

        self.post_payload = {
            'data': {
                'type': 'workspaces',
                'attributes': {
                    'name': self.workspace_name
                }
            }
        }

        if 'auto_apply' in self.kwargs:
            self.post_payload['data']['attributes']['auto_apply'] = self.kwargs['auto_apply']

        if 'terraform_version' in self.kwargs and self.kwargs['terraform_version'] != None:
            self.post_payload['data']['attributes']['terraform-version'] = self.kwargs['terraform_version']

        if 'vcs_repo' in self.kwargs:

            if 'vcs_oauth_token' not in self.kwargs:
                raise Exception(
                    'vcs outh token needs to be specified if providing vcs_repo'
                )
            self.post_payload['data']['attributes']['vcs-repo'] = {
                'identifier': self.kwargs['vcs_repo'],
                'branch': self.kwargs['vcs_branch'],
                'ingress-submodules': self.kwargs['vcs_ingress_submodules'],
                'oauth-token-id': self.kwargs['vcs_oauth_token']
            }

    def create_workspace(self):

        self.format_post_payload()
        r = requests.post(self.url, data=json.dumps(self.post_payload), headers=self.headers)
        return r

    def get_workspace(self):

        r = requests.get(self.url, headers=self.headers)
        data = r.json()

        if 'data' in data:
            for w in data['data']:
                if w['attributes']['name'] == self.workspace_name:
                    return w
        else:
            raise ResourceNotFoundException('Cant find workspace')

    def delete_workspace(self):

        url = self.url + "/" + self.workspace_name
        r = requests.delete(url, headers=self.headers)
        return r.json()

class workspace_var(base):
    def __init__(self, token, workspace_name, organization, variable_name, 
        variable_value, env=False, hcl=False, sensitive=False):

        base.__init__(self, token, organization, 'variables')

        # variables have a different endpoint for some reason.
        self.url = 'https://app.terraform.io/api/v2/vars'

        thisWorkspace = workspace(token, workspace_name, organization)
        w = thisWorkspace.get_workspace()


        self.workspace_id = w['id']
        self.workspace_name = workspace_name
        self.variable_name = variable_name
        self.variable_value = variable_value
        self.env = env
        self.hcl = hcl
        self.sensitive = sensitive


    def format_post_payload(self):

        self.post_payload = {
            "data": {
                "type":"vars",
                "attributes": {
                    "key": self.variable_name,
                    "value": self.variable_value,
                    "category": "env" if self.env else "terraform",
                    "hcl": self.hcl,
                    "sensitive": self.sensitive
                },
                "relationships": {
                    "workspace": {
                        "data": {
                            "id": self.workspace_id,
                            "type":"workspaces"
                        }
                    }
                }
            }
        }

    def create_variable(self):

        self.format_post_payload()
        r = requests.post(self.url, data=json.dumps(self.post_payload), headers=self.headers)
        return r.json()

    def get_variable(self):

        get_data = {
            'organization': self.organization,
            'workspace': self.workspace_name
        }
        r = requests.get(self.url, params=get_data, headers=self.headers)

        data = r.json()

        for v in data['data']:
            attr = v['attributes']

            if self.variable_name != attr['key']:
                continue

            return v

        raise ResourceNotFoundException('Cant find variable.')


class team(base):
    def __init__(self, token, team_name, organization):
        base.__init__(self, token, organization, 'teams')
        self.team_name = team_name

    def format_post_payload(self):
        self.post_payload = {
            "data": {
                "type": "teams",
                "attributes": {
                    "name": self.team_name
                }
            }
        }

    def create_team(self):
        self.format_post_payload()
        r = requests.post(self.url, data=json.dumps(self.post_payload), headers=self.headers)
        return r.json()

    def get_team(self):
        r = requests.get(self.url, headers=self.headers)
        data = r.json()

        for t in data['data']:
            if t['attributes']['name'] == self.team_name:
                return t
        raise ResourceNotFoundException('Cant find team.')



class team_access(base):
    def __init__(self, token, team_id, workspace_id, access):
        base.__init__(self, token, 'org', 'teams')
        
        if access not in ['read', 'write', 'admin']:
            raise Exception('Access value not valid. Should be read, write or admin.')

        # url is different than normal format.
        self.url = 'https://app.terraform.io/api/v2/team-workspaces'
        self.team_id = team_id
        self.workspace_id = workspace_id
        self.access = access

    def format_post_payload(self):

        self.post_payload = {
            "data": {
                "attributes": {
                "access": self.access
                },
                "relationships": {
                "workspace": {
                    "data": {
                    "type": "workspaces",
                    "id": self.workspace_id
                    }
                },
                "team": {
                    "data": {
                    "type": "teams",
                    "id": self.team_id
                    }
                }
                },
                "type": "team-workspaces"
            }
            }

    def create_team_access(self):
        
        self.format_post_payload()

        r = requests.post(url=self.url, data=json.dumps(self.post_payload), headers=self.headers)

        return r.json()


    def get_team_access(self):

        get_data = {
            "filter[workspace][id]": self.workspace_id
        }

        r = requests.get(self.url, params=get_data, headers=self.headers)
        data = r.json()

        for t_a in data['data']:
            team_id = t_a['relationships']['team']['data']['id']
            workspace_id = t_a['relationships']['workspace']['data']['id']

            if workspace_id == self.workspace_id and team_id == self.team_id:
                return t_a

        raise ResourceNotFoundException('Unable to find team access grant.')
