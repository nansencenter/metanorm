"""Normalizer for the interpretation of file name convention"""

import logging
import re

import dateutil.parser

import metanorm.utils as utils

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class SentinelIdentifierMetadataNormalizer(BaseMetadataNormalizer):
    """ Normalizer for extraction of information from the filename """

    def check_format(self, raw_attributes_entry_id):
        """ For more information, please check the format of filename to be correct as declared in
        "https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar/naming-conventions" """
        return re.match('S1\D_\D{2}_\D{4}_\d\D{3}_\d{8}T\d{6}_\d{8}T\d{6}', raw_attributes_entry_id)

    def cut_string(self, raw_attributes_entry_id, part):
        """ Cuts the filename string based on incoming part """
        m = re.match(r'^(?P<platform>S\d[AB])_(?P<mode>[A-Z]{2})_(?P<type>[A-Z]{3})(?P<resolution>[A-Z])_(?P<processing_level>[12])(?P<class>[SA])(?P<polarisationtion>[A-Z]{2})_(?P<time_coverage_start>\d{8}T\d{6})_(?P<time_coverage_end>\d{8}T\d{6})_(?P<orbit>\d{6})_(?P<mission_id>[A-Z0-9]{6})_(?P<product_id>[A-Z0-9]{4})', raw_attributes_entry_id)
        return m.groupdict()[part] # returns the specific part of the filename per each call of this function

    def get_entry_id(self, raw_attributes):
        """ returns the whole raw attribute as the indentifier (or in other words entry_id) """
        if set(['entry_id']).issubset(raw_attributes.keys()):
            match_result = self.check_format(raw_attributes['entry_id'])
            if match_result is not None:
                return raw_attributes['entry_id']
            else:
                return None
        else:
            return None

    def get_platform(self, raw_attributes):
        """ returns the suitable platform based on the filename """
        if set(['entry_id']).issubset(raw_attributes.keys()):
            match_result = self.check_format(raw_attributes['entry_id'])
            if match_result is not None:
                platform_str = self.cut_string(raw_attributes['entry_id'], 'platform').upper()
                platform_map = dict(S1A = 'SENTINEL-1A', S1B = 'SENTINEL-1B')
                return utils.get_gcmd_platform(platform_map[platform_str])
            else:
                return None
        else:
            return None

    def get_instrument(self, raw_attributes):
        """ returns the suitable instrument based on the filename """
        if set(['entry_id']).issubset(raw_attributes.keys()):
            match_result = self.check_format(raw_attributes['entry_id'])
            if match_result is not None:
                instrument_str = self.cut_string(raw_attributes['entry_id'], 'platform')
                if instrument_str.upper()[:2] == 'S1': # This if is only for safety checking
                    return utils.get_gcmd_instrument('C-SAR')
            else:
                return None
        else:
            return None

    def get_time_coverage_start(self, raw_attributes):
        """ returns the suitable time_coverage_start based on the filename """
        if set(['entry_id']).issubset(raw_attributes.keys()):
            match_result = self.check_format(raw_attributes['entry_id'])
            if match_result is not None:
                start_time_str = self.cut_string(
                    raw_attributes['entry_id'], 'time_coverage_start')
                return dateutil.parser.parse(start_time_str)
            else:
                return None
        else:
            return None

    def get_time_coverage_end(self, raw_attributes):
        """ returns the suitable time_coverage_end based on the filename """
        if set(['entry_id']).issubset(raw_attributes.keys()):
            match_result = self.check_format(raw_attributes['entry_id'])
            if match_result is not None:
                end_time_str = self.cut_string(
                    raw_attributes['entry_id'], 'time_coverage_end')
                return dateutil.parser.parse(end_time_str)
            else:
                return None
        else:
            return None

    def get_provider(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        if set(['entry_id']).issubset(raw_attributes.keys()):
            match_result = self.check_format(raw_attributes['entry_id'])
            if match_result is not None:
                provider_str = self.cut_string(raw_attributes['entry_id'], 'platform')
                if provider_str.upper()[:2] == 'S1': # This if is only for safety checking
                    return utils.get_gcmd_provider(['ESA/EO'])
            else:
                return None
        else:
            return None
