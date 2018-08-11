

class base():
    def __init__(self, token, organization, endpoint):

        self.token = token
        self.url = 'https://app.terraform.io/api/v2/organizations/{}/{}'.format(organization, endpoint)

        self.headers =  {
            'Authorization': 'Bearer {}'.format(self.token),
            'content-type': 'application/vnd.api+json'
        }
