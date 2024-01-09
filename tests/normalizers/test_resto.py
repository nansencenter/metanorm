"""Tests for the resto API metadata normalizer"""
import unittest
import unittest.mock as mock
from datetime import datetime

from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


class RestoAPIMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the restp API attributes normalizer"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.RestoAPIMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        valid_metadata = {
            'collection': "S2GLC",
            'status': "ONLINE",
            'license': {},
            'productIdentifier': "/eodata/auxdata/S2GLC/2017/S2GLC_T32TQS_2017",
            'parentIdentifier': None,
            'title': "S2GLC_T32TQS_2017",
            'description': "The S2GLC 2017 product r…ps://s2glc.cbk.waw.pl/].",
            'organisationName': None,
            'startDate': "2019-07-15T00:00:00.000Z",
            'completionDate': "2019-07-15T00:00:00.000Z",
            'productType': "GLC",
            'processingLevel': None,
            'platform': "",
            'instrument': None,
            'resolution': 0,
            'sensorMode': None,
            'orbitNumber': 0,
            'quicklook': None,
            'thumbnail': "https://catalogue.datasp…32TQS_2017/thumbnail.png",
            'updated': "2019-10-04T09:46:30.218Z",
            'published': "2019-10-04T09:46:30.218Z",
            'snowCover': 0,
            'cloudCover': 0,
            'gmlgeometry': '<gml:Polygon srsName="EP…undaryIs></gml:Polygon>',
            'centroid': {},
            'version': 0,
            'services': {},
            'links': [],
            'foo': 'bar',
        }
        invalid_metadata_examples = [
            {'productType': "GLC", 'processingLevel': None},
            {},
            {'foo': 'bar'}
        ]

        # use the URL attribute added in geospaas_harvesting
        self.assertTrue(self.normalizer.check(valid_metadata))
        for invalid_metadata in invalid_metadata_examples:
            self.assertFalse(self.normalizer.check(invalid_metadata),
                             f"check for {invalid_metadata} should return False")

    def test_entry_title(self):
        """entry_title from RestoAPIMetadataNormalizer"""
        self.assertEqual(self.normalizer.get_entry_title({'title': 'foo'}), 'foo')

    def test_missing_raw_title(self):
        """A MetadataNormalizationError must be raised if the raw title
        attribute is absent
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_title({})

    def test_entry_id(self):
        """entry_id from RestoAPIMetadataNormalizer """
        attributes = {
            'url': "https://zipper.creodias.eu/foo",
            'title': 'id_value'
        }
        self.assertEqual(self.normalizer.get_entry_id(attributes), 'id_value')

    def test_entry_id_missing_attribute(self):
        """entry_id method must return None if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})

    def test_summary_description_only(self):
        """summary from RestoAPIMetadataNormalizer"""
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
        """summary from RestoAPIMetadataNormalizer with processing level"""
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
        """time_coverage_start from RestoAPIMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'startDate': "2020-12-15T11:40:38.211Z"}),
            datetime(year=2020, month=12, day=15, hour=11, minute=40, second=38, tzinfo=tzutc()))

    def test_time_coverage_start_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_time_coverage_end(self):
        """time_coverage_end from RestoAPIMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'completionDate': "2020-12-15T11:43:38.211Z"}),
            datetime(year=2020, month=12, day=15, hour=11, minute=43, second=38, tzinfo=tzutc()))

    def test_time_coverage_end_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})

    def test_gcmd_platform(self):
        """Test getting the platform"""
        with mock.patch('metanorm.utils.get_gcmd_platform') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_platform({'platform': 'foo'}),
                mock_get_gcmd_method.return_value)

    def test_platform_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_platform({})

    def test_gcmd_instrument(self):
        """Test getting the instrument"""
        with mock.patch('metanorm.utils.get_gcmd_instrument') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_instrument({'instrument': 'foo'}),
                mock_get_gcmd_method.return_value)

    def test_instrument_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_instrument({})

    def test_location_geometry(self):
        """location_geometry from RestoAPIMetadataNormalizer"""

        attributes = {
            'geometry': '''{"type": "Polygon","coordinates": [[[-141.363,-70.8481],
                        [-142.187,-71.401],[-143.052,-71.9568],[-141.363,-70.8481]]}'''
        }

        self.assertEqual(self.normalizer.get_location_geometry(attributes), attributes['geometry'])

    def test_location_geometry_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({})

    def test_gcmd_provider(self):
        """Test getting the provider"""
        with mock.patch('metanorm.utils.get_gcmd_provider') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_provider({'organisationName': 'foo'}),
                mock_get_gcmd_method.return_value)

    def test_unknown_provider(self):
        """An exception must be raised if the provider is unknown"""
        with self.assertRaises(MetadataNormalizationError) as raised:
            self.normalizer.get_provider({'organisationName': 'something'})
        self.assertEqual(str(raised.exception), 'Unknown provider something')

    def test_provider_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_provider({})
