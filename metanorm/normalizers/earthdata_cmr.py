"""Normalizer for the metadata used in the Earthdata CMR search API"""

import logging
import re

import dateutil
import dateutil.parser

import metanorm.utils as utils

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class EarthdataCMRMetadataNormalizer(BaseMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset using Earthdata CMR attributes"""

    warning_message = 'The metadata does not have the expected structure'

    def get_entry_id(self, raw_attributes):
        """Get the dataset's entry ID"""
        # The idea here is to test that we are dealing with data from
        # Earthdata CMR (`if umm:`), then assume that this data has a
        # known structure (try block).
        # Testing the presence of the umm attribute is better done with
        # an explicit test than a try block, because this test will be
        # negative a lot of the time. But once we know that we are in
        # the case of Earthdata CMR metadata, using the try block is
        # more efficient because the data not having the expected
        # structure will be an exceptional event.
        # The same reasoning goes for the other `get_...` methods.
        umm = raw_attributes.get('umm')
        if umm:
            try:
                return umm['DataGranule']['Identifiers'][0]['Identifier'].rstrip('.nc')
            except (KeyError, IndexError):
                LOGGER.warning(self.warning_message, exc_info=True)
        return None

    def get_entry_title(self, raw_attributes):
        """Get the dataset's title"""
        return self.get_entry_id(raw_attributes)

    def get_summary(self, raw_attributes):
        """Get the dataset's summary"""
        umm = raw_attributes.get('umm')
        if umm:
            summary_fields = {}
            try:
                description = ''
                for platform in umm['Platforms']:
                    description += (
                        f"Platform={platform['ShortName']}, " +
                        ', '.join(f"Instrument={i['ShortName']}" for i in platform['Instruments']))

                description += (
                    f", Start date={umm['TemporalExtent']['RangeDateTime']['BeginningDateTime']}")
                summary_fields[utils.SUMMARY_FIELDS['description']] = description

                processing_level = re.match(
                    r'^.*_(L\d[^_]*)_.*$',
                    umm['CollectionReference']['ShortName']).group(1)
                summary_fields[utils.SUMMARY_FIELDS['processing_level']] = processing_level

                return utils.dict_to_string(summary_fields)
            except (KeyError, IndexError):
                LOGGER.warning(self.warning_message, exc_info=True)
        return None

    def get_time_coverage_start(self, raw_attributes):
        """Get the start of time coverage from the attributes"""
        umm = raw_attributes.get('umm')
        if umm:
            try:
                return dateutil.parser.parse(
                    umm['TemporalExtent']['RangeDateTime']['BeginningDateTime'])
            except (KeyError, IndexError):
                LOGGER.warning(self.warning_message, exc_info=True)
        return None

    def get_time_coverage_end(self, raw_attributes):
        """Get the end of time coverage from the attributes"""
        umm = raw_attributes.get('umm')
        if umm:
            try:
                return dateutil.parser.parse(
                    umm['TemporalExtent']['RangeDateTime']['EndingDateTime'])
            except (KeyError, IndexError):
                LOGGER.warning(self.warning_message, exc_info=True)
        return None

    def get_platform(self, raw_attributes):
        """Get the platform from the attributes"""
        umm = raw_attributes.get('umm')
        if umm:
            try:
                return utils.get_gcmd_platform(umm['Platforms'][0]['ShortName'])
            except (KeyError, IndexError):
                LOGGER.warning(self.warning_message, exc_info=True)
        return None

    def get_instrument(self, raw_attributes):
        """Get the instrument from the attributes'"""
        umm = raw_attributes.get('umm')
        if umm:
            try:
                return utils.get_gcmd_instrument(umm['Platforms'][0]['Instruments'][0]['ShortName'])
            except (KeyError, IndexError):
                LOGGER.warning(self.warning_message, exc_info=True)
        return None

    def get_location_geometry(self, raw_attributes):
        """Returns a GeoJSON string corresponding to the location of the dataset"""
        umm = raw_attributes.get('umm')
        if umm:
            try:
                bounds = (umm['SpatialExtent']
                             ['HorizontalSpatialDomain']
                             ['Geometry']
                             ['BoundingRectangles']
                             [0])
                return utils.wkt_polygon_from_wgs84_limits(
                    bounds['NorthBoundingCoordinate'],
                    bounds['SouthBoundingCoordinate'],
                    bounds['EastBoundingCoordinate'],
                    bounds['WestBoundingCoordinate']
                )
            except (IndexError, KeyError):
                LOGGER.warning(self.warning_message, exc_info=True)
        return None

    def get_provider(self, raw_attributes):
        """Returns a GCMD-like provider data structure"""
        meta = raw_attributes.get('meta')
        if meta:
            try:
                return utils.get_gcmd_provider([meta['provider-id']])
            except (IndexError, KeyError):
                LOGGER.warning(self.warning_message, exc_info=True)
        return None
