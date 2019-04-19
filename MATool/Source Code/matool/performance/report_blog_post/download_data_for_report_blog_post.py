from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
from multiprocessing.pool import threading,ThreadPool
from pprint import pprint

from Until_Common_V2.log import Log
from Until_Common_V2 import until
from Until_Common_V2.db_helper import db_helper
from Until_Common_V2.API.Hubspot_API.Handle_data.hubspot_handle_cms_blog_post_API import HubspotHandleCMSBlogAPI
from Until_Common_V2.API.Hubspot_API.Handle_data.hubspot_handle_cms_blog_topic_API import HubspotHandleCMSBlogTopicAPI
from Until_Common_V2.API.Hubspot_API.Handle_data.hubspot_handle_analytics_API import HubspotHandleAnalayticsAPI
from Until_Common_V2.API.Google_Custom_Search_API.Handle_data.gcs_handle_check_rank_api import HandleCheckRankAPI
#===============================================================================
db_controller = db_helper()
#===============================================================================

#================================================
#========  Lưu dữ liệu của blog info ============
#================================================
def save_blog_info(blog,site_id):
  try:
    #1)Lấy category thêm dấu , vào
    category = ''
    for i in range(len(blog['tag_id'])):
      category += blog['tag_id'][i] 

      if i < len(blog['tag_id']) - 1:
        category += ','

    # #2.1)Tìm keyword id trong bảng keyword
    # keyword = blog['keyword']
    # sql_keyword_ino = '''SELECT * FROM ranking_keyword WHERE keyword = "{0}"'''.format(keyword)
    # object_keyword_info = db_controller.query_scalar(sql_keyword_ino)

    # #2.1.1)Nếu tìm ra keyword thì gán id
    # if object_keyword_info:
    #   keyword_id = object_keyword_info['id']
    # #2.1.1)Nếu không tìm ra keyword thì tạo mới
    # else:
    #   #2.1.2)Tạo mới
    #   sql_insert_keyword = '''INSERT INTO ranking_keyword (site_id,keyword,current_target_url)
    #                           VALUE ({0},"{1}","{2}")'''.format(site_id,keyword,blog['url'])
    #   object_insert_keyword = db_controller.execute(sql_insert_keyword)

    #   #2.1.2)Lấy keyword_id từ cái keyword mới tạo ra
    #   sql_keyword_ino = '''SELECT * FROM ranking_keyword WHERE keyword = "{0}"'''.format(keyword)
    #   object_keyword_info = db_controller.query_scalar(sql_keyword_ino)
    #   keyword_id = object_keyword_info['id']

    #2.2)Chỉ lấy ngày tháng chứ không lấy giờ 2018-08-03 07:19:50 => 2018-08-03
    publish_date = blog['publish_date'][:10]

    #2.3)Kiểm tra tồn tại hay chưa
    title = until.sql_query_cover_special_charater(blog['title'])

    print("%10s %5s %20s %80s"%('Blog Info',site_id,blog['id'],title))
    sql_blog_info = '''SELECT * 
                        FROM performance_blog
                        WHERE hb_blog_id = "{0}" AND site_id = {1}'''.format(blog['id'],site_id)

    object_blog_info = db_controller.query(sql_blog_info)

    #3)Nếu chưa tồn tại thì tạo mới
    if len(object_blog_info) == 0:
      insert_blog_info = '''INSERT INTO performance_blog(site_id,url,title,category,publish_date,hb_blog_id,hb_content_group_id,hb_state) 
                            VALUE ({0},"{1}","{2}","{3}","{4}","{5}","{6}",'{7}')'''.format(site_id,blog['url'],title,category,
                                                                            publish_date,blog['id'],blog['content_group_id'],blog['state'])
      db_controller.execute(insert_blog_info)

    #4)Nếu đã tồn tại thì Update
    else:
      update_blog_info = '''UPDATE performance_blog
                            SET title = "{0}",category = "{1}",url = "{2}",publish_date = "{3}",
                                hb_state = "{4}"
                            WHERE hb_blog_id = "{5}" AND site_id = {6}'''.format(title,category,blog['url'],
                                                                        publish_date,blog['state'],blog['id'],site_id)
      db_controller.execute(update_blog_info)
  except Exception as inst:
    Log().write_log(inst)

def save_blog_info_by_site_id(site_id):
  try:
    #1) Lấy tất cả blog và blog_tag
    hub_cms_blog_post = HubspotHandleCMSBlogAPI(site_id)
    hub_cms_blog_topic = HubspotHandleCMSBlogTopicAPI(site_id)

    #1.1)Lấy list content group id ra, chỉ lọc những blog nằm trong diện này
    sql_blog_setting = '''SELECT * FROM performance_site_blog_setting WHERE site_id = {0}'''.format(site_id)
    object_blog_setting = db_controller.query(sql_blog_setting)
    list_content_group_id = object_blog_setting[0]['list_hb_content_group_id'].split(",")

    #1.2)Lấy dữ liệu từ Hubspot
    list_blog_info = hub_cms_blog_post.get_all_blog_posts_by_content_group_id(list_content_group_id)
    dict_blog_topic = hub_cms_blog_topic.get_list_blog_post_topic() 

    #2) Xử lý dữ liệu
    #2.1)Lấy tên của topic từ Hubspot thế nào topic_id
    for blog in list_blog_info:
      for i in range(len(blog['tag_id'])):
        tag_id = blog['tag_id'][i]
        blog['tag_id'][i] = dict_blog_topic.get(tag_id,'-1')

    #3)Gọi thread để lưu cho nhanh
    #Đây là Thread con
    pool = ThreadPool(processes=5)

    for blog_info in list_blog_info:
      pool.apply_async(save_blog_info,(blog_info,site_id))

    pool.close()
    pool.join()
  except Exception as inst:
    Log().write_log(inst)

def download_blog_post_info():
  try:
    #1) Lấy tổng số page hiện đang có ra 
    sql_site_info = '''SELECT * FROM management_site'''
    object_site_info = db_controller.query(sql_site_info)

    #Đây là Thread Cha
    for site_info in object_site_info:
      site_id = site_info['id']
    # for site_id in [3]:
      t = threading.Thread(target=save_blog_info_by_site_id,args=(site_id,))
      t.start()
  except Exception as inst:
    Log().write_log(inst)

#=====================================================================
#========  Lưu dữ liệu của blog data(Page view,CTA Click) ============
#=====================================================================
def insert_blog_data(blog_info,start_date,list_analytics_blog_post,site_id):
  try:
    #1) Lấy dữ liệu ra cái đã
    blog_id = blog_info['hb_blog_id']
    performance_blog_id = blog_info['id']
    hb_content_group_id = blog_info['hb_content_group_id']
    keyword_id = blog_info['keyword_id']
    # keyword = blog_info['keyword']

    if list_analytics_blog_post.get(blog_id):
      data = list_analytics_blog_post[blog_id]
      page_view = data.get('page_views')
      cta_click = data.get('cta_clicks')
      sessions = data.get('sessions')
      contacts = data.get('contacts')
    else:
      page_view = 0
      cta_click = 0
      sessions = 0
      contacts = 0

    #1.1)Keyword ranking
    api_key = 'AIzaSyCjteDrcxv2Tf5S2aHdNSfgBFpeHsLfijA'
    check_rank_api = HandleCheckRankAPI(api_key)
    result = check_rank_api.get_rank_keyword_checked_in_site(keyword_id)
    keyword_rank = result['position']
    # keyword_rank = 0
    
    #2.1)Lấy list content group id ra, chỉ lọc những blog nằm trong diện này
    sql_blog_setting = '''SELECT * FROM performance_site_blog_setting 
                          WHERE site_id = {0}'''.format(site_id)
    object_blog_setting = db_controller.query(sql_blog_setting)
    list_content_group_id = object_blog_setting[0]['list_hb_content_group_id'].split(",")

    #2.2)Kiểm tra xem bài blog này có cần được check hay không cần nữa
    if hb_content_group_id not in list_content_group_id:
      return -1

    #3)Kiểm tra tồn tại hay chưa
    sql_blog_data = '''SELECT * FROM performance_blog_view 
                    WHERE performance_blog_id = {0} and site_id = {1} and date = "{2}"'''.format(performance_blog_id,site_id,start_date)
    object_blog_data = db_controller.query(sql_blog_data)

    print("%10s %10s %10s %10s %10s %10s %10s"%('Blog Data',site_id,performance_blog_id,cta_click,sessions,page_view,start_date))
    #3)Nếu chưa tồn tại thì tạo mới
    if len(object_blog_data) == 0:
      insert_blog_data = '''INSERT INTO performance_blog_view (performance_blog_id,site_id,cta_click,sessions,page_view,contacts,date,keyword_id,keyword_rank)
                            VALUE({0},{1},{2},{3},{4},{5},"{6}",{7},{8})'''.format(performance_blog_id,site_id,cta_click,
                                                                        sessions,page_view,contacts,start_date,keyword_id,keyword_rank)
      db_controller.execute(insert_blog_data)
  except Exception as e:
    Log().write_log(e)

def insert_blog_data_by_site_id(site_id,start_date,end_date):
  try:
    #1)Lấy dữ liệu Hubspot
    hub_analytics_api = HubspotHandleAnalayticsAPI(site_id)

    list_analytics_blog_post = hub_analytics_api.get_data_analaytics_blog_post(start_date,end_date)

    #2)Lấy dữ liệu DB
    sql_blog_info = '''SELECT a.id,a.hb_blog_id,a.hb_content_group_id,a.hb_state,a.url,a.title,a.category,a.organic_keyword,a.publish_date,
                              a.keyword_id,b.keyword
                      FROM performance_blog a
                      INNER JOIN ranking_keyword b ON b.id = a.keyword_id
                      WHERE a.site_id = {0} and a.hb_state = "PUBLISHED"'''.format(site_id)
    object_blog_info = db_controller.query(sql_blog_info)

    #3)Tạo thread Con
    pool = ThreadPool(processes=5)  

    #3.1)Gọi thread để lưu cho nhanh
    for blog_info in object_blog_info:
      pool.apply_async(insert_blog_data,(blog_info,start_date,list_analytics_blog_post,site_id))

    pool.close()
    pool.join()
  except Exception as e:
    Log().write_log(e)

def download_blog_post_data():
  try:
    #1) Today phải là ngày đầu của tháng (2019-04-01,2019-05-01)
    today = datetime.now()

    start_date = today - relativedelta(months=1)
    start_date = start_date.strftime('%Y-%m-%d')

    end_date = today - timedelta(1)
    end_date = end_date.strftime('%Y-%m-%d')

    start_date = '2018-05-01'
    end_date = '2018-05-31'
    
    #2) Lấy tổng số page hiện đang có ra 
    sql_site_info = '''SELECT * FROM management_site'''
    object_site_info = db_controller.query(sql_site_info)

    #3)Đây là Thread Cha
    for site_info in object_site_info:
      site_id = site_info['id']
    # for site_id in [3]:
      t = threading.Thread(target=insert_blog_data_by_site_id,args=(site_id,start_date,end_date))
      t.start()
  except Exception as e:
    Log().write_log(e)