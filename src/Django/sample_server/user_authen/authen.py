from alm_qm.client import Client
from django.contrib.auth.models import User


def alm_authen_api(username, password, base_url):
    try:
        client = Client(base_url=base_url, username=username, password=password)
        client.query_projects()
        return client
    except Exception as e:
        # print("ERROR FAILED TO LOGIN, PLEASE CHECK USER ID & PASSWORD")
        # print(f"Detail: {e}")
        return None
    
def handle_alm_user(username, password):
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