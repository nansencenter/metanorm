"""Normalizer metadat from CSV file from Radarsat2 facility"""

import datetime as dt
import logging

from dateutil.tz import tzutc
import pythesint as pti

from .base import BaseMetadataNormalizer
import metanorm.utils as utils

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class Radarsat2CSVMetadataNormalizer(BaseMetadataNormalizer):
    """ Normalizer for metadata from CSV from Radarsat-2 searching facility """

    def match_metadata(self, raw_attributes):
        """ Check if metadata fits the normalizer """
        keys = set(['Satellite', 'Date', 'Order Key', 'Footprint'])
        return (keys.issubset(set(raw_attributes.keys()))
            and raw_attributes['Satellite'] == 'RADARSAT-2')

    def get_time_coverage_start(self, raw_attributes):
        """ return start date from Date """
        if self.match_metadata(raw_attributes):
            return dt.datetime.strptime(
                raw_attributes['Date'], '%Y-%m-%d %H:%M:%S GMT').replace(tzinfo=tzutc())

    def get_time_coverage_end(self, raw_attributes):
        """ return end data from start date and add 5 minutes """
        time_coverage_start = self.get_time_coverage_start(raw_attributes)
        if time_coverage_start:
            return time_coverage_start + dt.timedelta(minutes=5)

    def get_platform(self, raw_attributes):
        """ return Radrasat-2 platform """
        if self.match_metadata(raw_attributes):
            return pti.get_gcmd_platform('RADARSAT-2')

    def get_instrument(self, raw_attributes):
        """ return C-SAR instrument """
        if self.match_metadata(raw_attributes):
            return pti.get_gcmd_instrument('C-SAR')

    def get_provider(self, raw_attributes):
        """ return C-SAR instrument """
        if self.match_metadata(raw_attributes):
            return pti.get_gcmd_provider('CSA')

    def get_location_geometry(self, raw_attributes):
        """ return a WKT string corresponding to the location of the dataset"""
        if self.match_metadata(raw_attributes):
            fp = raw_attributes['Footprint'].strip().split(' ')
            return (f'POLYGON(({fp[0]} {fp[1]}, {fp[2]} {fp[3]}, {fp[4]} {fp[5]}, ' +
            f'{fp[6]} {fp[7]}, {fp[8]} {fp[9]}))')

    def get_gcmd_location(self, raw_attributes):
        """ return SEA SURFACE """
        if self.match_metadata(raw_attributes):
            return pti.get_gcmd_location('sea surface')

    def get_iso_topic_category(self, raw_attributes):
        """ return Oceans """
        if self.match_metadata(raw_attributes):
            return pti.get_iso19115_topic_category('oceans')

    def get_entry_id(self, raw_attributes):
        """ return filename """
        if self.match_metadata(raw_attributes):
            return raw_attributes['Order Key']

    def get_dataset_parameters(self, raw_attributes):
        """ return list with sigma0 parameter from wkv variable """
        if self.match_metadata(raw_attributes):
            return [pti.get_wkv_variable('surface_backwards_scattering_coefficient_of_radar_wave')]
        else:
            return []

    def get_entry_title(self, raw_attributes):
        """ return list with sigma0 parameter from wkv variable """
        if self.match_metadata(raw_attributes):
            keys = ['Title', 'Polarization', 'Beam Mode']
            return ' '.join([raw_attributes[key] for key in keys])
