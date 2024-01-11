"""Tests for the amsr2_asi normalizer"""

import unittest
import unittest.mock as mock
from datetime import datetime, timezone

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


class AMSR2ASIMetadataNormalizerTests(unittest.TestCase):
    """Tests for AMSR2ASIMetadataNormalizer"""

    def setUp(self):
        self.normalizer = normalizers.AMSR2ASIMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': 'https://data.seaice.uni-bremen.de/amsr2/asi_daygrid_swath/n6250/netcdf/'
                   '2024/asi-AMSR2-n6250-20240101-v5.4.nc'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': ''}))
        self.assertFalse(self.normalizer.check({'url': 'http://foo/bar/baz.nc'}))

    def test_get_entry_title(self):
        """Test getting the title"""
        self.assertEqual(self.normalizer.get_entry_title({}),
                         'ASI sea ice concentration from AMSR2')

    def test_get_entry_id(self):
        """Test getting the ID"""
        self.assertEqual(
            self.normalizer.get_entry_id({
                'url': 'https://data.seaice.uni-bremen.de/amsr2/asi_daygrid_swath/n6250/netcdf/'
                       '2024/asi-AMSR2-n6250-20240101-v5.4.nc'
            }),
            'asi-AMSR2-n6250-20240101-v5.4')

    def test_entry_id_error(self):
        """A MetadataNormalizationError should be raised if the url
        attribute is missing or the ID is not found
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({'url': 'foo'})

    def test_summary(self):
        """Test getting the summary"""
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: Sea ice concentration retrieved with the ARTIST Sea Ice (ASI) algorithm '
            '(Spreen et al., 2008) which is applied to microwave radiometer data of the sensor '
            'AMSR2 (Advanced Microwave Scanning Radiometer 2) on the JAXA satellite GCOM-W1.;'
            'Processing level: 3')

    def test_get_time_coverage_start(self):
        """Test getting the start of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'https://data.seaice.uni-bremen.de/amsr2/asi_daygrid_swath/n6250/netcdf/'
                       '2024/asi-AMSR2-n6250-20240101-v5.4.nc'
            }),
            datetime(year=2024, month=1, day=1, tzinfo=timezone.utc))

    def test_missing_time_coverage_start(self):
        """A MetadataNormalizationError must be raised when the
        time_coverage_start raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_get_time_coverage_end(self):
        """Test getting the end of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'https://data.seaice.uni-bremen.de/amsr2/asi_daygrid_swath/n6250/netcdf/'
                       '2024/asi-AMSR2-n6250-20240101-v5.4.nc'
            }),
            datetime(year=2024, month=1, day=2, tzinfo=timezone.utc))

    def test_missing_time_coverage_end(self):
        """A MetadataNormalizationError must be raised when the
        time_coverage_end raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})

    def test_gcmd_platform(self):
        """Test getting the platform"""
        with mock.patch('metanorm.utils.get_gcmd_platform') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_platform({}),
                mock_get_gcmd_method.return_value)

    def test_gcmd_instrument(self):
        """Test getting the instrument"""
        with mock.patch('metanorm.utils.get_gcmd_instrument') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_instrument({}),
                mock_get_gcmd_method.return_value)

    def test_gcmd_provider(self):
        """Test getting the provider"""
        with mock.patch('metanorm.utils.get_gcmd_provider') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_provider({}),
                mock_get_gcmd_method.return_value)

    def test_get_location_geometry(self):
        """get_location_geometry() should return the location
        of the dataset
        """
        self.assertEqual(
            self.normalizer.get_location_geometry({
                'url': 'https://data.seaice.uni-bremen.de/amsr2/asi_daygrid_swath/n6250/netcdf/'
                       '2024/asi-AMSR2-n6250-20240101-v5.4.nc'
            }),
            'POLYGON((-180 40,180 40,180 90,-180 90,-180 40))')
        self.assertEqual(
            self.normalizer.get_location_geometry({
                'url': 'https://data.seaice.uni-bremen.de/amsr2/asi_daygrid_swath/s6250/netcdf/'
                       '2024/asi-AMSR2-s6250-20240101-v5.4.nc'
            }),
            'POLYGON((-180 -40,180 -40,180 -90,-180 -90,-180 -40))')

    def test_location_geometry_error(self):
        """get_location_geometry() should raise an exception when the
        hemisphere can't be determined
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({'url': 'foo/asi-AMSR2-a6250-20240101-v5.4.nc'})
