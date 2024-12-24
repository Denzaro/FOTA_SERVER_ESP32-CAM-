from django.http import JsonResponse
from django.shortcuts import render,redirect,get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.contrib.auth.decorators import login_required,permission_required
from django.contrib.auth import login,authenticate
from django.utils.decorators import method_decorator
from .models import *
from APIs.user_config_api import get_active_alm_client_obj
import requests
from json import dumps 
import json
from datetime import datetime, timezone
from django.db import models
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .alm_config import ALM_CONFIG


def download_report(request):
    project = request.GET.get('project')
    test_setup = request.GET.get('test_setup') # lab PC name
    file_path = request.GET.get("report_path")
    project_obj = Project_Area.objects.get(name=project)
    lab_test_obj = HIL_Setup.objects.get(project=project_obj,name=test_setup)
    host = lab_test_obj.host
    port = lab_test_obj.port
    # print("file_path: ",file_path)
    # request_url = f"{str(host)}:{str(port)}/auto_execution/download_report/?report_path={file_path}"
    request_url = f"{str(host)}:{str(port)}/auto_execution/download_report/"
    response = requests.get(request_url,data={'report_path':file_path}, stream=True)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the filename from the 'Content-Disposition' header (if available)
        filename = response.headers.get('Content-Disposition', 'filename=""').split('filename=')[-1].strip('"')
        # print(filename)
        # Create a streaming HttpResponse to serve the file to the client
        response_content = HttpResponse(response.content, content_type=response.headers['Content-Type'])
        response_content['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response_content
    else:
        return HttpResponse('File not found', status=404)
    
def get_current_time():
    # Get the current date and time
    time = datetime.now(timezone.utc)

    # Format the datetime object as a string
    formatted_time = time.strftime('%Y-%m-%dT%H:%M:%SZ')

    return(formatted_time)

@method_decorator(login_required,name="dispatch")
class homepage(APIView):
# Create your views here.

    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('message', openapi.IN_QUERY, description="Message to be echoed back", type=openapi.TYPE_STRING),
            openapi.Parameter('name', openapi.IN_QUERY, description="Name of the sender", type=openapi.TYPE_STRING),
        ],
        operation_summary="Get a simple hello message with parameters."
    )
    def get(self,request):
        """
        Get home data info
        """
        if self.request.user.is_superuser:
            return render(request,"home_admin.html")
        else:
            return render(request,"home.html")

@method_decorator(login_required,name="dispatch")
class set_execution_plan_view(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('project_name', openapi.IN_QUERY, description="Project name", type=openapi.TYPE_STRING),
            openapi.Parameter('PC_setup', openapi.IN_QUERY, description="Name PC setup", type=openapi.TYPE_STRING),
        ],
        operation_summary="Get execution plan view with parameters."
    )
    def get(self,request):
        """
        Get execution plan view info
        """
        project = request.GET.get('project')
        PCsetup = request.GET.get('PCsetup')
        data = {
            'project' : str(project),
            'PCsetup' : str(PCsetup),
            'username': str(request.user)
        }
        dataJSON = dumps(data) 
        # print(project, PCsetup)
        return render(request,"execution_plan.html", {'data': dataJSON})

@method_decorator(login_required,name="dispatch")
class current_execution_plan(APIView):
    # Create your views here.
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('hil_name', openapi.IN_QUERY, description="HIL setup name that need to be checked", type=openapi.TYPE_STRING, example = 'HIL 1'),
        ],
        operation_summary="Response Execution Plan Status on HIL",
        responses={200: "Success response description"},
    )
    def get(self,request):
        """
        Get current execution plan
        """
        # get HIL name from user request
        hil_name = request.GET.get('hil_name')

        # initialize host and port
        host = ''
        port = ''

        # query host and port with HIL name from DB
        hil_data = HIL_Setup.objects.filter(name = hil_name).values()

        if hil_data.exists():

            for obj in hil_data:

                host = obj['host']
                port = obj['port']

            # create full api url to HIL setup
            request_url = str(host) + ":" + str(port) + "/auto_execution/check_execution_plan_status/"

            response = requests.get(request_url)

            data = response.json()
            
            return JsonResponse(data = data, status=status.HTTP_200_OK, safe = False)
        else:

            return JsonResponse(
                {"error": "HIL_Setup with the provided name not found."},
                status=status.HTTP_400_BAD_REQUEST
            )
@method_decorator(login_required, name="dispatch")
class save_streams_database(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description="stream's name", type=openapi.TYPE_STRING),
            openapi.Parameter('gc_id', openapi.IN_QUERY, description="stream's id", type=openapi.TYPE_STRING),
            openapi.Parameter('project', openapi.IN_QUERY, description="project's name", type=openapi.TYPE_STRING),
        ],
        operation_summary="Response Execution Plan Status on HIL",
        responses={200: "Success response description"},
    )
    def post(self,request):
        """
        Get ALM related data 
        """
        try:
            rawdata = request.data.dict()
            gc_id = rawdata['gc_id']
            option_text = rawdata['title']
            project_name = rawdata['project']
            component_href = rawdata['component_href']
            project = get_object_or_404(Project_Area, name=project_name)
            stream_selection,gc_status = Global_Configuration.objects.update_or_create(gc_id=gc_id, project=project, defaults={'component_href': component_href, 'title':option_text,})
            return JsonResponse({'status': 'success'})
        except KeyError as e:
            print('Error was found - reason "%s"' % str(e))
            return JsonResponse(
                    {"error": "Error while fetching data"},
                    status=status.HTTP_400_BAD_REQUEST
                )
@method_decorator(login_required, name="dispatch")
class save_testplan_database(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description="tplan's name", type=openapi.TYPE_STRING),
            openapi.Parameter('tplan_query_id', openapi.IN_QUERY, description="tplan's query id", type=openapi.TYPE_STRING),
            openapi.Parameter('tplan_view_id', openapi.IN_QUERY, description="tplan's view id", type=openapi.TYPE_STRING),
            openapi.Parameter('gc_id', openapi.IN_QUERY, description="gc's name", type=openapi.TYPE_STRING),
        ],
        operation_summary="Response Execution Plan Status on HIL",
        responses={200: "Success response description"},
    )
    def post(self,request):
        """
        Get ALM related data 
        """
        try:
            rawdata = request.data.dict()
            gc_id = rawdata['gc_id']
            option_text = rawdata['title']
            tplan_query_id = rawdata['tplan_query_id']
            tplan_view_id = rawdata['tplan_view_id']
            gc_obj = get_object_or_404(Global_Configuration, gc_id=gc_id)
            tplan_selection,tplan_status = Test_Plan.objects.update_or_create(gc_obj_link=gc_obj, title=option_text,tplan_view_id=tplan_view_id,tplan_query_id=tplan_query_id)
            return JsonResponse({'status': 'success'})
        except KeyError as e:
            print('Error was found - reason "%s"' % str(e))
            return JsonResponse(
                    {"error": "Error while fetching data"},
                    status=status.HTTP_400_BAD_REQUEST
                )
@method_decorator(login_required, name="dispatch")
class save_testsuite_database(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('title', openapi.IN_QUERY, description="tsuite's name", type=openapi.TYPE_STRING),
            openapi.Parameter('tsuite_query_id', openapi.IN_QUERY, description="tsuite's query id", type=openapi.TYPE_STRING),
            openapi.Parameter('tsuite_view_id', openapi.IN_QUERY, description="tsuite's view id", type=openapi.TYPE_STRING),
            openapi.Parameter('tplan_id', openapi.IN_QUERY, description="tplan's id", type=openapi.TYPE_STRING),
        ],
        operation_summary="Response Execution Plan Status on HIL",
        responses={200: "Success response description"},
    )
    def post(self,request):
        """
        Get ALM related data 
        """
        try:
            username = request.user
            client = get_active_alm_client_obj(username)
            data = request.data
            project_name = data['project']
            stream_id = data['stream_id']
            testplan_id = data['testplan_id']
            stream_obj = get_object_or_404(Global_Configuration, gc_id=stream_id)
            tplan_obj = get_object_or_404(Test_Plan, tplan_query_id=testplan_id, gc_obj_link=stream_obj)
            
            # ---------------Update test suites and test cases data------------------
            testsuites = data['testsuite']
            for key, value in testsuites.items():

                title = value['title']
                tsuite_query_id = value['query_id']
                tsuite_view_id = value['view_id']
                
                tsuite_obj,tsuite_status = Test_Suite.objects.update_or_create(
                    tplan_obj_link=tplan_obj ,
                    tsuite_query_id=tsuite_query_id, 
                    defaults={
                        'title':title,
                        'tsuite_view_id':tsuite_view_id,
                    })

                test_cases = client.Query_Test_Case_w_Test_Suite_url(tsuite_query_id)   

                for key, value in test_cases.items():

                    tcase_selection,tcase_status = Test_Case.objects.update_or_create(
                        tsuite_obj_link=tsuite_obj,
                        tcase_query_id=value['query_id'],
                        defaults={
                            'title': value['name'],
                            'tcase_view_id': value['id'],
                            'state': value['state'],
                            'owner': value['owner'],
                            'tcase_type': value['tcase_type'],
                            'functionality': value['functionality'],
                            'test_category': value['test_category'],
                            'tsg_Compliant': value['tsg_Compliant'],
                            'implementation_path': value['implementation_path'],
                            'life_cycle_start': value['life_cycle_start'],
                            'life_cycle_end': value['life_cycle_end'],
                        }
                    )

            # ---------------Update test iterations------------------
            iteration_data = client.Query_Iteration(stream_id, testplan_id)   
            
            for key, value in iteration_data.items():

                title = value['title']
                href = value['href']
                Iteration.objects.update_or_create(tplan_obj_link=tplan_obj, 
                                                   test_phase_title=title, 
                                                   test_phase_href=href)

            # ---------------Update RQM Sw Build------------------
            sw_build_data = client.Query_SW_Build(stream_id)

            for key, value in sw_build_data.items():

                Sw_Build_RQM.objects.update_or_create(
                    global_configuration = stream_obj, 
                    build_title = value['build_title'], 
                    build_href = value['build_href'],
                    build_id = value['build_id'],
                )
            
            # ---------------Update ALM static config data------------------
            static_data = ALM_CONFIG.DATA

            for key, value in static_data.items():
                if project_name in key:
                    project = get_object_or_404(Project_Area, name=project_name)
                    hw_variants = value['HW_Variant']
                    test_env_config = value['Test_Environment_Configuration']
                    test_result = value['Test_Result']
                    test_env = value['Test_Environment']

                    project.projectAreaHref = value['Project_Area_Href']
                    project.projectAreaAlias = value['Project_Area_Alias']
                    project.save()

                    for item in hw_variants:
                        HW_Variant.objects.update_or_create(
                            global_configuration = stream_obj, 
                            HW_Variant_value = item['value'],
                            HW_Variant_href = item['href'], 
                        )

                    for item in test_env_config:
                        Test_Environment_Configuration.objects.update_or_create(
                            global_configuration = stream_obj, 
                            Test_Environment_Configuration_name = item['title'], 
                            Test_Environment_Configuration_href = item['id']
                        )
        
                    for item in test_result:
                        Test_Result.objects.update_or_create(
                            project = project, 
                            result_state = item['result_state'], 
                            state_label = item['state_label']
                        )    

                    for item in test_env:
                        HIL_Setup.objects.update_or_create(
                            project = project, 
                            name = item['value'], 
                            href = item['href']
                        )
            return JsonResponse({'status': 'success'})
        except KeyError as e:
            print('Error was found - reason "%s"' % str(e))
            return JsonResponse(
                    {"error": "Error while fetching data"},
                    status=status.HTTP_400_BAD_REQUEST
                )

@method_decorator(login_required, name="dispatch")
class query_alm_streams(APIView):
    # Create your views here.
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('project', openapi.IN_QUERY, description="project name", type=openapi.TYPE_STRING),
        ],
        operation_summary="Response Execution Plan Status on HIL",
        responses={200: "Success response description"},
    )
    def get(self,request):
        """
        Get ALM related data 
        """
        try:
            # get related query data
            username = request.user
            project = request.GET.get('project')

            # get user alm client object to query
            client = get_active_alm_client_obj(username)

            streams = client.query_stream(project)

            return JsonResponse(data = streams, status=status.HTTP_200_OK)
        
        except KeyError as e:
            # Handle the exception if the username is not found
            print('Error was found - reason "%s"' % str(e))
            return JsonResponse(
                    {"error": "Error while fetching data"},
                    status=status.HTTP_400_BAD_REQUEST
                )
    
@method_decorator(login_required, name="dispatch")
class query_alm_test_plans(APIView):
    # Create your views here.
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('test_stream_id', openapi.IN_QUERY, description="test stream ID", type=openapi.TYPE_STRING),
        ],
        operation_summary="Response Test Plans Information on one stream",
        responses={200: "Success response description"},
    )
    def get(self,request):
        """
        Get ALM test plans based on stream id. Example: [_Y-B9sgwjEe-0dfdsuPal3g]
        """
        try:
            # get related query data
            username = request.user
            stream_id = request.GET.get('test_stream_id')

            # get user alm client object to query
            client = get_active_alm_client_obj(username)

            plans = client.Query_Test_Plans_w_Stream(stream_id)

            return JsonResponse(data = plans, status=status.HTTP_200_OK)
        except KeyError as e:
            # Handle the exception if the username is not found
            print('Error was found - reason "%s"' % str(e))
            return JsonResponse(
                    {"error": "Error while fetching data"},
                    status=status.HTTP_400_BAD_REQUEST
                )
    
@method_decorator(login_required, name="dispatch")
class query_alm_test_suites(APIView):
    # Create your views here.
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('test_plan_url', openapi.IN_QUERY, description="test plan URL", type=openapi.TYPE_STRING),
        ],
        operation_summary="Response Execution Plan Status on HIL",
        responses={200: "Success response description"},
    )
    def get(self,request):
        """
        Get ALM test suites based on test plan url
        """

        # get related query data
        try:
            username = request.user
            plan_url = request.GET.get('test_plan_url')

            # get user alm client object to query
            client = get_active_alm_client_obj(username)

            suites = client.Query_Test_Suites_w_Test_Plan_url(plan_url)

            return JsonResponse(data = suites, status=status.HTTP_200_OK)
        except KeyError as e:
            # Handle the exception if the username is not found
            print('Error was found - reason "%s"' % str(e))
            return JsonResponse(
                    {"error": "Error while fetching data"},
                    status=status.HTTP_400_BAD_REQUEST
                )
@method_decorator(login_required, name="dispatch")
class admin_interface_view(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('project_name', openapi.IN_QUERY, description="Project name", type=openapi.TYPE_STRING),
            openapi.Parameter('PC_setup', openapi.IN_QUERY, description="Name PC setup", type=openapi.TYPE_STRING),
        ],
        operation_summary="Get execution plan view with parameters."
    )
    def get(self,request):
        """
        Get execution plan view info
        """
        return render(request,"admin_interface.html") #execution_plan
    
@method_decorator(login_required, name="dispatch")
class query_alm_test_cases(APIView):
    # Create your views here.
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('test_suite_url', openapi.IN_QUERY, description="test suite URL", type=openapi.TYPE_STRING),
        ],
        operation_summary="Response Execution Plan Status on HIL",
        responses={200: "Success response description"},
    )
    def get(self,request):
        """
        Get ALM test cases based on test suite url
        """
        
        try:
            # get related query data
            username = request.user
            suite_url = request.GET.get('test_suite_url')

            # get user alm client object to query
            client = get_active_alm_client_obj(username)
            test_cases = client.Query_Test_Case_w_Test_Suite_url(suite_url)
            return JsonResponse(data = test_cases, safe=False, status=status.HTTP_200_OK)
        
        except KeyError as e:
            # Handle the exception if the username is not found
            print('Error was found - reason "%s"' % str(e))
            return JsonResponse(
                    {"error": "Error while fetching data"},
                    status=status.HTTP_400_BAD_REQUEST
                )

@method_decorator(login_required,name="dispatch")
class query_alm_data(APIView):
    # Create your views here.
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('stream_id', openapi.IN_QUERY, description="stream ID", type=openapi.TYPE_STRING),
        ],
        operation_summary="Response Execution Plan Status on HIL",
        responses={200: "Success response description"},
    )
    def get(self,request):
        """
        Get ALM related data 
        """
        # get related query data
        username = request.user
        stream_id = request.GET.get('stream_id')
        data = None
        try:
            client = get_active_alm_client_obj(username)
            data = client.query_alm_data(stream_id) #ex: _Y-B9sgwjEe-0dfdsuPal3g
            return Response(data = data, status=status.HTTP_200_OK)
        except KeyError:
        # Handle the exception if the username is not found
            print(f"No project was selected")
            return Response(data = data, status=status.HTTP_204_NO_CONTENT)
        
def project_hil_list(self):
    # Query all available project
    project_query = Project_Area.objects.all()

    # Initiate project dict variable
    data = {}

    # Go through every project to query project HILs
    for project in project_query:

        # Initiate HIL dictionary
        hil_dict = {}
        data.update({project.name: hil_dict})

        # Filter hil setup based on project name 
        hil_setups = HIL_Setup.objects.filter(project=project)

        for index, hil in enumerate(hil_setups):

            # update HIL information into created dict
            hil_dict.update({index:{"name": hil.name,"host": hil.host, "port": hil.port}})

    # data = serializers.serialize("json", data)
    return JsonResponse(data)

@method_decorator(login_required,name="dispatch")
class send_execution_plan_request(APIView):

    @swagger_auto_schema(
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'execution_plan': openapi.Schema(
                type=openapi.TYPE_OBJECT,
                description='Input execution plan request as a JSON string',
                properties={
                    'author': openapi.Schema(type=openapi.TYPE_STRING, description='author'),
                    'global_config_name': openapi.Schema(type=openapi.TYPE_STRING, description='global_config_name'),
                    'global_config_id': openapi.Schema(type=openapi.TYPE_STRING, description='global_config_id'),
                    'test_plan_name': openapi.Schema(type=openapi.TYPE_STRING, description='test_plan_name'),
                    'test_plan_id': openapi.Schema(type=openapi.TYPE_STRING, description='test_plan_id'),
                    'test_plan_query_id': openapi.Schema(type=openapi.TYPE_STRING, description='test_plan_query_id'),
                    'test_suite_name': openapi.Schema(type=openapi.TYPE_STRING, description='test_suite_name'),
                    'test_suite_id': openapi.Schema(type=openapi.TYPE_STRING, description='test_suite_id'),
                    'test_suite_query_id': openapi.Schema(type=openapi.TYPE_STRING, description='test_suite_query_id'),
                    'test_case_name': openapi.Schema(type=openapi.TYPE_STRING, description='test_case_name'),
                    'test_case_id': openapi.Schema(type=openapi.TYPE_STRING, description='test_case_id'),
                    'test_case_query_id': openapi.Schema(type=openapi.TYPE_STRING, description='test_case_query_id'),
                    'test_case_implementation_path': openapi.Schema(type=openapi.TYPE_STRING, description='test_case_implementation_path'),
                    'execution_scheduler': openapi.Schema(type=openapi.TYPE_STRING, description='execution_scheduler', example=str(get_current_time())),
                    'execution_status': openapi.Schema(type=openapi.TYPE_STRING, description='execution_status'),
                    'report_path': openapi.Schema(type=openapi.TYPE_STRING, description='report_path'),
                    'test_case_result': openapi.Schema(type=openapi.TYPE_STRING, description='test_case_result'),
                }
            ),
            'hil_name': openapi.Schema(type=openapi.TYPE_STRING, description="HIL setup name", example = 'HIL 1'),
            },
        ),
    )
    def post(self, request, format = None):

        execution_plan = request.data['execution_plan']
        execution_plan_name = request.data['execution_plan_name']
        # Initialize an empty list to store the transformed data
        transformed_data = []

        # Iterate over the execution plan data
        for key, value in execution_plan.items():
            # Create a new dictionary with the required structure
            new_data = {
            "author": value.get('author'),
            "global_config_name": value.get('global_config_name'),
            "global_config_id": value.get('global_config_id'),
            "test_plan_name": value.get('test_plan_name'),
            "test_plan_id": value.get('test_plan_id'),
            "test_plan_query_id": value.get('test_plan_query_id'),
            "test_suite_name": value.get('test_suite_name'),
            "test_suite_id": value.get('test_suite_id'),
            "test_suite_query_id": value.get('test_suite_query_id'),
            "test_case_name": value.get('test_case_name'),
            "test_case_id": value.get('test_case_id'),
            "test_case_query_id": value.get('test_case_query_id'),
            "test_case_implementation_path": value.get('test_case_implementation_path'),
            "execution_scheduler": value.get('execution_scheduler'),
            "execution_status": "planned",
            "report_path": "",
            "test_case_result": "",
            "execution_plan_name":execution_plan_name,
            }
            # Append the new data to the list
            transformed_data.append(new_data)
        
        print("transformed_data: ",transformed_data)
        hil_setup = request.data['hil_name']
         # initialize host and port
        host = ''
        port = ''

        # query host and port with HIL name from DB
        hil_data = HIL_Setup.objects.filter(name = hil_setup).values()
        if hil_data.exists():

            for obj in hil_data:

                host = obj['host']
                port = obj['port']

            # create full api url to HIL setup
            request_url = str(host) + ":" + str(port) + "/auto_execution/send_execution_plan/"
            
            get_response = requests.get(request_url)

            csrf_token = None

            if get_response.status_code == 200:

                csrf_token = get_response.headers.get('X-CSRF-Token')

            else:

                return JsonResponse({'message': 'Request error - No connection with PC setup. Please contact admin for support!','status': status.HTTP_400_BAD_REQUEST})

            # send request to the corresponding PC lab
            headers = {'X-CSRF-Token': csrf_token, 'Content-Type': 'application/json'}
            # print( {'X-CSRF-Token': csrf_token, 'Content-Type': 'application/json'})
            post_response = requests.post(request_url, json = transformed_data, headers = headers)
            
            if post_response.status_code == 201:
                return JsonResponse({'message': 'Resource created successfully', 'status' : status.HTTP_200_OK})
            
            elif post_response.status_code == 200:
                return JsonResponse({'message': "Request error - Request sent successfully but no resource created due to missing field or wrong format request.", 'status': status.HTTP_400_BAD_REQUEST})
            
            else:
                return JsonResponse({'message': 'Request error - PC Setup error. Please contact admin for support!', 'status': post_response.status_code})
            
        else:
            return JsonResponse({'message': "Request error - HIL_Setup with the provided name not found.",'status' : status.HTTP_400_BAD_REQUEST})
        
@method_decorator(login_required, name="dispatch")
class query_internal_streams(APIView):
    # Create your views here.
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('project', openapi.IN_QUERY, description="project name", type=openapi.TYPE_STRING),
        ],
        operation_summary="Response Requested Stream List with project name",
        responses={200: "Success response description"},
    )
    def get(self,request):
        """
        Get ALM related data 
        """
        try:
            project_name = request.GET.get('project')

            stream_dict = {}
            
            if project_name is not None:

                stream_list = Global_Configuration.objects.filter(project__name=project_name).values('title', 'gc_id')
            
                for i, item in enumerate(stream_list):

                    stream_dict[i] = {'title': item['title'], 'identifier': item['gc_id']}
            
            return JsonResponse(data=stream_dict, status=status.HTTP_200_OK)
        
        except KeyError as e:
            # Handle the exception if the username is not found
            print('Error was found - reason "%s"' % str(e))
            return JsonResponse(
                    {"error": "Error while fetching data"},
                    status=status.HTTP_400_BAD_REQUEST
                )
    
@method_decorator(login_required, name="dispatch")
class query_internal_test_plans(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('stream_id', openapi.IN_QUERY, description="Stream ID", type=openapi.TYPE_STRING),
        ],
        operation_summary="Response Requested Test Plan List with Stream ID",
        responses={200: "Success response description"},
    )
    def get(self, request):
        """
        Get Test Plans related data
        """
        try:
            stream_id = request.GET.get('test_stream_id')
            test_plan_dict = {}

            if stream_id is not None:
                test_plan_list = Test_Plan.objects.filter(gc_obj_link__gc_id=stream_id).values('title', 'tplan_view_id', 'tplan_query_id')

                for i, item in enumerate(test_plan_list):
                    test_plan_dict[i] = {'title': item['title'], 'id': item['tplan_view_id'], 'query_id': item['tplan_query_id']}
            print("test_plan_dict: ",test_plan_dict)
            return JsonResponse(data=test_plan_dict, status=status.HTTP_200_OK)

        except KeyError as e:
            # Handle the exception if the stream_id is not found
            print('Error was found - reason "%s"' % str(e))
            return JsonResponse(
                {"error": "Error while fetching data"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
@method_decorator(login_required, name="dispatch")
class query_internal_test_suites(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('plan_id', openapi.IN_QUERY, description="Plan ID", type=openapi.TYPE_STRING),
        ],
        operation_summary="Response Requested Test Suite List with Plan ID",
        responses={200: "Success response description"},
    )
    def get(self, request):
        """
        Get Test Suites related data
        """
        try:
            gc_id = request.GET.get('gc_id')
            plan_id = request.GET.get('test_plan_url')

            gc_object = get_object_or_404(Global_Configuration, gc_id=gc_id)
            test_plan = get_object_or_404(Test_Plan, gc_obj_link=gc_object, tplan_query_id=plan_id)

            test_suite_dict = {}

            test_suite_list = Test_Suite.objects.filter(tplan_obj_link=test_plan).values('title', 'tsuite_view_id', 'tsuite_query_id')

            for i, item in enumerate(test_suite_list):
                test_suite_dict[i] = {'name': item['title'], 'id': item['tsuite_view_id'], 'query_id': item['tsuite_query_id']}

            return JsonResponse(data=test_suite_dict, status=status.HTTP_200_OK)

        except KeyError as e:
            # Handle the exception if the plan_id is not found
            print('Error was found - reason "%s"' % str(e))
            return JsonResponse(
                {"error": "Error while fetching data"},
                status=status.HTTP_400_BAD_REQUEST
            )
    
@method_decorator(login_required, name="dispatch")
class query_internal_test_cases(APIView):
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('suite_id', openapi.IN_QUERY, description="Suite ID", type=openapi.TYPE_STRING),
        ],
        operation_summary="Response Requested Test Case List with Suite ID",
        responses={200: "Success response description"},
    )
    def get(self, request):
        """
        Get Test Cases related data
        """
        try:
            gc_id = request.GET.get('gc_id')
            plan_id = request.GET.get('plan_id')
            suite_id = request.GET.get('suite_id')
            gc_object = get_object_or_404(Global_Configuration, gc_id=gc_id)
            test_plan = get_object_or_404(Test_Plan, gc_obj_link=gc_object, tplan_query_id=plan_id)
            test_suite = get_object_or_404(Test_Suite, tplan_obj_link=test_plan, tsuite_query_id=suite_id)
            test_case_dict = {}
            test_case_list = Test_Case.objects.filter(tsuite_obj_link=test_suite)
            test_case_dict = {i:obj for i,obj in enumerate(test_case_list.values())}
            # for value in test_case_dict.values():
            #     value.pop("_state",None)
            # print(test_case_dict)
            return JsonResponse(data=test_case_dict, status=status.HTTP_200_OK)

        except KeyError as e:
            # Handle the exception if the suite_id is not found
            print('Error was found - reason "%s"' % str(e))
            return JsonResponse(
                {"error": "Error while fetching data"},
                status=status.HTTP_400_BAD_REQUEST
            )
