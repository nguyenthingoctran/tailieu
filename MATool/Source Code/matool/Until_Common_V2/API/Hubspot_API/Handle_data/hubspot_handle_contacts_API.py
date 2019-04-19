import requests

from Until_Common_V2.API.Hubspot_API.Connection.hubspot_contacts_API import HubspotContactsAPI

class HubspotHandleContactsAPI(HubspotContactsAPI):

  def __init__(self,site_id,request=None):
    HubspotContactsAPI.__init__(self,site_id,request)

  def get_data_contact_by_id(self,id):
    #1)Lấy dữ liệu từ Hubspot
    contact = self.get_contact_by_id(id)
    
    #2)Phân tích dữ liệu
    dict_data = {}
    dict_data[contact['vid']] = contact['properties']
    return dict_data

  def get_all_contact(self):
    headers = {'authorization': "Bearer " + self._access_token}
    # 1) CÁC BIẾN ĐỂ THỰC HIỆN VÒNG LẶP
    has_more = True
    vid_offset = ''
    dict_data = {}
    count = -100
    # 2) LẤY DỮ LIỆU TỪ HUBSPOT
    while has_more == True:
      count += 100
      print("%40s %10d" %("Get All Contact",count))

      url = "https://api.hubapi.com/contacts/v1/lists/all/contacts/all"
      url += '?count=100'
      url += '&property=firstname'
      url += '&property=lastname'
      url += '&property=company'
      url += '&property=email'
      url += '&property=phone'
      url += '&property=state'
      url += '&property=city'
      url += '&property=annualrevenue'
      url += '&property=numemployees'
      url += '&property=industry_en'
      url += '&property=annual_sales'
      url += '&property=jobtitle'
      url += '&property=resource_title'
      url += '&property=thank_page_url'
      url += '&property=lptool_daily_send'
      url += '&property=industry'
      url += '&property=business_challenge'
      url += '&property=department_type'
      url += '&property=problem_solving_time'
      url += '&property=roi_calculation'
      url += '&property=createdate'
      url += '&property=notes_last_updated'
      url += '&vidOffset=' + str(vid_offset)

      result = requests.get(url,headers=headers).json()

      #2.1)Lấy 2 biến này để tiếp tục vòng lặp
      has_more = result['has-more']
      vid_offset = result['vid-offset']
      #2.2)Xử lý các contact
      list_contacts = result['contacts']

      for contact in list_contacts:
        dict_data[contact['vid']] = contact['properties']

    return dict_data  