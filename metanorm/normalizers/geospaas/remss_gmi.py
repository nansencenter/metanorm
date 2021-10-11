"""Normalizer for the metadata of REMSS GMI datasets"""

import re
from dateutil.relativedelta import relativedelta

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer


class REMSSGMIMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset for a REMSS GMI
    dataset
    """

    def check(self, raw_metadata):
        """Checks that the URL starts with the right prefix"""
        return raw_metadata.get('url', '').startswith('ftp://ftp.remss.com/gmi')

    def get_entry_title(self, raw_metadata):
        return 'Atmosphere parameters from Global Precipitation Measurement Microwave Imager'

    @utils.raises((KeyError, AttributeError))
    def get_entry_id(self, raw_metadata):
        return re.search(r'([^/]+)\.gz$', raw_metadata['url']).group(1)

    def get_summary(self, raw_metadata):
        return utils.dict_to_string({
            utils.SUMMARY_FIELDS['description']:
            'GMI is a dual-polarization, multi-channel, conical-scanning, passive '
            'microwave radiometer with frequent revisit times.',
            utils.SUMMARY_FIELDS['processing_level']: '3'
        })

    time_patterns = (
        (
            re.compile(r'/y\d{4}/m\d{2}/f35_' + utils.YEARMONTHDAY_REGEX + r'v[\d.]+\.gz$'),
            utils.create_datetime,
            lambda time: (time, time + relativedelta(days=1))
        ),
        (
            re.compile(r'/y\d{4}/m\d{2}/f35_' + utils.YEARMONTHDAY_REGEX + r'v[\d.]+_d3d\.gz$'),
            utils.create_datetime,
            lambda time: (time - relativedelta(days=2), time + relativedelta(days=1))
        ),
        (
            re.compile(r'/weeks/f35_' + utils.YEARMONTHDAY_REGEX + r'v[\d.]+\.gz$'),
            utils.create_datetime,
            lambda time: (time - relativedelta(days=6), time + relativedelta(days=1))
        ),
        (
            re.compile(r'/y\d{4}/m\d{2}/f35_' + utils.YEARMONTH_REGEX + r'v[\d.]+\.gz$'),
            utils.create_datetime,
            lambda time: (time, time + relativedelta(months=1))
        ),
    )

    @utils.raises(KeyError)
    def get_time_coverage_start(self, raw_metadata):
        return utils.find_time_coverage(self.time_patterns, raw_metadata['url'])[0]

    @utils.raises(KeyError)
    def get_time_coverage_end(self, raw_metadata):
        return utils.find_time_coverage(self.time_patterns, raw_metadata['url'])[1]

    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform('GPM')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('GMI')

    def get_location_geometry(self, raw_metadata):
        return utils.WORLD_WIDE_COVERAGE_WKT

    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['Remote Sensing Systems'])

    def get_dataset_parameters(self, raw_metadata):
        return utils.create_parameter_list((
            'wind_speed',
            'atmosphere_mass_content_of_water_vapor',
            'atmosphere_mass_content_of_cloud_liquid_water',
            'rainfall_rate'
        ))
