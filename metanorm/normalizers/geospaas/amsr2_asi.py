"""Normalizer for ASI-AMSR2 sea ice concentration datasets from Uni
Bremen
"""

import re
from datetime import timedelta, timezone

import dateutil.parser
import pythesint as pti
from dateutil.relativedelta import relativedelta

import metanorm.utils as utils

from .base import GeoSPaaSMetadataNormalizer
from ...errors import MetadataNormalizationError


class AMSR2ASIMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of an ASI-AMSR2 GeoSPaaS Dataset"""

    time_patterns = (
        (
            re.compile(r'/asi-AMSR2-n6250-' + utils.YEARMONTHDAY_REGEX + r'-.*\.nc$'),
            utils.create_datetime,
            lambda time: (time, time + relativedelta(days=1))
        ),
    )

    def check(self, raw_metadata):
        """Check that the dataset's id matches an ASI-AMSR2 file"""
        try:
            entry_id = self.get_entry_id(raw_metadata)
        except MetadataNormalizationError:
            return False
        return bool(entry_id) # return True if the entry_id is not empty

    def get_entry_title(self, raw_metadata):
        return 'ASI sea ice concentration from AMSR2'

    @utils.raises((AttributeError, KeyError))
    def get_entry_id(self, raw_metadata):
        return re.match(
            r'^.*/(asi-AMSR2-[ns]6250-[0-9]{8}-v[0-9.]+)\.nc$',
            raw_metadata['url']
        ).group(1)

    def get_summary(self, raw_metadata):
        """Get the dataset's summary if it is available in the
        metadata, otherwise use a default
        """
        return utils.dict_to_string({
            utils.SUMMARY_FIELDS['description']: (
                'Sea ice concentration retrieved with the ARTIST Sea Ice (ASI) algorithm (Spreen et'
                ' al., 2008) which is applied to microwave radiometer data of the sensor AMSR2 '
                '(Advanced Microwave Scanning Radiometer 2) on the JAXA satellite GCOM-W1.'),
            utils.SUMMARY_FIELDS['processing_level']: '3',
        })

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

    @utils.raises((AttributeError, KeyError))
    def get_location_geometry(self, raw_metadata):
        hemisphere = re.match(
            r'^.*/asi-AMSR2-([ns])6250-[0-9]{8}-v[0-9.]+\.nc$',
            raw_metadata['url']
        ).group(1)
        if hemisphere == 'n':
            location = utils.wkt_polygon_from_wgs84_limits('90', '40', '180', '-180')
        elif hemisphere == 's':
            location = utils.wkt_polygon_from_wgs84_limits('-90', '-40', '180', '-180')
        return location

    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['U-BREMEN/IUP'])
