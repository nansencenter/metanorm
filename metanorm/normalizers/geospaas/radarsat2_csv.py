"""Normalize metadata from CSV file from Radarsat2 facility"""

from datetime import timedelta

import dateutil.parser
import pythesint as pti

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer


class Radarsat2CSVMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Normalizer for metadata from CSV from Radarsat-2 searching
    facility
    """

    def check(self, raw_metadata):
        keys = set(['Satellite', 'Date', 'Order Key', 'Footprint'])
        return (keys.issubset(set(raw_metadata.keys()))
            and raw_metadata['Satellite'] == 'RADARSAT-2')

    @utils.raises(KeyError)
    def get_entry_title(self, raw_metadata):
        keys = ['Title', 'Polarization', 'Beam Mode']
        return ' '.join([raw_metadata[key] for key in keys])

    @utils.raises(KeyError)
    def get_entry_id(self, raw_metadata):
        return raw_metadata['Order Key']

    @utils.raises((KeyError, dateutil.parser.ParserError))
    def get_time_coverage_start(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['Date'])

    def get_time_coverage_end(self, raw_metadata):
        return self.get_time_coverage_start(raw_metadata) + timedelta(minutes=5)

    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform('RADARSAT-2')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('C-SAR')

    @utils.raises(KeyError)
    def get_location_geometry(self, raw_metadata):
        """ return a WKT string corresponding to the location of the dataset"""
        footprint = raw_metadata['Footprint'].strip().split(' ')
        return (f"POLYGON(({footprint[0]} {footprint[1]}, {footprint[2]} {footprint[3]}, "
                f"{footprint[4]} {footprint[5]}, {footprint[6]} {footprint[7]}, "
                f"{footprint[8]} {footprint[9]}))")

    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['CSA'])

    def get_dataset_parameters(self, raw_metadata):
        return utils.create_parameter_list('surface_backwards_scattering_coefficient_of_radar_wave')
