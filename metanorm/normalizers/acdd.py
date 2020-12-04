"""Normalizer for the ACDD convention"""

import logging

import dateutil
import dateutil.parser

import metanorm.utils as utils

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class ACDDMetadataNormalizer(BaseMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset using ACDD attributes"""

    def get_entry_title(self, raw_attributes):
        """Get the dataset's title"""
        if set(['title']).issubset(raw_attributes.keys()):
            return raw_attributes['title']
        else:
            return None

    def get_summary(self, raw_attributes):
        """Get the dataset's summary"""
        summary_fields = {}

        if 'summary' in raw_attributes.keys():
            summary_fields[utils.SUMMARY_FIELDS['description']] = raw_attributes['summary']

            if 'processing_level' in raw_attributes.keys():
                processing_level = raw_attributes['processing_level'].lstrip('Ll')
                summary_fields[utils.SUMMARY_FIELDS['processing_level']] = processing_level

            return utils.dict_to_string(summary_fields)
        else:
            return None

    def get_time_coverage_start(self, raw_attributes):
        """Get the start of time coverage from the attributes"""
        if set(['time_coverage_start']).issubset(raw_attributes.keys()):
            return dateutil.parser.parse(raw_attributes['time_coverage_start'])
        else:
            return None

    def get_time_coverage_end(self, raw_attributes):
        """Get the end of time coverage from the attributes"""
        if set(['time_coverage_end']).issubset(raw_attributes.keys()):
            return dateutil.parser.parse(raw_attributes['time_coverage_end'])
        else:
            return None

    def get_platform(self, raw_attributes):
        """Get the platform from the attributes"""
        if set(['platform']).issubset(raw_attributes.keys()):
            return utils.get_gcmd_platform(raw_attributes['platform'])
        else:
            return None

    def get_instrument(self, raw_attributes):
        """Get the instrument from the attributes'"""
        if set(['instrument']).issubset(raw_attributes.keys()):
            return utils.get_gcmd_instrument(raw_attributes['instrument'])
        else:
            return None

    def get_location_geometry(self, raw_attributes):
        """Returns a WKT string corresponding to the location of the dataset"""

        if set(['geospatial_lat_max', 'geospatial_lat_min',
                'geospatial_lon_max', 'geospatial_lon_min']).issubset(raw_attributes.keys()):

            polygon = utils.wkt_polygon_from_wgs84_limits(
                raw_attributes['geospatial_lat_max'],
                raw_attributes['geospatial_lat_min'],
                raw_attributes['geospatial_lon_max'],
                raw_attributes['geospatial_lon_min']
            )
            return polygon
        elif set(['geospatial_bounds']).issubset(raw_attributes.keys()):
            srid = ''
            if 'geospatial_bounds_crs' in raw_attributes:
                srid = raw_attributes['geospatial_bounds_crs'].split(':')[1]
                srid = f'SRID={srid};'
            return srid + raw_attributes['geospatial_bounds']
        else:
            return None

    def get_provider(self, raw_attributes):
        """Returns a GCMD-like provider data structure"""
        name_values = [
            raw_attributes[attr] for attr in (
                'publisher_name', 'creator_name', 'project', 'institution')
            if attr in raw_attributes.keys()
        ]

        url_values = [
            raw_attributes[attr] for attr in ('publisher_url', 'creator_url')
            if attr in raw_attributes.keys()
        ]

        if name_values or url_values:
            # Try to find a GCMD value using all possible attributes
            provider = utils.get_gcmd_provider(name_values + url_values)

            # No provider was found, we generate one from the available information
            if not provider:
                name = name_values[0] if name_values else None
                url = url_values[0] if url_values else None
                provider = utils.get_gcmd_like_provider(name, url)
        else:
            provider = None

        return provider
