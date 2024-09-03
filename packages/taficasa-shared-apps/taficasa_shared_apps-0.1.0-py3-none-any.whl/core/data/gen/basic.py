from core.data.gen.organizations import generate_organizations
from core.data.gen.product_receipts import (
    ProductReceiptGeneratorStatus,
    generate_product_receipts,
)
from core.data.raw.basic import get_basic_dataset
from django.db import transaction
from supply_chain.profiles.constants import SupplyChainOrganizationType


def generate_basic_data():
    with transaction.atomic(durable=True):
        # Get organizations data
        result = generate_organizations(dataset=get_basic_dataset(), cache_result=True)

        # Get singular lender
        lender = result[SupplyChainOrganizationType.LENDER][0]
        # Generate product receipts data
        generate_product_receipts(
            merchants=result[SupplyChainOrganizationType.MERCHANT],
            endorsees=[
                [lender, distributor]
                for distributor in result[SupplyChainOrganizationType.DISTRIBUTOR]
            ],
            number_of_product_receipts=30,
            status_mix={
                ProductReceiptGeneratorStatus.CREATED: 0.25,
                ProductReceiptGeneratorStatus.IN_MERCHANT_BRANCH_VAULT: 0.15,
                ProductReceiptGeneratorStatus.IN_FIRST_ENDORSEMENT_CENTRAL_VAULT: 0.15,
                ProductReceiptGeneratorStatus.IN_FIRST_ENDORSEMENT_BRANCH_VAULT: 0.15,
                ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_CENTRAL_VAULT: 0.15,
                ProductReceiptGeneratorStatus.IN_SECOND_ENDORSEMENT_BRANCH_VAULT: 0.15,
            },
            participant_matrix_strategy="product",
        )
