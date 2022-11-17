
"""Tests for the CMEMS normalizers"""

import unittest
import unittest.mock as mock
from datetime import datetime, timezone

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


class GCMDTestsBuiltin():
    """Builtin used to easily add test methods for GCMD searches
    """

    def test_gcmd_platform(self):
        """Test getting the platform"""
        with mock.patch('metanorm.utils.get_gcmd_platform') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_platform(mock.MagicMock()),
                mock_get_gcmd_method.return_value)

    def test_gcmd_instrument(self):
        """Test getting the instrument"""
        with mock.patch('metanorm.utils.get_gcmd_instrument') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_instrument(mock.MagicMock()),
                mock_get_gcmd_method.return_value)

    def test_dataset_parameters(self):
        """Test getting the dataset parameters"""
        with mock.patch('metanorm.utils.create_parameter_list') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(mock.MagicMock()),
                mock_get_gcmd_method.return_value)


class CMEMSMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the CMEMSMetadataNormalizer base class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMSMetadataNormalizer()

    def test_check(self):
        """check() should always return False for the base class"""
        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': ''}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo'}))

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

    def test_entry_id_error(self):
        """a MetadataNormalizationError must be raised when an entry_id cannot be found"""
        # wrong file format
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({'url': 'ftp://foo/bar.txt'})
        # no url attribute
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})

    def test_gcmd_provider(self):
        """Test getting the provider"""
        with mock.patch('metanorm.utils.get_gcmd_provider') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_provider({}),
                mock_get_gcmd_method.return_value)

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

    def test_time_coverage_start_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_time_coverage_end_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})


class CMEMS008046MetadataNormalizerTestCase(GCMDTestsBuiltin, unittest.TestCase):
    """Tests for the CMEMS008046MetadataNormalizer class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMS008046MetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046/'
                   'dataset-duacs-nrt-global-merged-allsat-phy-l4/2020/06/'
                   'nrt_global_allsat_phy_l4_20200623_20200629.nc'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

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

    def test_location_geometry(self):
        """geometry from CMEMS008046MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')


class CMEMS015003MetadataNormalizerTestCase(GCMDTestsBuiltin, unittest.TestCase):
    """Tests for the CMEMS015003MetadataNormalizer class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMS015003MetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/dataset-uv-nrt-daily/'
                   '2021/05/dataset-uv-nrt-daily_20210512T0900Z_P20210707T0000.nc'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

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

    def test_location_geometry(self):
        """geometry from CMEMS015003MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')


class CMEMS001024MetadataNormalizerTestCase(GCMDTestsBuiltin, unittest.TestCase):
    """Tests for the CMEMS001024MetadataNormalizer class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMS001024MetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/'
                   'global-analysis-forecast-phy-001-024/2020/12/'
                   'mercatorpsy4v3r1_gl12_mean_20201223_R20210106.nc'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

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

    def test_location_geometry(self):
        """geometry from CMEMS001024MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')


class CMEMS006013MetadataNormalizerTestCase(GCMDTestsBuiltin, unittest.TestCase):
    """Tests for the CMEMS006013MetadataNormalizer class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMS006013MetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/'
                   'med-cmcc-cur-an-fc-d/2019/12/'
                   '20191201_d-CMCC--RFVL-MFSeas6-MEDATL-b20210101_an-sv07.00.nc'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

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

    def test_location_geometry(self):
        """geometry from CMEMS006013MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-17.29 45.98, -17.29 30.18, 36.30 30.18, 36.30 45.98, -17.29 45.98))')

    def test_dataset_parameters_cur(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/med-cmcc-cur'
        }
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(attributes),
                mock_utils_method.return_value)
            mock_utils_method.assert_called_once_with(
                (
                    'eastward_sea_water_velocity',
                    'northward_sea_water_velocity',
                )
            )

    def test_dataset_parameters_mld(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/med-cmcc-mld'
        }
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(attributes),
                mock_utils_method.return_value)
            mock_utils_method.assert_called_once_with(
                (
                    'ocean_mixed_layer_thickness_defined_by_sigma_theta',
                )
            )

    def test_dataset_parameters_sal(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/med-cmcc-sal'
        }
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(attributes),
                mock_utils_method.return_value)
            mock_utils_method.assert_called_once_with(
                (
                    'sea_water_salinity',
                )
            )

    def test_dataset_parameters_ssh(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/med-cmcc-ssh'
        }
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(attributes),
                mock_utils_method.return_value)
            mock_utils_method.assert_called_once_with(
                (
                    'sea_surface_height_above_geoid',
                )
            )

    def test_dataset_parameters_tem(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/med-cmcc-tem'
        }
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(attributes),
                mock_utils_method.return_value)
            mock_utils_method.assert_called_once_with(
                (
                    'sea_water_potential_temperature_at_sea_floor',
                    'sea_water_potential_temperature',
                )
            )

    def test_dataset_parameters_mask_bathy(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/" +
                   "MEDSEA_ANALYSISFORECAST_PHY_006_013-statics/MED-MFC_006_013_mask_bathy.nc"
        }
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(attributes),
                mock_utils_method.return_value)
            mock_utils_method.assert_called_once_with(
                (
                    'model_level_number_at_sea_floor',
                    'sea_binary_mask',
                    'sea_floor_depth_below_geoid',
                )
            )

    def test_dataset_parameters_coordinates(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/" +
                   "MEDSEA_ANALYSISFORECAST_PHY_006_013-statics/MED-MFC_006_013_coordinates.nc"
        }
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(attributes),
                mock_utils_method.return_value)
            mock_utils_method.assert_called_once_with(
                (
                    'cell_thickness',
                )
            )

    def test_dataset_parameters_mdt(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSISFORECAST_PHY_006_013/" +
                   "MEDSEA_ANALYSISFORECAST_PHY_006_013-statics/MED-MFC_006_013_mdt.nc"
        }
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(attributes),
                mock_utils_method.return_value)
            mock_utils_method.assert_called_once_with(
                (
                    'sea_surface_height_above_geoid',
                )
            )

    def test_dataset_parameters_unknown_url(self):
        """Should return an empty list if the URL starts with an
        unknown prefix
        """
        self.assertListEqual(self.normalizer.get_dataset_parameters({'url': 'https://foo'}), [])

    def test_dataset_parameters_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_dataset_parameters({})


class CMEMS005001MetadataNormalizerTestCase(GCMDTestsBuiltin, unittest.TestCase):
    """Tests for the CMEMS005001MetadataNormalizer class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMS005001MetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                   'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT1H-m/2020/02/'
                   'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav_20200217_20200217_R20200219_AN06.nc'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

    def test_entry_title(self):
        """entry_title from CMEMS005001MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_entry_title({}),
            'Atlantic-Iberian Biscay Irish-Ocean Physics Analysis and Forecast')

    def test_summary(self):
        """summary from CMEMS005001MetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: The operational IBI (Iberian Biscay Irish) Ocean Analysis and Forecasting'
            ' system provides a 5-day hydrodynamic forecast including high frequency '
            'processes of paramount importance to characterize regional scale marine '
            'processes.;'
            'Processing level: 4;'
            'Product: IBI_ANALYSISFORECAST_PHY_005_001')

    def test_time_coverage_start_15min(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT15M-m/2020/12/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_15minav_20201212_20201212_R20201221_AN04.nc'
            }),
            datetime(year=2020, month=12, day=12, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_daily(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-3D_P1D-m/2021/05/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01dav_20210503_20210503_R20210510_AN06.nc'
            }),
            datetime(year=2021, month=5, day=3, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_hourly(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT1H-m/2019/11/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav_20191112_20191112_R20191113_AN07.nc'
            }),
            datetime(year=2019, month=11, day=12, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_hourly3d(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-3D_PT1H-m/2021/08/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav3D_20210815_20210815_R20210816_HC01.nc'
            }),
            datetime(year=2021, month=8, day=15, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_monthly(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-3D_P1M-m/2019/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01mav_20191001_20191031_R20191031_AN01.nc'
            }),
            datetime(year=2019, month=10, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_15min(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT15M-m/2020/12/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_15minav_20201212_20201212_R20201221_AN04.nc'
            }),
            datetime(year=2020, month=12, day=13, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_daily(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-3D_P1D-m/2021/05/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01dav_20210503_20210503_R20210510_AN06.nc'
            }),
            datetime(year=2021, month=5, day=4, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_hourly(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT1H-m/2019/11/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav_20191112_20191112_R20191113_AN07.nc'
            }),
            datetime(year=2019, month=11, day=13, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_hourly3d(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-3D_PT1H-m/2021/08/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav3D_20210815_20210815_R20210816_HC01.nc'
            }),
            datetime(year=2021, month=8, day=16, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_monthly(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-3D_P1M-m/2019/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01mav_20191001_20191031_R20191031_AN01.nc'
            }),
            datetime(year=2019, month=11, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_location_geometry(self):
        """geometry from CMEMS005001MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-19 56, 5 56, 5 26, -19 26, -19 56))')

    def test_dataset_parameters_15min(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                   'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT15M-m/2020/12/'
                   'CMEMS_v5r1_IBI_PHY_NRT_PdE_15minav_20201212_20201212_R20201221_AN04.nc'
        }
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(attributes),
                mock_utils_method.return_value)
            mock_utils_method.assert_called_once_with(
                (
                    'sea_surface_height_above_geoid',
                    'eastward_sea_water_velocity',
                    'northward_sea_water_velocity',
                )
            )

    def test_dataset_parameters_daily(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
            'cmems_mod_ibi_phy_anfc_0.027deg-3D_P1D-m/2021/05/'
            'CMEMS_v5r1_IBI_PHY_NRT_PdE_01dav_20210503_20210503_R20210510_AN06.nc'
        }
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(attributes),
                mock_utils_method.return_value)
            mock_utils_method.assert_called_once_with(
                (
                    'sea_water_potential_temperature',
                    'sea_water_salinity',
                    'eastward_sea_water_velocity',
                    'northward_sea_water_velocity',
                    'sea_surface_height_above_geoid',
                    'ocean_mixed_layer_thickness_defined_by_sigma_theta',
                    'sea_water_potential_temperature_at_sea_floor',
                )
            )

    def test_dataset_parameters_hourly(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
            'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT1H-m/2019/11/'
            'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav_20191112_20191112_R20191113_AN07.nc'
        }
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(attributes),
                mock_utils_method.return_value)
            mock_utils_method.assert_called_once_with(
                (
                    'sea_water_potential_temperature',
                    'eastward_sea_water_velocity',
                    'northward_sea_water_velocity',
                    'barotropic_eastward_sea_water_velocity',
                    'barotropic_northward_sea_water_velocity',
                    'sea_surface_height_above_geoid',
                    'ocean_mixed_layer_thickness_defined_by_sigma_theta',
                )
            )

    def test_dataset_parameters_hourly3d(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
            'cmems_mod_ibi_phy_anfc_0.027deg-3D_PT1H-m/2021/08/'
            'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav3D_20210815_20210815_R20210816_HC01.nc'
        }
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(attributes),
                mock_utils_method.return_value)
            mock_utils_method.assert_called_once_with(
                (
                    'sea_water_potential_temperature',
                    'sea_water_salinity',
                    'eastward_sea_water_velocity',
                    'northward_sea_water_velocity',
                )
            )

    def test_dataset_parameters_monthly(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                   'cmems_mod_ibi_phy_anfc_0.027deg-3D_P1M-m/2019/'
                   'CMEMS_v5r1_IBI_PHY_NRT_PdE_01mav_20191001_20191031_R20191031_AN01.nc'
        }
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters(attributes),
                mock_utils_method.return_value)
            mock_utils_method.assert_called_once_with(
                (
                    'sea_water_potential_temperature',
                    'sea_water_salinity',
                    'eastward_sea_water_velocity',
                    'northward_sea_water_velocity',
                    'sea_surface_height_above_geoid',
                    'ocean_mixed_layer_thickness_defined_by_sigma_theta',
                    'sea_water_potential_temperature_at_sea_floor'
                )
            )

    def test_dataset_parameters_unknown_url(self):
        """Should return an empty list if the URL starts with an
        unknown prefix
        """
        self.assertListEqual(self.normalizer.get_dataset_parameters({'url': 'https://foo'}), [])

    def test_dataset_parameters_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_dataset_parameters({})


class CMEMS002003MetadataNormalizerTestCase(GCMDTestsBuiltin, unittest.TestCase):
    """Tests for the CMEMS002003MetadataNormalizer class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMS002003MetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': 'ftp://my.cmems-du.eu/Core/ARCTIC_MULTIYEAR_PHY_002_003/'
                    'cmems_mod_arc_phy_my_topaz4_P1D-m/2021/02/'
                    '20210204_dm-12km-NERSC-MODEL-TOPAZ4B-ARC-RAN.fv2.0.nc'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

    def test_entry_title(self):
        """test getting entry_title"""
        self.assertEqual(
            self.normalizer.get_entry_title({}),
            'Arctic Ocean Physics Reanalysis')

    def test_summary(self):
        """test getting summary"""
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: The current version of the TOPAZ system - TOPAZ4b - is nearly identical '
                'to the real-time forecast system run at MET Norway. It uses a recent version of '
                'the Hybrid Coordinate Ocean Model (HYCOM) developed at University of Miami (Bleck '
                '2002). HYCOM is coupled to a sea ice model; ice thermodynamics are described in '
                'Drange and Simonsen (1996) and the elastic-viscous-plastic rheology in Hunke and '
                'Dukowicz (1997).;'
            'Processing level: 4;'
            'Product: ARCTIC_MULTIYEAR_PHY_002_003')

    def test_time_coverage_start_dm(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://my.cmems-du.eu/Core/ARCTIC_MULTIYEAR_PHY_002_003/'
                       'cmems_mod_arc_phy_my_topaz4_P1D-m/2021/02/'
                       '20210204_dm-12km-NERSC-MODEL-TOPAZ4B-ARC-RAN.fv2.0.nc'
            }),
            datetime(year=2021, month=2, day=4, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_mm(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://my.cmems-du.eu/Core/ARCTIC_MULTIYEAR_PHY_002_003/'
                       'cmems_mod_arc_phy_my_topaz4_P1M/'
                       '19910115_mm-12km-NERSC-MODEL-TOPAZ4B-ARC-RAN.fv2.0.nc'
            }),
            datetime(year=1991, month=1, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_ym(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://my.cmems-du.eu/Core/ARCTIC_MULTIYEAR_PHY_002_003/'
                'cmems_mod_arc_phy_my_topaz4_P1M/'
                '19910101_ym-12km-NERSC-MODEL-TOPAZ4B-ARC-RAN.fv2.0.nc'
            }),
            datetime(year=1991, month=1, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_dm(self):
        """Should return the proper end time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://my.cmems-du.eu/Core/ARCTIC_MULTIYEAR_PHY_002_003/'
                       'cmems_mod_arc_phy_my_topaz4_P1D-m/2021/02/'
                       '20210204_dm-12km-NERSC-MODEL-TOPAZ4B-ARC-RAN.fv2.0.nc'
            }),
            datetime(year=2021, month=2, day=5, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_mm(self):
        """Should return the proper end time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://my.cmems-du.eu/Core/ARCTIC_MULTIYEAR_PHY_002_003/'
                       'cmems_mod_arc_phy_my_topaz4_P1M/'
                       '19910115_mm-12km-NERSC-MODEL-TOPAZ4B-ARC-RAN.fv2.0.nc'
            }),
            datetime(year=1991, month=2, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_ym(self):
        """Should return the proper end time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://my.cmems-du.eu/Core/ARCTIC_MULTIYEAR_PHY_002_003/'
                       'cmems_mod_arc_phy_my_topaz4_P1M/'
                       '19910101_ym-12km-NERSC-MODEL-TOPAZ4B-ARC-RAN.fv2.0.nc'
            }),
            datetime(year=1992, month=1, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_location_geometry(self):
        """test getting geometry"""
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 53, -180 90, 180 90, 180 53, -180 53))')


class CMEMS002001aMetadataNormalizerTestCase(GCMDTestsBuiltin, unittest.TestCase):
    """Tests for the CMEMS002001aMetadataNormalizer class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMS002001aMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': 'ftp://nrt.cmems-du.eu/Core/ARCTIC_ANALYSIS_FORECAST_PHYS_002_001_a/'
                   'dataset-topaz4-arc-myoceanv2-be/'
                   '20180104_dm-metno-MODEL-topaz4-ARC-b20180108-fv02.0.nc'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

    def test_entry_title(self):
        """test getting entry_title"""
        self.assertEqual(
            self.normalizer.get_entry_title({}),
            'Arctic Ocean Physics Analysis and Forecast')

    def test_summary(self):
        """test getting summary"""
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: The operational TOPAZ4 Arctic Ocean system uses the HYCOM model and a '
            '100-member EnKF assimilation scheme. It is run daily to provide 10 days of forecast'
            '(average of 10 members) of the 3D physical ocean, including sea ice data assimilation '
            'is performed weekly to provide 7 days of analysis(ensemble average). Output products '
            'are interpolated on a grid of 12.5 km resolution at the North Pole (equivalent to '
            '1/8 deg in mid-latitudes) on a polar stereographic projection.;'
            'Processing level: 4;'
            'Product: ARCTIC_ANALYSIS_FORECAST_PHYS_002_001_a')

    def test_time_coverage_start_dm(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/ARCTIC_ANALYSIS_FORECAST_PHYS_002_001_a/'
                       'dataset-topaz4-arc-myoceanv2-be/'
                       '20180104_dm-metno-MODEL-topaz4-ARC-b20180108-fv02.0.nc'
            }),
            datetime(year=2018, month=1, day=4, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_hourly(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/ARCTIC_ANALYSIS_FORECAST_PHYS_002_001_a/'
                       'dataset-topaz4-arc-1hr-myoceanv2-be/'
                       '20180102_hr-metno-MODEL-topaz4-ARC-b20180102-fv02.0.nc'
            }),
            datetime(year=2018, month=1, day=2, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_dm(self):
        """Should return the proper end time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/ARCTIC_ANALYSIS_FORECAST_PHYS_002_001_a/'
                       'dataset-topaz4-arc-myoceanv2-be/'
                       '20180104_dm-metno-MODEL-topaz4-ARC-b20180108-fv02.0.nc'
            }),
            datetime(year=2018, month=1, day=5, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_hourly(self):
        """Should return the proper end time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/ARCTIC_ANALYSIS_FORECAST_PHYS_002_001_a/'
                       'dataset-topaz4-arc-1hr-myoceanv2-be/'
                       '20180102_hr-metno-MODEL-topaz4-ARC-b20180102-fv02.0.nc'
            }),
            datetime(year=2018, month=1, day=3, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_location_geometry(self):
        """test getting geometry"""
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 62, -180 90, 180 90, 180 62, -180 62))')

    def test_unknown_parameters(self):
        """In case of unknown parameters, return an empty list"""
        self.assertEqual(self.normalizer.get_dataset_parameters({'url': 'https://foo'}), [])


class CMEMS002001MetadataNormalizerTestCase(GCMDTestsBuiltin, unittest.TestCase):
    """Tests for the CMEMS002001MetadataNormalizer class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMS002001MetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_phy_dm_files/2022/'
                   '09/20220929_dm-metno-MODEL-topaz5-ARC-b20220922-fv02.0.nc.html'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'https://foo/bar'}))

    def test_provider(self):
        """Test that we get the right provider if a CMEMS URL is used
        """
        with mock.patch('metanorm.utils.get_gcmd_provider') as mock_get_provider:
            self.normalizer.get_provider({})
            mock_get_provider.assert_called_with(['NO/MET'])

    def test_entry_title(self):
        """test getting entry_title"""
        self.assertEqual(
            self.normalizer.get_entry_title({}),
            'Arctic Ocean Physics Analysis and Forecast, 6.25 km')

    def test_summary(self):
        """test getting summary"""
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: TOPAZ 5 physical model;'
            'Processing level: 4;'
            'Product: ARCTIC_ANALYSISFORECAST_PHY_002_001')

    def test_time_coverage_start_dm(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_phy_dm_files/2022/09/'
                       '20220929_dm-metno-MODEL-topaz5-ARC-b20220922-fv02.0.nc.html'
            }),
            datetime(year=2022, month=9, day=29, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_hourly(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_phy_hr_files/2021/11/'
                       '20211130_hr-metno-MODEL-topaz5-ARC-b20211130-fv02.0.nc.html'
            }),
            datetime(year=2021, month=11, day=30, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_dm(self):
        """Should return the proper end time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_phy_dm_files/2022/09/'
                       '20220929_dm-metno-MODEL-topaz5-ARC-b20220922-fv02.0.nc.html'
            }),
            datetime(year=2022, month=9, day=30, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_hourly(self):
        """Should return the proper end time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_phy_hr_files/2021/11/'
                       '20211130_hr-metno-MODEL-topaz5-ARC-b20211130-fv02.0.nc.html'
            }),
            datetime(year=2021, month=12, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_location_geometry(self):
        """test getting geometry"""
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 50, -180 90, 180 90, 180 50, -180 50))')

    def test_dataset_parameters(self):
        """Test getting the dataset parameters"""
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            with self.subTest('hourly'):
                attributes = {
                    'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_phy_hr_files/2021/11/'
                        '20211130_hr-metno-MODEL-topaz5-ARC-b20211130-fv02.0.nc.html'
                }
                self.assertEqual(
                    self.normalizer.get_dataset_parameters(attributes),
                    mock_utils_method.return_value)
                mock_utils_method.assert_called_with(
                    (
                        'longitude',
                        'latitude',
                        'sea_floor_depth_below_geoid',
                        'sea_water_salinity',
                        'sea_water_potential_temperature',
                        'sea_ice_area_fraction',
                        'sea_ice_thickness',
                        'surface_snow_thickness',
                        'sea_ice_x_velocity',
                        'sea_ice_y_velocity',
                        'sea_surface_height_above_geoid',
                        'sea_water_x_velocity',
                        'sea_water_y_velocity',
                    )
                )
            with self.subTest('daily mean'):
                attributes = {
                    'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_phy_dm_files/2022/09/'
                        '20220929_dm-metno-MODEL-topaz5-ARC-b20220922-fv02.0.nc.html'
                }
                self.assertEqual(
                    self.normalizer.get_dataset_parameters(attributes),
                    mock_utils_method.return_value)
                mock_utils_method.assert_called_with(
                    (
                        'longitude',
                        'latitude',
                        'depth',
                        'sea_floor_depth_below_geoid',
                        'sea_water_potential_temperature',
                        'sea_water_salinity',
                        'sea_water_x_velocity',
                        'sea_water_y_velocity',
                        'ocean_mixed_layer_thickness_defined_by_sigma_theta',
                        'sea_surface_height_above_geoid',
                        'ocean_barotropic_streamfunction',
                        'sea_ice_area_fraction',
                        'sea_ice_thickness',
                        'sea_ice_x_velocity',
                        'sea_ice_y_velocity',
                        'surface_snow_thickness',
                        'age_of_sea_ice',
                        'sea_ice_classification',
                        'sea_ice_albedo',
                        'sea_water_potential_temperature_at_sea_floor',
                    )
                )
            with self.subTest('unknown'):
                self.assertEqual(self.normalizer.get_dataset_parameters({'url': 'https://foo'}), [])


class CMEMS002004MetadataNormalizerTestCase(GCMDTestsBuiltin, unittest.TestCase):
    """Tests for the CMEMS002004MetadataNormalizer class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMS002004MetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_bgc_dm_files/2021/10/'
                   '20211031_dm-metno-MODEL-topaz5_ecosmo-ARC-b20211028-fv02.0.nc.html'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'https://foo/bar'}))

    def test_provider(self):
        """Test that we get the right provider if a CMEMS URL is used
        """
        with mock.patch('metanorm.utils.get_gcmd_provider') as mock_get_provider:
            with self.subTest('cmems'):
                self.normalizer.get_provider({
                    'url': 'ftp://nrt.cmems-du.eu/Core/ARCTIC_ANALYSISFORECAST_BGC_002_004/'
                           'cmems_mod_arc_bgc_anfc_ecosmo_P1D-m'})
                mock_get_provider.assert_called_with(['CMEMS'])
            with self.subTest('met.no'):
                self.normalizer.get_provider({
                    'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_bgc_dm_files'})
                mock_get_provider.assert_called_with(['NO/MET'])
            with self.subTest('unknown'):
                self.assertIsNone(self.normalizer.get_provider({'url': 'https://foo'}))

    def test_entry_title(self):
        """test getting entry_title"""
        self.assertEqual(
            self.normalizer.get_entry_title({}),
            'Arctic Ocean Biogeochemistry Analysis and Forecast, 6.25 km')

    def test_summary(self):
        """test getting summary"""
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: TOPAZ 5 biochemistry model;'
            'Processing level: 4;'
            'Product: ARCTIC_ANALYSISFORECAST_BGC_002_004')

    def test_time_coverage_start_dm(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_bgc_dm_files/2021/10/'
                       '20211031_dm-metno-MODEL-topaz5_ecosmo-ARC-b20211028-fv02.0.nc.html'
            }),
            datetime(year=2021, month=10, day=31, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_start_mm(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_bgc_mm_files/2020/'
                       '202011_mm-metno-MODEL-topaz5_ecosmo-ARC-fv02.0.nc.html'
            }),
            datetime(year=2020, month=11, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_dm(self):
        """Should return the proper end time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_bgc_dm_files/2021/10/'
                       '20211031_dm-metno-MODEL-topaz5_ecosmo-ARC-b20211028-fv02.0.nc.html'
            }),
            datetime(year=2021, month=11, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_time_coverage_end_mm(self):
        """Should return the proper end time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_bgc_mm_files/2020/'
                       '202011_mm-metno-MODEL-topaz5_ecosmo-ARC-fv02.0.nc.html'
            }),
            datetime(year=2020, month=12, day=1, hour=0, minute=0, second=0, tzinfo=timezone.utc))

    def test_location_geometry(self):
        """test getting geometry"""
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 50, -180 90, 180 90, 180 50, -180 50))')

    def test_dataset_parameters(self):
        """Test getting the dataset parameters"""
        with mock.patch('metanorm.utils.create_parameter_list') as mock_utils_method:
            with self.subTest('monthly mean'):
                attributes = {
                    'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_bgc_mm_files/2020/'
                        '202011_mm-metno-MODEL-topaz5_ecosmo-ARC-fv02.0.nc.html'
                }
                self.assertEqual(
                    self.normalizer.get_dataset_parameters(attributes),
                    mock_utils_method.return_value)
                mock_utils_method.assert_called_with(
                    (
                        'longitude',
                        'latitude',
                        'sea_floor_depth_below_geoid',
                        ('net_primary_production_of_biomass_'
                         'expressed_as_carbon_per_unit_volume_in_sea_water'),
                        'mass_concentration_of_chlorophyll_a_in_sea_water',
                        'volume_attenuation_coefficient_of_downwelling_radiative_flux_in_sea_water',
                        'mole_concentration_of_nitrate_in_sea_water',
                        'mole_concentration_of_phosphate_in_sea_water',
                        'mole_concentration_of_phytoplankton_expressed_as_carbon_in_sea_water',
                        'mole_concentration_of_zooplankton_expressed_as_carbon_in_sea_water',
                        'mole_concentration_of_dissolved_molecular_oxygen_in_sea_water',
                        'mole_concentration_of_silicate_in_sea_water',
                        'sinking_mole_flux_of_particulate_organic_matter_'
                        'expressed_as_carbon_in_sea_water',
                        'sea_water_ph_reported_on_total_scale',
                        'mole_concentration_of_dissolved_inorganic_carbon_in_sea_water',
                        'surface_partial_pressure_of_carbon_dioxide_in_sea_water',
                    )
                )
            with self.subTest('daily mean'):
                attributes = {
                    'url': 'https://thredds.met.no/thredds/dodsC/cmems/topaz5_bgc_dm_files/2021/10/'
                        '20211031_dm-metno-MODEL-topaz5_ecosmo-ARC-b20211028-fv02.0.nc.html'
                }

                self.assertEqual(
                    self.normalizer.get_dataset_parameters(attributes),
                    mock_utils_method.return_value)
                mock_utils_method.assert_called_with(
                    (
                        'longitude',
                        'latitude',
                        'depth',
                        'sea_floor_depth_below_geoid',
                        ('net_primary_production_of_biomass_'
                         'expressed_as_carbon_per_unit_volume_in_sea_water'),
                        'mass_concentration_of_chlorophyll_a_in_sea_water',
                        'volume_attenuation_coefficient_of_downwelling_radiative_flux_in_sea_water',
                        'mole_concentration_of_nitrate_in_sea_water',
                        'mole_concentration_of_phosphate_in_sea_water',
                        'mole_concentration_of_phytoplankton_expressed_as_carbon_in_sea_water',
                        'mole_concentration_of_zooplankton_expressed_as_carbon_in_sea_water',
                        'mole_concentration_of_dissolved_molecular_oxygen_in_sea_water',
                        'mole_concentration_of_silicate_in_sea_water',
                        'sinking_mole_flux_of_particulate_organic_matter_expressed_as_carbon_in_sea_water',
                        'sea_water_ph_reported_on_total_scale',
                        'mole_concentration_of_dissolved_inorganic_carbon_in_sea_water',
                        'surface_partial_pressure_of_carbon_dioxide_in_sea_water',
                    )
                )
            with self.subTest('unknown'):
                self.assertEqual(self.normalizer.get_dataset_parameters({'url': 'https://foo'}), [])
