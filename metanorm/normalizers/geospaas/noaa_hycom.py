"""Normalizer for the metadata of NOAA HYCOM datasets"""

import re
from dateutil.relativedelta import relativedelta

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer
from ...errors import MetadataNormalizationError


class NOAAHYCOMMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset for a NOAA HYCOM
    dataset
    """

    url_prefix = 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy'

    def check(self, raw_metadata):
        """Checks that the URL starts with the right prefix"""
        return raw_metadata.get('url', '').startswith(self.url_prefix)

    def get_entry_title(self, raw_metadata):
        return 'Global Hybrid Coordinate Ocean Model (HYCOM)'

    @utils.raises((KeyError, AttributeError))
    def get_entry_id(self, raw_metadata):
        return utils.NC_H5_FILENAME_MATCHER.search(raw_metadata['url']).group(1)

    def get_summary(self, raw_metadata):
        return utils.dict_to_string({
            utils.SUMMARY_FIELDS['description']:
                'This system provides 4-day forecasts at 3-hour time steps, updated at 00Z '
                'daily. Navy Global HYCOM has a resolution of 1/12 degree in the horizontal '
                'and uses hybrid (isopycnal/sigma/z-level) coordinates in the vertical. The '
                'output is interpolated onto a regular 1/12-degree grid horizontally and '
                '40 standard depth levels.',
            utils.SUMMARY_FIELDS['processing_level']: '4',
            utils.SUMMARY_FIELDS['product']: 'HYCOM'
        })

    time_patterns = (
        (
            re.compile(
                r'/hycom_glb_\w+_' +
                utils.YEARMONTHDAY_REGEX +
                r'00_t(?P<hours>\d{3})\.nc\.gz'),
            lambda year, month, day, hours: (
                utils.create_datetime(year, month, day) + relativedelta(hours=int(hours))),
            lambda time: (time, time + relativedelta(hours=3))
        ),
    )

    @utils.raises(KeyError)
    def get_time_coverage_start(self, raw_metadata):
        return utils.find_time_coverage(self.time_patterns, raw_metadata['url'])[0]

    @utils.raises(KeyError)
    def get_time_coverage_end(self, raw_metadata):
        return utils.find_time_coverage(self.time_patterns, raw_metadata['url'])[1]

    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform('OPERATIONAL MODELS')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('Computer')

    @utils.raises(KeyError)
    def get_location_geometry(self, raw_metadata):
        locations = {
            'hycom_glb_regp01': 'POLYGON((-100.04 70.04, -100.04 -0.04, -49.96 -0.04, '
                                '-49.96 70.04, -100.04 70.04))',
            'hycom_glb_regp06': 'POLYGON((149.96 70.04, 149.96 9.96, 210.04 9.96, 210.04 70.04, '
                                '149.96 70.04))',
            'hycom_glb_regp07': 'POLYGON((-150.04 60.04, -150.04 9.96, -99.96 9.96, -99.96 60.04, '
                                '-150.04 60.04))',
            'hycom_glb_regp17': 'POLYGON((-180.04 80.02,-180.04 59.98,-119.96 59.98,-119.96 80.02,'
                                '-180.04 80.02))',
            'hycom_glb_sfc_u': utils.WORLD_WIDE_COVERAGE_WKT,
        }
        for prefix, location in locations.items():
            if raw_metadata['url'].startswith(f"{self.url_prefix}/{prefix}"):
                return location
        raise MetadataNormalizationError(f"Could not find a location gemetry for {raw_metadata}")

    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['DOC/NOAA/NWS/NCEP'])

    def get_dataset_parameters(self, raw_metadata):
        return utils.create_parameter_list((
            'sea_water_salinity',
            'sea_water_temperature',
            'sea_water_salinity_at_bottom',
            'sea_water_temperature_at_bottom',
            'sea_surface_height_above_geoid',
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity'
        ))
