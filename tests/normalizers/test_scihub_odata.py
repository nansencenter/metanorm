"""Tests for the ACDD metadata normalizer"""
import unittest
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
        attributes = {'Satellite name': 'SENTINEL-1', 'Satellite number': 'B'}

        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', 'Sentinel-1'),
                         ('Short_Name', 'Sentinel-1B'),
                         ('Long_Name', 'Sentinel-1B')])
        )

    def test_non_gcmd_platform(self):
        """Non-GCMD platform from ScihubODataMetadataNormalizer"""
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
        Non-GCMD platform from ScihubODataMetadataNormalizer, with a name longer than 250 characters
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
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_platform({})

    def test_gcmd_instrument_from_get(self):
        """
        GCMD instrument from ScihubODataMetadataNormalizer which is found using
        `pythesint.get_gcmd_instrument()`
        """
        self.assertEqual(
            self.normalizer.get_instrument({'Instrument': 'MODIS'}),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', 'MODIS'),
                         ('Long_Name', 'Moderate-Resolution Imaging Spectroradiometer')]))

    def test_gcmd_instrument_from_search(self):
        """
        GCMD instrument from ScihubODataMetadataNormalizer which is found using
        `pythesint.search_gcmd_instrument_list()`
        """
        self.assertEqual(
            self.normalizer.get_instrument({'Instrument': 'SRAL'}),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Active Remote Sensing'),
                         ('Type', 'Altimeters'),
                         ('Subtype', 'Radar Altimeters'),
                         ('Short_Name', 'Sentinel-3 SRAL'),
                         ('Long_Name', 'Sentinel-3 SAR Radar Altimeter')]))

    def test_gcmd_instrument_from_restricted_search(self):
        """
        GCMD instrument from ScihubODataMetadataNormalizer which is found using
        `pythesint.search_gcmd_instrument_list()` and restricting the search with an
        additional keyword
        """
        self.assertEqual(
            self.normalizer.get_instrument({
                'Satellite name': 'SENTINEL-2',
                'Instrument': 'MSI'}),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', 'Sentinel-2 MSI'),
                         ('Long_Name', 'Sentinel-2 Multispectral Imager')]))

    def test_c_sar_instrument(self):
        """Special case for C-SAR GCMD instrument from ScihubODataMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_instrument(
                {'Satellite name': 'SENTINEL-1','Instrument': 'SAR-C SAR'}),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Active Remote Sensing'),
                         ('Type', 'Imaging Radars'),
                         ('Subtype', ''),
                         ('Short_Name', 'SENTINEL-1 C-SAR'),
                         ('Long_Name', '')]))

    def test_non_gcmd_instrument(self):
        """Non-GCMD instrument from ScihubODataMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_instrument({'Instrument': 'TEST'}),
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
        """Non-GCMD instrument from ScihubODataMetadataNormalizer,
        with a name longer than 200 characters
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

    def test_gcmd_provider_from_url(self):
        """GCMD provider from ScihubODataMetadataNormalizer"""
        expected_provider = OrderedDict([
            ('Bucket_Level0', 'MULTINATIONAL ORGANIZATIONS'),
            ('Bucket_Level1', ''),
            ('Bucket_Level2', ''),
            ('Bucket_Level3', ''),
            ('Short_Name', 'ESA/EO'),
            ('Long_Name', 'Observing the Earth, European Space Agency'),
            ('Data_Center_URL', 'http://www.esa.int/esaEO/')])

        attributes = {'url': 'https://scihub.copernicus.eu'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            expected_provider
        )

        attributes = {'url': 'https://apihub.copernicus.eu'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            expected_provider
        )

    def test_dataset_parameters_sentinel1(self):
        """Test getting the dataset parameters for Sentinel 1 datasets
        """
        self.assertListEqual(
            self.normalizer.get_dataset_parameters({
                'Identifier': 'S1B_IW_GRDH_1SDV_20210916T103902_20210916T103927_028722_036D80_C8D0'
            }),
            [
                OrderedDict([
                    ('standard_name', 'surface_backwards_scattering_coefficient_of_radar_wave'),
                    ('canonical_units', '1'),
                    ('definition', 'The scattering/absorption/attenuation coefficient is assumed to'
                                   ' be an integral over all wavelengths, unless a coordinate of '
                                   'radiation_wavelength is included to specify the wavelength. '
                                   'Scattering of radiation is its deflection from its incident '
                                   'path without loss of energy. Backwards scattering refers to the'
                                   ' sum of scattering into all backward angles i.e. '
                                   'scattering_angle exceeding pi/2 radians. A scattering_angle '
                                   'should not be specified with this quantity.')
                ])
            ]
        )

    def test_unknown_dataset_parameters(self):
        """An empty list should be returned if no parameter is found"""
        self.assertListEqual(self.normalizer.get_dataset_parameters({'Identifier': 'foo'}), [])
