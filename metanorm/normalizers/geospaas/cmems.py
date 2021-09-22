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
