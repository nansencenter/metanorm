"""Normalizer for the metadata used in the Creodias finder API"""

import logging

import dateutil
import dateutil.parser

import metanorm.utils as utils

from .base import GeoSPaaSMetadataNormalizer
from ...errors import MetadataNormalizationError

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class CreodiasEOFinderMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset using Creodias attributes"""

    @utils.raises(KeyError)
    def check(self, raw_metadata):
        """Looks for a URL in raw_metadata['url'] (added in
        geospaas_harvesting) and in
        raw_metadata['services']['download']['url'] (original location)
        """
        url = (
            raw_metadata.get('url', '') or
            raw_metadata.get('services', {}).get('download', {}).get('url', '')
        )
        return url.startswith('https://zipper.creodias.eu')

    @utils.raises(KeyError)
    def get_entry_title(self, raw_metadata):
        return raw_metadata['title']

    @utils.raises(KeyError)
    def get_entry_id(self, raw_metadata):
        return raw_metadata['title']

    @utils.raises(KeyError)
    def get_summary(self, raw_metadata):
        """Get the dataset's summary"""
        description_attributes = ('sensorMode', 'platform', 'instrument', 'startDate')
        summary_fields = {}

        description = ', '.join([
            f"{attribute}={raw_metadata[attribute]}"
            for attribute in description_attributes
        ])
        summary_fields[utils.SUMMARY_FIELDS['description']] = description

        if 'processingLevel' in raw_metadata:
            processing_level = raw_metadata['processingLevel'].replace('LEVEL', '')
            summary_fields[utils.SUMMARY_FIELDS['processing_level']] = processing_level

        return utils.dict_to_string(summary_fields)

    @utils.raises(KeyError)
    def get_time_coverage_start(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['startDate']).replace(microsecond=0)

    @utils.raises(KeyError)
    def get_time_coverage_end(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['completionDate']).replace(microsecond=0)

    @utils.raises(KeyError)
    def get_platform(self, raw_metadata):
        platform = utils.get_gcmd_platform(raw_metadata['platform'])
        if platform:
            return platform
        else:
            raise MetadataNormalizationError(f"Unknown platform {platform}")

    @utils.raises(KeyError)
    def get_instrument(self, raw_metadata):
        instrument = utils.get_gcmd_instrument(raw_metadata['instrument'])
        if instrument:
            return instrument
        else:
            raise MetadataNormalizationError(f"Unknown instrument {instrument}")

    @utils.raises(KeyError)
    def get_location_geometry(self, raw_metadata):
        return raw_metadata['geometry']

    @utils.raises(KeyError)
    def get_provider(self, raw_metadata):
        """Returns a GCMD-like provider data structure"""
        provider = utils.get_gcmd_provider([raw_metadata['organisationName']])
        if provider:
            return provider
        else:
            raise MetadataNormalizationError(f"Unknown provider {raw_metadata['organisationName']}")
