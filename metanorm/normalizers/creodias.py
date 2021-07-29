"""Normalizer for the metadata used in the Creodias finder API"""

import logging
import re

import dateutil
import dateutil.parser

import metanorm.utils as utils

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class CreodiasEOFinderMetadataNormalizer(BaseMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset using Creodias attributes"""

    def get_entry_id(self, raw_attributes):
        """Get the dataset's entry ID"""
        if ('url' in raw_attributes and
                raw_attributes['url'].startswith('https://zipper.creodias.eu/')):
            return raw_attributes.get('title')
        return None

    def get_summary(self, raw_attributes):
        """Get the dataset's summary"""
        description_attributes = ('sensorMode', 'platform', 'instrument', 'startDate')
        summary_fields = {}
        if set(description_attributes).issubset(raw_attributes.keys()):
            description = ', '.join([
                f"{attribute}={raw_attributes[attribute]}"
                for attribute in description_attributes
                if attribute in list(raw_attributes.keys())
            ])
            summary_fields[utils.SUMMARY_FIELDS['description']] = description

            if 'processingLevel' in raw_attributes:
                processing_level = raw_attributes['processingLevel'].replace('LEVEL', '')
                summary_fields[utils.SUMMARY_FIELDS['processing_level']] = processing_level

            return utils.dict_to_string(summary_fields)
        else:
            return None

    def get_time_coverage_start(self, raw_attributes):
        """Get the start of time coverage from the attributes"""
        if 'startDate' in raw_attributes:
            return dateutil.parser.parse(raw_attributes['startDate']).replace(microsecond=0)
        else:
            return None

    def get_time_coverage_end(self, raw_attributes):
        """Get the end of time coverage from the attributes"""
        if 'completionDate' in raw_attributes:
            return dateutil.parser.parse(raw_attributes['completionDate']).replace(microsecond=0)
        else:
            return None

    def get_platform(self, raw_attributes):
        """Get the platform from the attributes"""
        platform_names = (
            (r'^S([1-3][A-B])$', 'Sentinel-{}'),
        )
        if 'platform' in raw_attributes:
            for platform_regex, platform_name in platform_names:
                match = re.match(platform_regex, raw_attributes['platform'])
                if match:
                    return utils.get_gcmd_platform(platform_name.format(match.group(1)))
        return None

    def get_instrument(self, raw_attributes):
        """Get the instrument from the attributes'"""
        instrument_names = {
            'OL': 'OLCI',
            'SL': 'SLSTR'
        }
        if 'instrument' in raw_attributes:
            instrument_name = raw_attributes['instrument']
            if instrument_name in instrument_names:
                return utils.get_gcmd_instrument(instrument_names[instrument_name])
        return None

    def get_location_geometry(self, raw_attributes):
        """Returns a GeoJSON string corresponding to the location of the dataset"""
        return raw_attributes.get('geometry')

    def get_provider(self, raw_attributes):
        """Returns a GCMD-like provider data structure"""
        provider_names = {
            'ESA': 'ESA/EO'
        }
        if 'organisationName' in raw_attributes:
            provider_name = raw_attributes['organisationName']
            if provider_name in provider_names:
                return utils.get_gcmd_provider([provider_names[provider_name]])
        return None
