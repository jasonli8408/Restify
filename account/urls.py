from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *
from django.urls import path

app_name = 'api'
urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('token/blacklist/')
]