"""
Tests for all the api views for the
"""
import json

import pytest
from django.test.client import MULTIPART_CONTENT
from django.urls import reverse
from rest_framework import status

from tracking.tests.factories import (ContractFactory, ProjectFactory,
                                      TimelogFactory)
from users.tests.factories import UserFactory


@pytest.fixture(name='project')
def project_instance():
    """
    Fixture to get a project instance
    """
    return ProjectFactory()


@pytest.fixture(name='contract')
def contract_instance():
    """
    Fixture to get a contract instance
    """
    return ContractFactory()


@pytest.fixture(name='timelog')
def timelog_instance():
    """
    Fixture to get a timelog instance
    """
    return TimelogFactory()


class TestProjectListCreateAPIView:
    """
    Test all the functionality for the Project list and create endpoint
    """

    url = reverse('project_list')

    @pytest.mark.django_db
    def test_get_projects_not_accessible_for_non_authenticated_user(
            self, client
    ):
        """
        Test that unauthorized access is not allowed
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_get_projects_accessible_for_authenticated_user(self, client):
        """
        Test that authenticated users are allowed access
        """
        total_projects = 5
        ProjectFactory.create_batch(total_projects)

        client.force_login(UserFactory())
        response = client.get(self.url)

        assert response.status_code == status.HTTP_200_OK
        print(response.data)
        assert response.data['count'] == total_projects
        assert len(response.data['results']) == total_projects

    def project_post_data(self):
        return {
            'name': 'Test Project'
        }

    @pytest.mark.django_db
    def test_post_new_project_not_accessible_for_non_admin_user(self, client):
        """
        Test that non admin users cannot create a new project
        """
        client.force_login(UserFactory())
        response = client.post(self.url, data=self.project_post_data())
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_post_new_project_accessible_for_admin_user(self, client):
        """
        Test that non admin users cannot create a new project
        """
        client.force_login(UserFactory(is_staff=True))
        response = client.post(self.url, data=self.project_post_data())
        assert response.status_code == 201


class TestProjectDetailAPIView:
    """
    Test that all the functionality related to a single project detail
    works correctly
    """

    @pytest.mark.django_db
    def test_project_detail_not_accessible_to_unauthenticated_users(
            self, client, project
    ):
        """
        Test that the project detail url is inaccessible for unauthenticated users
        """
        url = reverse('project_detail', kwargs={'pk': project.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_project_detail_accessible_to_authenticated_users_for_safe_actions(
            self, client, project
    ):
        """
        Test that the project detail url is accessible to all
        authenticated users for safe actions
        """
        client.force_login(UserFactory())
        url = reverse('project_detail', kwargs={'pk': project.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_project_detail_not_accessible_to_non_admin_users_for_unsafe_actions(
            self, client, project
    ):
        """
        Test that a non-admin user cannot do an unsafe action i.e PUT,
        PATCH, DELETE on the project detail url
        """
        client.force_login(UserFactory())
        url = reverse('project_detail', kwargs={'pk': project.id})
        response = client.delete(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_project_detail_accessible_to_admin_users_for_unsafe_actions(
            self, client, project
    ):
        """
        Test that a non-admin user cannot do an unsafe action i.e PUT,
        PATCH, DELETE on the project detail url
        """
        client.force_login(UserFactory(is_staff=True))
        url = reverse('project_detail', kwargs={'pk': project.id})
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestContractListAPIView:
    """
    Test that the Contract List API endpoint works as expected
    """

    url = reverse('contract_list')

    @pytest.mark.django_db
    def test_contract_list_not_accessible_for_non_authenticated_user(
            self, client
    ):
        """
        Test that unauthorized access is not allowed
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_contract_list_for_authenticated_users(self, client):
        """
        Test that non-admin user can only see their own contracts and
        admin users can see all contracts
        """
        user_one = UserFactory()
        total_user_one_contracts = 5
        ContractFactory.create_batch(
            total_user_one_contracts, user=user_one)

        user_two = UserFactory(is_staff=True)
        total_user_two_contracts = 3
        ContractFactory.create_batch(
            total_user_two_contracts, user=user_two)

        # Owner can see only their own contracts
        client.force_login(user_one)
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == total_user_one_contracts

        # Admin can see all the contracts
        client.force_login(user_two)
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == total_user_one_contracts + \
               total_user_two_contracts


class TestContractDetailAPIView:
    """
    Test all the functionality for the contract detail endpoint
    """

    @pytest.mark.django_db
    def test_contract_detail_not_accessible_to_unauthenticated_users(
            self, client, contract
    ):
        """
        Test that the contract detail url is not found
        for unauthenticated users
        """
        url = reverse('contract_detail', kwargs={'pk': contract.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_contract_detail_is_only_accessible_to_contract_owner_or_admin(
            self, client, contract
    ):
        """
        Test that a contract detail page is only accessible to the
        owner of the contract or to an admin user
        """
        url = reverse('contract_detail', kwargs={'pk': contract.id})

        owner_user = UserFactory()
        contract.user = owner_user
        contract.save()

        # Contract owner - Accessible
        client.force_login(owner_user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Admin user - Accessible
        client.force_login(UserFactory(is_staff=True))
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Neither owner nor admin - Should not be able to find the contract!
        client.force_login(UserFactory())
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_update_contract(self, client):
        """
        Test the updation of a contract
        """
        contract = ContractFactory()
        url = reverse('contract_detail', kwargs={'pk': contract.id})

        client.force_login(contract.user)
        contract_data = {
            'hourly_price': 999
        }

        response = client.patch(
            url,
            data=json.dumps(contract_data),
            content_type=MULTIPART_CONTENT
        )
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_delete_contract(self, client, contract):
        """
        Test the deletion of a contract
        """
        url = reverse('contract_detail', kwargs={'pk': contract.id})
        client.force_login(contract.user)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestUserContractListAPIView:
    """
    Test that the list of contracts for a user are displayed correctly
    to the users with right permissions
    """

    @pytest.mark.django_db
    def test_user_contract_list_not_accessible_for_unauthenticated_users(
            self, client
    ):
        """
        Test that the contract list for user will not be accessible
        for anonymous user
        """
        url = reverse(
            'contract_list_for_user', kwargs={'user_id': UserFactory().id}
        )
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


    @pytest.mark.django_db
    def test_user_contract_list_accessible_for_owner_or_admin(
            self, client
    ):
        """
        Test that only a user themselves or the admin can
        see their contract list
        """
        total_owned_contracts = 5
        owner_user = UserFactory()
        ContractFactory.create_batch(
            total_owned_contracts, user=owner_user
        )

        url = reverse(
            'contract_list_for_user', kwargs={'user_id': owner_user.id}
        )

        # Non-owner user - Inaccessible
        client.force_login(UserFactory())
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Owner user - Accessible
        client.force_login(owner_user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == total_owned_contracts

        # Non-owner admin user - Accessible
        client.force_login(UserFactory(is_staff=True))
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == total_owned_contracts


class TestTimelogListAPIView:
    """
    Test that the timelog list API endpoint works correctly
    """

    url = reverse('timelog_list')

    @pytest.mark.django_db
    def test_timelog_list_not_accessible_for_non_authenticated_user(
            self, client
    ):
        """
        Test that unauthorized access is not allowed
        """
        response = client.get(self.url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_timelog_list_for_authenticated_users(self, client):
        """
        Test that non-admin user can only see their own logs and admin users can
        see all logs for all users
        """
        user_one = UserFactory()
        total_user_one_logs = 5
        TimelogFactory.create_batch(
            total_user_one_logs, contract__user=user_one
        )

        user_two = UserFactory(is_staff=True)
        total_user_two_logs = 3
        TimelogFactory.create_batch(
            total_user_two_logs, contract__user=user_two
        )

        client.force_login(user_one)
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == total_user_one_logs

        client.force_login(user_two)
        response = client.get(self.url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == total_user_one_logs + \
               total_user_two_logs


class TestTimelogDetailAPIView:
    """
    Test that the timelog detail API endpoint works correctly
    """

    @pytest.mark.django_db
    def test_timelog_detail_not_accessible_to_unauthenticated_users(
            self, client, timelog
    ):
        """
        Test that the timelog detail url is inaccessible for
        unauthenticated users
        """
        url = reverse('timelog_detail', kwargs={'pk': timelog.id})
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    @pytest.mark.django_db
    def test_timelog_detail_is_only_accessible_to_contract_owner_or_admin(
            self, client
    ):
        """
        Test that a timelog detail page is only accessible to the owner
        of the timelog or to an admin user
        """
        timelog = TimelogFactory(contract__user=UserFactory())
        url = reverse('timelog_detail', kwargs={'pk': timelog.id})

        # Timelog owner - Accessible
        client.force_login(timelog.contract.user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Admin user - Accessible
        client.force_login(UserFactory(is_staff=True))
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK

        # Neither owner nor admin - Not accessible!
        client.force_login(UserFactory())
        response = client.get(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    @pytest.mark.django_db
    def test_update_timelog(self, client):
        """
        Test the updation of a timelog
        """
        owner = UserFactory()
        timelog = TimelogFactory(contract__user=owner)
        url = reverse('timelog_detail', kwargs={'pk': timelog.id})

        client.force_login(owner)
        data = {
            'hours_worked': 15.5
        }
        response = client.patch(
            url,
            data=json.dumps(data),
            content_type=MULTIPART_CONTENT
        )
        assert response.status_code == status.HTTP_200_OK

    @pytest.mark.django_db
    def test_delete_timelog(self, client, timelog):
        """
        Test the deletion of a timelog
        """
        url = reverse('timelog_detail', kwargs={'pk': timelog.id})
        client.force_login(timelog.user)
        response = client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT


class TestUserTimelogListAPIView:
    """
    Test that the timelogs for a user are given correctly
    """

    @pytest.mark.django_db
    def test_user_timelog_list_not_accessible_for_unauthenticated_users(
            self, client
    ):
        """
        Test that the timelog list for user will not be
        accessible for anonymous user
        """
        url = reverse('timelog_list_for_user', kwargs={'user_id': UserFactory().id})
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


    @pytest.mark.django_db
    def test_user_timelog_list_accessible_for_owner_or_admin(
            self, client
    ):
        """
        Test that only a user themselves or the admin can
        see their contract list
        """
        total_owned_contracts = 5
        owner_user = UserFactory()
        ContractFactory.create_batch(total_owned_contracts, user=owner_user)

        url = reverse('contract_list_for_user', kwargs={'user_id': owner_user.id})

        # Non-owner user - Inaccessible
        client.force_login(UserFactory())
        response = client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

        # Owner user - Accessible
        client.force_login(owner_user)
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == total_owned_contracts

        # Non-owner admin user - Accessible
        client.force_login(UserFactory(is_staff=True))
        response = client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == total_owned_contracts
