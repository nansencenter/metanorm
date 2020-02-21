"""Tests for the well known metadata normalizer"""

import unittest
from collections import OrderedDict

from django.contrib.gis.geos.geometry import GEOSGeometry

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
        expected_geometry = GEOSGeometry(
            ('POLYGON((' +
             '-175.084000 -15.3505001,' +
             '-142.755005 -15.3505001,' +
             '-142.755005 9.47472000,' +
             '-175.084000 9.47472000,' +
             '-175.084000 -15.3505001))'),
            srid=4326)

        normalizer = normalizers.GeoSpatialWellKnownMetadataNormalizer(['location_geometry'])
        normalized_params = normalizer.normalize(attributes)

        self.assertIsInstance(normalized_params, dict)
        self.assertTrue('location_geometry' in normalized_params)
        self.assertTrue(normalized_params['location_geometry'].equals(expected_geometry))

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
        normalizer = normalizers.GeoSpatialWellKnownMetadataNormalizer(['instrument'])
        self.assertDictEqual(normalizer.normalize(attributes), expected_result)


if __name__ == '__main__':
    unittest.main()
