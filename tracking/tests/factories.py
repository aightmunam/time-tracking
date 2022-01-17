"""
All the factories for the tracking app
"""

from factory import Faker, SubFactory
from factory.django import DjangoModelFactory

from tracking.models import Contract, Project, Timelog
from users.tests.factories import UserFactory


class ProjectFactory(DjangoModelFactory):
    """
    Factory for Project model
    """

    class Meta:
        model = Project

    name = Faker('word')


class ContractFactory(DjangoModelFactory):
    """
    Factory for Contract model
    """

    class Meta:
        model = Contract

    project = SubFactory(ProjectFactory)
    user = SubFactory(UserFactory)
    hourly_price = Faker('pydecimal', left_digits=2, right_digits=2, positive=True)


class TimelogFactory(DjangoModelFactory):
    """
    Factory for Timelog
    """

    class Meta:
        model = Timelog

    contract = SubFactory(ContractFactory)
    date = Faker('date')
    hours_worked = Faker('pydecimal', min_value=0.0, max_value=24.0)
