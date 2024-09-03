from core.data.gen.organizations import generate_organizations
from core.data.gen.product_receipts import (
    ProductReceiptGeneratorStatus,
    generate_product_receipts,
)
from core.data.raw.distributors import get_distributors_dataset, get_flux_distributor
from core.data.raw.lenders import get_flux_bank, get_lenders_dataset
from core.data.raw.merchants import get_flux_merchant, get_merchants_dataset
from django.db import transaction
from django.utils import timezone
from supply_chain.profiles.constants import SupplyChainOrganizationType


def generate_demo_data_no_analytics():
    with transaction.atomic(durable=True):
        # Get organizations data
        dataset = [get_flux_merchant(), get_flux_distributor(), get_flux_bank()]
        generate_organizations(dataset=dataset)


def generate_demo_data_with_analytics():
    with transaction.atomic(durable=True):
        # Get organizations data
        dataset = (
            get_merchants_dataset() + get_distributors_dataset() + get_lenders_dataset()
        )
        result = generate_organizations(dataset=dataset, cache_result=True)

        # Get singular lender
        lender = result[SupplyChainOrganizationType.LENDER][0]
        # Generate product receipts data
        generate_product_receipts(
            merchants=result[SupplyChainOrganizationType.MERCHANT],
            endorsees=[
                [lender, distributor]
                for distributor in result[SupplyChainOrganizationType.DISTRIBUTOR]
            ],
            number_of_product_receipts=10,
            status_mix={
                ProductReceiptGeneratorStatus.CREATED: 0,
                ProductReceiptGeneratorStatus.IN_MERCHANT_BRANCH_VAULT: 0,
                ProductReceiptGeneratorStatus.IN_FIRST_ENDORSEMENT_CENTRAL_VAULT: 0.60,
                ProductReceiptGeneratorStatus.IN_FIRST_ENDORSEMENT_BRANCH_VAULT: 0.40,
                ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_CENTRAL_VAULT: 0,
                ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_BRANCH_VAULT: 0,
            },
            participant_matrix_strategy="product",
            backdate_start=timezone.now() - timezone.timedelta(days=365),
        )
