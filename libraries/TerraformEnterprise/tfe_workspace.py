#!/usr/bin/python

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
module: tfe_workspace.py

short_description: Module is used to create and control Terraform Enterprise worksapces via the rest API.

version_added: "2.4"

description:
    - Create workspaces within an organization on TFE.
    - Link to a VCS repository.
    - Trigger a plan and apply to be run.

options:
    name:
        description:
            - This is the message to send to the sample module
        required: true
    new:
        description:
            - Control to demo if the result of this module is changed or not
        required: false

author:
    - Luke Griffith (@LukeGriffith)
'''

EXAMPLES = '''
# Pass in a message
- name: Test with a message
  my_new_test_module:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_new_test_module:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_new_test_module:
    name: fail me
'''

RETURN = '''
original_message:
    description: The original name param that was passed in
    type: str
message:
    description: The output message that the sample module generates
'''

from requests import Request
import requests

class api():
    def __init__(self, token, workspace_name, organization, **kwargs):
        self.token = token
        self.workspace_name = workspace_name
        self.kwargs = kwargs
        self.url = 'https://app.terraform.io/api/v2/organizations/{}/workspaces'.format(organization)

        self.headers =  {
            'Authorization': 'Bearer {}'.format(self.token)
        }

        self.format_post_payload()

    def format_post_payload(self):
        

        self.post_payload = {
            'data': {
                'type': 'workspace',
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

        data = self.post_payload

        r = Request('POST', self.url, data=data, headers=self.headers)   

        return r.json()

    def get_workspace(self):

        r = requests.get(self.url, headers=self.headers)

        return r


def run_module():
    # define the available arguments/parameters that a user can pass to
    # the module
    module_args = dict(
        token=dict(type='str', required=True),
        organization=dict(type='str', required=True),
        workspace_name=dict(type='str', required=True),
        auto_apply=dict(type='bool', required=False, default=False),
        terraform_version=dict(type='str', required=False, default=None),
        working_directory=dict(type='str', required=False, default=''),
        vcs_repo=dict(type='str', required=False, default=None),
        vcs_oauth_token=dict(type='str', required=False, default=None),
        vcs_branch=dict(type='str', required=False, default='master'),
        vcs_ingress_submodules=dict(type='str', required=False, default=False)

    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # change is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    from ansible.module_utils.basic import AnsibleModule
    main()