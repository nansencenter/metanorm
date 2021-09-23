"""Normalizers for the metadata of CMEMS datasets"""

import re
from dateutil.relativedelta import relativedelta

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer


class CMEMSMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Base class for CMEMS normalizers"""

    time_patterns = ()

    @utils.raises((AttributeError, KeyError))
    def get_entry_id(self, raw_metadata):
        return utils.NC_H5_FILENAME_MATCHER.search(raw_metadata['url']).group(1)

    def get_provider(self, raw_metadata):
        return utils.get_gcmd_provider(['CMEMS'])

    @utils.raises(KeyError)
    def get_time_coverage_start(self, raw_metadata):
        return utils.find_time_coverage(self.time_patterns, raw_metadata['url'])[0]

    @utils.raises(KeyError)
    def get_time_coverage_end(self, raw_metadata):
        return utils.find_time_coverage(self.time_patterns, raw_metadata['url'])[1]


class CMEMS008046MetadataNormalizer(CMEMSMetadataNormalizer):
    """Normalizer for the SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046
    product
    """

    time_patterns = (
        (
            re.compile(r'/nrt_global_allsat_phy_l4_' + utils.YEARMONTHDAY_REGEX + r'_.*\.nc$'),
            utils.create_datetime,
            lambda time: (time - relativedelta(hours=12), time + relativedelta(hours=12))
        ),
    )

    def check(self, raw_metadata):
        return raw_metadata.get('url', '').startswith(
            'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046')

    def get_entry_title(self, raw_metadata):
        return 'GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT'

    def get_summary(self, raw_metadata):
        return utils.dict_to_string({
            utils.SUMMARY_FIELDS['description']:
            'Altimeter satellite gridded Sea Level Anomalies (SLA) computed with '
            'respect to a twenty-year mean.',
            utils.SUMMARY_FIELDS['processing_level']: '4',
            utils.SUMMARY_FIELDS['product']: 'SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'
        })

    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform('Earth Observation satellites')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('altimeters')

    def get_location_geometry(self, raw_metadata):
        return utils.WORLD_WIDE_COVERAGE_WKT

    def get_dataset_parameters(self, raw_metadata):
        # based on "http://nrt.cmems-du.eu/motu-web/Motu?action=describeProduct
        #           &service=SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046-TDS"
        return utils.create_parameter_list((
            'sea_surface_height_above_geoid',
            'sea_surface_height_above_sea_level',
            'surface_geostrophic_eastward_sea_water_velocity',
            'surface_geostrophic_eastward_sea_water_velocity_assuming_mean_sea_level_for_geoid',
            'surface_geostrophic_northward_sea_water_velocity',
            'surface_geostrophic_northward_sea_water_velocity_assuming_mean_sea_level_for_geoid'
        ))


class CMEMS015003MetadataNormalizer(CMEMSMetadataNormalizer):
    """Normalizer for the MULTIOBS_GLO_PHY_NRT_015_003 product"""

    time_patterns = (
        (
            re.compile(r'/dataset-uv-nrt-(daily|hourly)_' +
                       utils.YEARMONTHDAY_REGEX + r'T.*\.nc$'),
            utils.create_datetime,
            lambda time: (time, time + relativedelta(days=1))
        ),
        (
            re.compile(r'/dataset-uv-nrt-monthly_' + utils.YEARMONTH_REGEX + r'T.*\.nc$'),
            utils.create_datetime,
            lambda time: (time, time + relativedelta(months=1))
        )
    )

    def check(self, raw_metadata):
        return raw_metadata.get('url', '').startswith(
            'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003')

    def get_entry_title(self, raw_metadata):
        return ('GLOBAL TOTAL SURFACE AND 15M CURRENT FROM ALTIMETRIC '
                'GEOSTROPHIC CURRENT AND MODELED EKMAN CURRENT PROCESSING')

    def get_summary(self, raw_metadata):
        return utils.dict_to_string({
            utils.SUMMARY_FIELDS['description']:
            'This product is a NRT L4 global total velocity field at 0m and 15m.',
            utils.SUMMARY_FIELDS['processing_level']: '4',
            utils.SUMMARY_FIELDS['product']: 'MULTIOBS_GLO_PHY_NRT_015_003'
        })

    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform('Earth Observation satellites')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('altimeters')

    def get_location_geometry(self, raw_metadata):
        return utils.WORLD_WIDE_COVERAGE_WKT

    def get_dataset_parameters(self, raw_metadata):
        # based on "http://nrt.cmems-du.eu/motu-web/Motu?
        #           action=describeProduct&service=MULTIOBS_GLO_PHY_NRT_015_003-TDS"
        return utils.create_parameter_list((
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity'
        ))


class CMEMS001024MetadataNormalizer(CMEMSMetadataNormalizer):
    """Normalizer for the GLOBAL_ANALYSIS_FORECAST_PHY_001_024 product
    """

    time_patterns = (
        (
            re.compile(
                r'/(SMOC|mercatorpsy4v3r1_gl12_(mean|hrly))_' +
                utils.YEARMONTHDAY_REGEX +
                r'_R.*\.nc$'),
            utils.create_datetime,
            lambda time: (time, time + relativedelta(days=1))
        ),
        (
            re.compile(r'/mercatorpsy4v3r1_gl12_mean_' + utils.YEARMONTH_REGEX + r'.*\.nc$'),
            utils.create_datetime,
            lambda time: (time, time + relativedelta(months=1))
        ),
        (
            re.compile(
                r'/mercatorpsy4v3r1_gl12_(thetao|so|uovo)_' +
                utils.YEARMONTHDAY_REGEX +
                r'_(?P<hour>\d{2})h_R.*\.nc$'),
            utils.create_datetime,
            lambda time: (time, time)
        )
    )

    def check(self, raw_metadata):
        return raw_metadata.get('url', '').startswith(
            'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024')

    def get_entry_title(self, raw_metadata):
        return 'GLOBAL OCEAN 1_12 PHYSICS ANALYSIS AND FORECAST UPDATED DAILY'

    def get_summary(self, raw_metadata):
        return utils.dict_to_string({
            utils.SUMMARY_FIELDS['description']:
                'The Operational Mercator global ocean analysis and forecast system at '
                '1/12 degree is providing 10 days of 3D global ocean forecasts updated daily.',
            utils.SUMMARY_FIELDS['processing_level']: '4',
            utils.SUMMARY_FIELDS['product']: 'GLOBAL_ANALYSIS_FORECAST_PHY_001_024'
        })

    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform('OPERATIONAL MODELS')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('Computer')

    def get_location_geometry(self, raw_metadata):
        return utils.WORLD_WIDE_COVERAGE_WKT

    def get_dataset_parameters(self, raw_metadata):
        # based on "http://nrt.cmems-du.eu/motu-web/Motu?
        #           action=describeProduct&service=GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS"
        return utils.create_parameter_list((
            'sea_water_potential_temperature_at_sea_floor',
            'ocean_mixed_layer_thickness_defined_by_sigma_theta',
            'sea_ice_area_fraction',
            'sea_ice_thickness',
            'sea_water_salinity',
            'sea_water_potential_temperature',
            'eastward_sea_water_velocity',
            'eastward_sea_ice_velocity',
            'northward_sea_water_velocity',
            'northward_sea_ice_velocity',
            'sea_surface_height_above_geoid'
        ))
