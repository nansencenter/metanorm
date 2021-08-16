"""Normalizer for OSISAF metadata"""

import re

import dateutil.parser
import pythesint as pti
from dateutil.tz import tzutc

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer


class OSISAFMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """ Normalizer for the attributes of datasets provided by OSISAF """

    def __init__(self):
        super().__init__()
        self.filename_matcher = re.compile(r"([^/]+)\.nc(\.dods)?$")

    def check(self, raw_metadata):
        #TODO revise the condition
        return raw_metadata.get('institution', '') == 'EUMETSAT OSI SAF'

    @utils.raises(KeyError)
    def get_entry_title(self, raw_metadata):
        return raw_metadata['title']

    @utils.raises((AttributeError, KeyError))
    def get_entry_id(self, raw_metadata):
        return self.filename_matcher.search(raw_metadata['url']).group(1)

    @utils.raises(KeyError)
    def get_summary(self, raw_metadata):
        summary_fields = {}
        summary_fields[utils.SUMMARY_FIELDS['description']] = raw_metadata['abstract']
        return utils.dict_to_string(summary_fields)

    @utils.raises(KeyError)
    def get_time_coverage_start(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['start_date']).replace(tzinfo=tzutc())

    @utils.raises(KeyError)
    def get_time_coverage_end(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['stop_date']).replace(tzinfo=tzutc())

    @utils.raises(KeyError)
    def get_platform(self, raw_metadata):
        """Try to get the platform from the metadata, and if not
        possible return a default value
        """
        return utils.get_gcmd_platform(
            raw_metadata.get('platform_name', 'Earth Observation Satellites'))

    def get_instrument(self, raw_metadata):
        """Try to get the instrument from the metadata, and if not
        possible return a default value
        """
        if 'instrument_type' in raw_metadata.keys():
            return utils.get_gcmd_instrument(raw_metadata['instrument_type'])
        elif 'product_name' in raw_metadata.keys():
            if ('_ice_conc' in raw_metadata['product_name']
                    or '_ice_type' in raw_metadata['product_name']
                    or '_ice_edge' in raw_metadata['product_name']):
                return pti.get_gcmd_instrument('Imaging Spectrometers/Radiometers')
            elif 'amsr2ice_conc' in raw_metadata['product_name']:
                return pti.get_gcmd_instrument('AMSR2')
            elif '_mr_ice_drift' in raw_metadata['product_name']:
                return pti.get_gcmd_instrument('AVHRR')
        return pti.get_gcmd_instrument('Earth Remote Sensing Instruments')

    @utils.raises(KeyError)
    def get_location_geometry(self, raw_metadata):
        # deal with a typo in some of the metadata:
        # northernSmost_latitude instead of northernmost_latitude
        northernmost_latitude = raw_metadata.get('northernmost_latitude')
        if not northernmost_latitude:
            northernmost_latitude = raw_metadata['northernsmost_latitude']

        return utils.wkt_polygon_from_wgs84_limits(
            northernmost_latitude,
            raw_metadata['southernmost_latitude'],
            raw_metadata['easternmost_longitude'],
            raw_metadata['westernmost_longitude']
        )

    @utils.raises(KeyError)
    def get_provider(self, raw_metadata):
        """Get a provider from the metadata if possible,
        otherwise use OSISAF as default
        """
        return utils.get_gcmd_provider([raw_metadata.get('institution', 'EUMETSAT/OSISAF')])
