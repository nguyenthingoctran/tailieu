import requests

from Until_Common_V2.API.Hubspot_API.Connection.hubspot_contact_lists_API import HubspotContactListsAPI

class HubspotHandleContactListsAPI(HubspotContactListsAPI):
  
  def __init__(self,site_id,request=None):
    HubspotContactListsAPI.__init__(self,site_id,request)

  def get_all_contact_in_contact_list(self,contact_list_id):
    headers = {'authorization': "Bearer " + self._access_token}
    # 1) CÁC BIẾN ĐỂ THỰC HIỆN VÒNG LẶP
    has_more = True
    vid_offset = ''
    dict_data = {}

    # 2) LẤY DỮ LIỆU TỪ HUBSPOT
    while has_more == True:
      url = "https://api.hubapi.com/contacts/v1/lists/" + str(contact_list_id) + "/contacts/all"
      url += '?count=100'
      url += '&property=firstname'
      url += '&property=lastname'
      url += '&property=company'
      url += '&property=email'
      url += '&property=phone'
      url += '&property=state'
      url += '&property=city'
      url += '&property=annualrevenue'
      url += '&property=number_of_employees_en'
      url += '&property=industry_en'
      url += '&property=annual_sales'
      url += '&property=jobtitle'
      url += '&property=resource_title'
      url += '&property=thank_page_url'
      url += '&property=lptool_daily_send'
      url += '&property=createdate'
      url += '&property=erp_odp_ns'
      url += '&vidOffset=' + str(vid_offset)
      result = requests.get(url,headers=headers).json()

      #2.1)Lấy 2 biến này để tiếp tục vòng lặp
      has_more = result['has-more']
      vid_offset = result['vid-offset']
      #2.2)Xử lý các contact
      list_contacts = result['contacts']
      for contact in list_contacts:
        #LẤY PROPERTIES VÀ VID_ID
        dict_data[contact['vid']] = {"properties" : contact['properties']}
    return dict_data
  