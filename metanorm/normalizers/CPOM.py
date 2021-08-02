"""Normalizer metadat from netcdf file from CPOM"""

import logging
from datetime import datetime, timezone
from os.path import basename

import metanorm.utils as utils
import pythesint as pti

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class CPOMaltimetryMetadataNormalizer(BaseMetadataNormalizer):
    """ Normalizer for metadata from local netcdf file from CPOM """

    def match_metadata(self, raw_attributes):
        """ Check if the filename exactly correct that fits the normalizer by checking it """
        if 'url' in raw_attributes:
            return basename(raw_attributes['url']) == "CPOM_DOT.nc"

    def get_platform(self, raw_attributes):
        """ return 'Earth Observation Satellites' platform """
        if self.match_metadata(raw_attributes):
            return utils.get_gcmd_platform('OPERATIONAL MODELS')

    def get_instrument(self, raw_attributes):
        """ return 'Computer' instrument """
        if self.match_metadata(raw_attributes):
            return utils.get_gcmd_instrument('Computer')

    def get_entry_id(self, raw_attributes):
        """ return a string """
        if self.match_metadata(raw_attributes):
            return "CPOM_DOT"

    def get_entry_title(self, raw_attributes):
        """ return a string """
        if self.match_metadata(raw_attributes):
            return 'CPOM SLA'

    def get_time_coverage_start(self, raw_attributes):
        """ return start date from Date """
        if self.match_metadata(raw_attributes):
            return datetime(2003, 1, 1, tzinfo=timezone.utc)

    def get_time_coverage_end(self, raw_attributes):
        """ return end date from Date """
        if self.match_metadata(raw_attributes):
            return datetime(2015, 1, 1, tzinfo=timezone.utc)

    def get_provider(self, raw_attributes):
        """ return CPOM provider """
        if self.match_metadata(raw_attributes):
            return pti.get_gcmd_provider('UC-LONDON/CPOM')

    def get_dataset_parameters(self, raw_attributes):
        """ return "sea surface height above sea level" parameter from wkv variable """
        if self.match_metadata(raw_attributes):
            return [pti.get_wkv_variable('sea_surface_height_above_sea_level')]
        else:
            return []
