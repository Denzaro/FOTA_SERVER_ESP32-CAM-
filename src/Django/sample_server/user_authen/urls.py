from django.urls import path
from .views import User_Authentication_Login,User_Authentication_Logout

urlpatterns = [
    path('login/', User_Authentication_Login.as_view(), name='u_login'),
    path('logout/', User_Authentication_Logout.as_view(), name='u_logout'),
]