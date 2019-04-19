import requests
import urllib
import urllib.parse

from bs4 import BeautifulSoup
from pprint import pprint

from urllib.request import Request, urlopen
from Until_Common_V2.HTML.check_html import CheckHTML 
from Until_Common_V2.log import Log
from Until_Common_V2.db_helper import db_helper

class ReadHtml:
  def get_page_content_from_url(self,url):
    try:
      req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
      webpage = urlopen(req).read()
    except:
      # CÁC ĐỊNH DẠNG URL CÓ TIẾNG NHẬT Ở TRONG 'https://www.yamato-b2b-pay.com/blog/tag/クロネコ掛け払い'
      url = urllib.parse.urlsplit(url)
      url = list(url)
      url[2] = urllib.parse.quote(url[2])
      url = urllib.parse.urlunsplit(url)
      req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
      webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage,'lxml')

    return soup

  def conver_href_to_url(self,base_url,list_href):
    #1)LẤY TẤT CẢ LINK TRONG THẺ A
    delete_pos = []
    #1.1)LỌC QUA ĐỂ ĐỊNH DẠNG LẠI TẤT CẢ CÁC LINK TRONG THẺ A THÀNH url
    for i,href in enumerate(list_href):
      #1.1.1)NẾU LÀ 1 URL 
      if CheckHTML().check_url(href) == True: 
        continue

      #1.1.2)NẾU TỚI ĐƯỢC ĐÂY THÌ NÓ KHÔNG PHẢI LÀ 1 URL
      #HOẶC NẾU BẮT ĐẦU BẰNG 2 DẤU //
      if href.startswith("//") == True:
        list_href[i] = list_href[i].replace('//','https://',1)
        continue

      #N1.1.3)ẾU BẮT ĐẦU KHÔNG PHẢI LÀ DẤU / THÌ BỎ QUA
      if href.startswith("/") == True:
        list_href[i] = base_url + list_href[i]
      else:
        delete_pos.append(i)
        continue 

    #2)XÓA NHỮNG PHẦN TỬ KHÔNG HỢP LỆ
    delete_pos.sort(reverse = True)
    for i in delete_pos:
      list_href.pop(i)

    return list_href

  def get_all_a_link_in_page(self,url):
    soup = self.get_page_content_from_url(url)

    list_href = []
    #1)Tìm tất cả thẻ <a> trong html
    for a in soup.find_all('a'):
      #1.1)NẾU CÓ LINK THÌ MỚI ĐƯA VÀO
      if a.get('href') != None:
        list_href.append(a.get('href'))

    return list_href

  def get_all_js_link_in_page(self,url):
    soup = self.get_page_content_from_url(url)

    list_href = []
    #1)Tìm tất cả thẻ <script> trong html
    for a in soup.find_all('script'):
      #1.1)NẾU CÓ LINK THÌ MỚI ĐƯA VÀO
      if a.get('src') != None:
        list_href.append(a.get('src'))

    return list_href

  def get_all_img_link_in_page(self,url):
    soup = self.get_page_content_from_url(url)

    list_href = []
    #1)Tìm tất cả thẻ <img> trong html
    for a in soup.find_all('img'):
      #1.1)NẾU CÓ LINK THÌ MỚI ĐƯA VÀO
      if a.get('src') != None:
        list_href.append(a.get('src'))

    return list_href

  def get_all_css_link_in_page(self,url):
    soup = self.get_page_content_from_url(url)

    list_href = []
    #1)Tìm tất cả thẻ <link> trong html
    for a in soup.find_all('link'):
      #1.1)NẾU CÓ LINK THÌ MỚI ĐƯA VÀO
      if a.get('href') != None:
        list_href.append(a.get('href'))

    return list_href

  def get_base_url_from_url(self,url):
    parsed_uri = urllib.parse.urlparse(url)
    result = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_uri)
    return result

  #===================================
  # === Lấy Follower trên FB và TW ===
  #===================================
  def get_social_followers_for_site(self,param_site_id):
    try:
      db_controller = db_helper()

      sql_query_site_info = '''Select * from report_site_setting 
                                  where site_id = {0}
                              '''.format(param_site_id)
      object_site_info = db_controller.query(sql_query_site_info)

      fb_url = object_site_info[0]['facebook_url']
      tw_url = object_site_info[0]['twitter_url']

      if fb_url != None:
          follow_fb = int(self.extract_followers_fb(fb_url))
      else:     
          follow_fb = 0
      if tw_url != None:    
          follow_tw = int(self.extract_followers_tw(tw_url))
      else:
          follow_tw = 0 
  
      return follow_fb, follow_tw
    except Exception as inst:
      Log().write_log(inst)

  def extract_followers_fb(self,url):
    print('extract_followers_fb -> url ' + url)
    result = 'Error'
    try :
      fb_pattern = 'people follow this'
      fb_pattern_jp = '人がフォローしています'
      fb_pattern_vn = 'người theo dõi trang này'
      has_in_en = True
      has_in_jp = False
      has_in_vn = False
      followers_num_value = ''

      page_response = requests.get(url)
      page_html = page_response.text
      number_indexof = page_html.find(fb_pattern)
      if number_indexof == -1:
        number_indexof =  page_html.find(fb_pattern_jp)
        has_in_en = False
        has_in_vn = False
        has_in_jp = True

      if number_indexof == -1:
        number_indexof =  page_html.find(fb_pattern_vn)
        has_in_en = False
        has_in_jp = False
        has_in_vn = True

      is_finish = False
      number_indexof -= 1
      while number_indexof > 0 and not is_finish:
        if page_html[number_indexof] != '>':
          followers_num_value += page_html[number_indexof]
        else :
          is_finish = True
        number_indexof -= 1                    

      result = followers_num_value[::-1]

      # Xu ly ky tu dac biet
      result = result.replace('.','')
      result = result.replace(',','')  
      return result
    except Exception as inst:
      Log().write_log(inst)
    return result

  def extract_followers_tw(self,url):
    result = 'Error'
    try:
      html_li_start = '<li class="ProfileNav-item ProfileNav-item--followers">'
      html_li_end = '</li>'

      html_cut_start = 'data-count='
      html_cut_end = 'data-is-compact'
      
      followers_num_value = 'Error'

      page_response = requests.get(url)
      page_html = page_response.text
      num_list_start = page_html.find(html_li_start)
      num_list_end = page_html.find(html_li_end, num_list_start)

      if num_list_start != -1 and num_list_end != -1:
        li_html = page_html[num_list_start:num_list_end]
        followers_num_value = li_html
        num_html_cut_start = followers_num_value.find(html_cut_start)
        num_html_cut_end = followers_num_value.find(html_cut_end, num_html_cut_start)
        if num_html_cut_start != -1 and num_html_cut_end != -1:
          num_trim_start = num_html_cut_start + len(html_cut_start) 
          num_trim_end = num_html_cut_end - 1
          followers_num_value = followers_num_value[num_trim_start:num_trim_end]
          
      result = followers_num_value

      # Xu ly ky tu dac biet
      result = result.replace('.','') 
      return result
    except Exception as inst:
      Log().write_log(inst)
    return result        