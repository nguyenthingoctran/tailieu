import requests

from Until_Common_V2.API.Hubspot_API.hubspot_API_auth import HubspotAPIAuth

class HubspotAnalyticsAPI(HubspotAPIAuth):
  __scope = 'business-intelligence'

  def __init__(self,site_id,request=None):
    HubspotAPIAuth.__init__(self,site_id,request)

  def get_scope(self):
    return self.__scope
    
  def get_analytics_landing_page(self,start_date, end_date):
    start_date = start_date.replace("-",'')
    end_date = end_date.replace("-",'')

    headers = {'authorization': "Bearer " + self._access_token}
    url = "https://api.hubapi.com/analytics/v2/reports/landing-pages/total" 
    url += '?start=' + start_date
    url += '&end=' + end_date
    url += '&limit=10000'

    result = requests.get(url,headers=headers).json()
    return result

  def get_analytics_landing_page_sort_by_submissions(self,start_date, end_date):
    start_date = start_date.replace("-",'')
    end_date = end_date.replace("-",'')

    headers = {'authorization': "Bearer " + self._access_token}
    url = "https://api.hubapi.com/analytics/v2/reports/landing-pages/total" 
    url += '?start=' + start_date
    url += '&end=' + end_date
    url += '&limit=10000'
    url += '&sort=submissions'
    result = requests.get(url,headers=headers).json()

    return result

  def get_analytics_blog_post(self,start_date,end_date):
    start_date = start_date.replace("-",'')
    end_date = end_date.replace("-",'')

    headers = {'authorization': "Bearer " + self._access_token}
    url = "https://api.hubapi.com/analytics/v2/reports/blog-posts/total" 
    url += '?start=' + start_date
    url += '&end=' + end_date
    result = requests.get(url,headers=headers).json()
    return result
  
  #Đường dẫn trên Hubspot Report => Analytics Tools => Analytics Traffics
  #Cái này mức độ tổng hợp cao hơn get_analytics_sources()
  def get_analytics_total(self,start_date, end_date):
    start_date = start_date.replace("-",'')
    end_date = end_date.replace("-",'')

    headers = {'authorization': "Bearer " + self._access_token}
    url = 'https://api.hubapi.com/analytics/v2/reports/totals/total'
    url += '?start=' + start_date
    url += '&end=' + end_date 
    result = requests.get(url,headers=headers)
    return result.json()

  #Đường dẫn trên Hubspot Report => Analytics Tools => Analytics Traffics
  def get_analytics_sources(self,start_date, end_date):
    start_date = start_date.replace("-",'')
    end_date = end_date.replace("-",'')

    headers = {'authorization': "Bearer " + self._access_token}
    url = 'https://api.hubapi.com/analytics/v2/reports/sources/total'
    url += '?start=' + start_date
    url += '&end=' + end_date 
    result = requests.get(url,headers=headers)
    return result.json()

  def get_analytics_sources_exclude_offline(self,start_date, end_date):
    start_date = start_date.replace("-",'')
    end_date = end_date.replace("-",'')

    headers = {'authorization': "Bearer " + self._access_token}
    url = 'https://api.hubapi.com/analytics/v2/reports/sources/total'
    url += '?start=' + start_date
    url += '&end=' + end_date
    url += '&e=offline'
    result = requests.get(url,headers=headers)
    return result.json() 

  def get_analytic_landing_page_by_id(self,start_date,end_date,page_id):
    #1) format date
    start_date_check = start_date.replace("-","")
    end_date_check = end_date.replace("-","")
    #1.1)biến setting
    headers = {'authorization': "Bearer " + self._access_token}
    #2) lấy dữ liệu
    url = 'https://api.hubapi.com/analytics/v2/reports/landing-pages/'
    url += str(page_id) + '/sources/total?' + 'start=' + start_date_check + '&end=' + end_date_check
    
    result = requests.get(url,headers=headers).json()
    return result

  def get_analytic_blog_post_by_id(self,start_date,end_date,blog_id):
    #1) format date
    start_date_check = start_date.replace("-","")
    end_date_check = end_date.replace("-","")
    #1.1)biến setting
    headers = {'authorization': "Bearer " + self._access_token}
    #2) lấy dữ liệu
    url = 'https://api.hubapi.com/analytics/v2/reports/blog-posts/'
    url += str(blog_id) + '/sources/total?' + 'start=' + start_date_check + '&end=' + end_date_check
    
    result = requests.get(url,headers=headers).json()
    return result  