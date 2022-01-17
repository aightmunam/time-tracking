"""
Urls for all the APIs in the project
"""
from django.urls import include, path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

urlpatterns = [
    # JWT token
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # tracking app
    path('', include('tracking.api.urls')),

    # users app
    path('users/', include("users.api.urls")),


]
