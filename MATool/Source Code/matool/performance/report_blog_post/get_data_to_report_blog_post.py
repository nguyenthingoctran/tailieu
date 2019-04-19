from pprint import pprint
from datetime import datetime
from dateutil.relativedelta import relativedelta

from Until_Common_V2 import until
from Until_Common_V2.date_caculate import DateCaculate  
from Until_Common_V2.log import Log
from Until_Common_V2.db_helper import db_helper

#===============================================================================
db_controller = db_helper()
#===============================================================================

def get_sessions_blog_post_from_DB(site_id,start_date,end_date):
  try:
    #1)Chuẩn bị các biến cần sử dụng
    dict_data_table = {
                    'Title':[],
                    'Category':[],
                    'Publish Date':[],
                    'Publication period(month)':[],
                    'Monthly view':[],
                    'CTA Click': [],
                    'CTA Click Rate': [],
                    'Conversion': [],
                    'Total sessions' : [],
                    'Sessions/month' : [],
                    'Organic Keyword' : [],

                    }
    #1.1)Chuyển đổi định dạng ngày rồi thêm vào dict
    list_date_range = DateCaculate().conver_date_to_list_year_month(start_date,end_date)
    for data in list_date_range:
      dict_data_table[data] = []

    #1.2)Lấy tất cả dữ liệu ra, nếu tháng nào data không có thì là Null
    sql_query_blog_info = '''
                          SELECT a.id,a.site_id,a.title,a.category,a.publish_date,a.organic_keyword,
                                b.page_view,b.date,b.contacts,b.sessions,b.cta_click
                            FROM performance_blog a 
                            LEFT JOIN performance_blog_view b 
                              ON b.performance_blog_id = a.id AND b.date >= '{1}' AND b.date <= '{2}'
                            WHERE a.site_id = {0} and a.hb_state="PUBLISHED"
                            ORDER BY date
                          '''.format(site_id,start_date,end_date)
    object_blog_info = db_controller.query(sql_query_blog_info)

    #2)Xử lý dữ liệu
    #2.1)Tạo đỡ 1 cái list để lọc data
    list_data_term = {}
    for blog_info in object_blog_info:
      blog_info_id = blog_info['id']
      date = str(blog_info['date'])
      page_view = blog_info['page_view']
      sessions = blog_info['sessions']
      contacts = blog_info['contacts']
      cta_click = blog_info['cta_click']
      # print("%40s %40s %40s"%(date,type(date),end_date))

      if list_data_term.get(blog_info_id) == None:
        list_data_term[blog_info_id] = {
                                        'title':blog_info['title'],
                                        'category':blog_info['category'],
                                        'publish_date':str(blog_info['publish_date']),
                                        'organic_keyword':blog_info['organic_keyword'],
                                        'value':{},
                                        'total_sessions':0,
                                        'cta_clicks':0,
                                        'cta_click_rate':0,
                                        'contacts':0,
                                        'page_views':0,
                                        }

      #2.1.1)Nếu không có dữ liệu thì bỏ qua
      if date == None:
        continue
      #2.1.2)Nếu có thì đưa thêm vào list
      #Lưu dữ liệu của tháng này
      if date == end_date:
        list_data_term[blog_info_id]['contacts'] = contacts
        list_data_term[blog_info_id]['page_views'] = page_view
        list_data_term[blog_info_id]['cta_clicks'] = cta_click
      list_data_term[blog_info_id]['total_sessions'] += sessions
      list_data_term[blog_info_id]['value'][str(date)] = sessions
    #2.2)Đổi nó thành kiểu list để sort,loại bỏ cái phần blog_info_id ở đầu đi, chỉ lấy phần dữ liệu phía sau
    list_data_term = list(list_data_term.values())

    #2.3)Hàm để sort theo số lượng dữ liệu mà blog đó có,để sắp xếp theo hình bậc thang
    f_sort = lambda x : len(x['value'])

    list_data_term.sort(key=f_sort,reverse=True)
    # pprint(list_data_term)

    #3) Lấy dữu liệu của data_table
    for data in list_data_term:
      #3.0)Lấy dữ liệu mặc định
      page_view = data['page_views']
      cta_click = data['cta_clicks']
      total_sessions = data['total_sessions']

      cta_click_rate = 0
      if page_view != 0:
        cta_click_rate = cta_click/page_view
        cta_click_rate = round(cta_click_rate,4)

      number_of_month = len(data['value'])
      monthly_sessions_average = 0
      #3.0.1)Số tháng mà blog đã publish
      date_range_by_month = DateCaculate().get_date_range_by_month(data['publish_date'])

      #3.1)Nếu bằng không thì tức là không có dữ liệu
      if number_of_month != 0:
        monthly_sessions_average = total_sessions/number_of_month
        monthly_sessions_average = round(monthly_sessions_average,1)

      dict_data_table['Sessions/month'].append(monthly_sessions_average)
      dict_data_table['CTA Click Rate'].append(cta_click_rate)
      dict_data_table['Publication period(month)'].append(date_range_by_month)
      dict_data_table['Publish Date'].append(data['publish_date'])
      dict_data_table['Category'].append(data['category'])
      dict_data_table['Title'].append(data['title'])
      dict_data_table['CTA Click'].append(data['cta_clicks'])
      dict_data_table['Monthly view'].append(data['page_views'])
      dict_data_table['Conversion'].append(data['contacts'])
      dict_data_table['Total sessions'].append(data['total_sessions'])
      dict_data_table['Organic Keyword'].append(data['organic_keyword'])

      #3.2)Dữ liệu sessions trong tháng,Chỗ nào không có dữ liệu thì viết vào dấu ----------
      for date_range in list_date_range:
        page_view = data['value'].get(date_range,'-----------------------------------')

        dict_data_table[date_range].append(page_view)

    return dict_data_table
  except Exception as e:
    Log().write_log(e)

def get_keyword_blog_post_from_DB(site_id,start_date,end_date):
  try:
    #1)Chuẩn bị các biến cần sử dụng
    dict_data_table = {
                    'Title':[],
                    'Category':[],
                    'Publish Date':[],
                    'Publication period(month)':[],
                    'Organic keyword':[],
                    'Organick keyword (Search volume)':[],
                    'Keyword' : [],
                    'Keyword (Search volume)' : [],
                    }
    #1.1)Chuyển đổi định dạng ngày rồi thêm vào dict
    list_date_range = DateCaculate().conver_date_to_list_year_month(start_date,end_date)
    for data in list_date_range:
      dict_data_table[data] = []

    #1.2)Lấy tất cả dữ liệu ra, nếu tháng nào data không có thì là Null
    sql_query_blog_info = '''
            SELECT a.id,a.site_id,a.title,a.category,a.publish_date,
                table_b.date,table_b.keyword_rank,table_b.keyword_in_this_month,
                table_b.keyword_search_volume,table_b.organic_keyword,table_b.organic_keyword_search_volume,
                c.keyword as current_keyword
            FROM dev_matool_db.performance_blog a 
            INNER JOIN dev_matool_db.ranking_keyword c on c.id = a.keyword_id
            INNER JOIN 	(

                  SELECT b.performance_blog_id,b.keyword_rank,b.keyword_search_volume,
						b.organic_keyword,b.organic_keyword_search_volume,b.date,
                      c.keyword as keyword_in_this_month
                  FROM dev_matool_db.performance_blog_view b 
                        INNER JOIN dev_matool_db.ranking_keyword c on c.id = b.keyword_id
                        WHERE b.date >= '{1}' AND b.date <= '{2}'
                        
                  )table_b ON table_b.performance_blog_id = a.id
            WHERE a.site_id = {0} and a.hb_state="PUBLISHED" 
            ORDER BY table_b.date
            '''.format(site_id,start_date,end_date)
    object_blog_info = db_controller.query(sql_query_blog_info)

    #2)Xử lý dữ liệu
    #2.1)Tạo đỡ 1 cái list để lọc data
    list_data_term = {}
    for blog_info in object_blog_info:
      blog_info_id = blog_info['id']
      date = str(blog_info['date'])
      keyword_rank = blog_info['keyword_rank']
      keyword_in_this_month = blog_info['keyword_in_this_month']
      # print("%40s %40s %40s"%(date,type(date),end_date))

      if list_data_term.get(blog_info_id) == None:
        list_data_term[blog_info_id] = {
                                        'title':blog_info['title'],
                                        'category':blog_info['category'],
                                        'publish_date':str(blog_info['publish_date']),
                                        'keyword':blog_info['current_keyword'],
                                        'organic_keyword':blog_info['organic_keyword'],
                                        'value':{},
                                        }

      #2.1.1)Nếu không có dữ liệu thì bỏ qua
      if date == None:
        continue
      #2.1.2)Nếu có thì đưa thêm vào list
      #Lưu dữ liệu của tháng này,tức là tháng gần nhất thời điểm hiện tại
      if date == end_date:
        list_data_term[blog_info_id]['organic_keyword_search_volume'] = blog_info['organic_keyword_search_volume']
        list_data_term[blog_info_id]['keyword_search_volume'] = blog_info['keyword_search_volume']

      list_data_term[blog_info_id]['value'][str(date)] = keyword_in_this_month + ":" + str(keyword_rank) 
    #2.2)Đổi nó thành kiểu list để sort,loại bỏ cái phần blog_info_id ở đầu đi, chỉ lấy phần dữ liệu phía sau
    list_data_term = list(list_data_term.values())

    #2.3)Hàm để sort theo số lượng dữ liệu mà blog đó có,để sắp xếp theo hình bậc thang
    f_sort = lambda x : len(x['value'])

    list_data_term.sort(key=f_sort,reverse=True)

    #3) Lấy dữu liệu của data_table
    for data in list_data_term:
      #3.1)Số tháng mà blog đã publish
      date_range_by_month = DateCaculate().get_date_range_by_month(data['publish_date'])

      dict_data_table['Title'].append(data['title'])
      dict_data_table['Category'].append(data['category'])
      dict_data_table['Publish Date'].append(data['publish_date'])
      dict_data_table['Publication period(month)'].append(date_range_by_month)
      dict_data_table['Organic keyword'].append(data['organic_keyword'])
      dict_data_table['Organick keyword (Search volume)'].append(data['organic_keyword_search_volume'])
      dict_data_table['Keyword'].append(data['keyword'])
      dict_data_table['Keyword (Search volume)'].append(data['keyword_search_volume'])

      #3.2)Dữ liệu sessions trong tháng,Chỗ nào không có dữ liệu thì viết vào dấu ----------
      for date_range in list_date_range:
        page_view = data['value'].get(date_range,'-----------------------------------')

        dict_data_table[date_range].append(page_view)

    return dict_data_table
  except Exception as e:
    Log().write_log(e)
    
