from Until_Common_V2.API.Hubspot_API.Connection.hubspot_contact_properties_API import HubspotContactPropertiesAPI

class HubspotHandleContactPropertiesAPI(HubspotContactPropertiesAPI):

  def __init__(self,site_id,request=None):
    HubspotContactPropertiesAPI.__init__(self,site_id,request)

  def get_list_properties(self):
    #1)Lấy dữ liệu từ Hubspot
    response = self.get_list_properties()

    #2)Phân tích dữ liệu
    list_properties = {}
    for r in response:
        list_properties[r['name']] = r['label']
    return list_properties
