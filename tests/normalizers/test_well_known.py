"""Tests for the well known metadata normalizer"""

import unittest
from collections import OrderedDict

import metanorm.errors as errors
import metanorm.normalizers as normalizers


class GeoSpatialWellKnownMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the well known attributes normalizer"""

    def test_location_geometry(self):
        """location_geometry from GeoSpatialWellKnownMetadataNormalizer"""
        attributes = {
            'northernmost_latitude': "9.47472000",
            'southernmost_latitude': "-15.3505001",
            'easternmost_longitude': "-142.755005",
            'westernmost_longitude': "-175.084000"
        }
        expected_geometry = ('POLYGON((' +
             '-175.084000 -15.3505001,' +
             '-142.755005 -15.3505001,' +
             '-142.755005 9.47472000,' +
             '-175.084000 9.47472000,' +
             '-175.084000 -15.3505001))')

        normalizer = normalizers.GeoSpatialWellKnownMetadataNormalizer(['location_geometry'], [])
        normalized_params = normalizer.normalize(attributes)

        self.assertIsInstance(normalized_params, dict)
        self.assertTrue('location_geometry' in normalized_params)
        self.assertEqual(normalized_params['location_geometry'], expected_geometry)

    def test_missing_location_attribute(self):
        """If the location attributes are not all present, an exception must be raised"""
        normalizer = normalizers.GeoSpatialWellKnownMetadataNormalizer(['location_geometry'], [])
        with self.assertRaises(errors.MetadataNormalizationError):
            _ = normalizer.normalize({})

    def test_instrument(self):
        """instrument from GeoSpatialWellKnownMetadataNormalizer"""
        attributes = {'sensor': "VIIRS"}
        expected_result = {
            'instrument': OrderedDict([
                ('Category', 'Earth Remote Sensing Instruments'),
                ('Class', 'Passive Remote Sensing'),
                ('Type', 'Spectrometers/Radiometers'),
                ('Subtype', 'Imaging Spectrometers/Radiometers'),
                ('Short_Name', 'VIIRS'),
                ('Long_Name', 'Visible-Infrared Imager-Radiometer Suite')
            ])
        }
        normalizer = normalizers.GeoSpatialWellKnownMetadataNormalizer(['instrument'], [])
        self.assertDictEqual(normalizer.normalize(attributes), expected_result)

    def test_missing_instrument_attribute(self):
        """If the 'sensor' attribute is not present, an exception must be raised"""
        normalizer = normalizers.GeoSpatialWellKnownMetadataNormalizer(['instrument'], [])
        with self.assertRaises(errors.MetadataNormalizationError):
            _ = normalizer.normalize({})
