import os
from typing import Dict

import sendgrid  # type: ignore
from core.email.schema import SendgridVerifiedSender, SengridEmailTemplate
from django.conf import settings
from sendgrid.helpers.mail import Mail, To


class EmailClientSendGrid:
    """
    A class used to send predefined emails using the
    SendGrid api.
    """

    def __init__(self):
        api_key = os.getenv("SENDGRID_API_KEY", None)
        self.client = sendgrid.SendGridAPIClient(api_key=api_key) if api_key else None
        self.max_retries = 3

    def _create_mail(self, mail_data: Dict[str, str]) -> Mail:
        # If this is local dev forward all emails to the
        # email dev address
        if settings.LOCAL:
            # Get current dev email
            if settings.LOCAL_GCLOUD_CONFIG:
                current_dev_email = settings.LOCAL_GCLOUD_CONFIG["active_account"]
            else:
                current_dev_email = "email-dev@taficasa.com"
            mail_data["to_emails"] = current_dev_email

        return Mail(
            from_email=mail_data["from_email"],
            to_emails=mail_data["to_emails"],
        )

    def _send(self, message: Mail):
        # Do not send mail during tests or if client is None
        if not self.client or settings.TESTING:
            return

        try_send_mail = True
        mail_send_tries = 0
        while try_send_mail:
            try:
                mail_send_tries += 1
                response = self.client.send(message)

                if response.status_code == 202 or mail_send_tries >= self.max_retries:
                    try_send_mail = False
            except Exception as e:
                try_send_mail = False
                # TODO Add logging functionality for any email failures
                pass

    def send_welcome_mail(self, user):
        message = self._create_mail(
            {
                "from_email": (SendgridVerifiedSender.SUPPORT),
                "to_emails": [To(email=user.email, name=user.full_name)],
            },
        )

        # Set transactional template id and data for the welcome mails
        message.template_id = SengridEmailTemplate.WELCOME_EMAIL
        message.dynamic_template_data = {"firstname": user.firstname}
        self._send(message)

    def send_welcome_mail_on_proxy_creation(
        self, user, creator, organization, temp_password
    ):
        message = self._create_mail(
            {
                "from_email": (SendgridVerifiedSender.SUPPORT),
                "to_emails": [To(email=user.email, name=user.full_name)],
            },
        )

        # Set transactional template id and data for the welcome mails
        message.template_id = SengridEmailTemplate.PROXY_WELCOME
        message.dynamic_template_data = {
            "firstname": user.firstname,
            "temp_password": temp_password,
            "creator_firstname": creator.firstname,
            "org_name": organization.name,
        }
        self._send(message)

    def send_password_reset_request_mail(self, user, reset_url):
        message = self._create_mail(
            {
                "from_email": (SendgridVerifiedSender.SUPPORT),
                "to_emails": [To(email=user.email, name=user.full_name)],
            },
        )

        # Set transactional template id and data for the password reset request mails
        message.template_id = SengridEmailTemplate.PASSWORD_RESET
        message.dynamic_template_data = {
            "firstname": user.firstname,
            "reset_url": reset_url,
        }
        self._send(message)

    def send_password_changed_mail(self, user):
        message = self._create_mail(
            {
                "from_email": (SendgridVerifiedSender.SUPPORT),
                "to_emails": [To(email=user.email, name=user.full_name)],
            },
        )

        # Set transactional template id and data for the password reset request mails
        message.template_id = SengridEmailTemplate.PASSWORD_CHANGED
        message.dynamic_template_data = {"firstname": user.firstname}

        self._send(message)

    def send_email_verification_mail(self, user, verify_url):
        message = self._create_mail(
            {
                "from_email": (SendgridVerifiedSender.SUPPORT),
                "to_emails": [To(email=user.email, name=user.full_name)],
            },
        )

        # Set transactional template id and data for the welcome mails
        message.template_id = SengridEmailTemplate.EMAIL_VERIFICATION
        message.dynamic_template_data = {
            "firstname": user.firstname,
            "verify_url": verify_url,
        }

        self._send(message)

    def send_verification_acknowledgement_mail(self, user):
        """Method for sending email when an organization verification request has been made."""
        message = self._create_mail(
            {
                "from_email": (SendgridVerifiedSender.SUPPORT),
                "to_emails": [To(email=user.email, name=user.full_name)],
            },
        )

        # Use this while we design a template for pending verifications
        message.template_id = SengridEmailTemplate.WELCOME_EMAIL
        message.dynamic_template_data = {"firstname": user.firstname}
        self._send(message)

    def send_verification_approval_mail(self, user):
        """Method for sending email to a user when an organization has been verified."""
        message = self._create_mail(
            {
                "from_email": (SendgridVerifiedSender.SUPPORT),
                "to_emails": [To(email=user.email, name=user.full_name)],
            },
        )

        # Use this while we design a template for approved verifications
        message.template_id = SengridEmailTemplate.WELCOME_EMAIL
        message.dynamic_template_data = {"firstname": user.firstname}
        self._send(message)
