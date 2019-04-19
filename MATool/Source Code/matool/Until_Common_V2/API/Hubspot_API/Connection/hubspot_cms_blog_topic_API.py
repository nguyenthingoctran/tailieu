import requests

from Until_Common_V2.API.Hubspot_API.hubspot_API_auth import HubspotAPIAuth

class HubspotCMSBlogTopicAPI(HubspotAPIAuth):
  __scope = 'content'
  
  def __init__(self,site_id,request=None):
    HubspotAPIAuth.__init__(self,site_id,request)

  def get_scope(self):
    return self.__scope

  def get_list_blog_post_topics(self):
    headers = {'authorization': "Bearer " + self._access_token}
    url = "https://api.hubapi.com/blogs/v3/topics?limit=1000"
    result = requests.get(url,headers=headers).json()
    return result

  