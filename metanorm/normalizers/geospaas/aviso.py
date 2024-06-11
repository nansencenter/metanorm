"""Normalizer for the metadata used in AVISO altimetry files"""

import dateutil.parser

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer
from ...errors import MetadataNormalizationError


class AVISOAltimetryMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset using AVISO
    attributes
    """

    def check(self, raw_metadata):
        return (('aviso.altimetry.fr' in raw_metadata.get('creator_url', '') and
                    raw_metadata.get('creator_email', '') == 'aviso@altimetry.fr')
                or ('aviso.altimetry.fr' in raw_metadata.get('url', '')))

    @utils.raises(KeyError)
    def get_entry_title(self, raw_metadata):
        return raw_metadata['title']

    @utils.raises((AttributeError, KeyError))
    def get_entry_id(self, raw_metadata):
        return utils.NC_H5_FILENAME_MATCHER.search(raw_metadata['url']).group(1)

    @utils.raises(KeyError)
    def get_summary(self, raw_metadata):
        summary_fields = {}

        summary_fields[utils.SUMMARY_FIELDS['description']] = raw_metadata['comment']

        processing_level = raw_metadata['processing_level'].lstrip('Ll')
        summary_fields[utils.SUMMARY_FIELDS['processing_level']] = processing_level

        return utils.dict_to_string(summary_fields)

    @utils.raises((dateutil.parser.ParserError,))
    def get_time_coverage_start(self, raw_metadata):
        keys = ('time_coverage_start', 'time_coverage_begin')
        for key in keys:
            if key in raw_metadata:
                return dateutil.parser.parse(raw_metadata[key])
        raise MetadataNormalizationError(f"{keys} not found in raw metadata")

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_end(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['time_coverage_end'])

    def get_platform(self, raw_metadata):
        platform = None
        try:
            platform = utils.get_gcmd_platform(raw_metadata['platform'])
        except KeyError:
            pass
        if platform is None or platform['Category'] == utils.UNKNOWN:
            platform = utils.get_gcmd_platform('Earth Observation Satellites')
        return platform

    def get_instrument(self, raw_metadata):
        instrument = None
        try:
            instrument = utils.get_gcmd_instrument(raw_metadata['instrument'])
        except KeyError:
            pass
        if instrument is None or instrument['Category'] == utils.UNKNOWN:
            instrument = utils.get_gcmd_instrument('Altimeters')
        return instrument

    @utils.raises(KeyError)
    def get_location_geometry(self, raw_metadata):
        if 'geometry' in raw_metadata:
            return raw_metadata['geometry']
        elif set(['geospatial_lat_max', 'geospatial_lat_min',
                  'geospatial_lon_max', 'geospatial_lon_min']).issubset(raw_metadata.keys()):
            return utils.wkt_polygon_from_wgs84_limits(
                raw_metadata['geospatial_lat_max'],
                raw_metadata['geospatial_lat_min'],
                raw_metadata['geospatial_lon_max'],
                raw_metadata['geospatial_lon_min'])
        else:
            return ''


    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['AVISO'])
