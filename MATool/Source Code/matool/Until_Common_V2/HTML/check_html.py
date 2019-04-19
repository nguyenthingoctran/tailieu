import requests
import urllib
import urllib.parse

from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from Until_Common_V2.HTML.read_html import ReadHtml
from pprint import pprint

class CheckHTML:
    def check_link_file(self,url):
      list_file = ['.pdf','.jpg','.png','.css','.js']

      #NẾU LÀ 1 LINK FILE THÌ TRẢ VỀ TRUE
      for data in list_file:
        if data in url:
          return True
      
      return False

    def check_sanbox_link_in_page(self,list_url):
      dict_result = {}

      for url in list_url:
        # LẤY LINK Ở TRONG THẺ <a>
        list_a_link = ReadHtml().get_all_a_link_in_page(url)
        # Trả về list sanbox link  trong trang đó
        list_sanbox_link = []
        for link in list_a_link:
          if 'sanbox' in link:
            list_sanbox_link.append(link)
        #Lấy kết quả trả về
        dict_result[url] = {'sanbox_link':list_sanbox_link}
      
      return dict_result

    def check_404_a_link_in_page(self,list_url):
        dict_result = {}
        #LƯU NHỮNG TRANG ĐÃ CHECK RỒI
        list_200_all_page = set()
        list_301_all_page = set()
        list_404_all_page = set()
        #LẤY base_url = https://www.yamato-b2b-pay.com/
        base_url = ReadHtml().get_base_url_from_url(list_url[0])

        count = 0
        for url in list_url:
            count += 1
            print("%4d %10s %100s"%(count,"URL",url))
            #KIỂM TRA PAGE TRƯỚC KHI ĐƯA VÀO LẤY LIST URL
            if self.check_301_404_error(url) == 404:
                list_404_all_page.add(url)
                continue
            elif self.check_301_404_error(url) == 301:
                list_301_all_page.add(url)
                continue
            elif self.check_301_404_error(url) == 200:
                list_200_all_page.add(url)

            #NẾU LÀ 1 LINK FILE PDF,IMG,JPG ... THÌ BỎ QUA KHÔNG CHECK
            if self.check_link_file(url) == True:
                continue
            # =========== CHECK THẺ <a> ===================
            # LẤY LINK Ở TRONG THẺ <a>
            list_a_link = ReadHtml().get_all_a_link_in_page(url)
            list_a_link = ReadHtml().conver_href_to_url(base_url,list_a_link)
            # pprint(list_a_link)
            list_a_link_200 = []
            list_a_link_301 = []
            list_a_link_404 = []
            for link in list_a_link:
                print("%4d %10s %100s"%(count,"<a> LINK",link))
                
                #NHỮNG LINK ĐÃ CHECK RỒI THÌ KHÔNG CHECK LẠI
                if link in list_200_all_page:
                    list_a_link_200.append(link)
                    continue
                elif link in list_301_all_page:
                    list_a_link_301.append(link)
                    continue
                elif link in list_404_all_page:
                    list_a_link_404.append(link)
                    continue

                #NHỮNG LINK MỚI CHƯA CÓ THÌ MỚI PHẢI CHECK LẠI
                if self.check_301_404_error(link) == 200:
                    list_200_all_page.add(link)
                    list_a_link_200.append(link)

                elif self.check_301_404_error(link) == 301:
                    list_301_all_page.add(link)
                    list_a_link_301.append(link)

                elif self.check_301_404_error(link) == 404:
                    list_404_all_page.add(link)
                    list_a_link_404.append(link)
            
            # =========== END CHECK THẺ <a> ===================
            dict_result[url] = {'<a>':{ 
                            200: list_a_link_200,
                            301: list_a_link_301,
                            404: list_a_link_404
                            }}
        
        return dict_result

    def check_title(self,url):
      try:
        #1) LẤY DỮ LIỆU TỪ URL
        soup = read_html.get_page_content_from_url(url)
        #2) PHÂN TÍCH DỮ LIỆU TRONG URL
        #NẾU LÀ TRANG PDF IMG THÌ BỎ QUA
        if check_link_file(url):
          return -1
        html_title = soup.title.text
        param_title = html_title.split("|")
        #NẾU TITLE CHỈ CÓ 1 BÊN THÌ CŨNG LÀ SAI,TITLE PHẢI CÓ DẤU |
        if len(param_title) != 2:
          return False

        # KHOẢNG CÁCH TRƯỚC VÀ SAU KHI XÓA SPACE
        sub_len_1 = len(param_title[0]) - len(param_title[0].strip())
        sub_len_2 = len(param_title[1]) - len(param_title[1].strip())

        if sub_len_1 == 1 and sub_len_2 == 1:
          return True
        else:
          return False
      except:
        return False

    def check_meta_description(self,url):
      try:
        # LẤY META DESCRIPTION
        soup = read_html.get_page_content_from_url(url)
        #NẾU LÀ TRANG PDF IMG THÌ BỎ QUA
        if check_link_file(url):
          return -1
        meta_description = soup.find('meta',{"name":"description"})['content']

        #KIỂM TRA XEM CÓ KHOẢNG TRẮNG Ở ĐẦU KHÔNG
        sub_len_1 = len(meta_description) - len(meta_description.strip())

        if sub_len_1 == 0:
          return True
        else:
          return False
      except:
          return False

    def check_noindex_nofollow(self,url):
      try:
        if '/thanks' in url:
          return True

        # LẤY META ROBOT TRONG ĐÓ CÓ CHƯA TÊN LÀ NO INDEX NO FOLLOW
        soup = read_html.get_page_content_from_url(url)
        #NẾU LÀ TRANG PDF IMG THÌ BỎ QUA
        if check_link_file(url):
          return -1
        meta_no_index_no_follow = soup.find('meta',{"name":"robots"})   

        # NẾU THỂ KHÔNG TỒN TẠI THÌ LÀ KHÔNG CÓ
        if meta_no_index_no_follow == None:
          return False
        else:
          #NẾU THẺ TỒN TẠI NHƯNG PHẢI ĐÚNG TÊN LÀ "noindex,nofollow"
          if meta_no_index_no_follow['content'] == "noindex,nofollow": 
            return True
          else:
            return False
      except:
        return False

    def check_hero_content(self,url,image_src):
      try:
        soup = ReadHtml().get_page_content_from_url(url)
        #NẾU LÀ TRANG PDF IMG THÌ BỎ QUA
        if check_link_file(url):
          return -1
        # KIỂM CÓ CÓ HÌNH HERO KHÔNG
        if soup.find('div',{"class":["Hero"]}) != None:
          param_image_src = soup.find('div',{"class":["Hero"]})['style']
          #KIỂM TRA HÌNH HERO CÓ ĐÚNG TÊN KHÔNG
          if param_image_src == image_src:
            return True
          else:
            return False
        else:
          return False
      except:
        return False

    def check_landing_page_thanks_page(self,url,data,data_thanks_page):
      result = {}
      #LẤY DỮ LIỆU CỦA TRANG WEB
      LP_soup = ReadHtml().get_page_content_from_url(url)
      if self.check_301_404_error(url+"/thanks") == 200:
        TX_soup = ReadHtml().get_page_content_from_url(url+"/thanks")
        result['TX_ERROR'] = 1
      else:
        result['TX_ERROR'] = 0
        return False,result

      #LẤY DỮ LIỆU TỪ PAGE
      LP_H1 = LP_soup.h1.text
      LP_PDF_alt = LP_soup.find('img',{'class' : 'pdf-thumb'})['alt']
      TX_H1 = LP_soup.h1.text
      TX_H2 = TX_soup.h2.text

      #LẤY PHẦN SAU CÙNG CỦA URL https://www.leadplus.net/resource/inbound-marketing-guide
      #CHỈ LẤY LP_URI = inbound-marketing-guide
      LP_URI = self.clear_url(url)
      LP_URI = LP_URI.split("/")
      LP_URI = LP_URI[len(LP_URI) -1]

      LP_PDF_src = LP_soup.find('img',{'class' : 'pdf-thumb'})['src']

      TX_PDF_url = TX_soup.find('div',{'class' : 'Download-button'}).find('a')['href']
      #LẤY DỮ LIỆU TỪ HUBSPOT
      LP_internal_page_name = data['label']
      LP_page_title = data['page_title']

      TX_internal_page_name = data_thanks_page['label']
      TX_page_title = data_thanks_page['page_title']
      
      #TEST TITLE
      
      if LP_H1 not in LP_PDF_alt:
        result['LP_PDF_alt'] = 0
      else:
        result['LP_PDF_alt'] = 1
      
      if LP_H1 not in TX_H1:
        result['TX_H1'] = 0
      else:
        result['TX_H1'] = 1

      if LP_H1 not in TX_H2:
        result['TX_H2'] = 0
      else:
        result['TX_H2'] = 1

      if LP_H1 not in LP_internal_page_name:
        result['LP_internal_page_name'] = 0
      else:
        result['LP_internal_page_name'] = 1
      
      if LP_H1 not in LP_page_title:
        result['LP_page_title'] = 0
      else:
        result['LP_page_title'] = 1
      
      if LP_H1 not in TX_internal_page_name:
        result['TX_internal_page_name'] = 0
      else:
        result['TX_internal_page_name'] = 1

      if LP_H1 not in TX_page_title:
        result['TX_page_title'] = 0
      else:
        result['TX_page_title'] = 1
      #TEST URL
      if LP_URI not in LP_PDF_src:
        result['LP_PDF_src'] = 0
      else:
        result['LP_PDF_src'] = 1

      if LP_URI not in TX_PDF_url:
        result['TX_PDF_url'] = 0
      else:
        result['TX_PDF_url'] = 1

      #NẾU CÓ 1 TRƯỜNG BẰNG 0 THÌ TỨC LÀ CÓ LỖI
      if 0 in result.values():
        return False,result
      else:
        return True,result

    def check_301_404_error(self,url):
      response = requests.head(url, verify=False)
      return response.status_code

    def clear_url(self,url):
      url = url.replace("https://www.","")
      url = url.replace("http://www.","")
      return url

    def check_url(self,url):
      if "https://www." in url or "http://www." in url:
        return True
      else:
        return False