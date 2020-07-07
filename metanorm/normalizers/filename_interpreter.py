"""Normalizer for the interpretation of file name convention"""

import logging

#import dateutil
import dateutil.parser as ps

import metanorm.utils as utils

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class SentinelIdentifierMetadataNormalizer(BaseMetadataNormalizer):
    """ Normalizer for extraction of information from the filename """

    def format_checker(self, raw_attributes):
        """ For more information, please check the format of filename to be correct as declared in
        "https://sentinel.esa.int/web/sentinel/user-guides/sentinel-1-sar/naming-conventions" """
        for i in [3, 6, 11, 16, 32, 48]:
            assert raw_attributes['entry_id'][i] == '_'

    def string_cutter(self, raw_attributes, part):
        """ Cuts the filename string based on incoming part """
        if part == 'platform':
            return raw_attributes['entry_id'][0:3]
        elif (part == 'instrument' or part == 'provider'):
            return raw_attributes['entry_id'][0:2]
        elif part == 'time_coverage_start':
            return raw_attributes['entry_id'][17:32]
        elif part == 'time_coverage_end':
            return raw_attributes['entry_id'][33:48]

    def get_entry_id(self, raw_attributes):
        """ returns the whole raw attribute as the indentifier (or in other words entry_id) """
        if set(['entry_id']).issubset(raw_attributes.keys()):
            self.format_checker(raw_attributes)
            return raw_attributes['entry_id']
        else:
            return None

    def get_platform(self, raw_attributes):
        """ returns the suitable platform based on the filename """
        if set(['entry_id']).issubset(raw_attributes.keys()):
            self.format_checker(raw_attributes)
            platform_str = self.string_cutter(raw_attributes, 'platform')
            if platform_str.upper() == 'S1A':
                return utils.get_gcmd_platform('SENTINEL-1A')  # 'SENTINEL-1A'
            elif platform_str.upper() == 'S1B':
                return utils.get_gcmd_platform('SENTINEL-1B')  # 'SENTINEL-1B'
        else:
            return None

    def get_instrument(self, raw_attributes):
        """ returns the suitable instrument based on the filename """
        if set(['entry_id']).issubset(raw_attributes.keys()):
            self.format_checker(raw_attributes)
            instrument_str = self.string_cutter(raw_attributes, 'instrument')
            if instrument_str.upper() == 'S1':
                return utils.get_gcmd_instrument('C-SAR')
        else:
            return None

    def get_time_coverage_start(self, raw_attributes):
        """ returns the suitable time_coverage_start based on the filename """
        if set(['entry_id']).issubset(raw_attributes.keys()):
            self.format_checker(raw_attributes)
            start_time_str = self.string_cutter(
                raw_attributes, 'time_coverage_start')
            return ps.parse(start_time_str)
        else:
            return None

    def get_time_coverage_end(self, raw_attributes):
        """ returns the suitable time_coverage_end based on the filename """
        if set(['entry_id']).issubset(raw_attributes.keys()):
            self.format_checker(raw_attributes)
            end_time_str = self.string_cutter(
                raw_attributes, 'time_coverage_end')
            return ps.parse(end_time_str)
        else:
            return None

    def get_provider(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        if set(['entry_id']).issubset(raw_attributes.keys()):
            self.format_checker(raw_attributes)
            provider_str = self.string_cutter(raw_attributes, 'provider')
            if provider_str.upper() == 'S1':
                return utils.get_gcmd_like_provider('ESA')  # 'ESA'
        else:
            return None
