"""Normalizer for the Copernicus In Situ TAC metadata convention"""

import logging
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

    def get_entry_id(self, raw_attributes):
        """Get the dataset's entry ID"""
        return raw_attributes.get('id')

    def get_summary(self, raw_attributes):
        """Get the dataset's summary"""
        description = None
        if 'summary' in raw_attributes:
            description = raw_attributes['summary']
        elif (set('author', 'title').issubset(raw_attributes)
                and raw_attributes['author'] == 'Coriolis and Copernicus data provider'
                and raw_attributes['title'] == 'Global Ocean - In Situ Observation Copernicus'):
            description = (
                'Global Ocean - near real-time (NRT) in situ quality controlled observations, '
                'hourly updated and distributed by INSTAC within 24-48 hours from acquisition '
                'in average. Data are collected mainly through global networks '
                '(Argo, OceanSites, GOSUD, EGO) and through the GTS'
            )

        if description:
            return utils.dict_to_string({
                utils.SUMMARY_FIELDS['description']: description,
                utils.SUMMARY_FIELDS['processing_level']: '2',
                utils.SUMMARY_FIELDS['product']: 'INSITU_GLO_NRT_OBSERVATIONS_013_030'
            })
        return None

    def get_time_coverage_start(self, raw_attributes):
        """Get the start of time coverage from the attributes"""
        return dateutil.parser.parse(raw_attributes.get('time_coverage_start'))

    def get_time_coverage_end(self, raw_attributes):
        """Get the end of time coverage from the attributes"""
        return dateutil.parser.parse(raw_attributes.get('time_coverage_end'))

    def get_platform(self, raw_attributes):
        """Get the platform from the attributes"""
        if raw_attributes.get('author') == 'Coriolis and Copernicus data provider':
            return OrderedDict([
                ('Category', 'In Situ Ocean-based Platforms'),
                ('Series_Entity', ''),
                ('Short_Name', ''),
                ('Long_Name', '')
            ])
        return None

    def get_instrument(self, raw_attributes):
        """Get the instrument from the attributes'"""
        if raw_attributes.get('author') == 'Coriolis and Copernicus data provider':
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
        """Returns a GeoJSON string corresponding to the location of the dataset"""
        return raw_attributes.get('geometry')

    def get_provider(self, raw_attributes):
        """Returns a GCMD-like provider data structure"""
        return utils.get_gcmd_provider('cmems')
