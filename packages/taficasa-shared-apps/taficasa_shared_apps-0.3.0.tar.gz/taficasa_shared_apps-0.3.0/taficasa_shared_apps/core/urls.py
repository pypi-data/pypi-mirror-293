from enum import StrEnum


class URLArgumentName(StrEnum):
    USER = "userid"
    ORGANIZATION = "organization_id"
    ORGANIZATION_PUBLIC = "public_id"
    TEAM = "team_id"
    ROLE = "role_id"
    ROLE_REQUEST = "role_request_id"
    BRANCH = "branch_id"
    WORKFLOW = "workflow_id"
    WORKFLOW_SCHEMA = "workflow_schema_id"
    WORKFLOW_SCHEMA_USE_CASE = "use_case"
    PRODUCT = "product_id"
    PRODUCT_CATEGORY = "product_category_id"
    NOTIFICATION = "notification_id"
    PRODUCT_RECEIPT = "product_receipt_id"
    PICKUP_REQUEST = "pickup_request_id"
    MERCHANT_REGISTRATION = "merchant_registration_id"
    SUPPLY_CHAIN_PROFILE = "profile_id"
    LOAN_APPLICATION = "application_id"
    VERIFICATION = "verification_id"
    STEP_ORDER = "step_order"
