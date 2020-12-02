"""Tests for the ACDD metadata normalizer"""
import unittest
from collections import OrderedDict
from datetime import datetime

from dateutil.tz import tzutc

import metanorm.normalizers as normalizers


class SentinelSAFEMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the ACDD attributes normalizer"""

    def setUp(self):
        self.normalizer = normalizers.SentinelSAFEMetadataNormalizer([], [])

    def test_entry_title(self):
        """entry_title from SentinelSAFEMetadataNormalizer"""
        attributes = {'Identifier': 'title_value'}
        self.assertEqual(self.normalizer.get_entry_title(attributes), 'title_value')

    def test_entry_title_missing_attribute(self):
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_entry_title({}), None)

    def test_summary_description_only(self):
        """summary from SentinelSAFEMetadataNormalizer"""
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
        """summary from SentinelSAFEMetadataNormalizer, with sentinel-1 style processing level"""
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
        """summary from SentinelSAFEMetadataNormalizer, with sentinel-2 style processing level"""
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
        """summary from SentinelSAFEMetadataNormalizer, with sentinel-3 style processing level"""
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
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_summary({}), None)

    def test_time_coverage_start(self):
        """time_coverage_start from SentinelSAFEMetadataNormalizer"""
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
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_time_coverage_start({}), None)

    def test_time_coverage_end(self):
        """time_coverage_end from SentinelSAFEMetadataNormalizer"""
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
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_time_coverage_end({}), None)

    def test_gcmd_platform(self):
        """gcmd_platform from SentinelSAFEMetadataNormalizer"""
        attributes = {'Satellite name': 'SENTINEL-1', 'Satellite number': 'B'}

        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', 'SENTINEL-1'),
                         ('Short_Name', 'SENTINEL-1B'),
                         ('Long_Name', 'SENTINEL-1B')])
        )

    def test_non_gcmd_platform(self):
        """Non-GCMD platform from SentinelSAFEMetadataNormalizer"""
        attributes = {'Satellite name': 'TEST', 'Satellite number': 'A'}

        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([
                ('Category', 'Unknown'),
                ('Series_Entity', 'Unknown'),
                ('Short_Name', 'TESTA'),
                ('Long_Name', 'TESTA')
            ])
        )

    def test_non_gcmd_platform_long_name(self):
        """
        Non-GCMD platform from SentinelSAFEMetadataNormalizer, with a name longer than 250 characters
        """
        attributes = {
            'Satellite name': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do ei' +
                              'usmod tempor incididunt ut labore et dolore magna aliqua. Bibendum' +
                              ' neque egest as congue quisque egestas diam in. Eget magna ferment' +
                              'um iaculis eu non diam phasellus vestibulum lorvgem. Tempor commodo',
            'Satellite number': 'A'
        }

        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([
                ('Category', 'Unknown'),
                ('Series_Entity', 'Unknown'),
                ('Short_Name', attributes['Satellite name'][:100]),
                ('Long_Name', attributes['Satellite name'][:250])
            ])
        )

    def test_platform_missing_attribute(self):
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_platform({}), None)

    def test_gcmd_instrument_from_get(self):
        """
        GCMD instrument from SentinelSAFEMetadataNormalizer which is found using
        `pythesint.get_gcmd_instrument()`
        """
        attributes = {'Instrument': 'MODIS'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', 'MODIS'),
                         ('Long_Name', 'Moderate-Resolution Imaging Spectroradiometer')])
        )

    def test_gcmd_instrument_from_search(self):
        """
        GCMD instrument from SentinelSAFEMetadataNormalizer which is found using
        `pythesint.search_gcmd_instrument_list()`
        """
        attributes = {'Instrument': 'SRAL'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Active Remote Sensing'),
                         ('Type', 'Altimeters'),
                         ('Subtype', 'Radar Altimeters'),
                         ('Short_Name', 'Sentinel-3 SRAL'),
                         ('Long_Name', 'Sentinel-3 SAR Radar Altimeter')])
        )

    def test_gcmd_instrument_from_restricted_search(self):
        """
        GCMD instrument from SentinelSAFEMetadataNormalizer which is found using
        `pythesint.search_gcmd_instrument_list()` and restricting the search with an
        additional keyword
        """
        attributes = {'Satellite name': 'SENTINEL-2', 'Instrument': 'MSI'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', 'Sentinel-2 MSI'),
                         ('Long_Name', 'Sentinel-2 Multispectral Imager')])
        )

    def test_c_sar_instrument(self):
        """Special case for C-SAR GCMD instrument from SentinelSAFEMetadataNormalizer"""
        attributes = {'Satellite name': 'SENTINEL-1', 'Instrument': 'SAR-C SAR'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Active Remote Sensing'),
                         ('Type', 'Imaging Radars'),
                         ('Subtype', ''),
                         ('Short_Name', 'SENTINEL-1 C-SAR'),
                         ('Long_Name', '')])
        )

    def test_non_gcmd_instrument(self):
        """Non-GCMD instrument from SentinelSAFEMetadataNormalizer"""
        attributes = {'Instrument': 'TEST'}

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
        Non-GCMD instrument from SentinelSAFEMetadataNormalizer, with a name longer than 200 characters
        """

        attributes = {
            'Instrument':
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
                ('Short_Name', attributes['Instrument'][:60]),
                ('Long_Name', attributes['Instrument'][:200])
            ])
        )

    def test_instrument_missing_attribute(self):
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_instrument({}), None)

    def test_wkt_bounds_location_geometry(self):
        """location_geometry from SentinelSAFEMetadataNormalizer"""

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
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_location_geometry({}), None)

    def test_gcmd_provider_from_url(self):
        """GCMD provider from SentinelSAFEMetadataNormalizer"""
        attributes = {'url': 'https://scihub.copernicus.eu'}

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

    def test_provider_is_none_for_non_scihub_url(self):
        """No provider must be returned if the URL is not one from Copernicus scihub"""
        attributes = {'url': 'https://random.url'}
        self.assertIs(self.normalizer.get_provider(attributes), None)

    def test_provider_missing_attribute(self):
        """Parameter method must return None if the attribute is missing"""
        self.assertEqual(self.normalizer.get_provider({}), None)

    def test_entry_id_copernicus(self):
        """entry_id from sentinelSafeMetadataNormalizer """
        attributes = {
            'url': "https://scihub.copernicus.eu/apihub/odata/v1/Products('1a4ff15b-1504-4d94-8675-e12c06b02858')/$value",
            'Identifier': 'finename_value'}
        self.assertEqual(self.normalizer.get_entry_id(
            attributes), 'finename_value')

    def test_entry_id_missing_attribute(self):
        """entry_id method must return None if the attribute is missing"""
        self.assertIsNone(self.normalizer.get_entry_id({}))

    def test_entry_id_is_none_for_non_scihub_url(self):
        """No entry_id must be returned if the URL is not one from Copernicus scihub"""
        attributes = {'url': 'https://random.url'}
        self.assertIsNone(self.normalizer.get_entry_id(attributes))
