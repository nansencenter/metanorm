"""Tests for the ACDD metadata normalizer"""
import unittest
import unittest.mock as mock
from collections import OrderedDict
from datetime import datetime

from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


class ScihubODataMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the Scihub OData attributes normalizer"""

    def setUp(self):
        self.normalizer = normalizers.ScihubODataMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': "https://apihub.copernicus.eu/apihub/odata/v1/"
                   "Products('ce560002-dcff-4663-b7bd-69635ca1ad2d')/$value"}))
        self.assertTrue(self.normalizer.check({
            'url': "https://scihub.copernicus.eu/apihub/odata/v1/"
                   "Products('ce560002-dcff-4663-b7bd-69635ca1ad2d')/$value"}))
        self.assertTrue(self.normalizer.check({
            'url': "https://colhub.met.no/odata/v1/"
                   "Products('0ebbcf14-e482-4e18-8159-b271681240bc')/$value"}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': ''}))
        self.assertFalse(self.normalizer.check({'url': 'https://foo'}))

    def test_entry_title(self):
        """entry_title from ScihubODataMetadataNormalizer"""
        attributes = {'Identifier': 'title_value'}
        self.assertEqual(self.normalizer.get_entry_title(attributes), 'title_value')

    def test_entry_id(self):
        """entry_id from ScihubODataMetadataNormalizer """
        attributes = {'Identifier': 'finename_value'}
        self.assertEqual(self.normalizer.get_entry_id(
            attributes), 'finename_value')

    def test_entry_id_missing_attribute(self):
        """entry_id method must return None if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})

    def test_missing_raw_title(self):
        """A MetadataNormalizationError must be raised if the raw title
        attribute is absent
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_title({})

    def test_summary_description_only(self):
        """summary from ScihubODataMetadataNormalizer"""
        attributes = {
            'Date': '2018-04-18T01:02:03Z',
            'Instrument name': 'instrument_value',
            'Mode': 'mode_value',
            'Satellite': 'satellite_value',
            'Size': 'size_value'
        }
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: Date=2018-04-18T01:02:03Z, Instrument name=instrument_value, ' +
            'Mode=mode_value, Satellite=satellite_value, Size=size_value')

    def test_summary_with_processing_level_sentinel1_style(self):
        """summary from ScihubODataMetadataNormalizer, with sentinel-1 style processing level"""
        attributes = {
            'Date': '2018-04-18T01:02:03Z',
            'Instrument name': 'instrument_value',
            'Mode': 'mode_value',
            'Satellite': 'satellite_value',
            'Size': 'size_value',
            'Product level': 'L1'
        }
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: Date=2018-04-18T01:02:03Z, Instrument name=instrument_value, ' +
            'Mode=mode_value, Satellite=satellite_value, Size=size_value;Processing level: 1')

    def test_summary_with_processing_level_sentinel2_style(self):
        """summary from ScihubODataMetadataNormalizer, with sentinel-2 style processing level"""
        attributes = {
            'Date': '2018-04-18T01:02:03Z',
            'Instrument name': 'instrument_value',
            'Mode': 'mode_value',
            'Satellite': 'satellite_value',
            'Size': 'size_value',
            'Processing level': 'Level-1C'
        }
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: Date=2018-04-18T01:02:03Z, Instrument name=instrument_value, ' +
            'Mode=mode_value, Satellite=satellite_value, Size=size_value;Processing level: 1C')

    def test_summary_with_processing_level_sentinel3_style(self):
        """summary from ScihubODataMetadataNormalizer, with sentinel-3 style processing level"""
        attributes = {
            'Date': '2018-04-18T01:02:03Z',
            'Instrument name': 'instrument_value',
            'Mode': 'mode_value',
            'Satellite': 'satellite_value',
            'Size': 'size_value',
            'Processing level': '1'
        }
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: Date=2018-04-18T01:02:03Z, Instrument name=instrument_value, ' +
            'Mode=mode_value, Satellite=satellite_value, Size=size_value;Processing level: 1')

    def test_summary_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_summary({})

    def test_time_coverage_start(self):
        """time_coverage_start from ScihubODataMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'Sensing start': "20200101T000001"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=0, second=1))
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'Sensing start': "20200101T000001Z"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=0, second=1, tzinfo=tzutc()))
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'Sensing start': "2020-01-01T00:00:01"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=0, second=1))
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'Sensing start': "2020-01-01T00:00:01Z"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=0, second=1, tzinfo=tzutc()))

    def test_time_coverage_start_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_time_coverage_end(self):
        """time_coverage_end from ScihubODataMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'Sensing stop': "20200101T000559"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=5, second=59))
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'Sensing stop': "20200101T000559Z"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=5, second=59, tzinfo=tzutc()))
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'Sensing stop': "2020-01-01T00:05:59"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=5, second=59))
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'Sensing stop': "2020-01-01T00:05:59Z"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=5, second=59, tzinfo=tzutc()))

    def test_time_coverage_end_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})

    def test_gcmd_platform(self):
        """gcmd_platform from ScihubODataMetadataNormalizer"""
        with mock.patch('metanorm.utils.get_gcmd_platform') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_platform({'Satellite name': 'foo', 'Satellite number': 'bar'}),
                mock_get_gcmd_method.return_value)

    def test_platform_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_platform({})

    def test_gcmd_instrument(self):
        """
        GCMD instrument from ScihubODataMetadataNormalizer which is found using
        `pythesint.get_gcmd_instrument()`
        """
        with mock.patch('metanorm.utils.get_gcmd_instrument') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_instrument({'Satellite name': 'foo', 'Instrument': 'bar'}),
                mock_get_gcmd_method.return_value)

    def test_instrument_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_instrument({})

    def test_wkt_bounds_location_geometry(self):
        """location_geometry from ScihubODataMetadataNormalizer"""

        attributes = {
            'JTS footprint': (
                'MULTIPOLYGON(((' +
                '-29.04 61.31,' +
                '-18.32 59.66,' +
                '-20.25 51.06,' +
                '-38.97 55.12,' +
                '-29.04 61.31)))'),
            'geospatial_bounds_crs': 'EPSG:4326'
        }
        expected_geometry = ('MULTIPOLYGON(((' +
             '-29.04 61.31,' +
             '-18.32 59.66,' +
             '-20.25 51.06,' +
             '-38.97 55.12,' +
             '-29.04 61.31)))')

        self.assertEqual(self.normalizer.get_location_geometry(attributes), expected_geometry)

    def test_location_geometry_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({})

    def test_gcmd_provider(self):
        """GCMD provider from ScihubODataMetadataNormalizer"""
        with mock.patch('metanorm.utils.get_gcmd_provider') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_provider({}),
                mock_get_gcmd_method.return_value)

    def test_dataset_parameters_sentinel1(self):
        """Test getting the dataset parameters for Sentinel 1 datasets
        """
        with mock.patch('metanorm.utils.create_parameter_list') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters({
                    'Identifier': 'S1B_IW_GRDH_1SDV_20210916T103902_20210916T103927_028722_036D80_'
                                  'C8D0',
                }),
                mock_get_gcmd_method.return_value)
            mock_get_gcmd_method.assert_called_with([
                'surface_backwards_scattering_coefficient_of_radar_wave'
            ])

    def test_unknown_dataset_parameters(self):
        """An empty list should be returned if no parameter is found"""
        self.assertListEqual(self.normalizer.get_dataset_parameters({'Identifier': 'foo'}), [])
