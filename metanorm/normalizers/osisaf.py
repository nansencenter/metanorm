import logging

import dateutil.parser
import pythesint as pti
from dateutil.tz import tzutc

import metanorm.utils as utils

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class OSISAFMetadataNormalizer(BaseMetadataNormalizer):
    """ Test class for osisaf normalizer """
    def get_instrument(self, raw_attributes):
        """ returns the suitable instrument based on the 'instrument_type' attribute (priortized one)
        and 'activity_type' attribute """
        if set(['instrument_type']).issubset(raw_attributes.keys()):
            return utils.get_gcmd_instrument(raw_attributes['instrument_type'])
        elif set(['product_name']).issubset(raw_attributes.keys()):
            if raw_attributes['product_name'][:7] == 'osi_saf':
                return utils.UNKNOWN # make it unknown only for osisaf products only
        else:
            return None

    def get_platform(self, raw_attributes):
        """ returns the suitable instrument based on the 'platform_name' attribute (priortized one)
        and 'activity_type' attribute """
        if set(['platform_name']).issubset(raw_attributes.keys()):
            return utils.get_gcmd_platform(raw_attributes['platform_name'])
        elif set(['product_name']).issubset(raw_attributes.keys()):
            if raw_attributes['product_name'][:7] == 'osi_saf':
                return utils.UNKNOWN # make it unknown only for osisaf products only
        else:
            return None

    def get_time_coverage_start(self, raw_attributes):
        """ returns the suitable instrument based on the 'start_date' attribute """
        if set(['start_date']).issubset(raw_attributes.keys()):
            return dateutil.parser.parse(raw_attributes['start_date']).replace(tzinfo=tzutc())
        else:
            return None

    def get_time_coverage_end(self, raw_attributes):
        """ returns the suitable instrument based on the 'stop_date' attribute """
        if set(['stop_date']).issubset(raw_attributes.keys()):
            return dateutil.parser.parse(raw_attributes['stop_date']).replace(tzinfo=tzutc())
        else:
            return None

    def get_summary(self, raw_attributes):
        """ returns the suitable instrument based on the 'abstract' attribute """
        if set(['abstract']).issubset(raw_attributes.keys()):
            return raw_attributes['abstract']
        else:
            return None

    def get_dataset_parameters(self, raw_attributes):
        """ returns the suitable instrument based on the lasting letters of 'product_name' attribute """
        if set(['product_name']).issubset(raw_attributes.keys()):
            if raw_attributes['product_name'][-4:] == 'conc':
                return [pti.get_wkv_variable('sea_ice_area_fraction'), ]
            elif raw_attributes['product_name'][-5:] == 'drift':
                return [pti.get_cf_standard_name('sea_ice_x_displacement'),
                        pti.get_cf_standard_name('sea_ice_y_displacement'), ]
            elif raw_attributes['product_name'][-4:] == 'type':
                return [pti.get_cf_standard_name('sea_ice_classification'), ]

        else:
            return None

    def get_provider(self, raw_attributes):
        """Returns a GCMD-like provider from data structure"""
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

            polygon = utils.wkt_polygon_from_wgs84_limits(
                # notice the difference between "northernSmost_latitude" and "northernmost_latitude" of default normalizer
                raw_attributes['northernsmost_latitude'],
                raw_attributes['southernmost_latitude'],
                raw_attributes['easternmost_longitude'],
                raw_attributes['westernmost_longitude']
            )
            return utils.geometry_from_wkt_string(polygon)

        else:
            return None
