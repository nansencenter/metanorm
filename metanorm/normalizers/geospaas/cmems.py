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


class CMEMS006013MetadataNormalizer(CMEMSMetadataNormalizer):
    """Normalizer for the MEDSEA_ANALYSISFORECAST_PHY_006_013 product
    """

    url_prefix = 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013'
    time_patterns = (
        (
            re.compile(utils.YEARMONTHDAY_REGEX + r'_(d|h|hts|qm)-.*\.nc$'),
            utils.create_datetime,
            lambda time: (time, time + relativedelta(days=1))
        ),
        (
            re.compile(utils.YEARMONTHDAY_REGEX + r'_m-.*\.nc$'),
            utils.create_datetime,
            lambda time: (time, time + relativedelta(months=1))
        )
    )

    def check(self, raw_metadata):
        return raw_metadata.get('url', '').startswith(self.url_prefix)

    def get_entry_title(self, raw_metadata):
        return 'Mediterranean Forecasting System (hydrodynamic-wave model)'

    def get_summary(self, raw_metadata):
        return utils.dict_to_string({
            utils.SUMMARY_FIELDS['description']:
                'The physical component of the Mediterranean Forecasting System '
                '(Med-Currents) is a coupled hydrodynamic-wave model implemented over the whole '
                'Mediterranean Basin.',
            utils.SUMMARY_FIELDS['processing_level']: '4',
            utils.SUMMARY_FIELDS['product']: 'MEDSEA_ANALYSISFORECAST_PHY_006_013'
        })

    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform('OPERATIONAL MODELS')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('Computer')

    def get_location_geometry(self, raw_metadata):
        return 'POLYGON((-17.29 45.98, -17.29 30.18, 36.30 30.18, 36.30 45.98, -17.29 45.98))'

    def get_dataset_parameters(self, raw_metadata):
        parameters = {
            "med-cmcc-cur": (
                'eastward_sea_water_velocity',
                'northward_sea_water_velocity',
            ),
            "med-cmcc-mld": ('ocean_mixed_layer_thickness_defined_by_sigma_theta',),
            "med-cmcc-sal": ('sea_water_salinity',),
            "med-cmcc-ssh": ('sea_surface_height_above_geoid',),
            "med-cmcc-tem": (
                'sea_water_potential_temperature_at_sea_floor',
                'sea_water_potential_temperature'
            ),
            "MEDSEA_ANALYSISFORECAST_PHY_006_013-statics/MED-MFC_006_013_mask_bathy.nc": (
                'model_level_number_at_sea_floor',
                'sea_binary_mask',
                'sea_floor_depth_below_geoid'
            ),
            "MEDSEA_ANALYSISFORECAST_PHY_006_013-statics/MED-MFC_006_013_coordinates.nc": (
                'cell_thickness',
            ),
            "MEDSEA_ANALYSISFORECAST_PHY_006_013-statics/MED-MFC_006_013_mdt.nc": (
                'sea_surface_height_above_geoid',
            )
        }

        for prefix, parameter_list in parameters.items():
            if raw_metadata['url'].startswith(f"{self.url_prefix}/{prefix}"):
                return utils.create_parameter_list(parameter_list)
        return []


class CMEMS005001MetadataNormalizer(CMEMSMetadataNormalizer):
    """Normalizer for the IBI_ANALYSISFORECAST_PHY_005_001 product"""

    url_prefix = 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001'
    time_patterns = (
        (
            re.compile(
                r'/CMEMS_v5r1_IBI_PHY_NRT_PdE_(15minav|01dav|01hav(3D)?)_' +
                utils.YEARMONTHDAY_REGEX + r'_.*\.nc$'
            ),
            utils.create_datetime,
            lambda time: (time, time + relativedelta(days=1))
        ),
        (
            re.compile(
                r'/CMEMS_v5r1_IBI_PHY_NRT_PdE_01mav_' + utils.YEARMONTHDAY_REGEX + r'_.*\.nc$'),
            utils.create_datetime,
            lambda time: (time, time + relativedelta(months=1))
        )
    )

    def check(self, raw_metadata):
        return raw_metadata.get('url', '').startswith(self.url_prefix)

    def get_entry_title(self, raw_metadata):
        return 'Atlantic-Iberian Biscay Irish-Ocean Physics Analysis and Forecast'

    def get_summary(self, raw_metadata):
        return utils.dict_to_string({
            utils.SUMMARY_FIELDS['description']:
                'The operational IBI (Iberian Biscay Irish) Ocean Analysis and Forecasting'
                ' system provides a 5-day hydrodynamic forecast including high frequency '
                'processes of paramount importance to characterize regional scale marine '
                'processes.',
            utils.SUMMARY_FIELDS['processing_level']: '4',
            utils.SUMMARY_FIELDS['product']: 'IBI_ANALYSISFORECAST_PHY_005_001'
        })

    def get_platform(self, raw_metadata):
        return utils.get_gcmd_platform('OPERATIONAL MODELS')

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('Computer')

    def get_location_geometry(self, raw_metadata):
        return 'POLYGON((-19 56, 5 56, 5 26, -19 26, -19 56))'

    def get_dataset_parameters(self, raw_metadata):
        parameters = {
            "cmems_mod_ibi_phy_anfc_0.027deg-2D_PT15M-m/": (
                'sea_surface_height_above_geoid',
                'eastward_sea_water_velocity',
                'northward_sea_water_velocity'
            ),
            "cmems_mod_ibi_phy_anfc_0.027deg-3D_P1D-m/": (
                'sea_water_potential_temperature',
                'sea_water_salinity',
                'eastward_sea_water_velocity',
                'northward_sea_water_velocity',
                'sea_surface_height_above_geoid',
                'ocean_mixed_layer_thickness_defined_by_sigma_theta',
                'sea_water_potential_temperature_at_sea_floor'
            ),
            "cmems_mod_ibi_phy_anfc_0.027deg-2D_PT1H-m/": (
                'sea_water_potential_temperature',
                'eastward_sea_water_velocity',
                'northward_sea_water_velocity',
                'barotropic_eastward_sea_water_velocity',
                'barotropic_northward_sea_water_velocity',
                'sea_surface_height_above_geoid',
                'ocean_mixed_layer_thickness_defined_by_sigma_theta'
            ),
            "cmems_mod_ibi_phy_anfc_0.027deg-3D_PT1H-m/": (
                'sea_water_potential_temperature',
                'sea_water_salinity',
                'eastward_sea_water_velocity',
                'northward_sea_water_velocity'
            ),
            "cmems_mod_ibi_phy_anfc_0.027deg-3D_P1M-m/": (
                'sea_water_potential_temperature',
                'sea_water_salinity',
                'eastward_sea_water_velocity',
                'northward_sea_water_velocity',
                'sea_surface_height_above_geoid',
                'ocean_mixed_layer_thickness_defined_by_sigma_theta',
                'sea_water_potential_temperature_at_sea_floor'
            )
        }

        for prefix, parameter_list in parameters.items():
            if raw_metadata['url'].startswith(f"{self.url_prefix}/{prefix}"):
                return utils.create_parameter_list(parameter_list)
        return []
