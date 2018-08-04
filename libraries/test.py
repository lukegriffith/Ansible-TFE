from TerraformEnterprise.tfe_workspace import api
import json


def main():
    a = api(
        'C3JU2C1RZXmeKA.atlasv1.dc95uQC5tLTl9mOqVlvdHHxptZTKUhK3GMYm7UphiKKg7IyWV6AcKRuSt4DFPJNa9No',
        'New_Workspace',
        'Demo-Infrastructure'
    )

    b = a.get_workspace()

    print(json.dumps(b.json()))




main()