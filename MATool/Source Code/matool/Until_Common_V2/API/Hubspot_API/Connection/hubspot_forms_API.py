import requests

from Until_Common_V2.API.Hubspot_API.hubspot_API_auth import HubspotAPIAuth

class HubspotFormsAPI(HubspotAPIAuth):
  __scope = 'forms'
  
  def __init__(self,site_id,request=None):
    HubspotAPIAuth.__init__(self,site_id,request)

  def get_scope(self):
    return self.__scope

  def get_all_form(self):
    headers = {"Content-Type": "application/json",
              'authorization': "Bearer " + self._access_token}
    url = "https://api.hubapi.com/forms/v2/forms"
    result = requests.get(url,headers=headers).json()
    return result

  