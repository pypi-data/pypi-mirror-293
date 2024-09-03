from typing import Tuple, final

import names
from authentication.users.models import User
from core.testing.constants import DEFAULT_TEST_PASSWORD
from django.contrib.auth import get_user_model
from organization_management.organizations.models import Organization

from .supply_chain import SupplyChainDataMixin


class BaseTestDataClient:
    """
    This client should provide an easy way of generating test data
    across the app
    """

    def __init__(self) -> None:
        self.created_users = set()
        self.created_products = set()

    def get_test_organization_profile(self) -> Tuple[User, Organization]:
        # Import services in functions to avoid circular imports
        from organization_management.organizations.services import OrganizationService
        from supply_chain.profiles.services import SupplyChainProfileService

        # Create a new user
        random_name = names.get_full_name()
        while random_name in self.created_users:
            random_name = names.get_full_name()

        firstname, lastname = random_name.split(" ")
        user_data = {
            "email": f"{firstname}{lastname}@test.com",
            "firstname": firstname,
            "lastname": lastname,
            "password": DEFAULT_TEST_PASSWORD,
        }

        # Create User to be used in tests
        user: User = get_user_model().objects.create_user(**user_data)
        user.email_validated = True
        user.save()

        organization = OrganizationService().create_organization(
            "Test Organization",
            user,
            location_data={
                "street_address": "No 1 lokogoma street",
                "country": "NG",
                "locality": "Wuse",
                "administrative_area": "Abuja",
            },
        )

        organization.is_verified = True
        organization.save()

        # Update the created users set
        self.created_users.add(random_name)

        return user, organization


@final
class TestDataClient(SupplyChainDataMixin, BaseTestDataClient):
    """
    This is the final data client that should include all mixins
    """
