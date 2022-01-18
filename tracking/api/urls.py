"""
All the urls for the APIs in tracking app
"""
from django.urls import path

from tracking.api import views

urlpatterns = [
    path('projects/', views.ProjectListCreateAPIView.as_view(), name='project_list'),
    path(
        'projects/<int:pk>/',
         views.ProjectRetrieveUpdateDestroyAPIView.as_view(),
        name='project_detail'
    ),

    path('contracts/', views.ContractListAPIView.as_view(), name='contract_list'),
    path(
        'contracts/<int:pk>/',
        views.ContractRetrieveUpdateDestroyAPIView.as_view(),
        name='contract_detail'
    ),
    path(
        'users/<int:user_id>/contracts/',
        views.UserContractListCreateAPIView.as_view(),
        name='contract_list_for_user'
    ),

    path('logs/', views.TimelogListAPIView.as_view(), name='timelog_list'),
    path(
        'logs/<int:pk>/',
        views.TimelogRetrieveUpdateDestroyAPIView.as_view(),
        name='timelog_detail'
    ),
    path(
        'users/<int:user_id>/logs/',
        views.UserTimelogListCreateAPIView.as_view(),
        name='timelog_list_for_user'
    ),

]
