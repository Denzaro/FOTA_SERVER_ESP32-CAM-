from django.urls import path,include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.homepage.as_view(), name='home'),
    
    path('query_alm_data/', views.query_alm_data.as_view() , name = 'query_alm_data'),
    path('query_alm_streams/', views.query_alm_streams.as_view() , name = 'query_alm_streams'),
    path('query_alm_test_plans/', views.query_alm_test_plans.as_view() , name = 'query_alm_test_plans'),
    path('query_alm_test_suites/', views.query_alm_test_suites.as_view() , name = 'query_alm_test_suites'),
    path('query_alm_test_cases/', views.query_alm_test_cases.as_view() , name = 'query_alm_test_cases'),

    path('query_internal_streams/', views.query_internal_streams.as_view() , name = 'query_internal_streams'),
    path('query_internal_test_plans/', views.query_internal_test_plans.as_view() , name = 'query_internal_test_plans'),
    path('query_internal_test_suites/', views.query_internal_test_suites.as_view() , name = 'query_internal_test_suites'),
    path('query_internal_test_cases/', views.query_internal_test_cases.as_view() , name = 'query_internal_test_cases'),

    path('send_execution_plan/', views.send_execution_plan_request.as_view(), name = 'send_execution_plan'),
    path('set_execution_plan_view/', views.set_execution_plan_view.as_view(), name='set_execution_plan_view'),
    path('project-hil-list/', views.project_hil_list , name = 'query-project-hil'),
    path('tfms_check_current_execution_plan/', views.current_execution_plan.as_view() , name = 'tfms_check_current_execution_plan'),
	
	path('save_streams_database/',views.save_streams_database.as_view(),name='save_streams_database'),
	path('save_testplan_database/',views.save_testplan_database.as_view(),name='save_testplan_database'),
    path('save_testsuite_database/',views.save_testsuite_database.as_view(),name='save_testsuite_database'),

    path('download_report/',views.download_report,name="download_report"),

   

]	