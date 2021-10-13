"""Tests for the Radarsat 2 CSV normalizer"""
import datetime as dt
import unittest
from collections import OrderedDict

from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError

class Radarsat2CSVNormalizerTests(unittest.TestCase):
    """Tests for the well known attributes normalizer"""

    def setUp(self):
        self.metadata = {
            'Result Number': '1',
            'Satellite': 'RADARSAT-2',
            'Date': '2020-07-16 02:14:27 GMT',
            'Beam Mode': 'ScanSAR Wide A (W1 W2 W3 S7)',
            'Polarization': 'HH HV',
            'Type': 'SGF',
            'Image Id': '831163',
            'Image Info': ('"{""headers"":[""Product Type"" ""LUT Applied"" ""Sampled Pixel ' +
            'Spacing (Panchromatic)"" ""Product Format"" ""Geodetic Terrain Height""] ""' +
            'relatedProducts"":[{""values"":[""SGF"" ""Ice"" ""100.0"" ""GeoTIFF"" ""0.00186""' +
            ']}] ""collectionID"":""Radarsat2"" ""imageID"":""7337877""}"'),
            'Metadata': 'dummy value',
            'Reason': '',
            'Sensor Mode': 'ScanSAR Wide',
            'Orbit Direction': 'Ascending',
            'Order Key': 'RS2_OK121511_PK1076349_DK1021326_SCWA_20200716_021427_HH_HV_SGF',
            'SIP Size (MB)': '84',
            'Service UUID': 'SERVICE-RSAT2_001-000000000000000000',
            'Footprint': ('-146.008396 73.905427 -143.459486 72.212173 -127.936480 73.451549'+
            ' -128.875274 75.249738 -146.008396 73.905427 '),
            'Look Orientation': 'Right',
            'Band': 'C',
            'Title': 'rsat2_20200716_N7370W13656',
            'Options': '',
            'Absolute Orbit': '65706',
            'Orderable': 'TRUE'}

        self.normalizer = normalizers.Radarsat2CSVMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check(self.metadata))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'foo': 'bar'}))

    def test_get_entry_title(self):
        """ shall return title composed of several fields """
        self.assertEqual(
            self.normalizer.get_entry_title(self.metadata),
            'rsat2_20200716_N7370W13656 HH HV ScanSAR Wide A (W1 W2 W3 S7)')

    def test_missing_entry_title(self):
        """A MetadataNormalizationError must be raised when the raw
        attributes used to generate the title are missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_title({})

    def test_get_entry_id(self):
        """ shall return RS2 image name """
        self.assertEqual(
            self.normalizer.get_entry_id(self.metadata),
            'RS2_OK121511_PK1076349_DK1021326_SCWA_20200716_021427_HH_HV_SGF')

    def test_missing_entry_id(self):
        """A MetadataNormalizationError must be raised when the raw
        Order Key attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})

    def test_get_time_coverage_start(self):
        """shall return the proper starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(self.metadata),
            dt.datetime(year=2020, month=7, day=16, hour=2, minute=14, second=27, tzinfo=tzutc()))

    def test_missing_time_coverage_start(self):
        """A MetadataNormalizationError must be raised when the
        Date raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_get_time_coverage_end(self):
        """shall return the proper starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(self.metadata),
            dt.datetime(year=2020, month=7, day=16, hour=2, minute=19, second=27, tzinfo=tzutc()))

    def test_missing_time_coverage_end(self):
        """A MetadataNormalizationError must be raised when the
        Date raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})

    def test_get_platform(self):
        """ shall return radarsat-2 """
        self.assertEqual(
            self.normalizer.get_platform(self.metadata),
            OrderedDict([('Category', 'Earth Observation Satellites'),
             ('Series_Entity', 'RADARSAT'),
             ('Short_Name', 'RADARSAT-2'),
             ('Long_Name', '')]))

    def test_get_instrument(self):
        """ shall return c-sar """
        self.assertEqual(
            self.normalizer.get_instrument(self.metadata),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Active Remote Sensing'),
                         ('Type', 'Imaging Radars'),
                         ('Subtype', ''),
                         ('Short_Name', 'C-SAR'),
                         ('Long_Name', 'C-Band Synthetic Aperture Radar')]))

    def test_get_location_geometry(self):
        """ shall return POLYGON """
        self.assertEqual(
            self.normalizer.get_location_geometry(self.metadata),
            ('POLYGON((-146.008396 73.905427, -143.459486 72.212173, -127.936480 73.451549, '+
             '-128.875274 75.249738, -146.008396 73.905427))'))

    def test_missing_geometry(self):
        """A MetadataNormalizationError must be raised when the
        Footprint raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({})

    def test_get_provider(self):
        """ shall return csa """
        self.assertEqual(
            self.normalizer.get_provider(self.metadata),
            OrderedDict([('Bucket_Level0', 'COMMERCIAL'),
                         ('Bucket_Level1', ''),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'CSA'),
                         ('Long_Name', 'Cambridge Scientific Abstracts'),
                         ('Data_Center_URL', 'http://www.csa.com/')]))

    def test_get_parameters(self):
        """ shall return sigma0 wkv """
        self.assertCountEqual(
            self.normalizer.get_dataset_parameters(self.metadata), [
                OrderedDict([
                    ('standard_name', 'surface_backwards_scattering_coefficient_of_radar_wave'),
                    ('long_name', 'Normalized Radar Cross Section'),
                    ('short_name', 'sigma0'),
                    ('units', 'm/m'),
                    ('minmax', '0 0.1'),
                    ('colormap', 'gray')])])
