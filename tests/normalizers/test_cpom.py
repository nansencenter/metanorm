"""Tests for the CPOM altimetry normalizer"""

import unittest
from collections import OrderedDict
from datetime import datetime, timezone

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


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

    def test_get_platform(self):
        """Test getting the platform"""
        self.assertDictEqual(self.normalizer.get_platform({}),
            OrderedDict([
                ('Category', 'Earth Observation Satellites'),
                ('Series_Entity', ''),
                ('Short_Name', ''),
                ('Long_Name', '')
            ]))

    def test_get_instrument(self):
        """Test getting the instrument"""
        self.assertDictEqual(
            self.normalizer.get_instrument({}),
            OrderedDict([
                ('Category', 'Earth Remote Sensing Instruments'),
                ('Class', 'Active Remote Sensing'),
                ('Type', 'Altimeters'),
                ('Subtype', ''),
                ('Short_Name', ''),
                ('Long_Name', '')
            ]))

    def test_get_location_geometry(self):
        """get_location_geometry() should return the location
        of the dataset
        """
        self.assertEqual(
            self.normalizer.get_location_geometry({'geometry': 'POINT(10 10)'}), 'POINT(10 10)')

    def test_missing_geometry(self):
        """A MetadataNormalizationError must be raised when the
        raw geometry attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({})

    def test_get_provider(self):
        """Test getting the provider"""
        self.assertDictEqual(
            self.normalizer.get_provider({}),
            OrderedDict([
                ('Bucket_Level0', 'ACADEMIC'),
                ('Bucket_Level1', ''),
                ('Bucket_Level2', ''),
                ('Bucket_Level3', ''),
                ('Short_Name', 'UC-LONDON/CPOM'),
                ('Long_Name', ''),
                ('Data_Center_URL', 'http://www.cpom.ucl.ac.uk/cpom_ucl_only/data_resources.html')
            ]))

    def test_get_parameters(self):
        """Test getting the only dataset parameter"""
        self.assertListEqual(
            self.normalizer.get_dataset_parameters({}),
            [
                OrderedDict([
                    ('standard_name', 'sea_surface_height_above_sea_level'),
                    ('long_name', 'Sea Surface Anomaly'),
                    ('short_name', 'SSA'),
                    ('units', 'm'),
                    ('minmax', '-100 100'),
                    ('colormap', 'jet')])
            ])
