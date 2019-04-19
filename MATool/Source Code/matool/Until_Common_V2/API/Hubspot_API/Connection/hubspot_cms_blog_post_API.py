import requests

from Until_Common_V2.API.Hubspot_API.hubspot_API_auth import HubspotAPIAuth

class HubspotCMSBlogPostAPI(HubspotAPIAuth):
  __scope = 'content'
  
  def __init__(self,site_id,request=None):
    HubspotAPIAuth.__init__(self,site_id,request)

  def get_scope(self):
    return self.__scope

  def get_blog_post_by_id(self,id):
    headers = {'authorization': "Bearer " + self._access_token}
    url = "https://api.hubapi.com/content/api/v2/blog-posts/" + str(id)
    result = requests.get(url,headers=headers).json()
    return result

  