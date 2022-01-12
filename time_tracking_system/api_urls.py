"""
Urls for all the APIs in the project
"""
from django.urls import include, path

urlpatterns = [
    # users app
    path("users/", include("users.api.urls")),

]
