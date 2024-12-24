import pyodbc
from pyodbc import Error
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.models import User
from django.db import connections
from django.db.utils import OperationalError, InterfaceError
from django.conf import settings

def sql_authen_api(username,password):
    try:
        # connectionQuery = "DRIVER={{SQL Server}}; SERVER=192.168.1.7,1433; Database=FOTA; UID={}; PWD={};Trusted_Connection=no".format(username,password)
        # conn = pyodbc.connect(connectionQuery)
        # settings.DATABASES['default'].update(USER=username,PASSWORD=password)
        # try:
        #     with connections['default'].cursor() as cursor:
        #         # Attempt a simple query to check if the login works
        #         cursor.execute("SELECT 1")  # Will raise OperationalError if login is invalid
        #         print('Login successfully')
        #     return True
        # except (OperationalError, InterfaceError):
        #     return False
        # ip_server = settings.IP_ADDRESS
        ip_server = "localhost\\TEW_SQLEXPRESS"
        connectionQuery = "DRIVER={{ODBC Driver 17 for SQL Server}}; SERVER={},1433; Database=FOTA; UID={}; PWD={};Trusted_Connection=no".format(ip_server,username,password)
        conn = pyodbc.connect(connectionQuery)
        if conn != None:
            print("Login successfully")
            settings.DATABASES['default'].update(USER=username,PASSWORD=password)
            return True
        else:
            return False
            
    except Error as e:
        print(e)

def handle_sql_user(username,password):
    try:
        # Try to get the user
        user = User.objects.get(username=username)
        # If user exists, change the password
        user.set_password(password)
        user.save()
        return True
    except User.DoesNotExist:
        # If user does not exist, create a new user
        user = User.objects.create_user(username=username, password=password)
        user.save()
        return False


class SQLServerAuthBackend(BaseBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Check SQL Server login
        if self.check_sql_server_login(username, password):
            # Check if the user exists in Django
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                # Register the user in Django if not exists
                user = User(username=username)
                user.set_password(password)  # or user.set_password(password) if storing password is necessary
                user.save()
            return user
        return None

    def check_sql_server_login(self, username, password):
        # Create a separate SQL Server connection to validate login
        settings.DATABASES['default'].update(USER=username,PASSWORD=password)
        try:
            with connections['default'].cursor() as cursor:
                # Attempt a simple query to check if the login works
                cursor.execute("SELECT 1")  # Will raise OperationalError if login is invalid
                print('Login successfully')
            return True
        except (OperationalError, InterfaceError):
            return False

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None