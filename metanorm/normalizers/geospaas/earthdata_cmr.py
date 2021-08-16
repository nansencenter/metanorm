"""Normalizer for the metadata used in the Earthdata CMR search API"""

import re

import dateutil
import dateutil.parser

import metanorm.utils as utils

from .base import GeoSPaaSMetadataNormalizer
from ...errors import MetadataNormalizationError


class EarthdataCMRMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset using
    Earthdata CMR attributes
    """

    def check(self, raw_metadata):
        return set(('umm', 'meta')).issubset(raw_metadata.keys())

    def get_entry_title(self, raw_metadata):
        return self.get_entry_id(raw_metadata)

    @utils.raises((KeyError, IndexError))
    def get_entry_id(self, raw_metadata):
        return raw_metadata['umm']['DataGranule']['Identifiers'][0]['Identifier'].rstrip('.nc')

    @utils.raises((KeyError, IndexError))
    def get_summary(self, raw_metadata):
        summary_fields = {}
        description = ''
        umm = raw_metadata['umm']

        for platform in umm['Platforms']:
            description += (
                f"Platform={platform['ShortName']}, " +
                ', '.join(f"Instrument={i['ShortName']}" for i in platform['Instruments']))

        description += (
            f", Start date={umm['TemporalExtent']['RangeDateTime']['BeginningDateTime']}")
        summary_fields[utils.SUMMARY_FIELDS['description']] = description

        processing_level = re.match(
            r'^.*_L(\d[^_]*)_.*$',
            umm['CollectionReference']['ShortName']).group(1)
        summary_fields[utils.SUMMARY_FIELDS['processing_level']] = processing_level

        return utils.dict_to_string(summary_fields)

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_start(self, raw_metadata):
        return dateutil.parser.parse(
            raw_metadata['umm']['TemporalExtent']['RangeDateTime']['BeginningDateTime'])

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_end(self, raw_metadata):
        return dateutil.parser.parse(
            raw_metadata['umm']['TemporalExtent']['RangeDateTime']['EndingDateTime'])

    @utils.raises((KeyError, IndexError))
    def get_platform(self, raw_metadata):
        """Only get the first platform from the raw metadata, because
        GeoSPaaS does not support more than one platform per dataset
        """
        return utils.get_gcmd_platform(raw_metadata['umm']['Platforms'][0]['ShortName'])

    @utils.raises((KeyError, IndexError))
    def get_instrument(self, raw_metadata):
        """Only get the first instrument from the raw metadata, because
        GeoSPaaS does not support more than one instrument per dataset
        """
        return utils.get_gcmd_instrument(
            raw_metadata['umm']['Platforms'][0]['Instruments'][0]['ShortName'])

    @utils.raises((KeyError, IndexError))
    def get_location_geometry(self, raw_metadata):
        bounds = (raw_metadata['umm']['SpatialExtent']
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

    @utils.raises((KeyError, IndexError))
    def get_provider(self, raw_metadata):
        provider_id = raw_metadata['meta']['provider-id']
        provider = utils.get_gcmd_provider([provider_id])
        if provider:
            return provider
        else:
            raise MetadataNormalizationError(f"Unknown provider {provider_id}")
