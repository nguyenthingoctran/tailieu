import requests

from Until_Common_V2.API.Hubspot_API.Connection.hubspot_events_email_API import HubspotEventsEmailAPI
from Until_Common_V2.date_caculate import DateCaculate

#Khai báo date caculate
date_caculate = DateCaculate()

class HubspotHandleEventsEmailAPI(HubspotEventsEmailAPI):

  def __init__(self,site_id,request=None):
    HubspotEventsEmailAPI.__init__(self,site_id,request)

  #Lấy tổng số Campain ID của gmail, mỗi mail có 1 campaing id riêng
  def get_list_name_total_campaign_email(self):
    list_id = self.get_list_all_campaign_for_a_portal()
    #1) lấy tất cả tên mail theo id
    list_mail_name = [] 
    for campaign_id in list_id:
      result = self.get_campaign_data_for_a_campaign(campaign_id)
      list_mail_name.append(result['name'])
    
    #2) Lọc những mail trùng tên
    set_data = set(list_mail_name)
    #2.1)format set ve list
    #2.1.1)tỉ lệ chênh lệch 1 -- > 4
    list_data = list(set_data)

    return list_data

  def get_list_all_campaign_for_a_portal(self):
    headers = {'authorization': "Bearer " + self._access_token}
    has_more = True
    offset = ""
    list_total_email_campain_id = []
    while has_more == True:

      url = "https://api.hubapi.com/email/public/v1/campaigns/by-id?" + str(offset)
      url += '&limit=1000'

      result = requests.get(url, headers=headers).json()
      if 'campaigns' in result:
        for i in result['campaigns']:
          list_total_email_campain_id.append(i['id'])

      has_more = result['hasMore']
      offset = "offset=" + str(result['offset']) + "&"

    #1)Lọc những list_campain có trùng giá trị bằng set()
    set_list_total_email_campain_id = set(list_total_email_campain_id)
    #2) format kết quả đã set() thành list()
    result_list_total_email_campain_id = list(set_list_total_email_campain_id)

    return result_list_total_email_campain_id

  #Hàm lấy số lượng email theo khoảng thời gian và loại sự kiện lựa chọn
  def get_list_email_by_type_event(self,start_date,end_date,sent_type=False,deliver_type=False,open_type=False,click_type=False):
    #1) các biến setting lấy dữ liệu
    type_event = ''
    #1.1) chọn loại event mail lấy dữ liệu
    if sent_type == True:
      type_event = 'SENT'
    elif deliver_type == True:
      type_event = 'DELIVERED'
    elif open_type == True :
      type_event = 'OPEN'
    elif click_type == True:
      type_event = 'CLICK'  

    has_more = True
    offset = ""
    headers = {'authorization': "Bearer " + self._access_token}
    date_start_millisecond = date_caculate.conver_datetime_to_millisecond(start_date) 
    date_end_millisecond = date_caculate.conver_datetime_to_millisecond(end_date) + 24*60*60*1000
    list_result = []
    while has_more == True:

      url = "https://api.hubapi.com/email/public/v1/events?" + str(offset)
      url += "eventType={0}&startTimestamp={1}&endTimestamp={2}&excludeFilteredEvents=True".format(type_event,date_start_millisecond,date_end_millisecond)
      url += '&limit=1000'

      result = requests.get(url, headers=headers).json()
      if 'events' in result:
        for i in result['events']:
            list_result.append(i)
      
      has_more = result['hasMore']
      offset = "offset=" + str(result['offset']) + "&"
    
    return list_result

  #Hàm lấy id mail của Shot mail
  def get_list_campain_email_for_shot_mail(self):

    has_more = True
    headers = {'authorization': "Bearer " + self._access_token}
    offset = ""
    list_email_campain_id = []

    while has_more == True:

      url = "https://api.hubapi.com/email/public/v1/campaigns/by-id?" + str(offset)
      url += '&limit=1000'

      result = requests.get(url, headers=headers).json()
      for i in result['campaigns']:
          
        if i['appId'] == 113 :
          list_email_campain_id.append(i['id'])

      has_more = result['hasMore']
      offset = "offset=" + str(result['offset']) + "&"   
  
    return list_email_campain_id
 