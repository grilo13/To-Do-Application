from django.urls import path
from .views import RegisterUser, LogoutUser, LoginUser, index

urlpatterns = [
    path('', LoginUser.as_view(), name='index'),
    path('register', RegisterUser.as_view(), name='register_user'),
    path('logout', LogoutUser.as_view(), name='logout_user'),
    path('login', LoginUser.as_view(), name='login_user')
]
