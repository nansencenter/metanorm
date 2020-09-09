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
            return dateutil.parser.parse(raw_attributes['Sensing start']).replace(microsecond=0)
        else:
            return None

    def get_time_coverage_end(self, raw_attributes):
        """Get the end of time coverage from the attributes"""
        if set(['Sensing stop']).issubset(raw_attributes.keys()):
            return dateutil.parser.parse(raw_attributes['Sensing stop']).replace(microsecond=0)
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
            # This is ugly but pythesint can't find C-SAR from 'SAR-C'
            if 'SAR-C' in raw_attributes['Instrument']:
                instrument = 'C-SAR'
            else:
                instrument = raw_attributes['Instrument']

            additional_keywords = []
            if set(['Satellite name']).issubset(raw_attributes.keys()):
                additional_keywords.append(raw_attributes['Satellite name'])
            return utils.get_gcmd_instrument(instrument, additional_keywords)
        else:
            return None

    def get_location_geometry(self, raw_attributes):
        """Returns a WKT string corresponding to the location of the dataset"""

        if set(['JTS footprint']).issubset(raw_attributes.keys()):
            return raw_attributes['JTS footprint']
        else:
            return None

    def get_provider(self, raw_attributes):
        """Returns a GCMD-like provider data structure"""
        provider = None
        if set(['url']).issubset(raw_attributes.keys()):
            if 'scihub.copernicus.eu' in raw_attributes['url']:
                provider = utils.get_gcmd_provider(['ESA/EO'])
        return provider
