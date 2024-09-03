import random
import string
from typing import List, Set, Tuple

import names
from authentication.users.models import User
from core.testing.constants import DEFAULT_TEST_PASSWORD
from django.contrib.auth import get_user_model
from organization_management.organizations.models import Organization
from organization_management.workflows.constants import (
    WorkflowSchemaUseCaseType,
    WorkflowStepType,
    WorkflowTargetObject,
)
from organization_management.workflows.models import WorkflowSchemaVersion
from organization_management.workflows.services import (
    WorkflowSchemaService,
    WorkflowService,
)
from pyre_extensions import none_throws
from supply_chain.merchant_registrations.constants import (
    MerchantRegistrationConfigurationStepType,
)
from supply_chain.merchant_registrations.models import (
    MerchantRegistrationConfigurationVersion,
)
from supply_chain.merchant_registrations.services import (
    SupplyChainMerchantRegistrationService,
)
from supply_chain.products.models import Product
from supply_chain.profiles.constants import SupplyChainOrganizationType
from supply_chain.profiles.models import SupplyChainProfile


class SupplyChainDataMixin:
    created_users: Set
    created_products: Set

    def get_test_supply_chain_profile(
        self, profile_type: SupplyChainOrganizationType
    ) -> Tuple[User, SupplyChainProfile]:
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

        # Set up a supply chain profiles needed for tests
        profile = none_throws(
            SupplyChainProfileService.create_profile(
                organization=organization,
                created_by=user,
                organization_type=profile_type,
                product_receipt_prefix="TEST"
                if profile_type == SupplyChainOrganizationType.MERCHANT
                else None,
            )
        )

        return user, profile

    def get_test_product(
        self, merchant: SupplyChainProfile, created_by: User
    ) -> Product:
        # Import services in functions to avoid circular imports
        from supply_chain.products.services import ProductService

        # Get a random product id
        product_id = "".join(random.choices(string.digits, k=5))
        while product_id in self.created_products:
            product_id = "".join(random.choices(string.digits, k=5))

        # First create workflow schema and workflow to create product
        self.create_test_workflow_schema(
            published_by=created_by,
            organization=merchant.organization,
            use_case=WorkflowSchemaUseCaseType.PRODUCT_PUBLISH,
        )

        product = ProductService.create_product(
            merchant=merchant,
            name="Test Product",
            unit="bags",
            merchant_product_id=product_id,
            created_by=created_by,
        )

        # Complete approval workflow for product
        WorkflowService.auto_complete_workflow(
            workflow=product.publish_approval_workflow,
            target_object=WorkflowTargetObject.NONE,
            target_object_id="1",
            use_case=WorkflowSchemaUseCaseType.PRODUCT_PUBLISH,
        )

        product = ProductService.publish_product(
            product=product, published_by=created_by
        )
        return product

    def create_test_workflow_schema(
        self,
        published_by: User,
        organization: Organization,
        use_case: WorkflowSchemaUseCaseType,
    ) -> WorkflowSchemaVersion:
        steps_data = {
            "steps": [
                {
                    "step_title": "Owner Review Step",
                    "step_order": 1,
                    "step_description": "Generated step for owner review.",
                    "step_type": WorkflowStepType.REVIEW,
                },
                {
                    "step_title": "Owner Approval Step",
                    "step_order": 2,
                    "step_description": "Generated step for owner approval.",
                    "step_type": WorkflowStepType.APPROVAL,
                },
            ],
        }

        workflow_schema_version = WorkflowSchemaService.create_or_update_schema_version(
            organization=organization,
            version_id=1,
            steps=steps_data["steps"],
            use_case=use_case,
            published_by=published_by,
            should_publish=True,
            updated_by=published_by,
        )

        return workflow_schema_version

    def create_test_merchant_registration_configuration(
        self,
        profile: SupplyChainProfile,
        created_by: User,
    ) -> MerchantRegistrationConfigurationVersion:
        steps = [
            {
                "name": "Generated name",
                "step_type": MerchantRegistrationConfigurationStepType.OTHER,
                "step_order": 1,
                "description": "Generated description",
            }
        ]

        configuration = SupplyChainMerchantRegistrationService.create_configuration(
            profile, steps, created_by
        )

        return SupplyChainMerchantRegistrationService.get_current_version(configuration)
