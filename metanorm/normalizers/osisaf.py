"""
Normalizer for OSISAF project
"""
import logging

import dateutil.parser
from dateutil.tz import tzutc
import pythesint as pti

import metanorm.utils as utils

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class OSISAFMetadataNormalizer(BaseMetadataNormalizer):
    """ Normalizer for the attributes of datasets provided by OSISAF """

    def get_instrument(self, raw_attributes):
        """
        Returns the suitable instrument based on the 'instrument_type' attribute (prioritized one)
        and 'activity_type' attribute
        """
        if set(['instrument_type']).issubset(raw_attributes.keys()):
            return utils.get_gcmd_instrument(raw_attributes['instrument_type'])
        elif set(['product_name']).issubset(raw_attributes.keys()):
            if 'osi_saf' in raw_attributes['product_name']:
                if ('_ice_conc' in raw_attributes['product_name']
                    or '_ice_type' in raw_attributes['product_name']
                    or '_ice_edge' in raw_attributes['product_name']):
                    return pti.get_gcmd_instrument('Imaging Spectrometers/Radiometers')
                elif 'amsr2ice_conc' in raw_attributes['product_name']:
                    return pti.get_gcmd_instrument('AMSR2')
                elif '_lr_ice_drift' in raw_attributes['product_name']:
                    return pti.get_gcmd_instrument('Earth Remote Sensing Instruments')
                elif '_mr_ice_drift' in raw_attributes['product_name']:
                    return pti.get_gcmd_instrument('AVHRR')
                return utils.get_gcmd_instrument(utils.UNKNOWN)
        else:
            return None

    def get_platform(self, raw_attributes):
        """ returns the suitable platform based on the 'platform_name' attribute (prioritized one)
        and 'activity_type' attribute """
        if set(['platform_name']).issubset(raw_attributes.keys()):
            return utils.get_gcmd_platform(raw_attributes['platform_name'])
        elif set(['product_name']).issubset(raw_attributes.keys()):
            if 'osi_saf' in raw_attributes['product_name']:
                # name it 'Earth Observation Satellites' for osisaf products only
                return utils.get_gcmd_platform('Earth Observation Satellites')
        else:
            return None

    def get_time_coverage_start(self, raw_attributes):
        """ returns the suitable start time based on the 'start_date' attribute """
        if set(['start_date']).issubset(raw_attributes.keys()):
            return dateutil.parser.parse(raw_attributes['start_date']).replace(tzinfo=tzutc())
        else:
            return None

    def get_time_coverage_end(self, raw_attributes):
        """ returns the suitable end time based on the 'stop_date' attribute """
        if set(['stop_date']).issubset(raw_attributes.keys()):
            return dateutil.parser.parse(raw_attributes['stop_date']).replace(tzinfo=tzutc())
        else:
            return None

    def get_summary(self, raw_attributes):
        """ returns the suitable summary based on the 'abstract' attribute """
        if set(['abstract']).issubset(raw_attributes.keys()):
            return raw_attributes['abstract']
        else:
            return None

    def get_provider(self, raw_attributes):
        """Returns a GCMD-like provider data structure"""
        name_values = [
            raw_attributes[attr] for attr in (
                'institution', 'project_name', 'PI_name', 'project', )
            if attr in raw_attributes.keys()
        ]
        if name_values:
            # Try to find a GCMD value using all possible attributes
            provider = utils.get_gcmd_provider(name_values)
            # No provider was found, we generate one from the available information
            if not provider:
                name = name_values[0] if name_values else None
                provider = utils.get_gcmd_like_provider(name,)
        else:
            provider = None
        return provider

    def get_location_geometry(self, raw_attributes):
        """Returns a GEOSGeometry object corresponding to the location of the dataset"""
        if set(['northernsmost_latitude', 'southernmost_latitude',
                'easternmost_longitude', 'westernmost_longitude']).issubset(raw_attributes.keys()):
            return utils.wkt_polygon_from_wgs84_limits(
                # notice the difference between "northernSmost_latitude"
                #                           and "northernmost_latitude" of default normalizer
                raw_attributes['northernsmost_latitude'],
                raw_attributes['southernmost_latitude'],
                raw_attributes['easternmost_longitude'],
                raw_attributes['westernmost_longitude']
            )
        else:
            return None
