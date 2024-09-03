from authentication.permissions.constants import (
    PERMISSION_EXPLANATION_MAP,
    PermissionType,
)
from django.core import checks


@checks.register()
def run_access_control_permissions_check(app_configs, **kwargs):
    errors = []
    for permission in PermissionType:
        if (
            permission not in PERMISSION_EXPLANATION_MAP
            and permission != PermissionType.UNKNOWN
        ):
            errors.append(
                checks.Error(
                    f"{permission} missing in Permission Type Explanations",
                    hint=(
                        "Please make sure every permission type defined in PermissionType "
                        "has an explanation in PERMISSION_EXPLANATION_MAP The only exception "
                        "is the UNKOWN Permission Type."
                    ),
                )
            )
            break

    return errors
