"""Normalizer for non-conventional but widely used attributes"""

import metanorm.utils as utils
from metanorm.errors import MetadataNormalizationError

from .base import BaseMetadataNormalizer


class GeoSpatialWellKnownMetadataNormalizer(BaseMetadataNormalizer):
    """Takes care of well-known attributes, which are non-standard but widely used"""

    def get_location_geometry(self, raw_attributes):
        """Returns a GEOSGeometry object corresponding to the location of the dataset"""
        if set(['northernmost_latitude', 'southernmost_latitude',
                'easternmost_longitude', 'westernmost_longitude']).issubset(raw_attributes.keys()):

            polygon = utils.wkt_polygon_from_wgs84_limits(
                raw_attributes['northernmost_latitude'],
                raw_attributes['southernmost_latitude'],
                raw_attributes['easternmost_longitude'],
                raw_attributes['westernmost_longitude']
            )

            return utils.geometry_from_wkt_string(polygon)
        else:
            raise MetadataNormalizationError(
                "Unable to find a value for the 'geographic_location' parameter")

    def get_instrument(self, raw_attributes):
        """Sometimes the instrument is defined as 'sensor'"""
        if set(['sensor']).issubset(raw_attributes.keys()):
            return utils.get_gcmd_instrument(raw_attributes['sensor'])
        else:
            raise MetadataNormalizationError(
                "Unable to find a value for the 'instrument' parameter")
