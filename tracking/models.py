"""
All the models for the tracking app
"""
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from djmoney.models.fields import MoneyField


class Project(models.Model):
    """
    Project that different employees work on
    """
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class Contract(models.Model):
    """
    Contract representing the agreement between a User
    and a Project with the decided upon hourly rate
    """
    project = models.ForeignKey(
        'tracking.Project',
        related_name='contracts',
        on_delete=models.CASCADE
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='contracts',
        on_delete=models.CASCADE
    )
    hourly_price = MoneyField(max_digits=14, decimal_places=2, default_currency='USD')

    class Meta:
        unique_together = ['project', 'user']

    def __str__(self):
        return f'User: {self.user} for Project: {self.project} ({self.hourly_price} hourly)'


class Timelog(models.Model):
    """
    Timelog represents the hours put in by a user under a contract
    for a single day
    """
    date = models.DateField()
    hours_worked = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(0.0), MaxValueValidator(24.0)]
    )
    contract = models.ForeignKey(
        'tracking.Contract',
        related_name='time_logs',
        on_delete=models.CASCADE
    )

    @property
    def user(self):
        """
        Return the user associated with this Timelog
        """
        return self.contract.user

    def __str__(self):
        return f'Contract: {self.contract} for date: {self.date})'
