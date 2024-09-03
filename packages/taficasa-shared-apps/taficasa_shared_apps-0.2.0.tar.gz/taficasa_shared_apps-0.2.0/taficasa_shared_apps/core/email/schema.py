from enum import StrEnum


class SendgridVerifiedSender(StrEnum):
    """
    Represents verified senders in sendgrid
    """

    SUPPORT = "support@taficasa.com"


class SengridEmailTemplate(StrEnum):
    """
    Email templates registered in sendgrid
    """

    PROXY_WELCOME = "d-0f7604d9f9714613b0d935470ff9f5d9"
    PASSWORD_RESET = "d-2310b065d2004e6ebfdd65a69de7fdef"
    PASSWORD_CHANGED = "d-c8cfe8afc49942b0885f08dfc312b151"
    EMAIL_VERIFICATION = "d-18d95840cfac477a93de3bac9b8975a6"
    WELCOME_EMAIL = "d-8ce326146bb64ffd910f34e51a74c91c"
