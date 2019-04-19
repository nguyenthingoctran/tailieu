import requests
import json 
import copy

from Until_Common_V2.API.Hubspot_API.hubspot_API_auth import HubspotAPIAuth
from Until_Common_V2.date_caculate import DateCaculate
from Until_Common_V2.log import Log

class HubspotCMSPageAPI(HubspotAPIAuth):
  __scope = 'content'

  def __init__(self,site_id,request=None):
    HubspotAPIAuth.__init__(self,site_id,request)

  def get_scope(self):
    return self.__scope

  def get_page_info_by_id(self,id):
    headers = {'authorization': "Bearer " + self._access_token}
    url = "https://api.hubapi.com/content/api/v2/pages/" + str(id)

    result = requests.get(url,headers=headers).json()
    return result

  def clone_a_page(self,page_master_id,page_clone_name):
    headers = {"Content-Type": "application/json",
            'authorization': "Bearer " + self._access_token}

    url = "https://api.hubapi.com/content/api/v2/pages/" + str(page_master_id) + "/clone"

    data = {'name': page_clone_name,
            # 'is_draft': False,
            # 'state': 'PUBLISHED_OR_SCHEDULED',
            }

    result = requests.post(url,data=json.dumps(data),headers=headers).json()

    return result

  def update_landing_page(self,page_id,title,meta_description,
                            sub_title,content_title,content,campaign_name,
                            uri,form_id,email_id,thanks_page_id,page_url,image_path_on_hubspot):
    #1)Lấy page info về
    data = self.get_page_info_by_id(page_id)

    headers = {"Content-Type": "application/json",
              'authorization': "Bearer " + self._access_token}

    url = "https://api.hubapi.com/content/api/v2/pages/" + str(page_id)

    #2) Sửa các thông số trong page info

    #== Các setting cơ bản ==
    today_millisecond = DateCaculate().get_current_milliseconde()

    data['subcategory'] = "landing_page"
    data['campaign_name'] = campaign_name
    data['publish_date'] = today_millisecond

    # print("%40s %40s"%('today_millisecond',today_millisecond))
    #== Title ==
    html_title = data['html_title']
    html_title = html_title.split("|")
    html_title = title + " |" + html_title[1]

    data['html_title'] = html_title

    # print("%40s %40s"%('html_title',html_title))
    #== Meta description ==
    data['meta_description'] = meta_description

    # print("%40s %40s"%('meta_description',meta_description))
    #== Hero ==
    if data['widget_containers']['Hero_Content']['widgets'][0]['body'].get('title'):
      data['widget_containers']['Hero_Content']['widgets'][0]['body']['title'] = title

    if data['widget_containers']['Hero_Content']['widgets'][0]['body'].get('sub_title'):
      data['widget_containers']['Hero_Content']['widgets'][0]['body']['sub_title'] = sub_title

    # print("%40s %40s"%('title',title))
    # print("%40s %40s"%('sub_title',sub_title))
    #== Content ==
    if data['widget_containers']['Main_Content']['widgets'][0]['body'].get('sub_title'):
      data['widget_containers']['Main_Content']['widgets'][0]['body']['sub_title'] = content_title

    if data['widget_containers']['Main_Content']['widgets'][0]['body'].get('text'):
      data['widget_containers']['Main_Content']['widgets'][0]['body']['text'] = content

    #== PDF THUMB==
    image_file_url = "https://" + page_url + '/hubfs' + image_path_on_hubspot + uri + '.png'

    data['widget_containers']['Main_Content']['widgets'][0]['body']['image']['src'] = image_file_url
    data['widget_containers']['Main_Content']['widgets'][0]['body']['image']['alt'] = title

    # print("%40s %40s"%('content_title',content_title))
    # print("%40s %40s"%('content',content))
    # print("%40s %40s"%('campaign_name',campaign_name))
    #== SETTING ==
    slug = data['slug']
    slug = slug.rsplit('/', 1)
    slug = slug[0] + '/' + uri

    data['slug'] = slug
    data['widgets']['lp_form']['body']['form_to_use'] = form_id
    data['widgets']['lp_form']['body']['simple_email_for_live_id'] = int(email_id)
    data['widgets']['lp_form']['body']['response_redirect_id'] = int(thanks_page_id)
    # data['widgets']['lp_form']['body']['response_redirect_name'] = '[TX]' + title + " (https://" + page_url + "/" + slug + "/thanks)"

    # print("%40s %40s"%('slug',slug))
    # print("%40s %40s"%('form_id',form_id))
    # print("%40s %40s"%('email_id',email_id))
    # print("%40s %40s"%('thanks_page_id',thanks_page_id))
    result = requests.put(url,data=json.dumps(data),headers=headers).json()

    return result

  def update_thanks_page(self,page_id,title,
                            sub_title,content_title,content,campaign_name,
                            uri,page_url,pdf_path_on_hubspot):
    #1)Lấy page info về
    data = self.get_page_info_by_id(page_id)

    headers = {"Content-Type": "application/json",
              'authorization': "Bearer " + self._access_token}

    url = "https://api.hubapi.com/content/api/v2/pages/" + str(page_id)

    #2) Sửa các thông số trong page info

    #== Các setting cơ bản ==
    today_millisecond = DateCaculate().get_current_milliseconde()

    data['subcategory'] = "landing_page"
    data['publish_date'] = today_millisecond
    data['campaign_name'] = campaign_name

    # print("%40s %40s"%('today_millisecond',today_millisecond))
    #== Title ==
    html_title = data['html_title']
    html_title = html_title.split("」")
    html_title = "「" + title + "」" + html_title[1]

    data['html_title'] = html_title

    # print("%40s %40s"%('html_title',html_title))
    #== Meta description ==
    meta_description = data['meta_description']
    meta_description = meta_description.split("」")
    meta_description = "「" + title + "」" + meta_description[1]

    data['meta_description'] = meta_description

    # print("%40s %40s"%('meta_description',meta_description))
    #== Hero ==
    param_title = data['widget_containers']['Hero_Content']['widgets'][0]['body']['title']
    param_title = param_title.split("」")
    param_title = "「" + title + "」" + param_title[1]

    if data['widget_containers']['Hero_Content']['widgets'][0]['body'].get('title'):
      data['widget_containers']['Hero_Content']['widgets'][0]['body']['title'] = param_title

    if data['widget_containers']['Hero_Content']['widgets'][0]['body'].get('sub_title'):
      data['widget_containers']['Hero_Content']['widgets'][0]['body']['sub_title'] = sub_title

    # print("%40s %40s"%('param_title',param_title))
    #== Content ==
    content_title = data['widget_containers']['Hero_Content']['widgets'][0]['body']['title']
    content_title = content_title.split("」")
    content_title = "「" + title + "」" + content_title[1]
    pdf_file_url = "https://" + page_url + '/hubfs' + pdf_path_on_hubspot + uri + '.pdf'

    data['widget_containers']['Main_Content']['widgets'][0]['body']['title'] = content_title
    data['widget_containers']['Main_Content']['widgets'][0]['body']['pdf_url'] = pdf_file_url

    # print("%40s %40s"%('content_title',content_title))
    # print("%40s %40s"%('content',content))
    # print("%40s %40s"%('campaign_name',campaign_name))
    #== SETTING ==
    slug = data['slug']
    slug = slug.rsplit('/', 2)
    slug = slug[0] + '/' + uri + '/thanks'

    data['slug'] = slug

    # print("%40s %40s"%('slug',slug))
    result = requests.put(url,data=json.dumps(data),headers=headers).json()

    return result

  def update_resource_page(self,resource_page_id,landing_page_id,
                            title,image_path_on_hubspot,uri,page_url,
                            select_category,select_resource,select_resource_pos):
    try:
      headers = {"Content-Type": "application/json",
                'authorization': "Bearer " + self._access_token}

      url = "https://api.hubapi.com/content/api/v2/pages/" + str(resource_page_id)

      #1)Lấy page info về
      data = self.get_page_info_by_id(resource_page_id)

      #2)Thêm resource vào 
      widgets = data['widget_containers']['Main_Content']['widgets']

      for i in range(len(widgets)):
        if widgets[i]['body']['title'] == select_category:
          # 2.1)Clone ra 1 cái khung rồi sửa lại
          resource_json = copy.deepcopy(widgets[i]['body']['field_group'][0])

          image_file_url = "https://" + page_url + '/hubfs' + image_path_on_hubspot + uri + '.png'

          resource_json['flex_image']['alt'] = title
          resource_json['flex_image']['src'] = image_file_url

          resource_json['flex_title'] = title
          resource_json['flex_page_link'] = int(landing_page_id)

          # 2.2)Thêm vào trong data rồi đưa lên lại
          data['widget_containers']['Main_Content']['widgets'][i]['body']['field_group'].insert(select_resource + select_resource_pos,resource_json)
        else:
          continue
          
      result = requests.put(url,data=json.dumps(data),headers=headers).json()
      return result
    except Exception as e:
      Log().write_log(e)