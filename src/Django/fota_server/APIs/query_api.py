# from alm_qm.types import Stream, Testcase, Testsuite, Testplan, Executionresult, Executionworkitem,Configuration, Testphase
# from alm_qm import utils
# from alm_qm.types import Baseline 
# from alm_qm.client import Client
# import re

# def extract_id(target_str):
#     # Extract 'id' parameter using regex
#     match = re.search('id=([0-9]+)', target_str)
#     id = ''
#     if match:
#         id = match.group(1)

#     return id

class Project_Configuration_API:

    def __init__(self, client):
        # init client object that is authenticated while log in
        self.client = client
        self.project = ""
        self.data = {}
        # self.proj_client = 
        
#     # query all GC based on project name
#     def query_global_configuration(self, project):

#         self.project = project

#         query_str = "title=%" + project + "%"
#         self.feed = self.client.query_projects(filter = query_str)
#         self.proj_client = self.client.create_project_client(self.feed.entry[0].content.project)

#         stream_feed = self.proj_client.query_resources(Stream)

#         # current_stream_page = utils.get_current_page_index(stream_feed)
#         last_stream_page = utils.get_last_page_index(stream_feed)

#         data = {}

#         for i in range(0, last_stream_page+1):

#             streams = self.proj_client.fetch_page(stream_feed, index=i)

#             for count, stream in streams.entry:
#                 data.update({count: 
#                             {
#                                 'title':stream.title.content[0],
#                                 'identifier':stream.link[0].href
#                             }
#                             })
            
#         return data   

#     def query_baseline(self, project):
#         """ Query Baseline data and get configuarion """

#         # Query project with title
#         query_str = "title=%" + project + "%"
#         self.feed = self.client.query_projects(filter = query_str)
#         self.proj_client = self.client.create_project_client(self.feed.entry[0].content.project)

#         self.page_step = 0
#         self.baseline_feed =  self.proj_client.query_resources(Baseline)
        
#         self.current_index_page = utils.get_current_page_index(self.baseline_feed)
#         self.last_index_page = utils.get_last_page_index(self.baseline_feed)

#         data = {}

#         for i in range(0, self.last_index_page+1):

#             baselines = self.proj_client.fetch_page(self.baseline_feed, index=i)

#             for count, baseline in baselines.entry:
#                 data.update({count: 
#                             {
#                                 'title':baseline.title.content[0],
#                                 'identifier':baseline.link[0].href
#                             }
#                             })
            
#         return data   

#     def query_stream(self, project):
#         """ Query stream data and get configuarion """
#         data = {}

#         try:
#             query_str = "title=%" + project + "%"
#             self.feed = self.client.query_projects(filter = query_str)
#             self.proj_client = self.client.create_project_client(self.feed.entry[0].content.project)

#             stream_feed =  self.proj_client.query_resources(Stream)

#             # current_index_page = utils.get_current_page_index(stream_feed)
#             last_index_page = utils.get_last_page_index(stream_feed)

#             for i in range(0,last_index_page+1):

#                 streams = self.proj_client.fetch_page(stream_feed, index=i)

#                 for count, stream in enumerate(streams.entry):
#                     data.update({count: 
#                                 {
#                                     'title':stream.content.stream.title,
#                                     'identifier': stream.link[0].href.split('/')[-1]
#                                 }
#                                 })
#         except Exception as e:
#             print(e)
        
#         return data   
            
#     def Query_Test_Plans_w_Stream(self, stream_id):
#         """ Query Test Plans related to the selected Stream/BaseLine"""
#         data = {}

#         try:
#             self.proj_client.select_stream(stream_id)
#             test_plans = self.proj_client.query_resources(Testplan)

#             self.last_index_page = utils.get_last_page_index(test_plans)
#             self.current_index_page = utils.get_current_page_index(test_plans)

#             """Get all test plans in specific stream data """

#             for count, test_plan in enumerate(test_plans.entry): 
#                 id = extract_id(str(test_plan.link[1].href))
#                 data.update({count: 
#                             {
#                                 'title':test_plan.content.testplan.title,
#                                 'query_id':test_plan.content.testplan.identifier,
#                                 'id': id,
#                             }
#                             })
                
#         except:
#             pass

#         return data
    
#     def Query_Test_Suites_w_Test_Plan_url(self, testplan_url):

#         data = {}

#         try: 
#             testplan_data = self.proj_client.fetch_single_resource_by_url(Testplan, str(testplan_url))

#             for suite_count, testsuite in enumerate(testplan_data.testsuite):
#                 # get the TestSuite name based on fetching id 
#                 testsuites_data = self.proj_client.fetch_single_resource_by_url(Testsuite, testsuite.href)
                
#                 data.update({
#                             str(suite_count): 
#                                 {
#                                     "name": testsuites_data.title,
#                                     "query_id": testsuites_data.identifier,
#                                     "id": testsuites_data.web_id,
#                                 }
#                             })
                
#         except:
#             pass

#         return data
            
    
#     def Query_Test_Case_w_Test_Suite_url(self, testsuite_url):
#         """ Query Test Case relate to TestSuite/TestPlan/ in selected Stream/Baseline/"""

#         data = {}
#         try:
#             testsuites_data = self.proj_client.fetch_single_resource_by_url(Testsuite,testsuite_url)

#             for testcase_count in range(0,len(testsuites_data.suiteelements.suiteelement)):

#                 test_case_data = self.proj_client.fetch_single_resource_by_url(Testcase, testsuites_data.suiteelements.suiteelement[testcase_count].testcase.href)
#                 # print(test_case_data.title,test_case_data.custom_attributes.custom_attribute[0].value,test_case_data.custom_attributes.custom_attribute[0].identifier)
#                 # print(test_case_data.custom_attributes)
#                 implementation_path = ''
#                 if len(test_case_data.custom_attributes.custom_attribute) > 0:
#                     for datas in test_case_data.custom_attributes.custom_attribute:
#                         if datas.name == 'Implementation_Path':
#                             implementation_path = datas.value
#                             break
#                 data.update({
#                             str(testcase_count): 
#                                 {
#                                     "name": test_case_data.title,
#                                     "query_id": test_case_data.identifier,
#                                     "id": test_case_data.web_id,
#                                     "implementation_path": implementation_path
#                                 }
#                             })
#         except:
#             pass

#         return data
    
#     def query_alm_data(self, stream_id):
        
#         """ Query Test Plans related to the selected Stream/BaseLine"""
#         self.proj_client.select_stream(stream_id)

#         Test_Plans = self.proj_client.query_resources(Testplan)

#         data = {}

#         plan_count = 0

#         """Get all test plans in specific stream data """
#         for test_plan in Test_Plans.entry:

#             if "BC_MMA_SYS.5_Master_Test_Plan" in test_plan.content.testplan.title:
#                 plan_count += 1
#                 testplan = {}

#                 data.update({"testplan_" + str(plan_count) : testplan})

#                 testsuites_dict = {}

#                 testplan.update({
#                                     "name": test_plan.content.testplan.title, 
#                                     "id": test_plan.link[0].href,
#                                     "testsuites": testsuites_dict
#                                 })
                
#                 testsuites_data = test_plan.content.testplan.testsuite
#                 # data.update({test_plan.content.testplan.title : testsuite})
#                 # test_plan_href = test_plan.link[0].href
                
#                 for suite_count, testsuite in enumerate(testsuites_data, start = 1):

#                     testsuite_single = {}

#                     testsuites_dict.update({"testsuite_" + str(suite_count) : testsuite_single})    

#                     testsuites_data = self.proj_client.fetch_single_resource_by_url(Testsuite,testsuite.href)

#                     testcases_dict = {}

#                     testsuite_single.update({
#                                             "name": testsuites_data.title,
#                                             "id": testsuites_data.identifier,
#                                             "testcases": testcases_dict,
#                                             })
#                     # print(testsuites_data.title)
#                     testcases = testsuites_data.suiteelements.suiteelement

#                     for testcase_count in range(0,len(testsuites_data.suiteelements.suiteelement)):

#                         testcase_single = {}

#                         testcases_dict.update({"testcase_" + str(testcase_count) : testcase_single})  
#                         test_case_data = self.proj_client.fetch_single_resource_by_url(Testcase, testsuites_data.suiteelements.suiteelement[testcase_count].testcase.href)
#                         # print(test_case_data.title,test_case_data.custom_attributes.custom_attribute[0].value,test_case_data.custom_attributes.custom_attribute[0].identifier)
#                         testcase_single.update({
#                                             "name": test_case_data.title,
#                                             "id": testsuites_data.suiteelements.suiteelement[testcase_count].testcase.href,
                                            
#                                         })
#                         # Test_Case.append(test_suite_data.suiteelements.suiteelement[testcase].testcase.href)
                       
        

#         return data 

#     def Query_Test_Case_Id(self, id):
#         """ Query Test Case with id TestCase """
#         return self.proj_client.fetch_single_resource_by_id(Testcase,id) 
#     def Query_Test_Case_Url(self, url):
#         """Query Test Case with Url """
#         return self.proj_client.fetch_single_resource_by_url(Testcase,url)
#     def Quey_Suite_id(self):
#         """ Query Test Suite with Id """
#         return self.proj_client.delete_resource_by_id(Testsuite,id)

#     def query_configuration(self):
#         """ Query Configuration """
#         return self.proj_client.query_resources(Configuration)

#     def Select_baseline(self,base_line: str): 
#         """ Select a specific baseline from the list of available baseline data """
#         return self.proj_client.select_baseline(base_line)

#     def Select_stream(self, stream: str):
#         """ Select a specific stream data form the list of available stream data """
#         return self.proj_client.select_stream

#     def Select_configuration(self, config):
#         """ Select a configuration to be used by the project """
#         return self.proj_client.select_configuration

#     def Query_Interation(self, stream_id):
#         """Query The Interation which belong to specific data of stream/baseline"""

#         Interation = []
#         self.proj_client.select_stream(stream_id)
#         Interations = self.proj_client.query_resources(Testphase) 
#         self.last_index_page = utils.get_last_page_index(Interations)
#         self.current_index_page = utils.get_current_page_index(Interations)
#         print ("Number of pages :",self.last_index_page + 1 )
#         for i in range(0,self.last_index_page+1):
#             data_iteration = self.proj_client.fetch_page(Interations, index=i)
#             for data_iteration in data_iteration.entry:
#                 print(data_iteration.content.testphase.title,data_iteration.content.testphase.identifier,data_iteration.content.testphase.iteration.href)
#                 Interation.append(data_iteration.content.testphase.title)
#         return Interation, data_iteration.content.testphase.iteration.href

