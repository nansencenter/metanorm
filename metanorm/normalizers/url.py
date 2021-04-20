"""Normalizer for the interpretation of file name convention"""
import logging
import re
from datetime import datetime

import pythesint as pti
from dateutil.relativedelta import relativedelta
from dateutil.tz import tzutc

import metanorm.utils as utils
from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())

class URLMetadataNormalizer(BaseMetadataNormalizer):
    """ Normalizer for hardcoding information based on URLS """

    urls_platforms = {
        "ftp://ftp.remss.com/gmi": 'GPM',
        "ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/": 'Earth Observation Satellites',
        "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W": 'GCOM-W1',
        "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046":
            'Earth Observation satellites',
        "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003": 'Earth Observation satellites',
        "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024": 'OPERATIONAL MODELS',
        "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013": 'OPERATIONAL MODELS',
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSIS_FORECAST_PHYS_005_001": 'OPERATIONAL MODELS',
        "ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/": 'OPERATIONAL MODELS',
        "ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod": 'OPERATIONAL MODELS',
    }

    urls_instruments = {
        'ftp://ftp.remss.com/gmi': 'GMI',
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2': 'AMSR2',
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/':
            'Imaging Spectrometers/Radiometers',
        "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046": 'altimeters',
        "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003": 'altimeters',
        "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024": 'computer',
        "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013": 'computer',
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSIS_FORECAST_PHYS_005_001": 'computer',
        "ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/": 'computer',
        "ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod": 'computer',
    }

    urls_provider = {
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': 'ESA/CCI',
        "ftp://ftp.remss.com/": 'Remote Sensing Systems',
        "ftp://ftp.gportal.jaxa.jp/standard": 'JP/JAXA/EOC',
        "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046": 'cmems',
        "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003": 'cmems',
        "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024": 'cmems',
        "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013": 'cmems',
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSIS_FORECAST_PHYS_005_001": 'cmems',
        "ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/": 'DOC/NOAA/NWS/NCEP',
        "ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod": 'DOC/NOAA/NWS/NCEP',
    }

    WORLD_WIDE_COVERAGE_WKT = 'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'

    def get_rtofs_geometry(self, url):
        """Return the right geometry for the possible RTOFS areas"""
        if 'US_east' in url:
            return ('POLYGON (('
                    '-105.193603515625 0, -40.719970703125 0,'
                    '-40.719970703125 79.74808502197266,'
                    '-105.193603515625 79.74808502197266,'
                    '-105.193603515625 0))')
        elif 'US_west' in url:
            return ('POLYGON (('
                    '-157.9200439453125 10.02840137481689,'
                    '-74.239990234375 10.02840137481689,'
                    '-74.239990234375 74.57466888427734,'
                    '-157.9200439453125 74.57466888427734,'
                    '-157.9200439453125 10.02840137481689))')
        elif 'alaska' in url:
            return ('POLYGON (('
                    '-179.1199951171875 45.77324676513672,'
                    '-112.6572265625 45.77324676513672,'
                    '-112.6572265625 78.41667938232422,'
                    '-179.1199951171875 78.41667938232422,'
                    '-179.1199951171875 45.77324676513672))')
        else:
            return self.WORLD_WIDE_COVERAGE_WKT

    urls_geometry = {
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/': WORLD_WIDE_COVERAGE_WKT,
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10': WORLD_WIDE_COVERAGE_WKT,
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25': WORLD_WIDE_COVERAGE_WKT,
        "ftp://ftp.remss.com/gmi/": WORLD_WIDE_COVERAGE_WKT,
        "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046":
            WORLD_WIDE_COVERAGE_WKT,
        "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003": WORLD_WIDE_COVERAGE_WKT,
        "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024": WORLD_WIDE_COVERAGE_WKT,
        "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013":
            'POLYGON((-17.29 45.98, -17.29 30.18, 36.30 30.18, 36.30 45.98, -17.29 45.98))',
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSIS_FORECAST_PHYS_005_001":
            'POLYGON((-19 56, 5 56, 5 26, -19 26, -19 56))',
        'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/hycom_glb_regp01':
            'POLYGON((-100.04 70.04, -100.04 -0.04, -49.96 -0.04, -49.96 70.04, -100.04 70.04))',
        'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/hycom_glb_regp06':
            'POLYGON((149.96 70.04, 149.96 9.96, 210.04 9.96, 210.04 70.04, 149.96 70.04))',
        'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/hycom_glb_regp07':
            'POLYGON((-150.04 60.04, -150.04 9.96, -99.96 9.96, -99.96 60.04, -150.04 60.04))',
        'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/hycom_glb_regp17':
            'POLYGON((-180.04 80.02,-180.04 59.98,-119.96 59.98,-119.96 80.02,-180.04 80.02))',
        'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/hycom_glb_sfc_u':
            WORLD_WIDE_COVERAGE_WKT,
        'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod': get_rtofs_geometry,
    }

    urls_title = {
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1':
            'ESA SST CCI OSTIA L4 Climatology',
        "ftp://ftp.remss.com/gmi/":
            'Atmosphere parameters from Global Precipitation Measurement Microwave Imager',
        "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST/":
            'AMSR2-L2 Sea Surface Temperature',
        "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10/":
            'AMSR2-L2 Sea Surface Temperature',
        "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/":
            'AMSR2-L3 Sea Surface Temperature',
        "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046":
            'GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT',
        "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003":
            'GLOBAL TOTAL SURFACE AND 15M CURRENT FROM ALTIMETRIC '
            'GEOSTROPHIC CURRENT AND MODELED EKMAN CURRENT PROCESSING',
        "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024":
            'GLOBAL OCEAN 1_12 PHYSICS ANALYSIS AND FORECAST UPDATED DAILY',
        "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013":
            'Mediterranean Forecasting System (hydrodynamic-wave model)',
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSIS_FORECAST_PHYS_005_001":
            'Atlantic-Iberian Biscay Irish-Ocean Physics Analysis and Forecast',
        "ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/":
            'Global Hybrid Coordinate Ocean Model (HYCOM)',
        "ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod":
            'Global operational Real-Time Ocean Forecast System',
    }

    NC_H5_FILENAME_MATCHER = re.compile(r"([^/]+)\.(nc|h5)(\.gz)?$")
    urls_entry_id = {
        "https://thredds.met.no/thredds/": re.compile(r"([^/]+)\.nc(\.dods)?$"),
        "https://opendap.jpl.nasa.gov/opendap/": NC_H5_FILENAME_MATCHER,
        "ftp://ftp.remss.com/gmi": re.compile(r"([^/]+)\.gz$"),
        "ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/": NC_H5_FILENAME_MATCHER,
        "ftp://nrt.cmems-du.eu/Core/": NC_H5_FILENAME_MATCHER,
        "ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/":
            NC_H5_FILENAME_MATCHER,
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSIS_FORECAST_PHYS_005_001": NC_H5_FILENAME_MATCHER,
        "ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/": NC_H5_FILENAME_MATCHER,
        "ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod": re.compile(
            r"(\d{8}/[^/]+)\.(nc|h5)(\.gz)?$"),
    }

    urls_summary = {
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4':
            utils.dict_to_string({
                utils.SUMMARY_FIELDS['description']: (
                    'This v2.1 SST_cci Climatology Data Record (CDR) consists of Level 4 daily'
                    ' climatology files gridded on a 0.05 degree grid.'
                ),
                utils.SUMMARY_FIELDS['processing_level']: '4',
                utils.SUMMARY_FIELDS['product']: 'ESA SST CCI Climatology'
            }),
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2':
            utils.dict_to_string({
                utils.SUMMARY_FIELDS['processing_level']: '2'
            }),
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3':
            utils.dict_to_string({
                utils.SUMMARY_FIELDS['processing_level']: '3'
            }),
        'ftp://ftp.remss.com/gmi/':
            utils.dict_to_string({
                utils.SUMMARY_FIELDS['description']:
                    'GMI is a dual-polarization, multi-channel, conical-scanning, passive '
                    'microwave radiometer with frequent revisit times.',
                utils.SUMMARY_FIELDS['processing_level']: '3'
            }),
        'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046':
            utils.dict_to_string({
                utils.SUMMARY_FIELDS['description']:
                    'Altimeter satellite gridded Sea Level Anomalies (SLA) computed with '
                    'respect to a twenty-year mean.',
                utils.SUMMARY_FIELDS['processing_level']: '4',
                utils.SUMMARY_FIELDS['product']: 'SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'
            }),
        'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003':
            utils.dict_to_string({
                utils.SUMMARY_FIELDS['description']:
                    'This product is a NRT L4 global total velocity field at 0m and 15m.',
                utils.SUMMARY_FIELDS['processing_level']: '4',
                utils.SUMMARY_FIELDS['product']: 'MULTIOBS_GLO_PHY_NRT_015_003'
            }),
        'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024':
            utils.dict_to_string({
                utils.SUMMARY_FIELDS['description']:
                    'The Operational Mercator global ocean analysis and forecast system at '
                    '1/12 degree is providing 10 days of 3D global ocean forecasts updated daily.',
                utils.SUMMARY_FIELDS['processing_level']: '4',
                utils.SUMMARY_FIELDS['product']: 'GLOBAL_ANALYSIS_FORECAST_PHY_001_024'
            }),
        'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013':
            utils.dict_to_string({
                utils.SUMMARY_FIELDS['description']:
                'The physical component of the Mediterranean Forecasting System '
                '(Med-Currents) is a coupled hydrodynamic-wave model implemented over the whole '
                'Mediterranean Basin.',
                utils.SUMMARY_FIELDS['processing_level']: '4',
                utils.SUMMARY_FIELDS['product']: 'MEDSEA_ANALYSIS_FORECAST_PHY_006_013'
            }),
        'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSIS_FORECAST_PHYS_005_001':
            utils.dict_to_string({
                utils.SUMMARY_FIELDS['description']:
                    'The operational IBI (Iberian Biscay Irish) Ocean Analysis and Forecasting'
                    ' system provides a 5-day hydrodynamic forecast including high frequency '
                    'processes of paramount importance to characterize regional scale marine '
                    'processes.',
                utils.SUMMARY_FIELDS['processing_level']: '4',
                utils.SUMMARY_FIELDS['product']: 'IBI_ANALYSIS_FORECAST_PHYS_005_001'
            }),
        'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/':
            utils.dict_to_string({
                utils.SUMMARY_FIELDS['description']:
                    'This system provides 4-day forecasts at 3-hour time steps, updated at 00Z '
                    'daily. Navy Global HYCOM has a resolution of 1/12 degree in the horizontal '
                    'and uses hybrid (isopycnal/sigma/z-level) coordinates in the vertical. The '
                    'output is interpolated onto a regular 1/12-degree grid horizontally and '
                    '40 standard depth levels.',
                utils.SUMMARY_FIELDS['processing_level']: '4',
                utils.SUMMARY_FIELDS['product']: 'HYCOM'
            }),
        'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod':
            utils.dict_to_string({
                utils.SUMMARY_FIELDS['description']:
                    "Real Time Ocean Forecast System (RTOFS) Global is a data-assimilating "
                    "nowcast-forecast system operated by the National Weather Service's National "
                    "Centers for Environmental Prediction (NCEP).",
                utils.SUMMARY_FIELDS['processing_level']: '4',
                utils.SUMMARY_FIELDS['product']: 'RTOFS'
            })
    }

    def get_rtofs_parameters(self, url):
        """Return the right parameters for RTOFS URLs"""
        result = []
        if 'rtofs_glo_2ds_' in url:
            if 'diag' in url:
                result = [
                    'sea_surface_height_above_geoid',
                    'barotropic_eastward_sea_water_velocity',
                    'barotropic_northward_sea_water_velocity',
                    'surface_boundary_layer_thickness',
                    'ocean_mixed_layer_thickness'
                ]
            elif 'prog' in url:
                result = [
                    'eastward_sea_water_velocity',
                    'northward_sea_water_velocity',
                    'sea_surface_temperature',
                    'sea_surface_salinity',
                    'sea_water_potential_density'
                ]
            elif 'ice' in url:
                result = [
                    'ice_coverage',
                    'ice_temperature',
                    'ice_thickness',
                    'ice_uvelocity',
                    'icd_vvelocity',
                ]
        elif 'rtofs_glo_3dz_' in url:
            result = [
                'eastward_sea_water_velocity',
                'northward_sea_water_velocity',
                'sea_surface_temperature',
                'sea_surface_salinity',
            ]
        return result

    urls_dataset_parameters = {
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/': ['sea_surface_temperature'],
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST': [
            'sea_surface_temperature'
        ],
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10': [
            'sea_surface_temperature'
        ],
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25': [
            'sea_surface_temperature'
        ],
        "ftp://ftp.remss.com/gmi/": [
            'wind_speed',
            'atmosphere_mass_content_of_water_vapor',
            'atmosphere_mass_content_of_cloud_liquid_water',
            'rainfall_rate'
        ],
        # based on http://nrt.cmems-du.eu/motu-web/Motu?action=describeProduct&service=SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046-TDS
        "ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046": [
            'sea_surface_height_above_geoid',
            'sea_surface_height_above_sea_level',
            'surface_geostrophic_eastward_sea_water_velocity',
            'surface_geostrophic_eastward_sea_water_velocity_assuming_mean_sea_level_for_geoid',
            'surface_geostrophic_northward_sea_water_velocity',
            'surface_geostrophic_northward_sea_water_velocity_assuming_mean_sea_level_for_geoid'
        ],
        # based on http://nrt.cmems-du.eu/motu-web/Motu?action=describeProduct&service=MULTIOBS_GLO_PHY_NRT_015_003-TDS
        "ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003": [
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity'
        ],
        # based on http://nrt.cmems-du.eu/motu-web/Motu?action=describeProduct&service=GLOBAL_ANALYSIS_FORECAST_PHY_001_024-TDS
        "ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024": [
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
        ],
        "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/med00-cmcc-cur": [
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity',
        ],
        "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/med00-cmcc-mld": [
            'ocean_mixed_layer_thickness_defined_by_sigma_theta'
        ],
        "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/med00-cmcc-sal": [
            'sea_water_salinity'
        ],
        "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/med00-cmcc-ssh": [
            'sea_surface_height_above_geoid'
        ],
        "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/med00-cmcc-tem": [
            'sea_water_potential_temperature_at_sea_floor',
            'sea_water_potential_temperature'
        ],
        "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/" +
        "MEDSEA_ANALYSIS_FORECAST_PHY_006_013-statics/MED-MFC_006_013_mask_bathy.nc": [
            'model_level_number_at_sea_floor',
            'sea_floor_depth_below_geoid'
        ],
        "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/" +
        "MEDSEA_ANALYSIS_FORECAST_PHY_006_013-statics/MED-MFC_006_013_coordinates.nc": [
            'cell_thickness'
        ],
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSIS_FORECAST_PHYS_005_001/" +
        "dataset-ibi-analysis-forecast-phys-005-001-15min/": [
            'sea_surface_height_above_geoid',
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity'
        ],
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSIS_FORECAST_PHYS_005_001/" +
        "dataset-ibi-analysis-forecast-phys-005-001-daily/": [
            'sea_water_potential_temperature',
            'sea_water_salinity',
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity',
            'sea_surface_height_above_geoid',
            'ocean_mixed_layer_thickness_defined_by_sigma_theta',
            'sea_water_potential_temperature_at_sea_floor'
        ],
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSIS_FORECAST_PHYS_005_001/" +
        "dataset-ibi-analysis-forecast-phys-005-001-hourly/": [
            'sea_water_potential_temperature',
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity',
            'barotropic_eastward_sea_water_velocity',
            'barotropic_northward_sea_water_velocity',
            'sea_surface_height_above_geoid',
            'ocean_mixed_layer_thickness_defined_by_sigma_theta'
        ],
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSIS_FORECAST_PHYS_005_001/" +
        "dataset-ibi-analysis-forecast-phys-005-001-hourly3d/": [
            'sea_water_potential_temperature',
            'sea_water_salinity',
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity'
        ],
        "ftp://nrt.cmems-du.eu/Core/IBI_ANALYSIS_FORECAST_PHYS_005_001/" +
        "dataset-ibi-analysis-forecast-phys-005-001-monthly/": [
            'sea_water_potential_temperature',
            'sea_water_salinity',
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity',
            'sea_surface_height_above_geoid',
            'ocean_mixed_layer_thickness_defined_by_sigma_theta',
            'sea_water_potential_temperature_at_sea_floor'
        ],
        "ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/": [
            'sea_water_salinity',
            'sea_water_temperature',
            'sea_water_salinity_at_bottom',
            'sea_water_temperature_at_bottom',
            'sea_surface_height_above_geoid',
            'eastward_sea_water_velocity',
            'northward_sea_water_velocity',
        ],
        "ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod": get_rtofs_parameters,
    }

    # See the docstring of find_time_coverage() to get
    # information about the dictionary structure
    urls_time = {
        'ftp://ftp.remss.com/gmi': [
            (
                re.compile(r'/y\d{4}/m\d{2}/f35_' + utils.YEARMONTHDAY_REGEX + r'v[\d.]+\.gz$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(days=1))
            ),
            (
                re.compile(r'/y\d{4}/m\d{2}/f35_' + utils.YEARMONTHDAY_REGEX + r'v[\d.]+_d3d\.gz$'),
                utils.create_datetime,
                lambda time: (time - relativedelta(days=2), time + relativedelta(days=1))
            ),
            (
                re.compile(r'/weeks/f35_' + utils.YEARMONTHDAY_REGEX + r'v[\d.]+\.gz$'),
                utils.create_datetime,
                lambda time: (time - relativedelta(days=6), time + relativedelta(days=1))
            ),
            (
                re.compile(r'/y\d{4}/m\d{2}/f35_' + utils.YEARMONTH_REGEX + r'v[\d.]+\.gz$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(months=1))
            ),
        ],
        'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1': [
            (   # model data over a year, based on observations from 1982 to 2010. TODO: confirm
                re.compile(r'/D(?P<d>\d{3})-.*\.nc$'),
                lambda d: utils.create_datetime(1982, day_of_year=d),
                lambda time: (time, datetime(2010, time.month, time.day).replace(tzinfo=tzutc()))
            )
        ],
        'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3': [
            (
                re.compile(r'/[A-Z\d]+_' + utils.YEARMONTHDAY_REGEX + r'_\d{2}D.*\.h5$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(days=1))
            ),
            (
                re.compile(r'/[A-Z\d]+_' + utils.YEARMONTH_REGEX + r'00_\d{2}M.*\.h5$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(months=1))
            ),
        ],
        'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046/' +
        'dataset-duacs-nrt-global-merged-allsat-phy-l4': [
            (
                re.compile(r'/nrt_global_allsat_phy_l4_' + utils.YEARMONTHDAY_REGEX + r'_.*\.nc$'),
                utils.create_datetime,
                lambda time: (time - relativedelta(hours=12), time + relativedelta(hours=12))
            )
        ],
        'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003': [
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
        ],
        'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/': [
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
            ),
        ],
        'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013': [
            (
                re.compile(utils.YEARMONTHDAY_REGEX + r'_(d|h|hts)-.*\.nc$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(days=1))
            ),
            (
                re.compile(utils.YEARMONTHDAY_REGEX + r'_m-.*\.nc$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(months=1))
            ),
        ],
        'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSIS_FORECAST_PHYS_005_001': [
            (
                re.compile(
                    r'/CMEMS_v4r1_IBI_PHY_NRT_PdE_(15minav|01dav|01hav(3D)?)_' +
                    utils.YEARMONTHDAY_REGEX + r'_.*\.nc$'
                ),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(days=1))
            ),
            (
                re.compile(
                    r'/CMEMS_v4r1_IBI_PHY_NRT_PdE_01mav_' + utils.YEARMONTHDAY_REGEX + r'_.*\.nc$'),
                utils.create_datetime,
                lambda time: (time, time + relativedelta(months=1))
            ),
        ],
        'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/': [
            (
                re.compile(
                    r'/hycom_glb_\w+_' +
                    utils.YEARMONTHDAY_REGEX +
                    r'00_t(?P<hours>\d{3})\.nc\.gz'),
                lambda year, month, day, hours: (
                    utils.create_datetime(year, month, day) + relativedelta(hours=int(hours))),
                lambda time: (time, time + relativedelta(hours=3))
            ),
        ],
        'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod': [
            (
                re.compile(
                    rf'/rtofs\.{utils.YEARMONTHDAY_REGEX}/' +
                    r'rtofs_glo_3dz_[nf](?P<hours>\d{3})_.*\.nc'),
                lambda year, month, day, hours: (
                    utils.create_datetime(year, month, day) + relativedelta(hours=int(hours))),
                lambda time: (time, time)
            ),
            (
                re.compile(
                    rf'/rtofs\.{utils.YEARMONTHDAY_REGEX}/' +
                    r'rtofs_glo_2ds_n(?P<hours>\d{3})_.*\.nc'),
                # the .../rtofs.20210519/rtofs_glo_2ds_n000_prog.nc
                # file has the date 2021-05-18 00:00:00
                lambda year, month, day, hours: (
                    utils.create_datetime(year, month, day)
                    - relativedelta(days=1)
                    + relativedelta(hours=int(hours))),
                lambda time: (time, time)
            ),
            (
                re.compile(
                    rf'/rtofs\.{utils.YEARMONTHDAY_REGEX}/' +
                    r'rtofs_glo_2ds_f(?P<hours>\d{3})_.*\.nc'),
                lambda year, month, day, hours: (
                    utils.create_datetime(year, month, day)
                    + relativedelta(hours=int(hours))),
                lambda time: (time, time)
            ),
        ]
    }

    def find_matching_value(self, associated_dict, raw_attributes):
        """ Loop through <associated_dict> and get the matching value  """
        if 'url' in raw_attributes:
            for url in associated_dict.keys():
                if raw_attributes['url'].startswith(url):
                    attribute = associated_dict[url]
                    if callable(attribute):
                        return attribute(self, raw_attributes['url'])
                    else:
                        return attribute
        return None

    def get_platform(self, raw_attributes):
        """ return the corresponding platfrom based on specified ftp source """
        found_value = self.find_matching_value(self.urls_platforms, raw_attributes)
        if found_value:
            return pti.get_gcmd_platform(found_value)

    def get_instrument(self, raw_attributes):
        """return the corresponding instrument based on specified ftp source """
        found_value = self.find_matching_value(self.urls_instruments, raw_attributes)
        if found_value:
            return pti.get_gcmd_instrument(found_value)

    def find_time_coverage(self, raw_attributes):
        """Find the time coverage based on the 'url' raw attribute.
        Returns a 2-tuple containing the start and end time,
        or a 2-tuple containing None if no time coverage was found.

        This method uses the `urls_time` dictionary.
        This dictionary has the following structure:
        urls_time = {
            'url_prefix': [
                (
                    compiled_regex,
                    datetime_creation_function,
                    time_coverage_function
                ),
                (...)
            ],
            ...
        }
        Where:
          - "url_prefix" is the prefix matched against the 'url' raw
            attribute

          - "compiled_regex" is a compiled regular expresion used to
            extract the time information from the URL. It should
            contain named groups which will be given as arguments
            to the datetime_creation_function

          - "datetime_creation_function" is a function which creates
            a datetime object from the information extracted using
            the regex.

          - "time_coverage_function" is a function which takes the
            datetime object returned by datetime_creation_function
            and returns the time coverage as a 2-tuple
        """
        if 'url' in raw_attributes:
            time_finder = self.find_matching_value(self.urls_time, raw_attributes)
            if time_finder:
                for matcher, get_time, get_coverage in time_finder:
                    match = matcher.search(raw_attributes['url'])
                    if match:
                        file_time = get_time(**match.groupdict())
                        return (get_coverage(file_time)[0], get_coverage(file_time)[1])
        return (None, None)

    def get_time_coverage_start(self, raw_attributes):
        """Returns the start time"""
        return self.find_time_coverage(raw_attributes)[0]

    def get_time_coverage_end(self, raw_attributes):
        """Return the end time"""
        return self.find_time_coverage(raw_attributes)[1]

    def get_provider(self, raw_attributes):
        """ returns the suitable provider based on the filename """
        found_value = self.find_matching_value(self.urls_provider, raw_attributes)
        if found_value:
            return pti.get_gcmd_provider(found_value)

    @staticmethod
    def create_parameter_list(parameters):
        """ Convert list with standard names into list with Pythesing dicts """
        if parameters:
            return [utils.get_cf_or_wkv_standard_name(cf_parameter) for cf_parameter in parameters]

    def get_dataset_parameters(self, raw_attributes):
        """ return list with different parameter(s) from cf_standard_name """
        return self.create_parameter_list(self.find_matching_value(
            self.urls_dataset_parameters, raw_attributes)) or []

    def get_location_geometry(self, raw_attributes):
        """ returns the suitable location geometry based on the filename """
        return self.find_matching_value(self.urls_geometry, raw_attributes)

    def get_entry_title(self, raw_attributes):
        """ returns the suitable entry_title based on the filename """
        return self.find_matching_value(self.urls_title, raw_attributes)

    def get_entry_id(self, raw_attributes):
        """ returns the suitable entry_id based on the filename """
        file_name = None
        if 'url' in raw_attributes:
            for url_start in self.urls_entry_id:
                if raw_attributes['url'].startswith(url_start):
                    try:
                        file_name = self.urls_entry_id[url_start].search(
                            raw_attributes['url']).group(1)
                    except AttributeError:
                        file_name = None
        return file_name

    def get_summary(self, raw_attributes):
        """returns the suitable summary based on the url"""
        return self.find_matching_value(self.urls_summary, raw_attributes)
