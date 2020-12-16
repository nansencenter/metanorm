"""Tests for the ACDD metadata normalizer"""
import unittest
from collections import OrderedDict
from datetime import datetime

from dateutil.tz import tzutc

import metanorm.normalizers as normalizers


class CreodiasEOFinderMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the Creodias API attributes normalizer"""

    def setUp(self):
        self.normalizer = normalizers.CreodiasEOFinderMetadataNormalizer([], [])

    def test_summary_description_only(self):
        """summary from CreodiasEOFinderMetadataNormalizer"""
        attributes = {
            'startDate': '2018-04-18T01:02:03Z',
            'instrument': 'instrument_value',
            'sensorMode': 'mode_value',
            'platform': 'platform_value'
        }
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: sensorMode=mode_value, platform=platform_value, ' +
            'instrument=instrument_value, startDate=2018-04-18T01:02:03Z')

    def test_summary_with_processing_level(self):
        """summary from CreodiasEOFinderMetadataNormalizer with processing level"""
        attributes = {
            'startDate': '2018-04-18T01:02:03Z',
            'instrument': 'instrument_value',
            'sensorMode': 'mode_value',
            'platform': 'platform_value',
            'processingLevel': 'LEVEL2'
        }
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: sensorMode=mode_value, platform=platform_value, ' +
            'instrument=instrument_value, startDate=2018-04-18T01:02:03Z;Processing level: 2')

    def test_summary_missing_attribute(self):
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_summary({}), None)

    def test_time_coverage_start(self):
        """time_coverage_start from CreodiasEOFinderMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'startDate': "2020-12-15T11:40:38.211Z"}),
            datetime(year=2020, month=12, day=15, hour=11, minute=40, second=38, tzinfo=tzutc()))

    def test_time_coverage_start_missing_attribute(self):
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_time_coverage_start({}), None)

    def test_time_coverage_end(self):
        """time_coverage_end from CreodiasEOFinderMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'completionDate': "2020-12-15T11:43:38.211Z"}),
            datetime(year=2020, month=12, day=15, hour=11, minute=43, second=38, tzinfo=tzutc()))

    def test_time_coverage_end_missing_attribute(self):
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_time_coverage_end({}), None)

    def test_platform(self):
        """gcmd_platform from CreodiasEOFinderMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_platform({'platform': 'S1A'}),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', 'SENTINEL-1'),
                         ('Short_Name', 'SENTINEL-1A'),
                         ('Long_Name', 'SENTINEL-1A')]),
        )

    def test_platform_missing_attribute(self):
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_platform({}), None)

    def test_gcmd_instrument(self):
        """GCMD instrument from CreodiasEOFinderMetadataNormalizer"""
        attributes = {'instrument': 'OL'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', 'OLCI'),
                         ('Long_Name', 'Ocean and Land Colour Imager')])
        )

    def test_instrument_missing_attribute(self):
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_instrument({}), None)

    def test_location_geometry(self):
        """location_geometry from CreodiasEOFinderMetadataNormalizer"""

        attributes = {
            'geometry': '''{"type": "Polygon","coordinates": [[[-141.363,-70.8481],
                        [-142.187,-71.401],[-143.052,-71.9568],[-141.363,-70.8481]]}'''
        }

        self.assertEqual(self.normalizer.get_location_geometry(attributes), attributes['geometry'])

    def test_location_geometry_missing_attribute(self):
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_location_geometry({}), None)

    def test_gcmd_provider_esa(self):
        """GCMD provider from CreodiasEOFinderMetadataNormalizer"""
        attributes = {'organisationName': 'ESA'}

        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0', 'MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1', ''),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'ESA/EO'),
                         ('Long_Name', 'Observing the Earth, European Space Agency'),
                         ('Data_Center_URL', 'http://www.esa.int/esaEO/')])
        )

    def test_unknown_provider_returns_none(self):
        """No provider must be returned if the provider is unknown"""
        attributes = {'organisationName': 'something'}
        self.assertIs(self.normalizer.get_provider(attributes), None)

    def test_provider_missing_attribute(self):
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_provider({}), None)

    def test_entry_id(self):
        """entry_id from CreodiasEOFinderMetadataNormalizer """
        attributes = {
            'url': "https://zipper.creodias.eu/foo",
            'title': 'id_value'
        }
        self.assertEqual(self.normalizer.get_entry_id(attributes), 'id_value')

    def test_entry_id_missing_attribute(self):
        """entry_id method must return None if the attribute is missing"""
        self.assertIsNone(self.normalizer.get_entry_id({}))

    def test_entry_id_is_none_for_non_creodias_url(self):
        """No entry_id must be returned if the URL is not one from Creodias"""
        attributes = {'url': 'https://random.url', 'title': 'foo'}
        self.assertIsNone(self.normalizer.get_entry_id(attributes))
