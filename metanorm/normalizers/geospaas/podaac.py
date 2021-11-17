"""Normalizer for the metadata used by PO.DAAC"""

import dateutil.parser
import shapely.geometry
import shapely.wkt

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer
from ...errors import MetadataNormalizationError

class PODAACMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset using PODAAC
    attributes
    """

    def check(self, raw_metadata):
        return raw_metadata.get('url', '').startswith('https://opendap.jpl.nasa.gov/opendap/')

    @utils.raises(KeyError)
    def get_entry_title(self, raw_metadata):
        return raw_metadata['title']

    @utils.raises((AttributeError, KeyError))
    def get_entry_id(self, raw_metadata):
        return utils.NC_H5_FILENAME_MATCHER.search(raw_metadata['url']).group(1)

    @utils.raises(KeyError)
    def get_summary(self, raw_metadata):
        summary_fields = {}

        summary_fields[utils.SUMMARY_FIELDS['description']] = raw_metadata['summary']

        processing_level = raw_metadata['processing_level'].lstrip('Ll')
        summary_fields[utils.SUMMARY_FIELDS['processing_level']] = processing_level

        return utils.dict_to_string(summary_fields)

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_start(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['time_coverage_start'])

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_end(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['time_coverage_end'])

    @utils.raises(KeyError)
    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform(raw_metadata['platform'])

    @utils.raises(KeyError)
    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument(raw_metadata['sensor'])

    @utils.raises(KeyError)
    def get_location_geometry(self, raw_metadata):
        """Get the location geometry (in WKT or GeoJSON) from the raw
        metadata
        """
        if 'geospatial_bounds' in raw_metadata:
            result_wkt = raw_metadata['geospatial_bounds']
        elif set(['northernmost_latitude', 'southernmost_latitude',
                  'easternmost_longitude', 'westernmost_longitude']).issubset(raw_metadata.keys()):
            result_wkt = utils.wkt_polygon_from_wgs84_limits(
                raw_metadata['northernmost_latitude'],
                raw_metadata['southernmost_latitude'],
                raw_metadata['easternmost_longitude'],
                raw_metadata['westernmost_longitude'])
        else:
            raise MetadataNormalizationError(
                f"Unable to find a value for the 'location_geometry' in {raw_metadata}")

        # detect if the spatial coverage crosses the
        # international dateline
        easternmost_longitude = raw_metadata.get('easternmost_longitude')
        westernmost_longitude = raw_metadata.get('westernmost_longitude')
        if (easternmost_longitude is not None and
                westernmost_longitude is not None and
                float(easternmost_longitude) < float(westernmost_longitude)):

            geometry = shapely.wkt.loads(result_wkt)
            if isinstance(geometry, shapely.geometry.Polygon):
                multipolygon = shapely.geometry.MultiPolygon((geometry,))
            elif isinstance(geometry, shapely.geometry.MultiPolygon):
                multipolygon = geometry
            else:
                raise MetadataNormalizationError(
                    f"Unsupported geometry: {raw_metadata['geospatial_bounds']}")
            result_wkt = utils.split_multipolygon_along_idl(multipolygon).wkt

        # get the SRID if it is defined
        if 'geospatial_bounds_crs' in raw_metadata:
            srid = f"SRID={raw_metadata['geospatial_bounds_crs'].split(':')[1]};"
        else:
            srid = ''

        return srid + result_wkt

    def get_provider(self, raw_metadata):
        """Get the provider from the raw metadata"""
        return utils.get_gcmd_provider(['NASA/JPL/PODAAC'])
