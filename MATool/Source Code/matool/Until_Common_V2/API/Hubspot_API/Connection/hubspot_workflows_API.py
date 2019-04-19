import requests

from Until_Common_V2.API.Hubspot_API.hubspot_API_auth import HubspotAPIAuth

class HubspotWorkflowsAPI(HubspotAPIAuth):
  __scope = 'automation'

  def __init__(self,site_id,request=None):
    HubspotAPIAuth.__init__(self,site_id,request)

  def get_scope(self):
    return self.__scope

  def get_all_workflows(self):
    headers = {'authorization': "Bearer " + self._access_token}
    url = 'https://api.hubapi.com/automation/v3/workflows'
    result = requests.get(url,headers=headers).json()
    return result

  def get_workflows_by_id(self,workflows_id):
    headers = {'authorization': "Bearer " + self._access_token}
    url = 'https://api.hubapi.com/automation/v3/workflows/' + str(workflows_id)
    result = requests.get(url,headers=headers).json()
    return result

  