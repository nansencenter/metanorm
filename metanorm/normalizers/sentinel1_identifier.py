"""Normalizer for the interpretation of file name convention"""

import logging
import re

import dateutil.parser
import pythesint as pti
import metanorm.utils as utils
from dateutil.tz import tzutc
from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class SentinelOneIdentifierMetadataNormalizer(BaseMetadataNormalizer):
    """ Normalizer for extraction of information from the filename """
    metadata_name = 'Identifier'
    MATCHER = re.compile('_'.join([
        r'^(?P<platform>S1[AB])',
        r'(?P<mode>[A-Z]{2}|_{2})',
        r'(?P<type>[A-Z]{3}|_{3})(?P<resolution>[A-Z_])',
        r'(?P<processing_level>[12_])(?P<class>[SA_])(?P<polarization>[A-Z]{2}|_{2})',
        r'(?P<time_coverage_start>\d{8}T\d{6}|_{15})',
        r'(?P<time_coverage_end>\d{8}T\d{6}|_{15})',
        r'(?P<orbit>\d{6}|_{6})',
        r'(?P<mission_id>[A-Z0-9]{6}|_{6})',
        r'(?P<product_id>[A-Z0-9]{4}|_{4})',
    ]))


    def get_entry_id(self, raw_attributes):
        """ returns the whole raw attribute as the indentifier """
        if self.match_identifier(raw_attributes):
            return raw_attributes['Identifier']

    def match_identifier(self, raw_attributes):
        """ Find Identifier in raw_attributes and match agains pattern.
              Return all metadata from Identifier or empty dictionary """
        if set([self.metadata_name]).issubset(raw_attributes.keys()):
            match_result = self.MATCHER.match(raw_attributes[self.metadata_name])
            if match_result:
                return match_result.groupdict()
        return {}

    def get_platform(self, raw_attributes):
        """ returns the suitable platform based on the filename """
        platform_map = dict(S1A='SENTINEL-1A', S1B='SENTINEL-1B')
        platform_str = self.match_identifier(raw_attributes).get('platform', None)
        if platform_str is None:
            return None
        return utils.get_gcmd_platform(platform_map[platform_str])

    def get_instrument(self, raw_attributes):
        """ returns the suitable instrument based on the filename """
        if self.match_identifier(raw_attributes):
            return utils.get_gcmd_instrument('SENTINEL-1 C-SAR')

    def get_time_coverage_start(self, raw_attributes):
        """ returns the suitable time_coverage_start based on the filename """
        s_time_str = self.match_identifier(raw_attributes).get('time_coverage_start', None)
        if s_time_str is None:
            return None
        return dateutil.parser.parse(s_time_str).replace(tzinfo=tzutc())

    def get_time_coverage_end(self, raw_attributes):
        """ returns the suitable time_coverage_end based on the filename """
        e_time_str = self.match_identifier(raw_attributes).get('time_coverage_end', None)
        if e_time_str is None:
            return None
        return dateutil.parser.parse(e_time_str).replace(tzinfo=tzutc())

    def get_provider(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        if self.match_identifier(raw_attributes):
            return utils.get_gcmd_provider(['ESA/EO'])

    def get_dataset_parameters(self, raw_attributes):
        """ return list with sigma0 parameter from wkv variable """
        if self.match_identifier(raw_attributes):
            return [utils.get_cf_or_wkv_standard_name('surface_backwards_scattering_coefficient_of_radar_wave')]
        else:
            return []
