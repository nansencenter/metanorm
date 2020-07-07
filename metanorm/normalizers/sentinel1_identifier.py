"""Normalizer for the interpretation of file name convention"""

import logging
import re

import dateutil.parser

import metanorm.utils as utils

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class SentinelOneIdentifierMetadataNormalizer(BaseMetadataNormalizer):
    """ Normalizer for extraction of information from the filename """
    MATCHER = re.compile('_'.join([
        r'^(?P<platform>S1[AB])',
        r'(?P<mode>[A-Z]{2})',
        r'(?P<type>[A-Z]{3})(?P<resolution>[A-Z])',
        r'(?P<processing_level>[12])(?P<class>[SA])(?P<polarization>[A-Z]{2})',
        r'(?P<time_coverage_start>\d{8}T\d{6})',
        r'(?P<time_coverage_end>\d{8}T\d{6})',
        r'(?P<orbit>\d{6})',
        r'(?P<mission_id>[A-Z0-9]{6})',
        r'(?P<product_id>[A-Z0-9]{4})',
    ]))

    def check_format(self, raw_attributes_entry_id):
        """ For more information, please check the format of filename to be correct as declared in
        "https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar/naming-conventions" """
        return self.MATCHER.match(raw_attributes_entry_id)

    def cut_string(self, raw_attributes_entry_id, part):
        """ Cuts the filename string based on incoming part """
        return self.MATCHER.match(raw_attributes_entry_id).groupdict()[part]

    def get_entry_id(self, raw_attributes):
        """ returns the whole raw attribute as the identifier """
        instrument_str = self.create_attr_string('platform', raw_attributes)
        if instrument_str is None:
            return None
        return raw_attributes['Identifier']

    def create_attr_string(self, attr_str, raw_attributes):
        """in the case of existance of 'metadata_name' in row data, it will check the format of it
        and cut the desired part of the string from the raw attribute of 'metadata_name' """
        metadata_name = 'Identifier'
        if not set([metadata_name]).issubset(raw_attributes.keys()):
            return None
        match_result = self.check_format(raw_attributes[metadata_name])
        if match_result is None:
            return None
        return self.cut_string(raw_attributes[metadata_name], attr_str).upper()

    def get_platform(self, raw_attributes):
        """ returns the suitable platform based on the filename """
        platform_map = dict(S1A='SENTINEL-1A', S1B='SENTINEL-1B')
        platform_str = self.create_attr_string('platform', raw_attributes)
        if platform_str is None:
            return None
        return utils.get_gcmd_platform(platform_map[platform_str])

    def get_instrument(self, raw_attributes):
        """ returns the suitable instrument based on the filename """
        instrument_str = self.create_attr_string('platform', raw_attributes)
        if instrument_str is None:
            return None
        # This if is only for safety checking
        if instrument_str.upper()[:2] == 'S1':
            return utils.get_gcmd_instrument('C-SAR')

    def get_time_coverage_start(self, raw_attributes):
        """ returns the suitable time_coverage_start based on the filename """
        s_time_str = self.create_attr_string(
            'time_coverage_start', raw_attributes)
        if s_time_str is None:
            return None
        return dateutil.parser.parse(s_time_str)

    def get_time_coverage_end(self, raw_attributes):
        """ returns the suitable time_coverage_end based on the filename """
        e_time_str = self.create_attr_string(
            'time_coverage_end', raw_attributes)
        if e_time_str is None:
            return None
        return dateutil.parser.parse(e_time_str)

    def get_provider(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        instrument_str = self.create_attr_string('platform', raw_attributes)
        if instrument_str is None:
            return None
        # This if is only for safety checking
        if instrument_str.upper()[:2] == 'S1':
            return utils.get_gcmd_provider(['ESA/EO'])
