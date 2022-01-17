"""
All the urls for the APIs in tracking app
"""
from django.urls import path

from tracking.api import views

urlpatterns = [
    path('projects/', views.ProjectListCreateAPIView.as_view()),
    path('projects/<int:pk>/', views.ProjectRetrieveUpdateDestroyAPIView.as_view()),

    path('contracts/', views.ContractListAPIView.as_view()),
    path('contracts/<int:pk>/', views.ContractRetrieveUpdateDestroyAPIView.as_view()),
    path('users/<int:user_id>/contracts/', views.UserContractListCreateAPIView.as_view()),

    path('logs/', views.TimelogListAPIView.as_view()),
    path('logs/<int:pk>/', views.TimelogRetrieveUpdateDestroyAPIView.as_view()),
    path('users/<int:user_id>/logs/', views.UserTimelogListCreateAPIView.as_view()),
    path('contracts/<int:contract_id>/logs/', views.ContractTimelogListAPIView.as_view())

]
