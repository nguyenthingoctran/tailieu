from Until_Common_V2.API.Hubspot_API.Connection.hubspot_workflows_API import HubspotWorkflowsAPI

class HubspotHandleWorkflowsAPI(HubspotWorkflowsAPI):

  def __init__(self,site_id,request=None):
    HubspotWorkflowsAPI.__init__(self,site_id,request)

  def get_data_all_workflows(self):
    #1)Lấy dữ liệu từ Hubspot
    result = self.get_all_workflows()

    #2)Phân tích dữ liệu
    dict_data = {}
    for workflow in result['workflows']:
      workflow_id = workflow['id']
      dict_data[workflow_id] = {
                                'total_contact_enrolled': workflow['contactCounts']['enrolled'],
                                'name' : workflow['name'],

                                }
    return dict_data
  
  def get_workflows_by_id_data(self,id):
    #1)Lấy dữ liệu từ Hubspot
    workflow = self.get_workflows_by_id(id)

    #2)Phân tích dữ liệu
    dict_data = {}

    dict_data['id'] = workflow['id']
    dict_data['name'] = workflow['name']
    
    return dict_data