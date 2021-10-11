"""Normalizer for the metadata used in AVISO altimetry files"""

import dateutil.parser

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer


class AVISOAltimetryMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset using AVISO
    attributes
    """

    def check(self, raw_metadata):
        return (
            'aviso.altimetry.fr' in raw_metadata.get('creator_url', '') and
            raw_metadata.get('creator_email', '') == 'aviso@altimetry.fr')

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

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_start(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['time_coverage_start'])

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_end(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['time_coverage_end'])

    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform('Earth Observation Satellites')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('Altimeters')

    @utils.raises(KeyError)
    def get_location_geometry(self, raw_metadata):
        return raw_metadata['geometry']

    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['AVISO'])
