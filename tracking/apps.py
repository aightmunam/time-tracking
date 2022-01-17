"""
App configuration for tracking app
"""
from django.apps import AppConfig


class TrackingConfig(AppConfig):
    """
    Config for tracking app
    """

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'tracking'
