"""Normalizer for the ACDD convention"""

import logging

import dateutil
import dateutil.parser

import metanorm.utils as utils

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class SentinelSAFEMetadataNormalizer(BaseMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset using ACDD attributes"""

    def get_entry_title(self, raw_attributes):
        """Get the dataset's title"""
        if set(['Identifier']).issubset(raw_attributes.keys()):
            return raw_attributes['Identifier']
        else:
            return None

    def get_summary(self, raw_attributes):
        """Get the dataset's summary"""
        summary_attributes = ['Date', 'Instrument', 'Mode', 'Satellite', 'Size']
        if set(summary_attributes).intersection(raw_attributes.keys()):
            return ', '.join([
                f"{attribute}: {raw_attributes[attribute]}"
                for attribute in summary_attributes
                if attribute in list(raw_attributes.keys())
            ])
        else:
            return None

    def get_time_coverage_start(self, raw_attributes):
        """Get the start of time coverage from the attributes"""
        if set(['Sensing start']).issubset(raw_attributes.keys()):
            return dateutil.parser.parse(raw_attributes['Sensing start'])
        else:
            return None

    def get_time_coverage_end(self, raw_attributes):
        """Get the end of time coverage from the attributes"""
        if set(['Sensing stop']).issubset(raw_attributes.keys()):
            return dateutil.parser.parse(raw_attributes['Sensing stop'])
        else:
            return None

    def get_platform(self, raw_attributes):
        """Get the platform from the attributes"""
        if set(['Satellite name', 'Satellite number']).issubset(raw_attributes.keys()):
            return utils.get_gcmd_platform(
                raw_attributes['Satellite name'] + raw_attributes['Satellite number'])
        else:
            return None

    def get_instrument(self, raw_attributes):
        """Get the instrument from the attributes'"""
        if set(['Instrument']).issubset(raw_attributes.keys()):
            # This is ugly but necessary as long as pythesint can't find SAR from 'SAR-C'
            if raw_attributes['Instrument'].startswith('SAR-'):
                instrument = 'SAR'
            else:
                instrument = raw_attributes['Instrument']
            return utils.get_gcmd_instrument(instrument)
        else:
            return None

    def get_location_geometry(self, raw_attributes):
        """Returns a GEOSGeometry object corresponding to the location of the dataset"""

        if set(['JTS footprint']).issubset(raw_attributes.keys()):
            srid = '4326'
            return utils.geometry_from_wkt_string(raw_attributes['JTS footprint'], srid)
        else:
            return None

    def get_provider(self, raw_attributes):
        """Returns a GCMD-like provider data structure"""
        if set(['Operator']).issubset(raw_attributes.keys()):
            if 'European Space Agency' in raw_attributes['Operator']:
                provider_name = 'ESA/EO'
            else:
                provider_name = raw_attributes['Operator']

            # Try to find a GCMD provider
            provider = utils.get_gcmd_provider([provider_name])
            # No provider was found, we generate one from the available information
            if not provider:
                provider = utils.get_gcmd_like_provider(provider_name)
        else:
            provider = None

        return provider
