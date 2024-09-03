import random
from pathlib import Path
from typing import Iterator, List

import organization_management.workflows.exceptions as workflow_exceptions
import supply_chain.products.exceptions as product_exceptions
from core.exceptions import APIServiceError
from django.conf import settings
from django.core.files.images import ImageFile
from django.db import transaction
from organization_management.workflows.constants import (
    WorkflowSchemaUseCaseType,
    WorkflowStepType,
    WorkflowTargetObject,
)
from organization_management.workflows.services import (
    WorkflowSchemaService,
    WorkflowService,
)
from supply_chain.products.models import Product
from supply_chain.products.services import ProductService
from supply_chain.profiles.models import SupplyChainProfile

PRODUCTS = [
    {
        "name": "Cement",
        "merchant_product_id": "0001",
        "image": "cement.jpeg",
        "unit": "bags",
    },
    {
        "name": "Cooking Oil",
        "merchant_product_id": "0002",
        "image": "cooking_oil.jpeg",
        "unit": "liters",
    },
    {
        "name": "Sugar",
        "merchant_product_id": "0003",
        "image": "sugar.jpg",
        "unit": "tons",
    },
    {
        "name": "Petrol",
        "merchant_product_id": "0004",
        "image": "petrol.jpg",
        "unit": "liters",
    },
    {
        "name": "Cassava",
        "merchant_product_id": "0005",
        "image": "cassava.jpg",
        "unit": "tons",
    },
]


def _get_products_data(qty: int) -> Iterator[Product]:
    # For each call shuffle products data
    random.shuffle(PRODUCTS)

    for idx in range(min(qty, len(PRODUCTS))):
        yield PRODUCTS[idx]


def generate_products(
    merchants: List[SupplyChainProfile], products_per_merchant: int = 1
) -> List[Product]:
    # if any error occurs during this process the user should be able to fix and retry
    with transaction.atomic():
        # Create Product and publishing schema for all merchants
        created_products = []
        for merchant in merchants:
            try:
                WorkflowSchemaService.create_or_update_schema_version(
                    version_id=1,
                    organization=merchant.organization,
                    steps=[
                        {
                            "step_title": "Owner Approval Step",
                            "step_description": "Generated step for owner approval",
                            "step_type": WorkflowStepType.APPROVAL,
                            "step_order": 1,
                        }
                    ],
                    updated_by=merchant.organization.owner,
                    use_case=WorkflowSchemaUseCaseType.PRODUCT_PUBLISH,
                    should_publish=True,
                    published_by=merchant.organization.owner,
                )
            except APIServiceError as e:
                if (
                    e.error_code == workflow_exceptions.WorkflowError0001
                    or workflow_exceptions.WorkflowError0002
                ):
                    # This is fine since it means that the schema already exists
                    pass
                else:
                    raise e

            for product_data in _get_products_data(qty=products_per_merchant):
                try:
                    # Load product image into uploaded file
                    image_path = (
                        Path(settings.BASE_DIR)
                        / "apps/core/data/static"
                        / product_data["image"]
                    )
                    image_file = ImageFile(
                        open(image_path, "rb"), name=product_data["image"]
                    )
                    # Create product
                    product = ProductService.create_product(
                        merchant=merchant,
                        name=product_data["name"],
                        merchant_product_id=product_data["merchant_product_id"],
                        created_by=merchant.organization.owner,
                        image=image_file,
                        unit=product_data["unit"],
                    )
                    # Autocomplete product workflow
                    WorkflowService.auto_complete_workflow(
                        workflow=product.publish_approval_workflow,
                        target_object=WorkflowTargetObject.NONE,
                        target_object_id=str(product.product_id),
                        use_case=WorkflowSchemaUseCaseType.PRODUCT_PUBLISH,
                    )
                    # Publish it
                    ProductService.publish_product(
                        product=product, published_by=merchant.organization.owner
                    )
                    created_products.append(product)
                except APIServiceError as e:
                    if e.error_code == product_exceptions.ProductError0001:
                        # This error is fine since it just means the product already exists
                        pass
                    elif e.error_code == product_exceptions.ProductError0005:
                        # This error is bad since it means the auto approval failed
                        raise e
                    else:
                        # For any other errors re raise
                        raise e
        return created_products
