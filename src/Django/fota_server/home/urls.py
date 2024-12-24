from django.urls import path,include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.homepage.as_view(), name='home'),
    path("upload/", views.upload_hex_file.as_view(), name="upload_hex"),
    path('download/',views.download_hex_file.as_view(), name="download_hex"),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('hw_select/',views.select_hardware.as_view(), name='select_hardware'),
    path('fota_page/',views.fota_page.as_view(), name='fota_page'),
    path('messages/',views.pump_message.as_view(), name='pump_message'),
    # path('data', views.upload_number, name='upload_number'),

    #add data here 
    path('set-data/', views.set_data, name='set_data'),
    path('get-data/', views.get_data, name='get_data'),
    path('clear-data/', views.clear_data, name='clear_data'),
    # path('stream/',views.stream_video.as_view(), name='stream_view'),
]