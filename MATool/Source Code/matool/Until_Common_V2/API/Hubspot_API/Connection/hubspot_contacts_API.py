import requests
import json

from Until_Common_V2.API.Hubspot_API.hubspot_API_auth import HubspotAPIAuth

class HubspotContactsAPI(HubspotAPIAuth):
  
  def __init__(self,site_id,request=None):
    HubspotAPIAuth.__init__(self,site_id,request)

  def get_contact_by_id(self,contact_id):
    headers = {'authorization': "Bearer " + self._access_token}
    url = "https://api.hubapi.com/contacts/v1/contact/vid/" + str(contact_id) + '/profile'
    result = requests.get(url,headers=headers).json()
    return result

  def update_contact_properties(self,vid,properties):
    headers = {"Content-Type": "application/json",
                'authorization': "Bearer " + self._access_token}
    url = "https://api.hubapi.com/contacts/v1/contact/vid/" + str(vid) + "/profile"

    # properties =  [
    #         {
    #         "property": property_sent_date,
    #         "value": start_millisecond
    #         }]

    data = {'properties':properties}
    result = requests.post(url,data=json.dumps(data),headers=headers)
    return result