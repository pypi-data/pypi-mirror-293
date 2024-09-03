import itertools
import random
from decimal import Decimal
from enum import IntEnum
from typing import Dict, List, Literal, Optional

import numpy as np
import supply_chain.product_receipts.exceptions as product_receipt_exceptions
from authentication.users.models import User
from core.currency import SupportedCurrencies
from core.exceptions import APIServiceError
from django.db import transaction
from django.utils import timezone
from organization_management.branches.services import BranchService
from organization_management.organizations.services import OrganizationService
from organization_management.workflows.constants import (
    WorkflowSchemaUseCaseType,
    WorkflowTargetObject,
)
from organization_management.workflows.services import WorkflowService
from supply_chain.product_receipts.models import (
    ProductReceipt,
    ProductReceiptAssignment,
)
from supply_chain.product_receipts.services import ProductReceiptService
from supply_chain.products.services import ProductService
from supply_chain.profiles.constants import SupplyChainOrganizationType
from supply_chain.profiles.models import SupplyChainProfile
from utils.terminal_colors import TerminalColor


class ProductReceiptGeneratorStatus(IntEnum):
    CREATED = 0
    IN_MERCHANT_BRANCH_VAULT = 5
    IN_FIRST_ENDORSEMENT_CENTRAL_VAULT = 10
    IN_FIRST_ENDORSEMENT_BRANCH_VAULT = 15
    IN_SECOND_ENDORSEMENT_CENTRAL_VAULT = 20
    IN_SECOND_ENDORSEMENT_BRANCH_VAULT = 25


def _apply_endorsement_status(
    product_receipts: List[ProductReceipt], should_back_date: bool = False
) -> None:
    for idx, product_receipt in enumerate(product_receipts):
        try:
            # Get current endorsee who owns product receipt
            product_receipt_owner = ProductReceiptService.get_owner(
                product_receipt=product_receipt
            )

            # Create endorsement workflow
            ProductReceiptService.start_endorsement_workflow(
                product_receipt=product_receipt,
                supply_chain_profile=product_receipt_owner,
                created_by=product_receipt_owner.organization.owner,
            )

            # Autocomplete workflow
            assignment = ProductReceiptAssignment.objects.filter(
                product_receipt=product_receipt,
                supply_chain_profile=product_receipt_owner,
            ).get()
            WorkflowService.auto_complete_workflow(
                workflow=assignment.endorsement_workflow,
                target_object=WorkflowTargetObject.PRODUCT_RECEIPT,
                target_object_id=str(product_receipt.product_receipt_id),
                use_case=WorkflowSchemaUseCaseType.PRODUCT_RECEIPT_ENDORSEMENT,
            )
            # Endorse product receipt
            ProductReceiptService.endorse_product_receipt(
                product_receipt=product_receipt,
                supply_chain_profile=product_receipt_owner,
                endorsed_by=product_receipt_owner.organization.owner,
                back_date_endorsement=product_receipt.created_on
                + timezone.timedelta(days=random.choice([1, 1, 1, 1, 2, 3]))
                if should_back_date
                else None,
            )
        except APIServiceError as e:
            if e.error_code == product_receipt_exceptions.ProductReceiptError0014:
                # This error is bad since it means the auto approval failed
                raise e
            else:
                # For any other errors re raise
                raise e


def _apply_branch_vault_status(product_receipts: List[ProductReceipt]) -> None:
    for product_receipt in product_receipts:
        try:
            # Get current endorsee who owns product receipt
            product_receipt_owner = ProductReceiptService.get_owner(
                product_receipt=product_receipt
            )
            #  Get all branches used for picking random branch to assign
            branches = OrganizationService(
                organization=product_receipt_owner.organization
            ).get_branches()

            # Create assignment workflow
            ProductReceiptService.start_branch_assignment_workflow(
                product_receipt=product_receipt,
                supply_chain_profile=product_receipt_owner,
                created_by=product_receipt_owner.organization.owner,
            )
            # Autocomplete workflow
            assignment = ProductReceiptAssignment.objects.filter(
                product_receipt=product_receipt,
                supply_chain_profile=product_receipt_owner,
            ).get()
            WorkflowService.auto_complete_workflow(
                workflow=assignment.branch_assignment_workflow,
                target_object=WorkflowTargetObject.PRODUCT_RECEIPT,
                target_object_id=str(product_receipt.product_receipt_id),
                use_case=WorkflowSchemaUseCaseType.PRODUCT_RECEIPT_ASSIGNMENT_TO_BRANCH,
            )
            # Complete assignment
            ProductReceiptService.assign_product_receipt_to_branch(
                product_receipt=product_receipt,
                supply_chain_profile=product_receipt_owner,
                assigned_by=product_receipt_owner.organization.owner,
                branch=random.choice(branches),
            )
        except APIServiceError as e:
            if e.error_code == product_receipt_exceptions.ProductReceiptError0026:
                # This error is bad since it means the auto approval failed
                raise e
            else:
                # For any other errors re raise
                raise e


def _create_product_receipts(
    merchant: SupplyChainProfile,
    endorsees: List[SupplyChainProfile],
    created_by: User,
    qty: int,
    back_date_list: Optional[List[timezone.datetime]] = None,
) -> list[ProductReceipt]:
    # Set up price details and precalculate random prices
    prices = [50, 100, 200, 500, 1000, 10000, 25000, 50000, 100000, 500000]
    weights = [0.15, 0.2, 0.2, 0.15, 0.1, 0.05, 0.05, 0.05, 0.025, 0.025]
    random_prices = random.choices(population=prices, weights=weights, k=qty)

    # Set up quantity details and precalculate random quantities
    quantities = [50000, 1000, 200, 500, 100000, 10000, 25000, 500000, 100, 50]
    random_quantities = random.choices(population=quantities, weights=weights, k=qty)

    product_receipts = []
    # Get merchants current products and distribute evenly amongst product receipts
    products = ProductService.get_products(
        merchant=merchant, include_unpublished="False"
    )
    for idx in range(qty):
        product_receipts.append(
            ProductReceiptService.create_product_receipt(
                merchant=merchant,
                holders=[endorsee.profile_id for endorsee in endorsees],
                product=products[idx % len(products)],
                quoted_price=Decimal(random_prices[idx]),
                quoted_price_currency=SupportedCurrencies.NIGERIAN_NAIRA,
                quoted_price_expiry=timezone.now() + timezone.timedelta(days=180),
                created_by=created_by,
                total_quantity=random_quantities[idx],
                documents=[],
                back_dated_creation=back_date_list[idx % len(back_date_list)]
                if back_date_list
                else None,
            )
        )
    return product_receipts


def generate_product_receipts(
    merchants: List[SupplyChainProfile],
    endorsees: List[List[SupplyChainProfile]],
    number_of_product_receipts: int = 1,
    status_mix: Dict[ProductReceiptGeneratorStatus, int] = {
        ProductReceiptGeneratorStatus.CREATED: 1
    },
    participant_matrix_strategy: Literal["product", "linear"] = "product",
    backdate_start: Optional[timezone.datetime] = None,
):
    """Generates product receipts based on passed params

    merchants -- The list of merchants to generate product receipts for
    bulk_agents -- The list of bulk agents to generate product receipts for
    customers -- The list of customers(distributor/end user) to create product receipts for
    number_of_product_receipts -- The number of product receipts to generate per merchant/customer pair
    status_mix -- The ratio for applying different statuses to the generated statuses
    participant_matrix_strategy -- The strategy for generating merchant/customer pairs
    backdate_start -- If this is set then the product receipts created will be backdated in an equal amount
                     starting at this date with a daily frequency
    """

    # Create participant matrix
    if participant_matrix_strategy == "linear":
        participant_matrix = zip(merchants, endorsees)
    else:
        # default to cross product always
        participant_matrix = itertools.product(merchants, endorsees)

    # if any error occurs during this process the user should be able to fix and retry
    with transaction.atomic():
        # Create a list of random dates starting from the backdate start date to the present
        back_date_list = None
        if backdate_start:
            days_delta = (timezone.now() - backdate_start).days
            back_date_list = [
                backdate_start + timezone.timedelta(days=idx)
                for idx in range(days_delta)
            ]

        back_date_start = 0
        back_date_stop = min(number_of_product_receipts, len(back_date_list))
        product_receipts = []
        for pair in participant_matrix:
            # Create product receipts first
            product_receipts.extend(
                _create_product_receipts(
                    merchant=pair[0],
                    endorsees=pair[1],
                    created_by=pair[0].organization.owner,
                    qty=number_of_product_receipts,
                    back_date_list=back_date_list[back_date_start:back_date_stop],
                )
            )

            # Calculate next start and stop indices for back date list
            if back_date_list:
                # If there is still more dates in the list then use them
                if len(back_date_list) > back_date_stop:
                    back_date_start = back_date_stop
                    back_date_stop = min(
                        back_date_start + number_of_product_receipts,
                        len(back_date_list),
                    )
                # If not then reset
                else:
                    back_date_start = 0
                    back_date_stop = min(
                        number_of_product_receipts, len(back_date_list)
                    )

        print(f"{TerminalColor.OKGREEN}Successfully created all product receipts")

        # Shuffle product receipts before partitioning
        random.shuffle(product_receipts)

        # Calculate Normalized chunks
        status_keys = list(status_mix.keys())

        # Get split indices from status mix percentages
        split_indices_raw = [
            int(len(product_receipts) * status_mix[status]) for status in status_keys
        ][:-1]
        split_indices = np.cumsum(split_indices_raw)

        # Split product receipts and store in distribution dict
        product_receipts_split = np.split(product_receipts, split_indices)
        distribution = {
            status_keys[idx]: list(product_receipts_split[idx])
            for idx in range(len(status_keys))
        }

        # Apply status
        for status in distribution:
            if status == ProductReceiptGeneratorStatus.IN_MERCHANT_BRANCH_VAULT:
                _apply_branch_vault_status(
                    product_receipts=distribution[
                        ProductReceiptGeneratorStatus.IN_MERCHANT_BRANCH_VAULT
                    ]
                    + distribution[
                        ProductReceiptGeneratorStatus.IN_FIRST_ENDORSEMENT_CENTRAL_VAULT
                    ]
                    + distribution[
                        ProductReceiptGeneratorStatus.IN_FIRST_ENDORSEMENT_BRANCH_VAULT
                    ]
                    + distribution[
                        ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_CENTRAL_VAULT
                    ]
                    + distribution[
                        ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_BRANCH_VAULT
                    ]
                )
                print(
                    f"{TerminalColor.OKGREEN}Successfully applied merchant branch vault status"
                )
            elif (
                status
                == ProductReceiptGeneratorStatus.IN_FIRST_ENDORSEMENT_CENTRAL_VAULT
            ):
                _apply_endorsement_status(
                    product_receipts=(
                        distribution[
                            ProductReceiptGeneratorStatus.IN_FIRST_ENDORSEMENT_CENTRAL_VAULT
                        ]
                        + distribution[
                            ProductReceiptGeneratorStatus.IN_FIRST_ENDORSEMENT_BRANCH_VAULT
                        ]
                        + distribution[
                            ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_CENTRAL_VAULT
                        ]
                        + distribution[
                            ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_BRANCH_VAULT
                        ]
                    ),
                    should_back_date=backdate_start != None,
                )
                print(
                    f"{TerminalColor.OKGREEN}Successfully applied first endorsement central vault status"
                )
            elif (
                status
                == ProductReceiptGeneratorStatus.IN_FIRST_ENDORSEMENT_BRANCH_VAULT
            ):
                _apply_branch_vault_status(
                    product_receipts=(
                        distribution[
                            ProductReceiptGeneratorStatus.IN_FIRST_ENDORSEMENT_BRANCH_VAULT
                        ]
                        + distribution[
                            ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_CENTRAL_VAULT
                        ]
                        + distribution[
                            ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_BRANCH_VAULT
                        ]
                    )
                )
                print(
                    f"{TerminalColor.OKGREEN}Successfully applied first endorsement branch vault status"
                )
            elif (
                status
                == ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_CENTRAL_VAULT
            ):
                _apply_endorsement_status(
                    product_receipts=(
                        distribution[
                            ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_CENTRAL_VAULT
                        ]
                        + distribution[
                            ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_BRANCH_VAULT
                        ]
                    )
                )
                print(
                    f"{TerminalColor.OKGREEN}Successfully applied second endorsement central vault status"
                )
            elif (
                status
                == ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_BRANCH_VAULT
            ):
                _apply_endorsement_status(
                    product_receipts=distribution[
                        ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_BRANCH_VAULT
                    ]
                )
                print(
                    f"{TerminalColor.OKGREEN}Successfully applied second endorsement branch vault status"
                )


def product_receipts_data(number: int):
    """
    This scenario sets up a fairly small/basic amount of
    data for product receipts and skips all the prep for products and merchant registrations

    For now it assumes that the basic user/organization scenario has been
    ran
    """

    # Get the relevant supply chain profiles for each users org
    merchant_profiles = list(
        SupplyChainProfile.objects.filter(
            organization_type=SupplyChainOrganizationType.MERCHANT
        ).all()
    )
    lender_profiles = list(
        SupplyChainProfile.objects.filter(
            organization_type=SupplyChainOrganizationType.LENDER
        ).all()
    )
    distributor_profiles = list(
        SupplyChainProfile.objects.filter(
            organization_type=SupplyChainOrganizationType.DISTRIBUTOR
        ).all()
    )

    # Scramble the returned lender profiles so that every time this is ran we get a slightly
    # different mix
    random.shuffle(lender_profiles)

    # Create endorsees list
    if len(distributor_profiles) >= len(lender_profiles):
        endorsees = [
            [lender_profiles[idx % len(lender_profiles)], distributor]
            for idx, distributor in enumerate(distributor_profiles)
        ]
    else:
        endorsees = [
            [
                lender,
                distributor_profiles[idx % len(distributor_profiles)],
            ]
            for idx, lender in enumerate(lender_profiles)
        ]

    # Generate product receipts
    generate_product_receipts(
        merchants=merchant_profiles,
        endorsees=endorsees,
        number_of_product_receipts=number,
        status_mix={
            ProductReceiptGeneratorStatus.CREATED: 0.25,
            ProductReceiptGeneratorStatus.IN_MERCHANT_BRANCH_VAULT: 0.15,
            ProductReceiptGeneratorStatus.IN_FIRST_ENDORSEMENT_CENTRAL_VAULT: 0.15,
            ProductReceiptGeneratorStatus.IN_FIRST_ENDORSEMENT_BRANCH_VAULT: 0.15,
            ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_CENTRAL_VAULT: 0.15,
            ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_BRANCH_VAULT: 0.15,
        },
        participant_matrix_strategy="product",
        backdate_start=timezone.now() - timezone.timedelta(days=365),
    )
