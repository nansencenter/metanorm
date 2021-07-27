"""Normalizer metadata from netcdf file from aviso"""

import logging
from os.path import basename

import metanorm.utils as utils

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class AVISOaltimetryMetadataNormalizer(BaseMetadataNormalizer):
    """ Normalizer for metadata from local netcdf file from aviso """

    def match_metadata(self, raw_attributes):
        """ Check if the filename exactly correct that fits the normalizer by checking it """
        if 'url' in raw_attributes:
            return basename(raw_attributes['url']) == "dt_arctic_multimission_sea_level_20160701_20190429.nc"


    def get_platform(self, raw_attributes):
        """ return 'OPERATIONAL MODELS' platform """
        if self.match_metadata(raw_attributes):
            return utils.get_gcmd_platform('OBSERVATION BASED ANALYSES')

    def get_instrument(self, raw_attributes):
        """ return 'Computer' instrument """
        if self.match_metadata(raw_attributes):
            return utils.get_gcmd_instrument('Computer')

    def get_entry_id(self, raw_attributes):
        """ return title section of raw attributes """
        if self.match_metadata(raw_attributes):
            return "dt_arctic_multimission_sea_level_20160701_20190429"
