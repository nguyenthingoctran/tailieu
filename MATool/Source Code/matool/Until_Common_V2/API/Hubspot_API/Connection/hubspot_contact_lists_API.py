import requests
import json

from Until_Common_V2.API.Hubspot_API.hubspot_API_auth import HubspotAPIAuth

class HubspotContactListsAPI(HubspotAPIAuth):
  __scope = 'contacts'

  def __init__(self,site_id,request=None):
    HubspotAPIAuth.__init__(self,site_id,request)

  def get_scope(self):
    return self.__scope
    
  def get_contact_list_by_id(self,contact_list_id):
    # headers = { "Content-Type": "application/json"}
    headers = {'authorization': "Bearer " + self._access_token}
    url = "https://api.hubapi.com/contacts/v1/lists/" + str(contact_list_id)
    result = requests.get(url,headers=headers).json()
    return result
  
  def clone_contact_list_submit_form_in_LP_by_id(self,contact_list_id,form_guid_id,page_id,contact_list_name):
    # 1) LẤY CONTACT LIST
    contact_list = self.get_contact_list_by_id(contact_list_id)

    # 2) Lọc ra những filter cũ ở trong contact_list
    list_filters = {    "name" : contact_list_name,
                        "dynamic": True,
                        "filters" : contact_list["filters"]
                    }
    for list_data in list_filters.get("filters"):
        for data in list_data:
            if data.get("filterFamily") and data.get("filterFamily") == 'FormSubmission':
                data['form'] = form_guid_id
                data['page'] = page_id

    # 3)Lưu dữ liệu vào hupspot
    headers = {"Content-Type": "application/json",
                'authorization': "Bearer " + self._access_token}
    url = "https://api.hubapi.com/contacts/v1/lists/"
    result = requests.post(url,data=json.dumps(list_filters),headers=headers)
    return result