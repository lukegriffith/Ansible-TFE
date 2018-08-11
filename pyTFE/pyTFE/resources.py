import requests
import json
from api import base

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
            return None


class workspace_var(base):
    def __init__(self, token, workspace_name, organization, variable_name, 
        variable_value, env=False, hcl=False, sensitive=False):

        base.__init__(self, token, organization, 'variables')

        # variables have a different endpoint for some reason.
        self.url = 'https://app.terraform.io/api/v2/vars'

        thisWorkspace = workspace(token, workspace_name, organization)
        w = thisWorkspace.get_workspace()

        if w == None:
            raise Exception("Workspace does not exist.")

        self.workspace_id = w['id']
        self.workspace_name = workspace_name
        self.organization = organization
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

        return None