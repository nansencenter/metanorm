"""Tests for the CPOM altimetry normalizer"""

import unittest
import unittest.mock as mock
from collections import OrderedDict
from datetime import datetime, timezone

import metanorm.normalizers as normalizers


class CPOMAltimetryMetadataNormalizerTests(unittest.TestCase):
    """Tests for CPOMAltimetryMetadataNormalizer"""

    def setUp(self):
        self.normalizer = normalizers.CPOMAltimetryMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({'url': '/foo/bar/CPOM_DOT.nc'}))

    def test_get_entry_title(self):
        """Test getting the title"""
        self.assertEqual(self.normalizer.get_entry_title({}), 'CPOM SLA')

    def test_get_entry_id(self):
        """Test getting the ID"""
        self.assertEqual(self.normalizer.get_entry_id({}), 'CPOM_DOT')

    def test_get_time_coverage_start(self):
        """Test getting the start of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({}),
            datetime(year=2003, month=1, day=1, tzinfo=timezone.utc))

    def test_get_time_coverage_end(self):
        """Test getting the end of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({}),
            datetime(year=2015, month=1, day=1, tzinfo=timezone.utc))

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
            self.normalizer.get_location_geometry({'geometry': 'POINT(10 10)'}), 'POINT(10 10)')

    def test_missing_geometry(self):
        """An empty string must be returned when the geometry raw
        attribute is missing
        """
        self.assertEqual(self.normalizer.get_location_geometry({}), '')

    def test_dataset_parameters(self):
        """dataset_parameters from CEDAESACCIMetadataNormalizer """
        with mock.patch('metanorm.utils.create_parameter_list') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters({}),
                mock_get_gcmd_method.return_value)
