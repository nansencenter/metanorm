"""Tests for the base GeoSPaaS normalizer"""

import logging
import unittest
import unittest.mock as mock
from collections import OrderedDict

import metanorm.errors as errors
import metanorm.normalizers as normalizers
import metanorm.utils as utils


class GeoSPaaSMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for GeoSPaaSMetadataNormalizer"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.GeoSPaaSMetadataNormalizer()

    def test_check(self):
        """check() should always return False"""
        self.assertFalse(self.normalizer.check({}))

    def test_get_entry_title(self):
        """get_entry_title() should be raise a NotImplementedError"""
        with self.assertRaises(NotImplementedError):
            self.normalizer.get_entry_title({})

    def test_get_entry_id(self):
        """get_entry_id() should be raise a NotImplementedError"""
        with self.assertRaises(NotImplementedError):
            self.normalizer.get_entry_id({})

    def test_summary(self):
        """get_summary() should return the UNKNOWN value defined in
        utils as default value
        """
        self.assertEqual(self.normalizer.get_summary({}), utils.UNKNOWN)

    def test_get_time_coverage_start(self):
        """get_time_coverage_start() should be raise a
        NotImplementedError
        """
        with self.assertRaises(NotImplementedError):
            self.normalizer.get_time_coverage_start({})

    def test_get_time_coverage_end(self):
        """get_time_coverage_end() should be raise a
        NotImplementedError
        """
        with self.assertRaises(NotImplementedError):
            self.normalizer.get_time_coverage_end({})

    def test_get_platform(self):
        """get_platform() should be raise a NotImplementedError"""
        with self.assertRaises(NotImplementedError):
            self.normalizer.get_platform({})

    def test_get_instrument(self):
        """get_instrument() should be raise a NotImplementedError"""
        with self.assertRaises(NotImplementedError):
            self.normalizer.get_instrument({})

    def test_get_location_geometry(self):
        """get_location_geometry() should be raise a NotImplementedError"""
        with self.assertRaises(NotImplementedError):
            self.normalizer.get_location_geometry({})

    def test_get_provider(self):
        """get_provider() should be raise a NotImplementedError"""
        with self.assertRaises(NotImplementedError):
            self.normalizer.get_provider({})

    def test_iso_topic_category(self):
        """get_iso_topic_category() should return the "Oceans" keyword
        as default value
        """
        self.assertDictEqual(
            self.normalizer.get_iso_topic_category({}),
            OrderedDict([('iso_topic_category', 'Oceans')])
        )

    def test_iso_topic_category_pti_error(self):
        """A MetadataNormalizationError must be raised in case of pythesint error"""
        with mock.patch('pythesint.get_iso19115_topic_category', side_effect=IndexError):
            with self.assertRaises(errors.MetadataNormalizationError):
                _ = self.normalizer.get_iso_topic_category({})

    def test_gcmd_location(self):
        """get_gcmd_location() should return the "SEA SURFACE" keyword
        as default value
        """
        self.assertDictEqual(
            self.normalizer.get_gcmd_location({}),
            OrderedDict([
                ('Location_Category', 'VERTICAL LOCATION'),
                ('Location_Type', 'SEA SURFACE'),
                ('Location_Subregion1', ''),
                ('Location_Subregion2', ''),
                ('Location_Subregion3', '')
            ])
        )

    def test_gcmd_location_pti_error(self):
        """A MetadataNormalizationError must be raised in case of pythesint error"""
        with mock.patch('pythesint.get_gcmd_location', side_effect=IndexError):
            with self.assertRaises(errors.MetadataNormalizationError):
                _ = self.normalizer.get_gcmd_location({})

    def test_get_dataset_parameters(self):
        """Test getting parameters from the 'raw_dataset_parameters'
        attribute
        """
        with mock.patch('metanorm.utils.get_cf_or_wkv_standard_name') as mock_utils_get:
            mock_utils_get.side_effect = ('foo', 'bar')
            self.assertCountEqual(
                self.normalizer.get_dataset_parameters({'raw_dataset_parameters': ['baz', 'qux']}),
                ['foo', 'bar'])

    def test_get_dataset_parameters_pti_error(self):
        """get_dataset_parameters() should log a warning and continue
        processing if no parameter is found using pythesint
        """
        with mock.patch('metanorm.utils.get_cf_or_wkv_standard_name') as mock_utils_get:
            mock_utils_get.side_effect = (IndexError, 'bar')
            with self.assertLogs(normalizers.geospaas.base.logger, level=logging.WARNING):
                self.assertCountEqual(
                    self.normalizer.get_dataset_parameters({
                        'raw_dataset_parameters': ['baz', 'qux']
                    }),
                    ['bar'])

    def test_get_dataset_parameters_no_raw_parameters(self):
        """get_dataset_parameters() should return an empty string when
        'raw_dataset_parameters' is not present in the raw metadata
        """
        self.assertListEqual(self.normalizer.get_dataset_parameters({}), [])

    def test_normalize(self):
        """Test that the normalize method returns the right attributes
        """

        class TestNormalizer(normalizers.geospaas.GeoSPaaSMetadataNormalizer):
            """Normalizer class inheriting from
            GeoSPaaSMetadataNormalizer for testing purposes
            """

            def get_entry_title(self, raw_metadata):
                """Get the entry title from the raw metadata"""
                return 'entry_title'

            def get_entry_id(self, raw_metadata):
                """Get the entry ID from the raw metadata"""
                return 'entry_id'

            def get_summary(self, raw_metadata):
                """Get the summary from the raw metadata"""
                return 'summary'

            def get_time_coverage_start(self, raw_metadata):
                """Get the start of the time coverage from the raw metadata"""
                return 'time_coverage_start'

            def get_time_coverage_end(self, raw_metadata):
                """Get the end of the time coverage from the raw metadata"""
                return 'time_coverage_end'

            def get_platform(self, raw_metadata):
                """Get the platform from the raw metadata"""
                return 'platform'

            def get_instrument(self, raw_metadata):
                """Get the instrument from the raw metadata"""
                return 'instrument'

            def get_location_geometry(self, raw_metadata):
                """Get the location geometry (in WKT or GeoJSON) from the raw
                metadata
                """
                return 'location_geometry'

            def get_provider(self, raw_metadata):
                """Get the provider from the raw metadata"""
                return 'provider'

            @utils.raises(IndexError)
            def get_iso_topic_category(self, raw_metadata):
                """Get the ISO topic category from the raw metadata"""
                return 'iso_topic_category'

            @utils.raises(IndexError)
            def get_gcmd_location(self, raw_metadata):
                """Get the GCMD location from the raw metadata"""
                return 'gcmd_location'

            def get_dataset_parameters(self, raw_metadata):
                """Get the dataset parameters, if any, from the raw metadata"""
                return 'dataset_parameters'

        self.assertDictEqual(
            TestNormalizer().normalize({}),
            {
                'entry_title': 'entry_title',
                'entry_id': 'entry_id',
                'summary': 'summary',
                'time_coverage_start': 'time_coverage_start',
                'time_coverage_end': 'time_coverage_end',
                'platform': 'platform',
                'instrument': 'instrument',
                'location_geometry': 'location_geometry',
                'provider': 'provider',
                'iso_topic_category': 'iso_topic_category',
                'gcmd_location': 'gcmd_location',
                'dataset_parameters': 'dataset_parameters'
            }
        )
