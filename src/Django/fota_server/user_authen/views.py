# user_authen/views.py
from rest_framework.views import APIView
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from django.shortcuts import render, redirect,HttpResponseRedirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
# from .models import ALM_Server
from .authen import sql_authen_api,handle_sql_user
from django.conf import settings
from APIs.user_config_api import set_curret_fota_obj
import pyodbc
from pyodbc import Error


class User_Authentication_Login(APIView):
     
    def get(self,request):

        if request.user.is_authenticated:
            # Go to home page if user is loged in 
            return redirect('home')
        
        else:
            return render(request, 'user_login.html')

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description='Input username of SQL'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Input password of SQL'),
            }
        ),
        operation_summary="User authentication",
        responses={200: "Success response description"},
    )
    
    def post(self,request):
        # Log in with POST method

        # Get log in form data
        username = request.data.get('username')
        password = request.data.get('password')

        # user = authenticate(username=username, password=password)
        # if user is not None:
        #         login(request, user)
        #         return redirect('home')

        client = sql_authen_api(username, password)
        if client:
            set_curret_fota_obj(username ,client)
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            else:
                handle_sql_user(username=username,password=password)
                user = authenticate(username=username, password=password)
                login(request, user)
            return redirect('home')
        else:
            messages.success(request, 'Incorrect username or password')
        return HttpResponseRedirect(reverse('u_login'))
        # user = authenticate(request, username=username, password=password)
        # if user is not None:
        #     login(request, user)
        #     return redirect('home')  # or any desired page
        # else:
        #     # Return an error message if login fails
        #     # return render(request, 'user_login.html', {'error': 'Invalid login'})
        #     messages.success(request, 'Incorrect username or password')
        # return HttpResponseRedirect(reverse('u_login'))
        
        # Authenticate with FOTA API
        # client = sql_authen_api(username, password)
        # print(client)
        
        # if (client):
            
        #     # Set current fota user object to global setting
        #     set_curret_fota_obj(username ,client)

        #     # Django authetication again with SQL credentials
        #     user = authenticate(username=username, password=password)
            
            
        #     if not user is None:
        #         # Log the user in
        #         login(request, user)
        #     else:
        #         # handle_alm_user(username, password)
        #         user = authenticate(username=username, password=password)
        #         login(request, user)
        #     return redirect('home')
        # else:
        #     # Django authetication again with ALM credentials
        #     user = authenticate(username=username, password=password)
        #     if not user is None:
        #         # Log the user in
        #         login(request, user)
        #         return redirect('home')
        #     else:
        #         messages.success(request, 'Incorrect username or password')

        # return HttpResponseRedirect(reverse('u_login'))    
        
class User_Authentication_Logout(APIView):
    def get(self,request):
        logout(request)
        return HttpResponseRedirect(reverse('u_login'))
    
