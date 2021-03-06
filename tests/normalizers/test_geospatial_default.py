"""Tests for the default metadata normalizer"""

import unittest
import unittest.mock as mock
from collections import OrderedDict

import metanorm.errors as errors
import metanorm.normalizers as normalizers


class GeoSpatialDefaultMetadataNormalizerTestCase(unittest.TestCase):
    """
    Test case for the GeoSpatialDefaultMetadataNormalizer, mainly checking default values and raised
    exceptions
    """

    def setUp(self):
        self.normalizer = normalizers.GeoSpatialDefaultMetadataNormalizer([], [])

    def tearDown(self):
        self.normalizer = None

    def test_iso_topic_category(self):
        """ISO topic category default value"""
        self.assertDictEqual(
            self.normalizer.get_iso_topic_category({}),
            OrderedDict([('iso_topic_category', 'Oceans')])
        )

    def test_iso_topic_category_pti_error(self):
        """A MetadataNormalizationError must be raised in case of pythesint error"""
        pti_mock = mock.Mock(**{'get_iso19115_topic_category.side_effect': IndexError})

        with mock.patch('metanorm.normalizers.geospatial_defaults.pti', pti_mock):
            with self.assertRaises(errors.MetadataNormalizationError):
                _ = self.normalizer.get_iso_topic_category({})

    def test_gcmd_location(self):
        """gcmd_location default value"""
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
        pti_mock = mock.Mock(**{'get_gcmd_location.side_effect': IndexError})

        with mock.patch('metanorm.normalizers.geospatial_defaults.pti', pti_mock):
            with self.assertRaises(errors.MetadataNormalizationError):
                _ = self.normalizer.get_gcmd_location({})

    def test_summary(self):
        """summary default value"""
        self.assertEqual(self.normalizer.get_summary({}), 'Unknown')
