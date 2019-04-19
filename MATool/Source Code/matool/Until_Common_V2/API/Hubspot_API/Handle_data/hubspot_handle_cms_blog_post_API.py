import requests
import json

from Until_Common_V2.API.Hubspot_API.Connection.hubspot_cms_blog_post_API import HubspotCMSBlogPostAPI
from Until_Common_V2.date_caculate import DateCaculate
from Until_Common_V2.log import Log

class HubspotHandleCMSBlogAPI(HubspotCMSBlogPostAPI):

  def __init__(self,site_id,request=None):
    HubspotCMSBlogPostAPI.__init__(self,site_id,request)

  def get_data_blog_by_id(self,id):
    #1)Lấy dữ liệu blog từ Hubspot
    data = self.get_blog_post_by_id(id)

    #2)Phân tích dữ liệu ra
    blog_info = {}
    publish_date = DateCaculate().conver_millisecond_to_datetime(data["publish_date"])# + 9*60*60*1000) 
    middle_cta_index = data['post_body'].find('cta-auto cta-middle')
    if middle_cta_index > -1 : 
      has_middle_cta = True
    else :
      has_middle_cta = False

    #CHECK FOOTER CTA
    cta_image = ''
    cta_token = ''
    is_hide_cta = False
    has_footer_cta = False
    for k,v in data['widgets'].items():
        if k == 'blog_cta':
            for k2,v2 in v.items():
                if k2 == 'body':
                    for k3,v3 in v2.items():
                        if(k3 == 'hide_cta'):
                            hide_cta_value = v3
                            if hide_cta_value:
                                is_hide_cta = True
                        if(k3 == 'guid'):
                            cta_token = v3
                        if(k3 == 'image_src'):
                            cta_image = v3

    if  not is_hide_cta:
      has_footer_cta = True

    keyword = ''
    if data['widgets'].get('text_keyword'):
      keyword = data['widgets']['text_keyword']['body']['value']

    footer_cta_guid = ''
    if data['widgets'].get('blog_cta') and data['widgets']['blog_cta']['body'].get('guid'):
      footer_cta_guid = data['widgets']['blog_cta']['body'].get('guid')
    if data['widgets'].get('blog_cta_footer') and data['widgets']['blog_cta_footer']['body'].get('guid'):
      footer_cta_guid = data['widgets']['blog_cta_footer']['body'].get('guid')

    tag_id = ''
    if data["meta"].get('tag_ids'):
      tag_id = data["meta"]['tag_ids']
        
    #Lấy kết quả trả về 
    blog_info['url'] = data["absolute_url"]
    blog_info['slug'] = data['slug']
    blog_info['has_middle_cta'] = has_middle_cta
    blog_info['has_footer_cta'] = has_footer_cta
    blog_info['id'] = data["analytics_page_id"]
    blog_info['title'] = data["title"]
    blog_info['publish_date'] = publish_date
    blog_info['tag_id'] = tag_id
    blog_info['keyword'] = keyword
    blog_info['footer_cta_guid'] = footer_cta_guid

    return blog_info
    
  def get_all_blog_posts(self):
    try:
      offset = 0
      total = 1

      list_blog_info = []

      CTA_WIDGET_NAME = 'blog_cta'
      while offset < total:
        headers = {'authorization': "Bearer " + self._access_token}
        url = "https://api.hubapi.com/content/api/v2/blog-posts" 
        url += '?limit=1000' 
        url += '&state=PUBLISHED'
        url += '&offset=' + str(offset)
        result = requests.get(url,headers=headers).json()
        #1)LẤY TẤT CẢ CÁC BLOG
        total = result['total']
        offset += 300
        print('%50s %4d'%('Get all blog post',offset))
        for data in result['objects']:
          if '/blog/' in data['absolute_url'] or "/columns/" in data["absolute_url"]:
            publish_date = DateCaculate().conver_millisecond_to_datetime(data["publish_date"])# + 9*60*60*1000) 
            middle_cta_index = data['post_body'].find('cta-auto cta-middle')
            if middle_cta_index > -1 : 
              has_middle_cta = True
            else :
              has_middle_cta = False

            #CHECK FOOTER CTA
            cta_image = ''
            cta_token = ''
            is_hide_cta = False
            has_footer_cta = False
            for k,v in data['widgets'].items():
                if k == CTA_WIDGET_NAME:
                    for k2,v2 in v.items():
                        if k2 == 'body':
                            for k3,v3 in v2.items():
                                if(k3 == 'hide_cta'):
                                    hide_cta_value = v3
                                    if hide_cta_value:
                                        is_hide_cta = True
                                if(k3 == 'guid'):
                                    cta_token = v3
                                if(k3 == 'image_src'):
                                    cta_image = v3

            if  not is_hide_cta:
              has_footer_cta = True

            keyword = ''
            if data['widgets'].get('text_keyword'):
              keyword = data['widgets']['text_keyword']['body']['value']

            footer_cta_guid = ''
            if data['widgets'].get('blog_cta') and data['widgets']['blog_cta']['body'].get('guid'):
              footer_cta_guid = data['widgets']['blog_cta']['body'].get('guid')
            if data['widgets'].get('blog_cta_footer') and data['widgets']['blog_cta_footer']['body'].get('guid'):
              footer_cta_guid = data['widgets']['blog_cta_footer']['body'].get('guid')

            tag_id = ''
            if data["meta"].get('tag_ids'):
              tag_id = data["meta"]['tag_ids']
            
            content_group_id = data['content_group_id']
            state = data['current_state']

            #Lấy kết quả trả về 
            list_blog_info.append({
                'url' : data["absolute_url"],
                'slug' : data['slug'],
                'has_middle_cta' : has_middle_cta,
                'has_footer_cta' : has_footer_cta,
                'id' : data["analytics_page_id"],
                'title' : data["title"],
                'publish_date' : publish_date,
                'tag_id' : tag_id,
                'keyword' : keyword,
                'footer_cta_guid' : footer_cta_guid,
                "content_group_id" : content_group_id,
                "state" : state,
            })
      return list_blog_info
    except Exception as e:
      Log().write_log(e)
  
  def get_all_blog_posts_by_content_group_id(self,list_hb_content_group_id):
    try:
      offset = 0
      total = 1

      list_blog_info = []

      CTA_WIDGET_NAME = 'blog_cta'
      while offset < total:
        headers = {'authorization': "Bearer " + self._access_token}
        url = "https://api.hubapi.com/content/api/v2/blog-posts" 
        url += '?limit=1000' 
        # url += '&state=PUBLISHED'
        url += '&offset=' + str(offset)
        result = requests.get(url,headers=headers).json()
        #1)LẤY TẤT CẢ CÁC BLOG
        total = result['total']
        offset += 300
        print('%50s %4d'%('Get all blog post',offset))

        for data in result['objects']:
          #1.1)Lấy content Group id ra
          content_group_id = str(data['content_group_id'])
          #1.2)Nếu nó nằm trong list cần lọc thì thực hiện lọc
          if content_group_id in list_hb_content_group_id:
            publish_date = DateCaculate().conver_millisecond_to_datetime(data["publish_date"])# + 9*60*60*1000)
            #1.3)Lấy luôn cả những trang DRAFT nhưng những trang rác thì bỏ qua
            try: 
              middle_cta_index = data['post_body'].find('cta-auto cta-middle')
            except:
              continue

            if middle_cta_index > -1 : 
              has_middle_cta = True
            else :
              has_middle_cta = False

            #CHECK FOOTER CTA
            cta_image = ''
            cta_token = ''
            is_hide_cta = False
            has_footer_cta = False
            for k,v in data['widgets'].items():
                if k == CTA_WIDGET_NAME:
                    for k2,v2 in v.items():
                        if k2 == 'body':
                            for k3,v3 in v2.items():
                                if(k3 == 'hide_cta'):
                                    hide_cta_value = v3
                                    if hide_cta_value:
                                        is_hide_cta = True
                                if(k3 == 'guid'):
                                    cta_token = v3
                                if(k3 == 'image_src'):
                                    cta_image = v3

            if  not is_hide_cta:
              has_footer_cta = True

            keyword = ''
            if data['widgets'].get('text_keyword'):
              keyword = data['widgets']['text_keyword']['body']['value']

            footer_cta_guid = ''
            if data['widgets'].get('blog_cta') and data['widgets']['blog_cta']['body'].get('guid'):
              footer_cta_guid = data['widgets']['blog_cta']['body'].get('guid')
            if data['widgets'].get('blog_cta_footer') and data['widgets']['blog_cta_footer']['body'].get('guid'):
              footer_cta_guid = data['widgets']['blog_cta_footer']['body'].get('guid')

            tag_id = ''
            if data["meta"].get('tag_ids'):
              tag_id = data["meta"]['tag_ids']
            
            state = data['current_state']

            #Lấy kết quả trả về 
            list_blog_info.append({
                'url' : data["absolute_url"],
                'slug' : data['slug'],
                'has_middle_cta' : has_middle_cta,
                'has_footer_cta' : has_footer_cta,
                'id' : data["analytics_page_id"],
                'title' : data["title"],
                'publish_date' : publish_date,
                'tag_id' : tag_id,
                'keyword' : keyword,
                'footer_cta_guid' : footer_cta_guid,
                "content_group_id" : content_group_id,
                "state" : state,
            })
      return list_blog_info
    except Exception as e:
      Log().write_log(e)

  def get_blog_post_by_publish_date(self,pusblish_start_date,pusblish_end_date):
    try:
        #1) CHUYỂN NGÀY THÁNG THÀNH MILLISECOND
        pusblish_start_millisecond = DateCaculate().conver_datetime_to_millisecond(pusblish_start_date) # - 9*60*60*1000
        pusblish_end_millisecond = DateCaculate().conver_datetime_to_millisecond(pusblish_end_date) + 24*60*60*1000 # - 9*60*60*1000
        #2) REQUEST SERVER HUBSPOT
        offset = 0
        total = 1
        list_page_info = []

        CTA_WIDGET_NAME = 'blog_cta'

        while offset < total:
            headers = {'authorization': "Bearer " + self._access_token}
            url = "https://api.hubapi.com/content/api/v2/blog-posts" 
            url += '?limit=1000'
            url += '&state=PUBLISHED'
            url += '&publish_date__range=' + str(pusblish_start_millisecond) + "," + str(pusblish_end_millisecond)
            # url += '&publish_date__lte=' + str(pusblish_end_millisecond)
            result = requests.get(url,headers=headers).json()
            total = result['total']
            offset += 300
            for data in result["objects"]:
                #LẤY RA CẢ NEWS SEMINAR NHƯNG BỎ HẾT ĐI, CHỈ CHỌN NHỮNG BÀI BLOG MÀ THÔI
                if "/blog/" in data["absolute_url"] or "/columns/" in data["absolute_url"]:
                    #ĐỊNH DẠNG TRÊN HUBSPOT LÀ MILLISECOND, CHUYỂN VỀ KIỂU NGÀY THÁNG
                    publish_date = DateCaculate().conver_millisecond_to_datetime(data["publish_date"]) #+ 9*60*60*1000) 
                    middle_cta_index = data['post_body'].find('cta-auto cta-middle')
                    if middle_cta_index > -1 : 
                        has_middle_cta = True
                    else :
                        has_middle_cta = False

                    #CHECK FOOTER CTA
                    cta_image = ''
                    cta_token = ''
                    is_hide_cta = False
                    has_footer_cta = False
                    for k,v in data['widgets'].items():
                        if k == CTA_WIDGET_NAME:
                            for k2,v2 in v.items():
                                if k2 == 'body':
                                    for k3,v3 in v2.items():
                                        if(k3 == 'hide_cta'):
                                            hide_cta_value = v3
                                            if hide_cta_value:
                                                is_hide_cta = True
                                        if(k3 == 'guid'):
                                            cta_token = v3
                                        if(k3 == 'image_src'):
                                            cta_image = v3

                    if  not is_hide_cta:
                        has_footer_cta = True

                    list_page_info.append({
                        'url' : data["absolute_url"],
                        'slug' : data['slug'],
                        'has_middle_cta' : has_middle_cta,
                        'has_footer_cta' : has_footer_cta,
                        'id' : data["analytics_page_id"],
                        'title' : data["title"],
                        "publish_date" : publish_date
                    })

        return list_page_info
    except Exception as e:
        return Log().write_log(e)

