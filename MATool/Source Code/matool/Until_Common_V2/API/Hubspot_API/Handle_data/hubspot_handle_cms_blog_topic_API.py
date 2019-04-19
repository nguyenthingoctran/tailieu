from Until_Common_V2.API.Hubspot_API.Connection.hubspot_cms_blog_topic_API import HubspotCMSBlogTopicAPI

class HubspotHandleCMSBlogTopicAPI(HubspotCMSBlogTopicAPI):

  def __init__(self,site_id,request=None):
    HubspotCMSBlogTopicAPI.__init__(self,site_id,request)

  def get_list_blog_post_topic(self):
    #1)Lấy dữ liệu từ Hubspot
    result = self.get_list_blog_post_topics()

    #2)Phân tích dữ liệu
    dict_blog_post_topic = {}
    for data in result['objects']:
      topic_id = data['id']
      topic_name = data['name']
      dict_blog_post_topic[topic_id] = topic_name

    return dict_blog_post_topic
