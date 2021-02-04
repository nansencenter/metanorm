"""Normalizer for the Copernicus In Situ TAC metadata convention"""

import logging
import re
from collections import OrderedDict

import dateutil.parser

import metanorm.utils as utils

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

class CMEMSInSituTACMetadataNormalizer(BaseMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset using
    CMEMS In Situ TAC attributes
    """

    def matches_identifier(self, raw_attributes):
        """Check that the dataset's id matches CMEMS in situ TAC data"""
        identifier = raw_attributes.get('id', '')
        return bool(re.match('^[A-Z]{2}_[A-Z]{2}_[A-Z]{2}(_[^_]+){1,2}$', identifier))

    def get_entry_id(self, raw_attributes):
        """Get the dataset's entry ID"""
        if self.matches_identifier(raw_attributes):
            return raw_attributes.get('id')
        return None

    def get_summary(self, raw_attributes):
        """Get the dataset's summary"""
        if self.matches_identifier(raw_attributes):
            description = None
            raw_summary = raw_attributes.get('summary')
            if raw_summary:
                description = raw_summary
            else:
                description = (
                    'Global Ocean - near real-time (NRT) in situ quality controlled observations, '
                    'hourly updated and distributed by INSTAC within 24-48 hours from acquisition '
                    'in average. Data are collected mainly through global networks '
                    '(Argo, OceanSites, GOSUD, EGO) and through the GTS'
                )

            return utils.dict_to_string({
                utils.SUMMARY_FIELDS['description']: description or '',
                utils.SUMMARY_FIELDS['processing_level']: '2',
                utils.SUMMARY_FIELDS['product']: 'INSITU_GLO_NRT_OBSERVATIONS_013_030'
            })
        return None

    def get_time_coverage_start(self, raw_attributes):
        """Get the start of time coverage from the attributes"""
        if self.matches_identifier(raw_attributes):
            return dateutil.parser.parse(raw_attributes.get('time_coverage_start'))
        return None

    def get_time_coverage_end(self, raw_attributes):
        """Get the end of time coverage from the attributes"""
        if self.matches_identifier(raw_attributes):
            return dateutil.parser.parse(raw_attributes.get('time_coverage_end'))
        return None

    def get_platform(self, raw_attributes):
        """Get the platform from the attributes"""
        if self.matches_identifier(raw_attributes):
            return OrderedDict([
                ('Category', 'In Situ Ocean-based Platforms'),
                ('Series_Entity', ''),
                ('Short_Name', ''),
                ('Long_Name', '')
            ])
        return None

    def get_instrument(self, raw_attributes):
        """Get the instrument from the attributes'"""
        if self.matches_identifier(raw_attributes):
            return OrderedDict([
                ('Category', 'In Situ/Laboratory Instruments'),
                ('Class', ''),
                ('Type', ''),
                ('Subtype', ''),
                ('Short_Name', ''),
                ('Long_Name', '')
            ])
        return None

    def get_location_geometry(self, raw_attributes):
        """Passes on the "geometry" attribute if it is present"""
        if self.matches_identifier(raw_attributes):
            return raw_attributes.get('geometry')
        return None

    def get_provider(self, raw_attributes):
        """Returns a GCMD-like provider data structure"""
        if self.matches_identifier(raw_attributes):
            return utils.get_gcmd_provider('cmems')
        return None