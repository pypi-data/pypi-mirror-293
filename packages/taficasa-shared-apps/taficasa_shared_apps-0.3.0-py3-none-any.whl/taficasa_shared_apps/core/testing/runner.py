from django.conf import settings
from django.test.runner import DiscoverRunner
from mongoengine import connect, disconnect, get_connection
from pymongo import MongoClient


class ExtendedTestRunner(DiscoverRunner):
    def setup_databases(self, **kwargs):
        # Disconnect from the current default alias db
        disconnect()

        # Setup mongo db test db
        connect(
            db=f"test_{settings.LOCAL_MONGO_DB_NAME}",
            username=settings.LOCAL_MONGO_DB_USER,
            password=settings.LOCAL_MONGO_DB_PASSWORD,
        )

        # Continue rest of db setup
        return super().setup_databases(**kwargs)

    def teardown_databases(self, old_config, **kwargs):
        # Get connection to test db and drop db
        mongo_client = MongoClient(
            f"mongodb://{settings.LOCAL_MONGO_DB_USER}:{settings.LOCAL_MONGO_DB_PASSWORD}@localhost:27017/"
        )
        mongo_client.drop_database(f"test_{settings.LOCAL_MONGO_DB_NAME}")

        # Disconnect from the test db
        disconnect()

        # Reconnect to the current default alias db
        connect(
            db=settings.LOCAL_MONGO_DB_NAME,
            username=settings.LOCAL_MONGO_DB_USER,
            password=settings.LOCAL_MONGO_DB_PASSWORD,
        )

        return super().teardown_databases(old_config, **kwargs)
