"""Tests for the nextsim normalizer"""

import unittest
import unittest.mock as mock
from datetime import datetime, timezone

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


class DownscaledECMWFMetadataNormalizerTests(unittest.TestCase):
    """Tests for DownscaledECMWFMetadataNormalizer"""

    def setUp(self):
        self.normalizer = normalizers.DownscaledECMWFMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({'url': '/foo/bar/Seasonal_Nov23_SAT_n15.nc'}))
        self.assertTrue(self.normalizer.check({'url': '/foo/bar/Seasonal_Nov23_SDA_n15.nc'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': ''}))
        self.assertFalse(self.normalizer.check({'url': '/foo/bar/baz.nc'}))

    def test_get_entry_title(self):
        """Test getting the title"""
        self.assertEqual(self.normalizer.get_entry_title({}), 'Downscaled ECMWF seasonal forecast')

    def test_get_entry_id(self):
        """Test getting the ID"""
        self.assertEqual(
            self.normalizer.get_entry_id({
                'url': '/foo/bar/Seasonal_Nov23_SDA_n15.nc'
            }),
            'Seasonal_Nov23_SDA_n15')
        self.assertEqual(
            self.normalizer.get_entry_id({
                'url': '/foo/bar/Seasonal_Nov23_SAT_n15.nc'
            }),
            'Seasonal_Nov23_SAT_n15')

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
            "Downscaled version of ECMWF's seasonal forecasts")

    def test_get_time_coverage_start(self):
        """Test getting the start of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'date': '2023-11-14 13:21:08'}),
            datetime(year=2023, month=11, day=1, tzinfo=timezone.utc))

    def test_missing_time_coverage_start(self):
        """A MetadataNormalizationError must be raised when the
        time_coverage_start raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_get_time_coverage_end(self):
        """Test getting the end of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'date': '2023-11-14 13:21:08'}),
            datetime(year=2024, month=5, day=1, tzinfo=timezone.utc))

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
            mock_get_gcmd_method.assert_called_with('OPERATIONAL MODELS')

    def test_gcmd_instrument(self):
        """Test getting the instrument"""
        with mock.patch('metanorm.utils.get_gcmd_instrument') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_instrument({}),
                mock_get_gcmd_method.return_value)
            mock_get_gcmd_method.assert_called_with('Computer')

    def test_gcmd_provider(self):
        """Test getting the provider"""
        with mock.patch('metanorm.utils.get_gcmd_provider') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_provider({}),
                mock_get_gcmd_method.return_value)
            mock_get_gcmd_method.assert_called_with(['NERSC'])

    def test_get_location_geometry(self):
        """get_location_geometry() should return the location
        of the dataset
        """
        self.assertEqual(self.normalizer.get_location_geometry({}), '')
