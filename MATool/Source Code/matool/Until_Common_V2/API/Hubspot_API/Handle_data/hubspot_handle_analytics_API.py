from Until_Common_V2.API.Hubspot_API.Connection.hubspot_analytics_API import HubspotAnalyticsAPI

class HubspotHandleAnalayticsAPI(HubspotAnalyticsAPI):

  def __init__(self,site_id,request=None):
    HubspotAnalyticsAPI.__init__(self,site_id,request)

  def get_top_10_landing_page_submissions(self,start_date, end_date):
    #1)Lấy dữ liệu từ Hubspot
    result = self.get_analytics_landing_page_sort_by_submissions(start_date, end_date)
    
    #2)Phân tích dữ liệu
    count = 0
    list_page_id_submissions = {}

    for data in result['breakdowns']:
      count +=1
      if data.get('submissions'):
          list_page_id_submissions[data['breakdown']] = data['submissions']
      else:
          break

      if count == 10:
          break

    return list_page_id_submissions

  def get_data_analytics_landing_page(self,start_date, end_date):
    #1)Lấy dữ liêu từ Hubspot
    result = self.get_analytics_landing_page(start_date, end_date)

    #2)Phân tách dữ liệu
    dict_data = {}
    #2.1)Lấy dữ liệu tổng,có thể bị sai số trên Hubspot vì trên Hubspot có những site đã bị xóa nhưng vẫn hiển thị
    dict_data['totals'] = result['totals']

    for breakdown in result['breakdowns']:
        vid = breakdown['breakdown']
        cta_clicks = breakdown.get('ctaClicks',0)
        cta_views = breakdown.get('ctaViews',0)
        page_views = breakdown.get('rawViews',0)
        entrances = breakdown.get('entrances',0) #session
        exits = breakdown.get('exits',0)
        submissions = breakdown.get('submissions',0)
        contacts = breakdown.get('contacts',0)
        leads = breakdown.get('leads',0)

        dict_data[vid] = {
                            'cta_clicks' :cta_clicks,
                            'cta_views' :cta_views,
                            'page_views' :page_views,
                            'entrances' :entrances,
                            'exits' :exits,
                            'submissions' :submissions,
                            'contacts' :contacts,
                            'leads' :leads,
                        }
    return dict_data

  def get_data_analaytics_blog_post(self,start_date,end_date):
    #1)Lấy dữ liệu từ Hubspot
    result = self.get_analytics_blog_post(start_date,end_date)

    #2)Phân tích dữ liệu
    dict_data = {}
    #2.1)Lấy dữ liệu tổng,có thể bị sai số trên Hubspot vì trên Hubspot có những site đã bị xóa nhưng vẫn hiển thị
    dict_data['totals'] = result['totals']

    for breakdown in result['breakdowns']:
        vid = breakdown['breakdown']
        cta_clicks = breakdown.get('ctaClicks',0)
        cta_views = breakdown.get('ctaViews',0)
        page_views = breakdown.get('rawViews',0)
        entrances = breakdown.get('entrances',0) #session
        exits = breakdown.get('exits',0)
        submissions = breakdown.get('submissions',0)
        contacts = breakdown.get('contacts',0)
        leads = breakdown.get('leads',0)
        subscribers = breakdown.get('subscribers',0)

        dict_data[vid] = {
                            'cta_clicks' :cta_clicks,
                            'cta_views' :cta_views,
                            'page_views' :page_views,
                            'sessions' :entrances,
                            'exits' :exits,
                            'submissions' :submissions,
                            'contacts' :contacts,
                            'leads' :leads,
                            'subscribers' :subscribers,
                        }
    return dict_data
  
  def get_data_analaytics_total(self,start_date,end_date):
    #1)Lấy dữ liệu từ Hubspot
    result = self.get_analytics_total(start_date,end_date)

    #2)Phân tích dữ liệu
    dict_data = {}
    #2.1)Lấy dữ liệu tổng,có thể bị sai số trên Hubspot vì trên Hubspot có những site đã bị xóa nhưng vẫn hiển thị
    dict_data['totals'] = result['totals']

    for breakdown in result['breakdowns']:
        vid = breakdown['breakdown']
        page_views = breakdown.get('rawViews',0)
        sessions = breakdown.get('visits',0) #session
        exits = breakdown.get('exits',0)
        submissions = breakdown.get('submissions',0)
        contacts = breakdown.get('contacts',0)
        leads = breakdown.get('leads',0)
        subscribers = breakdown.get('subscribers',0)
        sql = breakdown.get('salesQualifiedLeads',0)
        mql = breakdown.get('marketingQualifiedLeads',0)

        dict_data[vid] = {
                            'page_views' :page_views,
                            'sessions' :sessions,
                            'exits' :exits,
                            'submissions' :submissions,
                            'contacts' :contacts,
                            'leads' :leads,
                            'subscribers' :subscribers,
                            'sql' :sql,
                            'mql' :mql,
                        }
    return dict_data

  def get_data_analaytics_sources(self,start_date,end_date):
    #1)Lấy dữ liệu từ Hubspot
    result = self.get_analytics_sources(start_date,end_date)

    #2)Phân tích dữ liệu
    dict_data = {}
    #2.1)Lấy dữ liệu tổng,có thể bị sai số trên Hubspot vì trên Hubspot có những site đã bị xóa nhưng vẫn hiển thị
    dict_data['totals'] = result['totals']

    for breakdown in result['breakdowns']:
        vid = breakdown['breakdown']
        page_views = breakdown.get('rawViews',0)
        sessions = breakdown.get('visits',0) #session
        submissions = breakdown.get('submissions',0)
        contacts = breakdown.get('contacts',0)
        leads = breakdown.get('leads',0)
        subscribers = breakdown.get('subscribers',0)
        sql = breakdown.get('salesQualifiedLeads',0)
        mql = breakdown.get('marketingQualifiedLeads',0)

        dict_data[vid] = {
                            'page_views' :page_views,
                            'sessions' :sessions,
                            'submissions' :submissions,
                            'contacts' :contacts,
                            'leads' :leads,
                            'subscribers' :subscribers,
                            'sql' :sql,
                            'mql' :mql,
                        }
    return dict_data
  
  def get_data_analytics_sources_exclude_offline(self,start_date,end_date):
    #1)Lấy dữ liệu từ Hubspot
    result = self.get_analytics_sources_exclude_offline(start_date,end_date)

    #2)Phân tích dữ liệu
    dict_data = {}
    #2.1)Lấy dữ liệu tổng,có thể bị sai số trên Hubspot vì trên Hubspot có những site đã bị xóa nhưng vẫn hiển thị
    dict_data['totals'] = result['totals']

    for breakdown in result['breakdowns']:
        vid = breakdown['breakdown']
        page_views = breakdown.get('rawViews',0)
        sessions = breakdown.get('visits',0) #session
        submissions = breakdown.get('submissions',0)
        contacts = breakdown.get('contacts',0)
        leads = breakdown.get('leads',0)
        subscribers = breakdown.get('subscribers',0)
        sql = breakdown.get('salesQualifiedLeads',0)
        mql = breakdown.get('marketingQualifiedLeads',0)

        dict_data[vid] = {
                            'page_views' :page_views,
                            'sessions' :sessions,
                            'submissions' :submissions,
                            'contacts' :contacts,
                            'leads' :leads,
                            'subscribers' :subscribers,
                            'sql' :sql,
                            'mql' :mql,
                        }
    return dict_data

  def get_data_analytic_landing_page_by_id(self,start_date,end_date,page_id):
    #1) dữ liệu trả về
    result = self.get_analytic_landing_page_by_id(start_date,end_date,page_id)
    #1.1) Format đầy đủ dữ liệu:
    # 'totals': {'contacts': 1,
    #           'contactsPerPageview': 0.058823529411764705,
    #           'exits': 5,
    #           'exitsPerPageview': 0.29411764705882354,
    #           'others': 1,
    #           'pageTime': 815,
    #           'rawViews': 17,
    #           'submissions': 3,
    #           'submissionsPerPageview': 0.17647058823529413,
    #           'timePerPageview': 67.91666666666667}}

    #2) Tách dữ liệu cần lấy, check dữ liệu tồn tại trước khi lấy, đề phòng lỗi
    dict_data = {}
    if result['totals'] != '':
      if 'contacts' in result['totals']:
        value_contacts = result['totals']['contacts']
      else:
        value_contacts = 0

      if 'submissions' in result['totals']:
        value_submissions = result['totals']['submissions']
        if value_submissions == None:
          value_submissions = 0
      else:
        value_submissions = 0

      if 'rawViews' in result['totals']:
        value_rawViews = result['totals']['rawViews']
      else:
        value_rawViews = 0
    else:
      value_rawViews = 0
      value_submissions = 0
      value_contacts = 0
    
    dict_data = {
                  'views': value_rawViews,
                  'submissions' : value_submissions,
                  'contacts' : value_contacts
                }  

    return  dict_data
