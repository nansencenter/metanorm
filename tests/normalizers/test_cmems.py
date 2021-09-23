"""Tests for the CMEMS normalizers"""

import unittest
import unittest.mock as mock
from collections import OrderedDict
from datetime import datetime, timezone

import metanorm.normalizers as normalizers
from .data import DATASET_PARAMETERS
from metanorm.errors import MetadataNormalizationError


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
