import os
from typing import Optional

import google_crc32c
from google.cloud import secretmanager


class GCPSecretManager:
    def __init__(self) -> None:
        self.client = secretmanager.SecretManagerServiceClient()
        self.project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")

    def get_secret(self, secret_name: str) -> str:
        full_key = f"projects/{self.project_id}/secrets/{secret_name}/versions/latest"
        response = self.client.access_secret_version(name=full_key)

        # Verify payload checksum.
        crc32c = google_crc32c.Checksum()
        crc32c.update(response.payload.data)
        if response.payload.data_crc32c != int(crc32c.hexdigest(), 16):
            raise RuntimeError("Secret Manager Data Corruption Detected")

        # Return decoded string
        return response.payload.data.decode("UTF-8")
