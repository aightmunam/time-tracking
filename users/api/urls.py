"""
Local urls for the users apis
"""
from django.urls import path

from .views import ListRegisterView, UserRetrieveUpdateDestroyView

urlpatterns = [
    path('', ListRegisterView.as_view(), name='register'),
    path('<int:pk>/', UserRetrieveUpdateDestroyView.as_view(), name='detail'),
]
