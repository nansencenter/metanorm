"""Normalizer for CPOM altimetry"""

from datetime import datetime, timezone

import pythesint as pti

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer


class CPOMAltimetryMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Normalizer for CPOM altimetry file. Everything is hard-coded
    because there is close to no metadata in the file
    """

    def check(self, raw_metadata):
        return raw_metadata.get('url', '').rstrip('/').split('/')[-1] == "CPOM_DOT.nc"

    def get_entry_title(self, raw_metadata):
        return 'CPOM SLA'

    def get_entry_id(self, raw_metadata):
        return "CPOM_DOT"

    def get_time_coverage_start(self, raw_metadata):
        return datetime(2003, 1, 1, tzinfo=timezone.utc)

    def get_time_coverage_end(self, raw_metadata):
        return datetime(2015, 1, 1, tzinfo=timezone.utc)

    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform('Earth Observation Satellites')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('Altimeters')

    @utils.raises(KeyError)
    def get_location_geometry(self, raw_metadata):
        return raw_metadata.get('geometry', '')

    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['UC-LONDON/CPOM'])

    def get_dataset_parameters(self, raw_metadata):
        return utils.create_parameter_list(['sea_surface_height_above_sea_level'])
