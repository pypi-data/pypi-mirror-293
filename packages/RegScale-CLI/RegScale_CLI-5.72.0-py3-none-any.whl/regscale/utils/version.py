"""Version utility functions"""

import logging

from django.utils.functional import classproperty
from packaging.version import Version
from regscale.core.app.utils.api_handler import APIHandler
from regscale.core.app.application import Application

logger = logging.getLogger(__name__)


class RegscaleVersion:
    """Regscale version utility class"""

    def __init__(self):
        self._regscale_version = None

    @classproperty
    def regscale_version(cls) -> str:
        """Fetch the platform version.

        :return: Platform version
        """
        return cls.get_platform_version()

    @staticmethod
    def get_platform_version() -> str:
        """Fetch the platform version using the provided API handler.

        :param APIHandler api_handler: API handler
        """
        logger.debug("Fetching platform version using API handler")
        try:
            api_handler = APIHandler()
            response = api_handler.get("/assets/json/version.json")
            if response.status_code == 200:
                version_data = response.json()
                return version_data.get("version", "Unknown")
            else:
                logger.error(f"Failed to fetch version. Status code: {response.status_code}")
                return "dev"
        except Exception as e:
            logger.error(f"Error fetching version: {e}", exc_info=True)
            return "dev"

    @classmethod
    def compare_versions(cls, version1: str) -> bool:
        """
        Compare two versions. Return True if version1 is greater than version2, False otherwise.

        :param str version1: Version 1 to compare with the platform version i.e. "1.0.0"
        :return: Comparison result
        :rtype: bool
        """
        special_versions = {"dev": "9999.9999.9999", "localdev": "9998.9998.9998", "Unknown": "0.0.0"}
        regscale_version = cls.get_platform_version()
        version2 = special_versions.get(regscale_version, regscale_version)
        input_version = special_versions.get(version1, version1)
        return Version(input_version) >= Version(version2)
