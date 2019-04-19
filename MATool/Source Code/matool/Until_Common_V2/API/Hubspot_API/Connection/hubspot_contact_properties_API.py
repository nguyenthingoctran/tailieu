import requests

from Until_Common_V2.API.Hubspot_API.hubspot_API_auth import HubspotAPIAuth

class HubspotContactPropertiesAPI(HubspotAPIAuth):
  
  def __init__(self,site_id,request=None):
    HubspotAPIAuth.__init__(self,site_id,request)

  def get_list_properties(self):
    headers = {'authorization': "Bearer " + self._access_token}
    requestURL = 'https://api.hubapi.com/properties/v1/contacts/properties?'
    response = requests.get(requestURL, headers=headers).json()
    return response

  