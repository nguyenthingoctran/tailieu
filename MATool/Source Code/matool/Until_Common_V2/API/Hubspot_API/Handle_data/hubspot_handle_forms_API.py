from Until_Common_V2.API.Hubspot_API.Connection.hubspot_forms_API import HubspotFormsAPI

class HubspotHandleFormsAPI(HubspotFormsAPI):

  def __init__(self,site_id,request=None):
    HubspotFormsAPI.__init__(self,site_id,request)

  def get_form_name_and_guid_id(self):
    #1)Lấy dữ liệu từ Hubspot
    result = self.get_all_form()

    #2)Phân tích dữ liệu
    list_forms = []
    for data in result:
        form_name = data['name']
        form_guid_id = data['guid']
        list_forms.append({'guid' : form_guid_id,'name':form_name})

    return list_forms
