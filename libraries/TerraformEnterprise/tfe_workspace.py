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
        vcs_ingress_submodules=dict(type='str', required=False, default=False),
        absent=dict(type='bool', required=False, default=False)

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

    extra_params = {}

    for key in ['auto_apply','terraform_version',
        'vcs_repo', 'vcs_branch', 'vcs_ingress_submodules',
        'vcs_oauth_token']:
        if  key in module.params:
            extra_params[key] = module.params[key]

    wks = workspace(
        token=module.params['token'],
        workspace_name=module.params['workspace_name'],
        organization=module.params['organization'],
        **extra_params
    )

    module.params['compliant'] = True

    try: 
        result = wks.get_workspace()

    except ResourceNotFoundException:
        if module.params['absent'] == False:
            result['message'] = 'Workspace not found'
            result['compliant'] = False
        else:
            result['message'] = 'Workspace not found, and expected absent'
            result['compliant'] = True

    except Exception as e:
        module.fail_json(msg='General error occured: ' + e, **result)

    if module.params['absent']:
        result['message'] = 'Workspace found, but expected absent'
        result['compliant'] = False

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        return result


    if not result['compliant']:

        if module.params['absent']:

            try: 
                wks.delete_workspace()
                result['message'] = 'Workspace deleted'
            except Exception as e:
                result['changed'] = True
                module.fail_json(msg='General error occured: ' + e, **result)
        else:
            try:
                wks.create_workspace()
                result['message'] = 'Workspace created'
            except Exception as e:
                result['changed'] = True
                module.fail_json(msg='General error occured: ' + e, **result)

        result['changed'] = True

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    from ansible.module_utils.basic import AnsibleModule
    from pyTFE.resources import workspace
    from pyTFE.api import ResourceNotFoundException
    main()  