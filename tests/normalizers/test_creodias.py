"""Tests for the Creodias metadata normalizer"""
import unittest
from collections import OrderedDict
from datetime import datetime

from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError

class CreodiasEOFinderMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the Creodias API attributes normalizer"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CreodiasEOFinderMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        valid_url = 'https://zipper.creodias.eu/download/023c3fe8-bfac-5b58-a359-6aab4bf30bd6'
        invalid_url = 'https://apihub.copernicus.eu/'

        # use the URL attribute added in geospaas_harvesting
        self.assertTrue(self.normalizer.check({'url': valid_url}))
        self.assertFalse(self.normalizer.check({'url': invalid_url}))

        # use the URL attribute in the original location
        self.assertTrue(self.normalizer.check({'services': {'download': {'url': valid_url}}}))
        self.assertFalse(self.normalizer.check({'services': {'download': {'url': invalid_url}}}))

        # no URL attribute can be found
        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'foo': 'bar'}))

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
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_summary({})

    def test_time_coverage_start(self):
        """time_coverage_start from CreodiasEOFinderMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'startDate': "2020-12-15T11:40:38.211Z"}),
            datetime(year=2020, month=12, day=15, hour=11, minute=40, second=38, tzinfo=tzutc()))

    def test_time_coverage_start_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_time_coverage_end(self):
        """time_coverage_end from CreodiasEOFinderMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'completionDate': "2020-12-15T11:43:38.211Z"}),
            datetime(year=2020, month=12, day=15, hour=11, minute=43, second=38, tzinfo=tzutc()))

    def test_time_coverage_end_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})

    def test_platform(self):
        """gcmd_platform from CreodiasEOFinderMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_platform({'platform': 'S1A'}),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', 'Sentinel-1'),
                         ('Short_Name', 'Sentinel-1A'),
                         ('Long_Name', 'Sentinel-1A')]),
        )

    def test_platform_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_platform({})

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
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_instrument({})

    def test_location_geometry(self):
        """location_geometry from CreodiasEOFinderMetadataNormalizer"""

        attributes = {
            'geometry': '''{"type": "Polygon","coordinates": [[[-141.363,-70.8481],
                        [-142.187,-71.401],[-143.052,-71.9568],[-141.363,-70.8481]]}'''
        }

        self.assertEqual(self.normalizer.get_location_geometry(attributes), attributes['geometry'])

    def test_location_geometry_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({})

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
        """An exception must be raised if the provider is unknown"""
        with self.assertRaises(MetadataNormalizationError) as raised:
            self.normalizer.get_provider({'organisationName': 'something'})
        self.assertEqual(str(raised.exception), 'Unknown provider something')

    def test_provider_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_provider({})

    def test_entry_id(self):
        """entry_id from CreodiasEOFinderMetadataNormalizer """
        attributes = {
            'url': "https://zipper.creodias.eu/foo",
            'title': 'id_value'
        }
        self.assertEqual(self.normalizer.get_entry_id(attributes), 'id_value')

    def test_entry_id_missing_attribute(self):
        """entry_id method must return None if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})
