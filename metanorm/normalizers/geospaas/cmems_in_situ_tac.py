"""Normalizer for the Copernicus In Situ TAC metadata convention"""

import logging
import re

import dateutil.parser
import pythesint as pti

import metanorm.utils as utils

from .base import GeoSPaaSMetadataNormalizer


class CMEMSInSituTACMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset using
    CMEMS In Situ TAC attributes
    """

    def check(self, raw_metadata):
        """Check that the dataset's id matches CMEMS in situ TAC data"""
        identifier = raw_metadata.get('id', '')
        file_types = r'(TS|PR|TV|RV|WS)'
        data_types = r'(BO|CT|DB|DC|FB|GL|HF|ML|MO|PF|RF|SD|SF|SM|TG|TS|TX|VA|XB|XX)'
        return bool(re.match(rf'^[A-Z]{{2}}_{file_types}_{data_types}(_[^_]+){{1,2}}$', identifier))

    @utils.raises(KeyError)
    def get_entry_title(self, raw_metadata):
        return raw_metadata['title']

    @utils.raises(KeyError)
    def get_entry_id(self, raw_metadata):
        return raw_metadata['id']

    def get_summary(self, raw_metadata):
        """Get the dataset's summary if it is available in the
        metadata, otherwise use a default
        """
        description = None
        raw_summary = raw_metadata.get('summary')
        url = raw_metadata.get('url', '')

        if raw_summary and raw_summary.strip():
            description = raw_summary

        if 'INSITU_GLO_NRT_OBSERVATIONS_013_030' in url:
            product = 'INSITU_GLO_NRT_OBSERVATIONS_013_030'
            if not description:
                description = (
                    'Global Ocean - near real-time (NRT) in situ quality controlled '
                    'observations, hourly updated and distributed by INSTAC within 24-48 hours '
                    'from acquisition in average. Data are collected mainly through global '
                    'networks (Argo, OceanSites, GOSUD, EGO) and through the GTS'
                )
        elif 'INSITU_GLO_UV_NRT_OBSERVATIONS_013_048' in url:
            product = 'INSITU_GLO_UV_NRT_OBSERVATIONS_013_048'
            if not description:
                description = (
                    'This product is entirely dedicated to ocean current data observed in '
                    'near-real time. Surface current data from 2 different types of instruments'
                    ' are distributed: velocities calculated along the trajectories of drifting'
                    ' buoys from the DBCP’s Global Drifter Program, and velocities measured by '
                    'High Frequency radars from the European High Frequency radar Network'
                )
        else:
            product = utils.UNKNOWN
            if not description:
                description = 'CMEMS in situ TAC data'

        return utils.dict_to_string({
            utils.SUMMARY_FIELDS['description']: description or '',
            utils.SUMMARY_FIELDS['processing_level']: '2',
            utils.SUMMARY_FIELDS['product']: product
        })

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_start(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['time_coverage_start'])

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_end(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['time_coverage_end'])

    def get_platform(self, raw_metadata):
        return pti.get_gcmd_platform('In Situ Ocean-based Platforms')

    def get_instrument(self, raw_metadata):
        return pti.get_gcmd_instrument('In Situ/Laboratory Instruments')

    @utils.raises(KeyError)
    def get_location_geometry(self, raw_metadata):
        return raw_metadata['geometry']

    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['cmems'])
