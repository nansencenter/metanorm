"""Normalizer for the Sentinel SAFE convention, used by Scihub"""

import logging
import re

import dateutil
import dateutil.parser

import metanorm.utils as utils

from .base import GeoSPaaSMetadataNormalizer
from ...errors import MetadataNormalizationError

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class ScihubODataMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset using attributes
    from the Scihub OData API
    """

    def check(self, raw_metadata):
        url = raw_metadata.get('url', '')
        return (url.startswith('https://apihub.copernicus.eu/apihub/odata/v1')
                or url.startswith('https://scihub.copernicus.eu/apihub/odata/v1')
                or url.startswith('https://colhub.met.no/odata/v1'))

    @utils.raises(KeyError)
    def get_entry_title(self, raw_metadata):
        return raw_metadata['Identifier']

    @utils.raises(KeyError)
    def get_entry_id(self, raw_metadata):
        """Returns a entry_id for scihub copernicus cases"""
        return raw_metadata['Identifier']

    @utils.raises(KeyError)
    def get_summary(self, raw_metadata):
        """Get the dataset's summary"""
        description_attributes = ['Date', 'Instrument name', 'Mode', 'Satellite', 'Size',
                                  'Timeliness Category']
        summary_fields = {}

        description = ', '.join([
            f"{attribute}={raw_metadata[attribute]}"
            for attribute in description_attributes
            if attribute in list(raw_metadata.keys())
        ])
        if not description:
            raise MetadataNormalizationError(f"Could not build a description from {raw_metadata}")
        summary_fields[utils.SUMMARY_FIELDS['description']] = description

        for attribute_name in ['Processing level', 'Product level']:
            if attribute_name in raw_metadata.keys():
                processing_level = re.match(
                    '^(L|Level-)?([0-9A-Z]+)$', raw_metadata[attribute_name]).group(2)
                summary_fields[utils.SUMMARY_FIELDS['processing_level']] = processing_level

        return utils.dict_to_string(summary_fields)

    @utils.raises(KeyError)
    def get_time_coverage_start(self, raw_metadata):
        """Get the start of time coverage from the attributes"""
        return dateutil.parser.parse(raw_metadata['Sensing start']).replace(microsecond=0)

    @utils.raises(KeyError)
    def get_time_coverage_end(self, raw_metadata):
        """Get the end of time coverage from the attributes"""
        return dateutil.parser.parse(raw_metadata['Sensing stop']).replace(microsecond=0)

    @utils.raises(KeyError)
    def get_platform(self, raw_metadata):
        """Get the platform from the attributes"""
        return utils.get_gcmd_platform(
            raw_metadata['Satellite name'] + raw_metadata['Satellite number'])

    @utils.raises(KeyError)
    def get_instrument(self, raw_metadata):
        """Get the instrument from the attributes'"""
        instrument = raw_metadata['Instrument']
        additional_keywords = []
        if 'Satellite name' in raw_metadata:
            additional_keywords.append(raw_metadata['Satellite name'])
        return utils.get_gcmd_instrument(instrument, additional_keywords)

    @utils.raises(KeyError)
    def get_location_geometry(self, raw_metadata):
        """Returns a WKT string corresponding to the location of the dataset"""
        return raw_metadata['JTS footprint']

    @utils.raises(KeyError)
    def get_provider(self, raw_metadata):
        """Returns a GCMD-like provider data structure"""
        return utils.get_gcmd_provider(['ESA/EO'])
