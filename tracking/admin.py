"""
Admin for the tracking app
"""
from django.contrib import admin

from .models import Contract, Project, Timelog


@admin.register(Project, Contract, Timelog)
class TrackingAdmin(admin.ModelAdmin):
    """
    Admin for Project, Contract and Timelog models
    """
