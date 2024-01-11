"""Normalizer for NextSIM datasets"""

import re
from datetime import timedelta, timezone

import dateutil.parser
import pythesint as pti

import metanorm.utils as utils

from .base import GeoSPaaSMetadataNormalizer
from ...errors import MetadataNormalizationError


class NextsimMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a NextSIM GeoSPaaS Dataset
    """

    def check(self, raw_metadata):
        """Check that the dataset's id matches a NextSIM file"""
        try:
            entry_id = self.get_entry_id(raw_metadata)
        except MetadataNormalizationError:
            return False
        return bool(entry_id) # return True if the entry_id is not empty

    @utils.raises(KeyError)
    def get_entry_title(self, raw_metadata):
        return raw_metadata['title']

    @utils.raises((AttributeError, KeyError))
    def get_entry_id(self, raw_metadata):
        return re.match(
            r'^.*/(\d{8}_hr-nersc-MODEL-nextsimf-ARC-b\d{8}-fv\d{2}.\d).nc$',
            raw_metadata['url']
        ).group(1)

    def get_summary(self, raw_metadata):
        """Get the dataset's summary if it is available in the
        metadata, otherwise use a default
        """
        return utils.dict_to_string({
            utils.SUMMARY_FIELDS['description']: (
                'The Arctic Sea Ice Analysis and Forecast system uses the neXtSIM stand-alone sea '
                'ice model running the Brittle-Bingham-Maxwell sea ice rheology on an adaptive '
                'triangular mesh of 10 km average cell length.'),
            utils.SUMMARY_FIELDS['processing_level']: '4',
            utils.SUMMARY_FIELDS['product']: 'ARCTIC_ANALYSISFORECAST_PHY_ICE_002_011'
        })

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_start(self, raw_metadata):
        date = dateutil.parser.parse(raw_metadata['field_date'])
        if not date.tzinfo:
            date = date.replace(tzinfo=timezone.utc)
        return date

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_end(self, raw_metadata):
        return self.get_time_coverage_start(raw_metadata) + timedelta(days=1)

    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform('OPERATIONAL MODELS')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('Computer')

    def get_location_geometry(self, raw_metadata):
        return utils.wkt_polygon_from_wgs84_limits('90', '62', '180', '-180')

    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['NERSC'])
