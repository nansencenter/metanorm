"""Normalizer for the metadata of ESA CCI datasets"""

import re
from datetime import datetime
from dateutil.tz import tzutc

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer


class CEDAESACCIMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset for an ESA CCI
    climatology dataset hosted by CEDA
    """

    def check(self, raw_metadata):
        """Checks that the URL starts with the right prefix"""
        return re.match(
            r'^ftp://(anon-)?ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/.*',
            raw_metadata.get('url', ''))

    def get_entry_title(self, raw_metadata):
        return 'ESA SST CCI OSTIA L4 Climatology'

    @utils.raises((KeyError, AttributeError))
    def get_entry_id(self, raw_metadata):
        return utils.NC_H5_FILENAME_MATCHER.search(raw_metadata['url']).group(1)

    def get_summary(self, raw_metadata):
        return utils.dict_to_string({
            utils.SUMMARY_FIELDS['description']: (
                'This v2.1 SST_cci Climatology Data Record (CDR) consists of Level 4 daily'
                ' climatology files gridded on a 0.05 degree grid.'
            ),
            utils.SUMMARY_FIELDS['processing_level']: '4',
            utils.SUMMARY_FIELDS['product']: 'ESA SST CCI Climatology'
        })

    time_patterns = (
        (   # model data over a year, based on observations from 1982 to 2010
            re.compile(r'/D(?P<d>\d{3})-.*\.nc$'),
            lambda d: utils.create_datetime(1982, day_of_year=d),
            lambda time: (time, datetime(2010, time.month, time.day).replace(tzinfo=tzutc()))
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
        return utils.get_gcmd_provider(['ESA/CCI'])

    def get_dataset_parameters(self, raw_metadata):
        return utils.create_parameter_list(('sea_surface_temperature',))
