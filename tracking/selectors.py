"""
Selectors to retrieve data from db for the tracking app
"""

from .models import Contract, Timelog


def get_contracts_for_user(user_id):
    """
    Get all the contracts for the given user ID

    Args:
        user_id (int): Id of the User

    Returns:
        QuerySet: A qs of all the relevant Contract objects
    """
    return Contract.objects.filter(user_id=user_id)


def get_timelogs_for_user(user_id):
    """
    Get all the logs for the given user ID

    Args:
        user_id (int): Id of the User

    Returns:
        QuerySet: A qs of all the relevant Timelog objects
    """
    return Timelog.objects.filter(contract__user=user_id)


def get_timelogs_for_contract(contract_id):
    """
    Get all the logs for the given contract ID

    Args:
        contract_id (int): Id of the Contract

    Returns:
        QuerySet: A qs of all the relevant Timelog objects
    """
    return Timelog.objects.filter(contract_id=contract_id)
