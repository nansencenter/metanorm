"""Tests for the CMEMS normalizers"""

import unittest
import unittest.mock as mock
from collections import OrderedDict
from datetime import datetime, timezone

import metanorm.normalizers as normalizers
from .data import DATASET_PARAMETERS


class CMEMSMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the CMEMSMetadataNormalizer base class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMSMetadataNormalizer()

    def test_entry_id(self):
        """Test extracting the entry_id from a URL"""
        self.assertEqual(self.normalizer.get_entry_id({'url': 'ftp://foo/bar/baz123.nc'}), 'baz123')
        self.assertEqual(self.normalizer.get_entry_id({'url': 'ftp://foo/bar/baz123.h5'}), 'baz123')
        self.assertEqual(
            self.normalizer.get_entry_id({'url': 'ftp://foo/bar/baz123.nc.gz'}),
            'baz123')
        self.assertEqual(
            self.normalizer.get_entry_id({'url': 'ftp://foo/bar/baz123.h5.gz'}),
            'baz123')

    def test_provider(self):
        """The provider is always CMEMS"""
        self.assertEqual(
            self.normalizer.get_provider({}),
            OrderedDict([('Bucket_Level0', 'MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1', ''),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'CMEMS'),
                         ('Long_Name', 'Copernicus - Marine Environment Monitoring Service'),
                         ('Data_Center_URL', '')]))

    def test_time_coverage(self):
        """Test that the time coverage is extracted using
        utils.find_time_coverage()
        """
        url = 'ftp://foo/bar.nc'
        raw_metadata = {'url': url}
        with mock.patch('metanorm.utils.find_time_coverage') as mock_find_time_coverage:
            mock_find_time_coverage.return_value = ('start', 'end')

            # test time_coverage_start
            self.assertEqual(self.normalizer.get_time_coverage_start(raw_metadata), 'start')
            mock_find_time_coverage.assert_called_with(self.normalizer.time_patterns, url)

            # test time_coverage_end
            self.assertEqual(self.normalizer.get_time_coverage_end(raw_metadata), 'end')
            mock_find_time_coverage.assert_called_with(self.normalizer.time_patterns, url)


class CMEMS008046MetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the CMEMS008046MetadataNormalizer class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMS008046MetadataNormalizer()

    def test_entry_title(self):
        """entry_title from CMEMS008046MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_entry_title({}),
            'GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT')

    def test_summary(self):
        """summary from CMEMS008046MetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: Altimeter satellite gridded Sea Level Anomalies (SLA) computed with '
            'respect to a twenty-year mean.;'
            'Processing level: 4;'
            'Product: SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046')

    def test_time_coverage_start(self):
        """time_coverage_start from CMEMS008046MetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046/'
                       'dataset-duacs-nrt-global-merged-allsat-phy-l4/2019/04/'
                       'nrt_global_allsat_phy_l4_20190403_20200320.nc'}),
            datetime(year=2019, month=4, day=2, hour=12, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end(self):
        """time_coverage_end from CMEMS008046MetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046/'
                       'dataset-duacs-nrt-global-merged-allsat-phy-l4/2019/04/'
                       'nrt_global_allsat_phy_l4_20190403_20200320.nc'}),
            datetime(year=2019, month=4, day=3, hour=12, minute=0, second=0, tzinfo=timezone.utc))

    def test_platform(self):
        """platform from CMEMS008046MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_platform({}),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                        ('Series_Entity', ''),
                        ('Short_Name', ''),
                        ('Long_Name', '')]))

    def test_instrument(self):
        """instrument from CMEMS008046MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_instrument({}),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Active Remote Sensing'),
                         ('Type', 'Altimeters'),
                         ('Subtype', ''),
                         ('Short_Name', ''),
                         ('Long_Name', '')]))

    def test_location_geometry(self):
        """geometry from CMEMS008046MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_dataset_parameters(self):
        """dataset_parameters from CMEMS008046MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_dataset_parameters({}),
            [
                DATASET_PARAMETERS['sea_surface_height_above_geoid'],
                DATASET_PARAMETERS['sea_surface_height_above_sea_level'],
                DATASET_PARAMETERS['surface_geostrophic_eastward_sea_water_velocity'],
                DATASET_PARAMETERS['surface_geostrophic_eastward_sea_water_velocity_'
                                   'assuming_mean_sea_level_for_geoid'],
                DATASET_PARAMETERS['surface_geostrophic_northward_sea_water_velocity'],
                DATASET_PARAMETERS['surface_geostrophic_northward_sea_water_velocity_'
                                        'assuming_mean_sea_level_for_geoid'],
            ])


class CMEMS015003MetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the CMEMS015003MetadataNormalizer class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMS015003MetadataNormalizer()

    def test_entry_title(self):
        """entry_title from CMEMS015003MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_entry_title({}),
            'GLOBAL TOTAL SURFACE AND 15M CURRENT FROM ALTIMETRIC '
            'GEOSTROPHIC CURRENT AND MODELED EKMAN CURRENT PROCESSING')

    def test_summary(self):
        """summary from CMEMS015003MetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: This product is a NRT L4 global total velocity field at 0m and 15m.;'
            'Processing level: 4;'
            'Product: MULTIOBS_GLO_PHY_NRT_015_003')

    def test_time_coverage_start_daily(self):
        """time_coverage_start from CMEMS015003MetadataNormalizer for a
        daily file
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/'
                       'dataset-uv-nrt-daily/2020/03/'
                       'dataset-uv-nrt-daily_20200301T0000Z_P20200307T0000.nc'}),
            datetime(year=2020, month=3, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_monthly(self):
        """time_coverage_start from CMEMS015003MetadataNormalizer for a
        monthly file
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/'
                       'dataset-uv-nrt-monthly/2020/'
                       'dataset-uv-nrt-monthly_202004T0000Z_P20200506T0000.nc'}),
            datetime(year=2020, month=4, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_hourly(self):
        """time_coverage_start from CMEMS015003MetadataNormalizer for a
        hourly file
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/'
                       'dataset-uv-nrt-hourly/2020/09/'
                       'dataset-uv-nrt-hourly_20200906T0000Z_P20200912T0000.nc'}),
            datetime(year=2020, month=9, day=6, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_daily(self):
        """time_coverage_end from CMEMS015003MetadataNormalizer for a
        daily file
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/'
                       'dataset-uv-nrt-daily/2020/03/'
                       'dataset-uv-nrt-daily_20200302T0000Z_P20200307T0000.nc'}),
            datetime(year=2020, month=3, day=3, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_monthly(self):
        """time_coverage_end from CMEMS015003MetadataNormalizer for a
        monthly file
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/'
                       'dataset-uv-nrt-monthly/2020/'
                       'dataset-uv-nrt-monthly_202004T0000Z_P20200506T0000.nc'}),
            datetime(year=2020, month=5, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_hourly(self):
        """time_coverage_end from CMEMS015003MetadataNormalizer for a
        hourly file
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/'
                       'dataset-uv-nrt-hourly/2020/09/'
                       'dataset-uv-nrt-hourly_20200906T0000Z_P20200918T0000.nc'}),
            datetime(year=2020, month=9, day=7, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_platform(self):
        """platform from CMEMS015003MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_platform({}),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                        ('Series_Entity', ''),
                        ('Short_Name', ''),
                        ('Long_Name', '')]))

    def test_instrument(self):
        """instrument from CMEMS015003MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_instrument({}),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Active Remote Sensing'),
                         ('Type', 'Altimeters'),
                         ('Subtype', ''),
                         ('Short_Name', ''),
                         ('Long_Name', '')]))

    def test_location_geometry(self):
        """geometry from CMEMS015003MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_dataset_parameters(self):
        """dataset_parameters from CMEMS015003MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_dataset_parameters({}),
            [
                DATASET_PARAMETERS['eastward_sea_water_velocity'],
                DATASET_PARAMETERS['northward_sea_water_velocity']
            ])


class CMEMS001024MetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the CMEMS001024MetadataNormalizer class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMS001024MetadataNormalizer()

    def test_entry_title(self):
        """entry_title from CMEMS001024MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_entry_title({}),
            'GLOBAL OCEAN 1_12 PHYSICS ANALYSIS AND FORECAST UPDATED DAILY')

    def test_summary(self):
        """summary from CMEMS001024MetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: The Operational Mercator global ocean analysis and forecast system at '
            '1/12 degree is providing 10 days of 3D global ocean forecasts updated daily.;'
            'Processing level: 4;'
            'Product: GLOBAL_ANALYSIS_FORECAST_PHY_001_024')

    def test_time_coverage_start(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                       'global-analysis-forecast-phy-001-024/2016/03/'
                       'mercatorpsy4v3r1_gl12_mean_20160303_R20160316.nc'}),
            datetime(year=2016, month=3, day=3, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_3dinst_so(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer for a
        3dinst_so dataset
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                'global-analysis-forecast-phy-001-024-3dinst-so/2019/04/'
                'mercatorpsy4v3r1_gl12_so_20190403_18h_R20190404.nc'}),
            datetime(year=2019, month=4, day=3, hour=18, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_3dinst_thetao(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer for a
        3dinst_thetao dataset"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                'global-analysis-forecast-phy-001-024-3dinst-thetao/2020/04/'
                'mercatorpsy4v3r1_gl12_thetao_20200404_18h_R20200405.nc'}),
            datetime(year=2020, month=4, day=4, hour=18, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_3dinst_uovo(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer for a
        3dinst_uovo dataset"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                'global-analysis-forecast-phy-001-024-3dinst-uovo/2020/04/'
                'mercatorpsy4v3r1_gl12_uovo_20200403_06h_R20200404.nc'}),
            datetime(year=2020, month=4, day=3, hour=6, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_hourly_merged_uv(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer for a
        hourly_merged_uv dataset"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                'global-analysis-forecast-phy-001-024-hourly-merged-uv/2019/05/'
                'SMOC_20190515_R20190516.nc'}),
            datetime(year=2019, month=5, day=15, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_hourly_t_u_v_ssh(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer for a
        hourly_t_u_v_ssh dataset"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                'global-analysis-forecast-phy-001-024-hourly-t-u-v-ssh/2020/05/'
                'mercatorpsy4v3r1_gl12_hrly_20200511_R20200520.nc'}),
            datetime(year=2020, month=5, day=11, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_monthly(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer for a
        monthly dataset"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                'global-analysis-forecast-phy-001-024-monthly/2018/'
                'mercatorpsy4v3r1_gl12_mean_201807.nc'}),
            datetime(year=2018, month=7, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                       'global-analysis-forecast-phy-001-024/2016/03/'
                       'mercatorpsy4v3r1_gl12_mean_20160303_R20160316.nc'}),
            datetime(year=2016, month=3, day=4, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_3dinst_so(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer for a
        3dinst_so dataset
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                       'global-analysis-forecast-phy-001-024-3dinst-so/2019/04/'
                       'mercatorpsy4v3r1_gl12_so_20190403_18h_R20190404.nc'}),
            datetime(year=2019, month=4, day=3, hour=18, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_3dinst_thetao(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer for a
        3dinst_thetao dataset
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                       'global-analysis-forecast-phy-001-024-3dinst-thetao/2020/04/'
                       'mercatorpsy4v3r1_gl12_thetao_20200404_18h_R20200405.nc'}),
            datetime(year=2020, month=4, day=4, hour=18, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_3dinst_uovo(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer for a
        3dinst_uovo dataset
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                       'global-analysis-forecast-phy-001-024-3dinst-uovo/2020/04/'
                       'mercatorpsy4v3r1_gl12_uovo_20200403_06h_R20200404.nc'}),
            datetime(year=2020, month=4, day=3, hour=6, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_hourly_merged_uv(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer for a
        hourly_merged_uv dataset
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                       'global-analysis-forecast-phy-001-024-hourly-merged-uv/2019/05/'
                       'SMOC_20190515_R20190516.nc'}),
            datetime(year=2019, month=5, day=16, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_hourly_t_u_v_ssh(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer for a
        hourly_t_u_v_ssh dataset
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                       'global-analysis-forecast-phy-001-024-hourly-t-u-v-ssh/2020/05/'
                       'mercatorpsy4v3r1_gl12_hrly_20200511_R20200520.nc'}),
            datetime(year=2020, month=5, day=12, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_monthly(self):
        """time_coverage_start from CMEMS001024MetadataNormalizer for a
        monthly dataset
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                       'global-analysis-forecast-phy-001-024-monthly/2018/'
                       'mercatorpsy4v3r1_gl12_mean_201807.nc'}),
            datetime(year=2018, month=8, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_platform(self):
        """platform from CMEMS001024MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_platform({}),
            OrderedDict([('Category', 'Models/Analyses'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'OPERATIONAL MODELS'),
                         ('Long_Name', '')]))

    def test_instrument(self):
        """instrument from CMEMS001024MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_instrument({}),
            OrderedDict([('Category', 'In Situ/Laboratory Instruments'),
                         ('Class', 'Data Analysis'),
                         ('Type', 'Environmental Modeling'),
                         ('Subtype', ''),
                         ('Short_Name', 'Computer'),
                         ('Long_Name', 'Computer')]))

    def test_location_geometry(self):
        """geometry from CMEMS001024MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_dataset_parameters(self):
        """dataset_parameters from CMEMS001024MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_dataset_parameters({}),
            [
                DATASET_PARAMETERS['sea_water_potential_temperature_at_sea_floor'],
                DATASET_PARAMETERS['ocean_mixed_layer_thickness_defined_by_sigma_theta'],
                DATASET_PARAMETERS['sea_ice_area_fraction'],
                DATASET_PARAMETERS['sea_ice_thickness'],
                DATASET_PARAMETERS['sea_water_salinity'],
                DATASET_PARAMETERS['sea_water_potential_temperature'],
                DATASET_PARAMETERS['eastward_sea_water_velocity'],
                DATASET_PARAMETERS['eastward_sea_ice_velocity'],
                DATASET_PARAMETERS['northward_sea_water_velocity'],
                DATASET_PARAMETERS['northward_sea_ice_velocity'],
                DATASET_PARAMETERS['sea_surface_height_above_geoid']
            ])


class CMEMS006013MetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the CMEMS006013MetadataNormalizer class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMS006013MetadataNormalizer()

    def test_entry_title(self):
        """entry_title from CMEMS006013MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_entry_title({}),
            'Mediterranean Forecasting System (hydrodynamic-wave model)')

    def test_summary(self):
        """summary from CMEMS006013MetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: The physical component of the Mediterranean Forecasting System '
            '(Med-Currents) is a coupled hydrodynamic-wave model implemented over the whole '
            'Mediterranean Basin.;'
            'Processing level: 4;'
            'Product: MEDSEA_ANALYSISFORECAST_PHY_006_013')

    def test_time_coverage_start_daily_mean(self):
        """Should return the proper starting time for a daily mean file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/'
               'med-cmcc-cur-an-fc-d/2020/06/'
               '20200601_d-CMCC--RFVL-MFSeas6-MEDATL-b20210101_an-sv07.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'url': url}),
            datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_hourly_mean(self):
        """Should return the proper starting time for an hourly mean file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/'
               'med-cmcc-cur-an-fc-h/2021/06/'
               '20210601_h-CMCC--RFVL-MFSeas6-MEDATL-b20210615_an-sv07.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'url': url}),
            datetime(year=2021, month=6, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_15min_inst(self):
        """Should return the proper starting time for a 15 min instantaneous file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/'
               'med-cmcc-cur-an-fc-qm/2020/05/'
               '20200502_qm-CMCC--RFVL-MFSeas6-MEDATL-b20210101_an-sv07.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'url': url}),
            datetime(year=2020, month=5, day=2, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_hourly_mean_hts(self):
        """Should return the proper starting time for an hts hourly mean file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/'
               'med-cmcc-cur-an-fc-hts/2021/06/'
               '20210601_hts-CMCC--RFVL-MFSeas6-MEDATL-b20210615_an-sv07.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'url': url}),
            datetime(year=2021, month=6, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_month(self):
        """Should return the proper starting time"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/'
               'med-cmcc-cur-an-fc-m/2021/'
               '20210601_m-CMCC--RFVL-MFSeas6-MEDATL-b20210713_an-sv07.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'url': url}),
            datetime(year=2021, month=6, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_daily_mean(self):
        """Should return the proper ending time for a daily mean file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/'
               'med-cmcc-cur-an-fc-d/2020/06/'
               '20200601_d-CMCC--RFVL-MFSeas6-MEDATL-b20210101_an-sv07.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'url': url}),
            datetime(year=2020, month=6, day=2, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_hourly_mean(self):
        """Should return the proper ending time for an hourly mean file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/'
               'med-cmcc-cur-an-fc-h/2021/06/'
               '20210601_h-CMCC--RFVL-MFSeas6-MEDATL-b20210615_an-sv07.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'url': url}),
            datetime(year=2021, month=6, day=2, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_hourly_mean_hts(self):
        """Should return the proper ending time for an hts hourly mean file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/'
               'med-cmcc-cur-an-fc-hts/2021/06/'
               '20210601_hts-CMCC--RFVL-MFSeas6-MEDATL-b20210615_an-sv07.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'url': url}),
            datetime(year=2021, month=6, day=2, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_15min_inst(self):
        """Should return the proper ending time for a 15 min instantaneous file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/'
               'med-cmcc-cur-an-fc-qm/2020/05/'
               '20200502_qm-CMCC--RFVL-MFSeas6-MEDATL-b20210101_an-sv07.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'url': url}),
            datetime(year=2020, month=5, day=3, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_month(self):
        """Should return the proper ending time"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/'
               'med-cmcc-cur-an-fc-m/2021/'
               '20210601_m-CMCC--RFVL-MFSeas6-MEDATL-b20210713_an-sv07.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'url': url}),
            datetime(year=2021, month=7, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_platform(self):
        """platform from CMEMS006013MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_platform({}),
            OrderedDict([('Category', 'Models/Analyses'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'OPERATIONAL MODELS'),
                         ('Long_Name', '')]))

    def test_instrument(self):
        """instrument from CMEMS006013MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_instrument({}),
            OrderedDict([('Category', 'In Situ/Laboratory Instruments'),
                         ('Class', 'Data Analysis'),
                         ('Type', 'Environmental Modeling'),
                         ('Subtype', ''),
                         ('Short_Name', 'Computer'),
                         ('Long_Name', 'Computer')]))

    def test_location_geometry(self):
        """geometry from CMEMS006013MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-17.29 45.98, -17.29 30.18, 36.30 30.18, 36.30 45.98, -17.29 45.98))')

    def test_dataset_parameters_cur(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/med-cmcc-cur'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes), [
                DATASET_PARAMETERS['eastward_sea_water_velocity'],
                DATASET_PARAMETERS['northward_sea_water_velocity']
            ])

    def test_dataset_parameters_mld(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/med-cmcc-mld'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes), [
                DATASET_PARAMETERS['ocean_mixed_layer_thickness_defined_by_sigma_theta']
            ])

    def test_dataset_parameters_sal(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/med-cmcc-sal'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [DATASET_PARAMETERS['sea_water_salinity']])

    def test_dataset_parameters_ssh(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/med-cmcc-ssh'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [DATASET_PARAMETERS['sea_surface_height_above_geoid']])

    def test_dataset_parameters_tem(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/med-cmcc-tem'}
        self.assertEqual(self.normalizer.get_dataset_parameters(attributes), [
            DATASET_PARAMETERS['sea_water_potential_temperature_at_sea_floor'],
            DATASET_PARAMETERS['sea_water_potential_temperature']
        ])

    def test_dataset_parameters_mask_bathy(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/" +
                   "MEDSEA_ANALYSISFORECAST_PHY_006_013-statics/MED-MFC_006_013_mask_bathy.nc"
        }
        self.assertEqual(self.normalizer.get_dataset_parameters(attributes), [
            DATASET_PARAMETERS['model_level_number_at_sea_floor'],
            DATASET_PARAMETERS['sea_binary_mask'],
            DATASET_PARAMETERS['sea_floor_depth_below_geoid'],
        ])

    def test_dataset_parameters_coordinates(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/" +
                   "MEDSEA_ANALYSISFORECAST_PHY_006_013-statics/MED-MFC_006_013_coordinates.nc"
        }
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [DATASET_PARAMETERS['cell_thickness']])

    def test_dataset_parameters_mdt(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/" +
                   "MEDSEA_ANALYSISFORECAST_PHY_006_013-statics/MED-MFC_006_013_mdt.nc"
        }
        self.assertEqual(self.normalizer.get_dataset_parameters(attributes), [
            DATASET_PARAMETERS['sea_surface_height_above_geoid'],
        ])
