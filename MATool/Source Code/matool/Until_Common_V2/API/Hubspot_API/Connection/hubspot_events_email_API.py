import requests

from Until_Common_V2.API.Hubspot_API.hubspot_API_auth import HubspotAPIAuth
from Until_Common_V2.date_caculate import DateCaculate

#Khai báo date caculate
date_caculate = DateCaculate()

class HubspotEventsEmailAPI(HubspotAPIAuth):
  __scope = 'content'

  def __init__(self,site_id,request=None):
    HubspotAPIAuth.__init__(self,site_id,request)

  def get_scope(self):
    return self.__scope

  def get_campaign_data_for_a_campaign(self,campaign_id):
    headers = {'authorization': "Bearer " + self._access_token}
    url = "https://api.hubapi.com/email/public/v1/campaigns/{0}?".format(campaign_id)
    result = requests.get(url,headers=headers).json()
    return result


