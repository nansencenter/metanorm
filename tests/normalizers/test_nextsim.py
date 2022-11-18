"""Tests for the nextsim normalizer"""

import unittest
import unittest.mock as mock
from datetime import datetime, timezone

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


class NextsimMetadataNormalizerTests(unittest.TestCase):
    """Tests for NextsimMetadataNormalizer"""

    def setUp(self):
        self.normalizer = normalizers.NextsimMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': '/foo/bar/20210823_hr-nersc-MODEL-nextsimf-ARC-b20210817-fv00.0.nc'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': ''}))
        self.assertFalse(self.normalizer.check({'url': '/foo/bar/baz.nc'}))

    def test_get_entry_title(self):
        """Test getting the title"""
        self.assertEqual(self.normalizer.get_entry_title({'title': 'foo'}), 'foo')

    def test_missing_title(self):
        """A MetadataNormalizationError should be raised if the raw title
        is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_title({})

    def test_get_entry_id(self):
        """Test getting the ID"""
        self.assertEqual(
            self.normalizer.get_entry_id({
                'url': '/foo/bar/20210823_hr-nersc-MODEL-nextsimf-ARC-b20210817-fv00.0.nc'
            }),
            '20210823_hr-nersc-MODEL-nextsimf-ARC-b20210817-fv00.0')

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
            'Description: The Arctic Sea Ice Analysis and Forecast system uses the neXtSIM '
            'stand-alone sea ice model running the Brittle-Bingham-Maxwell sea ice rheology on an '
            'adaptive triangular mesh of 10 km average cell length.;'
            'Processing level: 4;'
            'Product: ARCTIC_ANALYSISFORECAST_PHY_ICE_002_011')

    def test_get_time_coverage_start(self):
        """Test getting the start of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'field_date': '2021-08-23'}),
            datetime(year=2021, month=8, day=23, tzinfo=timezone.utc))

    def test_missing_time_coverage_start(self):
        """A MetadataNormalizationError must be raised when the
        time_coverage_start raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_get_time_coverage_end(self):
        """Test getting the end of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'field_date': '2021-08-23'}),
            datetime(year=2021, month=8, day=24, tzinfo=timezone.utc))

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
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 62,180 62,180 90,-180 90,-180 62))')
