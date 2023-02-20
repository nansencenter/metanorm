"""Tests for the OSISAF metadata normalizer"""
import unittest
import unittest.mock as mock

import dateutil
from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


class OSISAFMetadataNormalizer(unittest.TestCase):
    """Tests for the OSISAF attributes normalizer"""

    def setUp(self):
        self.normalizer = normalizers.OSISAFMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({'project_name': 'EUMETSAT OSI SAF'}))

        self.assertFalse(self.normalizer.check({'project_name': 'foo'}))
        self.assertFalse(self.normalizer.check({}))

    def test_entry_title(self):
        """Test getting the title"""
        self.assertEqual(self.normalizer.get_entry_title({'title': 'foo'}), 'foo')

    def test_missing_entry_title(self):
        """A MetadataNormalizationError must be raised when the raw
        title attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_title({})

    def test_get_entry_id(self):
        """Test getting the entry ID from the URL"""
        self.assertEqual(self.normalizer.get_entry_id({'url': 'https://foo/bar/baz.nc'}), 'baz')
        self.assertEqual(
            self.normalizer.get_entry_id({'url': 'https://foo/bar/baz.nc.dods'}), 'baz')

    def test_get_entry_id_no_url(self):
        """A MetadataNormalizationError must be raised when the raw
        url attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})

    def test_summary(self):
        """Test getting the summary"""

        attributes = {'abstract': 'value_abs'}
        self.assertEqual(self.normalizer.get_summary(attributes), 'Description: value_abs')

    def test_get_summary_missing_raw_attributes(self):
        """A MetadataNormalizationError must be raised when any of the
        raw attributes used to build the summary is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_summary({})

    def test_time_coverage_start(self):
        """Test getting the start of the time coverage"""
        attributes = {'start_date': '2020-07-12 00:00:00'}
        self.assertEqual(self.normalizer.get_time_coverage_start(attributes),
                         dateutil.parser.parse("2020-07-12").replace(tzinfo=tzutc()))

    def test_missing_time_coverage_start(self):
        """A MetadataNormalizationError must be raised when the
        time_coverage_start raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_time_coverage_end(self):
        """Test getting the end of the time coverage."""
        attributes = {'stop_date': '2020-07-14 00:00:00'}
        self.assertEqual(self.normalizer.get_time_coverage_end(attributes),
                         dateutil.parser.parse("2020-07-14").replace(tzinfo=tzutc()))

    def test_missing_time_coverage_end(self):
        """A MetadataNormalizationError must be raised when the
        time_coverage_end raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})

    def test_gcmd_platform(self):
        """Test getting the platform"""
        with mock.patch('metanorm.utils.get_gcmd_platform') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_platform({}),
                mock_get_gcmd_method.return_value)

    def test_get_instrument_from_instrument_type(self):
        """Test getting the instrument from the 'instrument_type'
        attribute
        """
        with mock.patch('metanorm.utils.get_gcmd_instrument') as mock_get_gcmd_instrument:
            mock_get_gcmd_instrument.return_value = 'instrument'
            self.assertEqual(
                self.normalizer.get_instrument({'instrument_type': 'value_1'}), 'instrument')
        mock_get_gcmd_instrument.assert_called_once_with('value_1')

    def test_get_instrument_radiometer(self):
        """Test getting a spectrometer/radiometer instrument from the
        'product_name' attribute
        """
        with mock.patch('metanorm.utils.get_gcmd_instrument') as mock_get_gcmd_instrument:
            self.assertEqual(
                self.normalizer.get_instrument({'product_name': 'osi_saf_ice_conc'}),
                mock_get_gcmd_instrument.return_value)
            mock_get_gcmd_instrument.assert_called_with('Imaging Spectrometers/Radiometers')

            self.assertEqual(
                self.normalizer.get_instrument({'product_name': 'osi_saf_ice_type'}),
                mock_get_gcmd_instrument.return_value)
            mock_get_gcmd_instrument.assert_called_with('Imaging Spectrometers/Radiometers')

            self.assertEqual(
                self.normalizer.get_instrument({'product_name': 'osi_saf_ice_edge'}),
                mock_get_gcmd_instrument.return_value)
            mock_get_gcmd_instrument.assert_called_with('Imaging Spectrometers/Radiometers')

    def test_get_instrument_amsr2(self):
        """Test getting an AMSR2 instrument from the 'product_name'
        attribute
        """
        with mock.patch('metanorm.utils.get_gcmd_instrument') as mock_get_gcmd_instrument:
            self.assertEqual(
                self.normalizer.get_instrument({'product_name': 'osi_saf_amsr2ice_conc'}),
                mock_get_gcmd_instrument.return_value)
            mock_get_gcmd_instrument.assert_called_with('AMSR2')

    def test_instrument_avhrr(self):
        """Test getting an AVHRR instrument from the 'product_name'
        attribute
        """
        with mock.patch('metanorm.utils.get_gcmd_instrument') as mock_get_gcmd_instrument:
            self.assertEqual(
                self.normalizer.get_instrument({'product_name': 'osi_saf_mr_ice_drift'}),
                mock_get_gcmd_instrument.return_value)
            mock_get_gcmd_instrument.assert_called_with('AVHRR')

    def test_get_instrument_default(self):
        """Test getting the default instrument"""
        with mock.patch('metanorm.utils.get_gcmd_instrument') as mock_get_gcmd_instrument:
            self.assertEqual(
                self.normalizer.get_instrument({'product_name': 'osi_saf_lr_ice_drift'}),
                mock_get_gcmd_instrument.return_value)
            mock_get_gcmd_instrument.assert_called_with('Earth Remote Sensing Instruments')

            self.assertEqual(
                self.normalizer.get_instrument({'product_name': 'osi_saf_2'}),
                mock_get_gcmd_instrument.return_value)
            mock_get_gcmd_instrument.assert_called_with('Earth Remote Sensing Instruments')

            self.assertEqual(
                self.normalizer.get_instrument({}),
                mock_get_gcmd_instrument.return_value)
            mock_get_gcmd_instrument.assert_called_with('Earth Remote Sensing Instruments')

    def test_location_geometry(self):
        """Test getting the location_geometry, with and without the
        typo in the "northernmost" attribute
        """
        expected_geometry = ('POLYGON((' +
             '-175.084000 -15.3505001,' +
             '-142.755005 -15.3505001,' +
             '-142.755005 9.47472000,' +
             '-175.084000 9.47472000,' +
             '-175.084000 -15.3505001))')

        self.assertEqual(expected_geometry, self.normalizer.get_location_geometry({
            'northernsmost_latitude': "9.47472000",
            'southernmost_latitude': "-15.3505001",
            'easternmost_longitude': "-142.755005",
            'westernmost_longitude': "-175.084000"
        }))

        self.assertEqual(expected_geometry, self.normalizer.get_location_geometry({
            'northernmost_latitude': "9.47472000",
            'southernmost_latitude': "-15.3505001",
            'easternmost_longitude': "-142.755005",
            'westernmost_longitude': "-175.084000"
        }))

    def test_gcmd_provider(self):
        """Test getting the provider"""
        with mock.patch('metanorm.utils.get_gcmd_provider') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_provider({}),
                mock_get_gcmd_method.return_value)
