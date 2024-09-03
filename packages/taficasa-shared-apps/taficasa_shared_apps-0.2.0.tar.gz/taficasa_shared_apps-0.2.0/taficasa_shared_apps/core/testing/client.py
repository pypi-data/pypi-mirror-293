from django.urls import reverse
from rest_framework.test import APIClient


class CustomAPIClient(APIClient):
    def __init__(self, login_data):
        super().__init__()
        self._login_data = login_data
        self._login_data["remember"] = False

    def update_login_data(self, field: str, value: str):
        self._login_data[field] = value

    def custom_login(self):
        login_response = self.post(
            reverse("authentication:login"), self._login_data, format="json"
        )
        return login_response

    def custom_logout(self):
        return self.post(reverse("authentication:logout"))
