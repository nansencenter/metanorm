"""Normalizer for the metadata of GPortal GCOM-W datasets"""

import re
from dateutil.relativedelta import relativedelta

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer


class GPortalGCOMAMSR2L3MetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset for a GCOM-W AMSR2
    L3 dataset
    """

    def check(self, raw_metadata):
        """Checks that the URL starts with the right prefix"""
        return raw_metadata.get('url', '').startswith(
            'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST')

    def get_entry_title(self, raw_metadata):
        return 'AMSR2-L3 Sea Surface Temperature'

    @utils.raises((AttributeError, KeyError))
    def get_entry_id(self, raw_metadata):
        return utils.NC_H5_FILENAME_MATCHER.search(raw_metadata['url']).group(1)

    def get_summary(self, raw_metadata):
        return utils.dict_to_string({
            utils.SUMMARY_FIELDS['description']: 'GCOM-W AMSR2 data',
            utils.SUMMARY_FIELDS['processing_level']: '3'
        })

    time_patterns = (
        (
            re.compile(r'/[A-Z\d]+_' + utils.YEARMONTHDAY_REGEX + r'_\d{2}D.*\.h5$'),
            utils.create_datetime,
            lambda time: (time, time + relativedelta(days=1))
        ),
        (
            re.compile(r'/[A-Z\d]+_' + utils.YEARMONTH_REGEX + r'00_\d{2}M.*\.h5$'),
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
        return utils.get_gcmd_platform('GCOM-W1')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('AMSR2')

    def get_location_geometry(self, raw_metadata):
        return utils.WORLD_WIDE_COVERAGE_WKT

    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['JP/JAXA/EOC'])

    def get_dataset_parameters(self, raw_metadata):
        return utils.create_parameter_list(('sea_surface_temperature',))
