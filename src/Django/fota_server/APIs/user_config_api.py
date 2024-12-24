# """
# ==================================================
# File: user_config_api.py
# Author:
# Date: 27-May-2024

# This Python module contains the API endpoints for our application.

# Each function in this file corresponds to an API endpoint. 

# ==================================================

# """

from django.conf import settings
from APIs.query_api import Project_Configuration_API

# def get_active_sql_client_obj(username):

#     username  = str(username)
#     username = username.lower()
    
#     client_list = settings.ALM_CLIENT
#     client_obj = None

#     try:
#         # Try to access the client obj of the username
#         client_obj = client_list[username]
#     except KeyError:
#         # Handle the exception if the username is not found
#         print(f"The username '{username}' does not exist in the settings.")

#     return client_obj

def set_curret_fota_obj(username, client):

    username  = str(username)
    username = username.lower()

    # add new alm client object to setting dict, if exist overwrite it 

    fota_client = Project_Configuration_API(client)
    settings.FOTA_CLIENT.update({username : fota_client})

    print(settings.FOTA_CLIENT)

