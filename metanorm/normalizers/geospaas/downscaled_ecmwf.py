"""Normalizer for the downscaled ECMWF seasonal forecasts"""

import re
from datetime import datetime, timezone

import dateutil.parser
from dateutil.relativedelta import relativedelta

import metanorm.utils as utils

from .base import GeoSPaaSMetadataNormalizer
from ...errors import MetadataNormalizationError


class DownscaledECMWFMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset from a downscaled
    ECMWF seasonal forecast netcdf file
    """

    def check(self, raw_metadata):
        """Check that the dataset's id matches the pattern"""
        try:
            entry_id = self.get_entry_id(raw_metadata)
        except MetadataNormalizationError:
            return False
        return bool(entry_id) # return True if the entry_id is not empty

    def get_entry_title(self, raw_metadata):
        return 'Downscaled ECMWF seasonal forecast'

    @utils.raises((AttributeError, KeyError))
    def get_entry_id(self, raw_metadata):
        return re.match(
            r'^.*[/\\](Seasonal_[a-zA-Z]{3}[0-9]{2}_[a-zA-Z]+_n[0-9]+).nc$',
            raw_metadata['url']
        ).group(1)

    def get_summary(self, raw_metadata):
        """Get the dataset's summary if it is available in the
        metadata, otherwise use a default
        """
        return "Downscaled version of ECMWF's seasonal forecasts"

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_start(self, raw_metadata):
        creation_date = dateutil.parser.parse(raw_metadata['date'])
        return datetime(creation_date.year, creation_date.month, 1,
                        tzinfo=creation_date.tzinfo or timezone.utc)

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_end(self, raw_metadata):
        return self.get_time_coverage_start(raw_metadata) + relativedelta(months=6)

    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform('OPERATIONAL MODELS')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('Computer')

    def get_location_geometry(self, raw_metadata):
        return ''

    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['NERSC'])
