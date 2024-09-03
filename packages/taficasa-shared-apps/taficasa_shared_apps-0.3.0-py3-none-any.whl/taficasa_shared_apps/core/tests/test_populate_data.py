from unittest import TestCase, mock, skip

from core.data.gen import generate_basic_data


def mock_save(*args, **kwargs):
    return "Fake file"


@skip("Skipping until we add logs that do not show in test for the populate functions")
class PopulateDataTests(TestCase):
    @mock.patch("core.storage.backends.BaseStorage.save", mock_save)
    def test_populate_data(self):
        # Test basic scenario
        generate_basic_data()
