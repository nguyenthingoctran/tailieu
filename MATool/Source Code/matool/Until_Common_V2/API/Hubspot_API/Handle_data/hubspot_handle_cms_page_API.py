import requests

from Until_Common_V2.API.Hubspot_API.Connection.hubspot_cms_page_API import HubspotCMSPageAPI
from Until_Common_V2.date_caculate import DateCaculate

class HubspotHandleCMSPageAPI(HubspotCMSPageAPI):

  def __init__(self,site_id,request=None):
    HubspotCMSPageAPI.__init__(self,site_id,request)

  def get_data_page_info_by_id(self,id):
    #1)Lấy dữ liệu từ Hubspot
    data = self.get_page_info_by_id(id)

    #2)Phân tích dữ liệu
    page_info = {}

    #2.1)Đổi định dạng ngày tháng
    publish_date = DateCaculate().conver_millisecond_to_datetime(data["publish_date"])
    
    #2.2)Lấy dữ liệu để trả về
    page_info['url'] = data["absolute_url"]
    page_info['id'] = data["analytics_page_id"]
    page_info['title'] = data["html_title"]
    page_info['publish_date'] = publish_date
    page_info['label'] = data["label"]

    return page_info
    
  def get_all_resources_page(self):
    #1)Các biến để tiến hành lọc dữ liệu
    offset = 0
    total = 1
    list_page_info = []

    #2)Vòng lặp để lọc dữ liệu
    while offset < total:
      headers = {'authorization': "Bearer " + self._access_token}
      url = "https://api.hubapi.com/content/api/v2/pages"
      url += '?limit=1000'
      result = requests.get(url, headers=headers).json()
      #2.1)LẤY TẤT CẢ CÁC CONTACT
      total = result['total']
      offset += 300
      print('%50s %4d'%('Get all resources page',offset))

      #2.2)CÓ CÁI LÀ /resources/ có cái là /resource
      for data in result["objects"]:
        if '/resource' in data["absolute_url"] and '/thanks' not in data["absolute_url"]:
          publish_date = DateCaculate().conver_millisecond_to_datetime(data["publish_date"])
          
          list_page_info.append({
                                  'url': data["absolute_url"],
                                  'id': data["analytics_page_id"],
                                  'title' : data["html_title"],
                                  'publish_date' : publish_date,
                                  'label' : data['label'],
                              })
    return list_page_info

  def get_all_resources_page_by_publish_date(self,pusblish_start_date,pusblish_end_date):
    #1) CHUYỂN NGÀY THÁNG THÀNH MILLISECOND
    pusblish_start_millisecond = DateCaculate().conver_datetime_to_millisecond(pusblish_start_date) # - 9*60*60*1000
    pusblish_end_millisecond = DateCaculate().conver_datetime_to_millisecond(pusblish_end_date) + 24*60*60*1000  #- 9*60*60*1000

    #2) REQUEST SERVER HUBSPOT
    offset = 0
    total = 1
    list_page_info = []
    while offset < total:
      headers = {'authorization': "Bearer " + self._access_token}
      url = "https://api.hubapi.com/content/api/v2/pages"
      url += '?limit=1000'
      url += '&publish_date__range=' + str(pusblish_start_millisecond) + "," + str(pusblish_end_millisecond)
      result = requests.get(url, headers=headers).json()
      #2.1)LẤY TẤT CẢ CÁC CONTACT
      total = result['total']
      offset += 300
      print('%50s %4d'%('Get all resources',offset))
      for data in result["objects"]:
        if '/resources/' in data["absolute_url"] and '/thanks' not in data["absolute_url"]:
          #2.2)ĐỊNH DẠNG TRÊN HUBSPOT LÀ MILLISECOND, CHUYỂN VỀ KIỂU NGÀY THÁNG
          publish_date = DateCaculate().conver_millisecond_to_datetime(data["publish_date"]) #+ 9*60*60*1000) 
          
          list_page_info.append({'url': data["absolute_url"], 
                                  'id': data["analytics_page_id"],
                                  'title':data["title"],
                                  'label':data['label'],
                                  "publish_date" : publish_date})
    return list_page_info

  def get_all_pages(self):
    #1)Các biến để tiến hành lọc dữ liệu
    offset = 0
    total = 1
    list_page_info = []
    #2)Vòng lặp để lọc dữ liệu
    while offset < total:
      headers = {'authorization': "Bearer " + self._access_token}
      url = "https://api.hubapi.com/content/api/v2/pages"
      url += '?limit=1000'
      url += '&is_draft=false'
      url += '&archived=false'

      result = requests.get(url, headers=headers).json()
      #2.1)LẤY TẤT CẢ CÁC CONTACT
      if 'total' in result:
        total = result['total']
        offset += 300
        print('%50s %4d'%('Get all pages',offset))
        #2.2)CÓ CÁI LÀ /resources/ có cái là /resource
        for data in result["objects"]: 
          list_page_info.append({
                                  'url': data["absolute_url"],
                                  'id': data["analytics_page_id"],
                                  'title' : data["name"],
                                  'publish_date' : data['publish_date']
          })
    return list_page_info