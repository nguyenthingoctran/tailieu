import requests
import json

from Until_Common_V2.API.Hubspot_API.hubspot_API_auth import HubspotAPIAuth

class HubspotFiletsAPI(HubspotAPIAuth):
  __scope = 'files'

  def __init__(self,site_id,request=None):
    HubspotAPIAuth.__init__(self,site_id,request)

  def get_scope(self):
    return self.__scope

  def upload_file(self,folder_paths,files,file_names):
    headers = {'authorization': "Bearer " + self._access_token}
    url = "https://api.hubapi.com/filemanager/api/v2/files"

    #Vị trí lưu file trên server
    data = {
            "folder_paths": folder_paths,
            "file_names" : file_names,
            }

    my_files = {'files': files}
    result = requests.post(url,data=data,files=my_files,headers=headers)
    return result