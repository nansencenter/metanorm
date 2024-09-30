"""Normalizer for the metadata of REMSS MW SST datasets"""

import re
from dateutil.relativedelta import relativedelta

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer


class REMSSMWSSTMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset for a REMSS
    passive mivrowaves SST dataset
    """

    def check(self, raw_metadata):
        """Checks that the URL starts with the right prefix"""
        return bool(re.match(
            r'(https|ftp)://(data|ftp).remss.com/SST/daily/mw/',
            raw_metadata.get('url', '')))

    def get_entry_title(self, raw_metadata):
        return 'Sea surface temperature from passive microwave sensors'

    @utils.raises((KeyError, AttributeError))
    def get_entry_id(self, raw_metadata):
        return re.search(utils.NC_H5_FILENAME_MATCHER, raw_metadata['url']).group(1)

    def get_summary(self, raw_metadata):
        return utils.dict_to_string({
            utils.SUMMARY_FIELDS['description']:
            'Sea surface temperature from TMI, AMSR-E, AMSR2, WindSat, GMI',
            utils.SUMMARY_FIELDS['processing_level']: '4'
        })

    time_patterns = (
        (
            re.compile(utils.YEARMONTHDAY_REGEX + r'[0-9]{6}-REMSS-L4_GHRSST-SSTfnd-MW_OI-GLOB-v[0-9.]+-fv[0-9.]+\.nc$'),
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
        return utils.get_gcmd_platform('Satellites')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('Earth Remote Sensing Instruments')

    def get_location_geometry(self, raw_metadata):
        return utils.WORLD_WIDE_COVERAGE_WKT

    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['Remote Sensing Systems'])

    def get_dataset_parameters(self, raw_metadata):
        return utils.create_parameter_list((
            'sea_surface_temperature',
        ))
