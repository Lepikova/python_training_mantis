from suds.client import Client
from suds import WebFault

class SoapHelper:
    def __init__(self, app, config):
        self.app = app
        self.config = config

    def can_login(self, username, password):
        client = Client(self.config['web']['baseUrl'] + "api/soap/mantisconnect.php?wsdl")
        try:
            client.service.mc_login(username, password)
            return True
        except WebFault:
            return False

    def get_project_list(self):
        client = Client(self.config['web']['baseUrl'] + "api/soap/mantisconnect.php?wsdl")
        try:
            return client.service.mc_projects_get_user_accessible(self.config['webadmin']['username'], self.config['webadmin']['password'])
        except WebFault as e:
            print(f"SOAP error: {e}")
            return []
