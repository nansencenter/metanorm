"""Normalizer for the metadata of ESA CCI datasets"""

import re
from datetime import datetime

from dateutil.tz import tzutc
from dateutil.relativedelta import relativedelta

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer


class MarineHeatWavesMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset for a NOAA marine
    heatwaves dataset
    """

    def check(self, raw_metadata):
        """Checks that the URL starts with the right prefix"""
        return raw_metadata.get('url', '').startswith(
            'https://www.star.nesdis.noaa.gov/pub/socd/mecb/crw/data/marine_heatwave/'
            'v1.0.1/category/nc')

    def get_entry_title(self, raw_metadata):
        return 'NOAA marine heatwaves'

    @utils.raises((KeyError, AttributeError))
    def get_entry_id(self, raw_metadata):
        return utils.NC_H5_FILENAME_MATCHER.search(raw_metadata['url']).group(1)

    def get_summary(self, raw_metadata):
        return ''

    time_patterns = (
        (
            re.compile(r'/noaa-crw_mhw.*' + utils.YEARMONTHDAY_REGEX + r'\.nc$'),
            utils.create_datetime,
            lambda time: (time, time + relativedelta(days=1))
        ),
    )

    @utils.raises(KeyError)
    def get_time_coverage_start(self, raw_metadata):
        return utils.find_time_coverage(self.time_patterns, raw_metadata['url'])[0]

    @utils.raises(KeyError)
    def get_time_coverage_end(self, raw_metadata):
        return utils.find_time_coverage(self.time_patterns, raw_metadata['url'])[1]

    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform('Earth Observation Satellites')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('Imaging Spectrometers/Radiometers')

    def get_location_geometry(self, raw_metadata):
        return utils.WORLD_WIDE_COVERAGE_WKT

    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['DOC/NOAA'])

    def get_dataset_parameters(self, raw_metadata):
        return []
