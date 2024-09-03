from pathlib import Path

from authentication.roles.models import Role
from authentication.roles.services import RoleService
from authentication.users.models.auxillary import PasswordResetRequest
from authentication.users.services import UserService
from authentication.users.services.profiles import UserProfileService
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files.images import ImageFile
from django.db import transaction
from organization_management.branches.services import BranchService
from organization_management.organizations.services import OrganizationService
from organization_management.teams.services import TeamService
from organization_management.workflows.constants import (
    WorkflowSchemaUseCaseType,
    WorkflowTargetObject,
)
from organization_management.workflows.services.workflow_schema_services import (
    WorkflowSchemaService,
)
from organization_management.workflows.services.workflow_services import WorkflowService
from supply_chain.product_receipts.services.pickup import ProductReceiptPickupService
from supply_chain.products.services import ProductService
from supply_chain.profiles.constants import SupplyChainOrganizationType
from supply_chain.profiles.services import SupplyChainProfileService
from utils.terminal_colors import TerminalColor


def _get_logo_image(
    image_name: str, org_type: SupplyChainOrganizationType
) -> ImageFile | None:
    # Load logo image into uploaded file
    image_path = (
        Path(settings.BASE_DIR) / f"apps/core/data/static/{org_type}/{image_name}"
    )
    if image_path.exists():
        return ImageFile(open(image_path, "rb"), name=image_name)

    return None


def _get_profile_image(image_name: str) -> ImageFile | None:
    # Load logo image into uploaded file
    image_path = Path(settings.BASE_DIR) / f"apps/core/data/static/users/{image_name}"
    if image_path.exists():
        return ImageFile(open(image_path, "rb"), name=image_name)

    return None


def generate_organizations(dataset, cache_result: bool = False):
    """
    This scenario sets up data for the merchants
    """

    # Cache result if requested for now only cache supply chain profiles
    result_cache = {}

    # Generate users, orgs etc.
    with transaction.atomic():
        for data in dataset:
            # First create the organization owner
            organization_owner = get_user_model().objects.create_user(
                firstname=data["owner"]["firstname"],
                lastname=data["owner"]["lastname"],
                password=data["owner"]["password"],
                email=data["owner"]["email"],
            )
            organization_owner.email_validated = True
            organization_owner.save()
            print(
                f"{TerminalColor.OKGREEN}Successfully created organization owner for {data['organization_name']}{TerminalColor.ENDC}"
            )

            # Create the organization for the owner
            organization = OrganizationService().create_organization(
                name=data["organization_name"],
                creator=organization_owner,
                location_data=data["branches"][data["headquarter_branch_name"]][
                    "location"
                ],
                logo=_get_logo_image(
                    image_name=data["logo_file"], org_type=data["organization_type"]
                ),
            )
            organization.is_verified = True
            organization.save()
            print(
                f"{TerminalColor.OKGREEN}Successfully created organization {data['organization_name']}{TerminalColor.ENDC}"
            )

            # Create the proper supply chain profile
            supply_chain_profile = SupplyChainProfileService.create_profile(
                organization=organization,
                created_by=organization_owner,
                organization_type=data["organization_type"],
                product_receipt_prefix=data["product_receipt_prefix"]
                if data["organization_type"] == SupplyChainOrganizationType.MERCHANT
                else None,
            )

            # Cache supply chain profile if necessary
            if cache_result:
                if data["organization_type"] not in result_cache:
                    result_cache[data["organization_type"]] = []
                result_cache[data["organization_type"]].append(supply_chain_profile)

            print(
                f"{TerminalColor.OKGREEN}Successfully created supply chain profile {data['organization_name']}{TerminalColor.ENDC}"
            )

            # Create all branches
            branch_obj_map = {}
            for branch_key, branch in data["branches"].items():
                if branch["is_headquarters"]:
                    # Just save and skip headquarters branch since it has already been created
                    headquarters = BranchService.get_headquarter_branch(
                        organization=organization
                    )
                    BranchService.update_branch(
                        branch=headquarters,
                        validated_data={"name": branch["name"]},
                        updated_by=organization_owner,
                    )
                    branch_obj_map[branch_key] = headquarters
                else:
                    branch_obj = BranchService.create_branch(
                        name=branch["name"],
                        organization=organization,
                        creator=organization_owner,
                        location_data=branch["location"],
                    )
                    branch_obj_map[branch_key] = branch_obj

            print(
                f"{TerminalColor.OKGREEN}Successfully created branches for {data['organization_name']}{TerminalColor.ENDC}"
            )

            # Create all teams
            team_obj_map = {}
            for team_key, team in data["teams"].items():
                team_obj = TeamService().create_team(
                    name=team["name"],
                    organization=organization,
                    creator=organization_owner,
                )
                team_obj_map[team_key] = team_obj

            print(
                f"{TerminalColor.OKGREEN}Successfully created teams for {data['organization_name']}{TerminalColor.ENDC}"
            )

            # Create all roles
            role_obj_map = {}
            for role_key, role in data["roles"].items():
                role_obj = RoleService.create_role(
                    name=role["name"],
                    description=role["description"],
                    organization=organization,
                    creator=organization_owner,
                    permission_types=role["permissions"],
                )
                role_obj_map[role_key] = role_obj

            # Also add the organization's default roles to the map
            for key, name in [
                ("technical_admin", "Technical Admin"),
                ("super_user", "Super User"),
            ]:
                role_obj_map[key] = Role.objects.filter(
                    name=name, organization=organization
                ).get()

            print(
                f"{TerminalColor.OKGREEN}Successfully created roles for {data['organization_name']}{TerminalColor.ENDC}"
            )

            # Add Members to the org if necessary
            if len(data["members"]) > 0:
                OrganizationService.add_member(
                    organization=organization,
                    emails=[member["email"] for member in data["members"]],
                    added_by=organization_owner,
                )

            print(
                f"{TerminalColor.OKGREEN}Successfully added members for {data['organization_name']}{TerminalColor.ENDC}"
            )

            # Complete user sign up
            user_obj_map = {}
            for member in data["members"]:
                member_obj = (
                    get_user_model().objects.filter(email=member["email"]).get()
                )

                # Save obj for later use
                user_obj_map[member["email"]] = member_obj

                # Roundabout way to get password, we first reset with a known password then use
                # that to complete the signup. This is done because the password for a new member is
                # normally sent to their email directly
                UserService(user=member_obj).request_password_reset()
                reset_request = PasswordResetRequest.objects.filter(
                    user=member_obj, completed=False
                ).get()
                UserService(user=member_obj).reset_password(
                    reset_id=reset_request.reset_id, new_password=member["password"]
                )

                UserService().complete_proxy_user_signup(
                    user=member_obj,
                    firstname=member["firstname"],
                    lastname=member["lastname"],
                    old_password=member["password"],
                    new_password="Admin@Password1",
                )
                member_obj.email_validated = True
                member_obj.save()

                # Update profile photo
                UserProfileService(user=member_obj).update_profile_picture(
                    new_picture=_get_profile_image(image_name=member["profile_photo"])
                )

                # Add user to their branch
                BranchService.add_member(
                    user=member_obj,
                    branch=branch_obj_map[member["branch"]],
                    added_by=organization_owner,
                )

                # Add user to any teams they are a part of
                for team in member["teams"]:
                    TeamService.add_member(
                        user=member_obj,
                        team=team_obj_map[team],
                        added_by=organization_owner,
                    )

                # Add any necessary roles to users
                for role in member["roles"]:
                    RoleService.assign_user_to_role(
                        user=member_obj,
                        role=role_obj_map[role],
                        added_by=organization_owner,
                    )
            print(
                f"{TerminalColor.OKGREEN}Successfully updated all member attributes for {data['organization_name']}{TerminalColor.ENDC}"
            )

            # Give the org owner all permissions via a role
            RoleService.assign_user_to_role(
                user=organization_owner,
                role=role_obj_map["org_owner"],
                added_by=organization_owner,
            )
            print(
                f"{TerminalColor.OKGREEN}Successfully created super role and assigned to owner for {data['organization_name']}{TerminalColor.ENDC}"
            )

            # Generate any workflows for the organization
            for use_case, workflow in data["workflows"].items():
                # Replace roles in workflow steps with role objects
                for step in workflow["steps"]:
                    if "owned_by_role" in step:
                        step["owned_by_role"] = role_obj_map[step["owned_by_role"]]

                WorkflowSchemaService.create_or_update_schema_version(
                    version_id=1,
                    organization=organization,
                    steps=workflow["steps"],
                    updated_by=organization_owner,
                    use_case=use_case,
                    should_publish=True,
                    published_by=organization_owner,
                )
            print(
                f"{TerminalColor.OKGREEN}Successfully created all workflows for {data['organization_name']}{TerminalColor.ENDC}"
            )

            # Generate depots products only for merchant
            if data["organization_type"] == SupplyChainOrganizationType.MERCHANT:
                for product in data["products"]:
                    # Load product image into uploaded file
                    image_path = (
                        Path(settings.BASE_DIR)
                        / "apps/core/data/static/products"
                        / product["image"]
                    )
                    image_file = ImageFile(
                        open(image_path, "rb"), name=product["image"]
                    )
                    # Create product
                    product = ProductService.create_product(
                        merchant=supply_chain_profile,
                        name=product["name"],
                        merchant_product_id=product["merchant_product_id"],
                        created_by=organization_owner,
                        image=image_file,
                        unit=product["unit"],
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
                        product=product, published_by=organization_owner
                    )

                for branch in branch_obj_map.values():
                    ProductReceiptPickupService.create_pickup_depot(
                        supply_chain_profile=supply_chain_profile,
                        name=branch.name,
                        merchant_depot_id=f"depot-{branch.name}",
                        branch=branch,
                        created_by=organization_owner,
                    )
            # Generate access requests for the bank only
            if data["organization_type"] == SupplyChainOrganizationType.LENDER:
                for request in data["access_requests"]:
                    RoleService.start_role_request_workflow(
                        role=role_obj_map[request["role"]],
                        users=[user_obj_map[user] for user in request["users"]],
                        organization=organization,
                        requested_by=organization_owner,
                    )
            print(
                f"{TerminalColor.OKGREEN}Successfully created products for {data['organization_name']}{TerminalColor.ENDC}"
            )

    return result_cache
