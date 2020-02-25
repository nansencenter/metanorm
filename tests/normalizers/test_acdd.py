"""Tests for the ACDD metadata normalizer"""
import unittest
from collections import OrderedDict
from datetime import datetime

from dateutil.tz import tzlocal
from django.contrib.gis.geos.geometry import GEOSGeometry

import metanorm.normalizers as normalizers


class ACDDMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the ACDD attributes normalizer"""

    def setUp(self):
        self.normalizer = normalizers.ACDDMetadataNormalizer([])

    def test_entry_title(self):
        """entry_title from ACDDMetadataNormalizer"""
        attributes = {'title': 'title_value'}
        self.assertEqual(self.normalizer.get_entry_title(attributes), 'title_value')

    def test_summary(self):
        """summary from ACDDMetadataNormalizer"""
        attributes = {'summary': 'summary_value'}
        self.assertEqual(self.normalizer.get_summary(attributes), 'summary_value')

    def test_time_coverage_start(self):
        """time_coverage_start from ACDDMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'time_coverage_start': "20200101T000001"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=0, second=1))
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'time_coverage_start': "20200101T000001Z"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=0, second=1, tzinfo=tzlocal()))
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'time_coverage_start': "2020-01-01T00:00:01"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=0, second=1))
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'time_coverage_start': "2020-01-01T00:00:01Z"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=0, second=1, tzinfo=tzlocal()))

    def test_time_coverage_end(self):
        """time_coverage_end from ACDDMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'time_coverage_end': "20200101T000559"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=5, second=59))
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'time_coverage_end': "20200101T000559Z"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=5, second=59, tzinfo=tzlocal()))
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'time_coverage_end': "2020-01-01T00:05:59"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=5, second=59))
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'time_coverage_end': "2020-01-01T00:05:59Z"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=5, second=59, tzinfo=tzlocal()))

    def test_gcmd_platform(self):
        """gcmd_platform from ACDDMetadataNormalizer"""
        attributes = {'platform': 'SENTINEL-1'}

        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([
                ('Category', 'Earth Observation Satellites'),
                ('Series_Entity', 'SENTINEL-1'),
                ('Short_Name', ''),
                ('Long_Name', '')
            ])
        )

    def test_non_gcmd_platform(self):
        """Non-GCMD platform from ACDDMetadataNormalizer"""
        attributes = {'platform': 'TEST'}

        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([
                ('Category', 'Unknown'),
                ('Series_Entity', 'Unknown'),
                ('Short_Name', 'TEST'),
                ('Long_Name', 'TEST')
            ])
        )

    def test_non_gcmd_platform_long_name(self):
        """Non-GCMD platform from ACDDMetadataNormalizer, with a name longer than 250 characters"""
        attributes = {
            'platform': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod ' +
                        'tempor incididunt ut labore et dolore magna aliqua. Bibendum neque egest' +
                        'as congue quisque egestas diam in. Eget magna fermentum iaculis eu non d' +
                        'iam phasellus vestibulum lorvgem. Tempor commodo.'
        }

        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([
                ('Category', 'Unknown'),
                ('Series_Entity', 'Unknown'),
                ('Short_Name', attributes['platform'][:100]),
                ('Long_Name', attributes['platform'][:250])
            ])
        )

    def test_gcmd_instrument(self):
        """GCMD instrument from ACDDMetadataNormalizer"""
        attributes = {'instrument': 'VIIRS'}

        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([
                ('Category', 'Earth Remote Sensing Instruments'),
                ('Class', 'Passive Remote Sensing'),
                ('Type', 'Spectrometers/Radiometers'),
                ('Subtype', 'Imaging Spectrometers/Radiometers'),
                ('Short_Name', 'VIIRS'),
                ('Long_Name', 'Visible-Infrared Imager-Radiometer Suite')
            ])
        )

    def test_non_gcmd_instrument(self):
        """Non-GCMD instrument from ACDDMetadataNormalizer"""
        attributes = {'instrument': 'TEST'}

        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([
                ('Category', 'Unknown'),
                ('Class', 'Unknown'),
                ('Type', 'Unknown'),
                ('Subtype', 'Unknown'),
                ('Short_Name', 'TEST'),
                ('Long_Name', 'TEST')
            ])
        )

    def test_non_gcmd_instrument_long_name(self):
        """
        Non-GCMD instrument from ACDDMetadataNormalizer, with a name longer than 200 characters
        """

        attributes = {
            'instrument':
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod ' +
                'tempor incididunt ut labore et dolore magna aliqua. Bibendum neque egest' +
                'as congue quisque egestas diam in. Eget magna fermentum iaculis eu non d' +
                'iam phasellus vestibulum lorvgem. Tempor commodo.'
        }

        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([
                ('Category', 'Unknown'),
                ('Class', 'Unknown'),
                ('Type', 'Unknown'),
                ('Subtype', 'Unknown'),
                ('Short_Name', attributes['instrument'][:60]),
                ('Long_Name', attributes['instrument'][:200])
            ])
        )

    def test_min_max_lon_lat_location_geometry(self):
        """location_geometry from ACDDMetadataNormalizer"""

        attributes = {
            'geospatial_lat_max': "10",
            'geospatial_lat_min': "5",
            'geospatial_lon_max': "80",
            'geospatial_lon_min': "0"
        }
        expected_geometry = GEOSGeometry(
            ('POLYGON((' +
             '0 5,' +
             '80 5,' +
             '80 10,' +
             '0 10,' +
             '0 5))'),
            srid=4326)

        self.assertTrue(self.normalizer.get_location_geometry(attributes).equals(expected_geometry))

    def test_wkt_bounds_location_geometry(self):
        """location_geometry from ACDDMetadataNormalizer"""

        attributes = {
            'geospatial_bounds': (
                'POLYGON((' +
                '-29.04 61.31,' +
                '-18.32 59.66,' +
                '-20.25 51.06,' +
                '-38.97 55.12,' +
                '-29.04 61.31))'),
            'geospatial_bounds_crs': 'EPSG:4326'
        }
        expected_geometry = GEOSGeometry(
            ('POLYGON((' +
             '-29.04 61.31,' +
             '-18.32 59.66,' +
             '-20.25 51.06,' +
             '-38.97 55.12,' +
             '-29.04 61.31))'),
            srid=4326)

        self.assertTrue(self.normalizer.get_location_geometry(attributes).equals(expected_geometry))

    def test_gcmd_provider(self):
        """GCMD provider from ACDDMetadataNormalizer"""
        attributes = {
            'publisher_name': 'NERSC',
            'publisher_url': 'http://www.nersc.no'
        }

        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([
                ('Bucket_Level0', 'CONSORTIA/INSTITUTIONS'),
                ('Bucket_Level1', ''),
                ('Bucket_Level2', ''),
                ('Bucket_Level3', ''),
                ('Short_Name', 'NERSC'),
                ('Long_Name', 'Nansen Environmental and Remote Sensing Centre'),
                ('Data_Center_URL', 'http://www.nersc.no/main/index2.php')
            ])
        )

    def test_non_gcmd_provider(self):
        """Non-GCMD provider from ACDDMetadataNormalizer"""
        attributes = {
            'publisher_name': 'TEST',
            'publisher_url': 'http://random.url'
        }

        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([
                ('Bucket_Level0', 'Unknown'),
                ('Bucket_Level1', 'Unknown'),
                ('Bucket_Level2', 'Unknown'),
                ('Bucket_Level3', 'Unknown'),
                ('Short_Name', 'TEST'),
                ('Long_Name', 'TEST'),
                ('Data_Center_URL', 'http://random.url')
            ])
        )

    def test_non_gcmd_provider_long_name(self):
        """Non-GCMD provider from ACDDMetadataNormalizer, with a name longer than 250 characters"""

        attributes = {
            'publisher_name':
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod ' +
                'tempor incididunt ut labore et dolore magna aliqua. Bibendum neque egest' +
                'as congue quisque egestas diam in. Eget magna fermentum iaculis eu non d' +
                'iam phasellus vestibulum lorvgem. Tempor commodo.',
            'publisher_url': 'http://random.url'
        }

        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([
                ('Bucket_Level0', 'Unknown'),
                ('Bucket_Level1', 'Unknown'),
                ('Bucket_Level2', 'Unknown'),
                ('Bucket_Level3', 'Unknown'),
                ('Short_Name', attributes['publisher_name'][:50]),
                ('Long_Name', attributes['publisher_name'][:250]),
                ('Data_Center_URL', 'http://random.url')
            ])
        )
