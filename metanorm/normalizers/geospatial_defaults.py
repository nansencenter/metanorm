"""Default normalizer"""

import logging

import pythesint as pti

import metanorm.utils as utils
from metanorm.errors import MetadataNormalizationError

from .base import BaseDefaultMetadataNormalizer

LOGGER = logging.getLogger(__name__)


class GeoSpatialDefaultMetadataNormalizer(BaseDefaultMetadataNormalizer):
    """
    Last resort normalizer. Sets a default value when possible, otherwise raises an Exception.
    """

    def get_iso_topic_category(self, raw_attributes):  # pylint: disable=unused-argument
        """Default ISO topic category"""
        try:
            result = pti.get_iso19115_topic_category('Oceans')
        except IndexError as pti_error:
            raise MetadataNormalizationError(
                "Unable to find a value for the 'iso_topic_category' parameter") from pti_error
        return result

    def get_gcmd_location(self, raw_attributes):  # pylint: disable=unused-argument
        """Default GCMD location"""
        try:
            result = pti.get_gcmd_location('SEA SURFACE')
        except IndexError as pti_error:
            raise MetadataNormalizationError(
                "Unable to find a value for the 'gcmd_location' parameter") from pti_error
        return result

    def get_summary(self, raw_attributes):  # pylint: disable=unused-argument
        """Default summary"""
        return utils.UNKNOWN
