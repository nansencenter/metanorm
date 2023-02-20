"""Tests for the ACDD metadata normalizer"""
import unittest
import unittest.mock as mock
from datetime import datetime

from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


class EarthdataCMRMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the Creodias API attributes normalizer"""

    def setUp(self):
        self.normalizer = normalizers.EarthdataCMRMetadataNormalizer()

    def test_check(self):
        """Test checking condition"""
        self.assertTrue(self.normalizer.check({'meta': {}, 'umm': {}}))
        self.assertTrue(self.normalizer.check({'umm': {}, 'meta': {}, 'url': ''}))

        self.assertFalse(self.normalizer.check({}))

    def test_entry_id(self):
        """Test getting the ID"""
        attributes = {
            'umm': {
                "DataGranule": {
                    "Identifiers": [
                        {
                            "IdentifierType": "ProducerGranuleId",
                            "Identifier": "V2020245000600.L2_SNPP_OC.nc"
                        }
                    ]
                }
            }
        }
        self.assertEqual(self.normalizer.get_entry_id(attributes), 'V2020245000600.L2_SNPP_OC')

    def test_entry_id_missing_attribute(self):
        """A MetadataNormalizationError must be raised if the raw
        attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({'umm': {'foo': 'bar'}})

    def test_entry_title(self):
        """Test getting the title"""
        attributes = {
            'umm': {
                "DataGranule": {
                    "Identifiers": [
                        {
                            "IdentifierType": "ProducerGranuleId",
                            "Identifier": "V2020245000600.L2_SNPP_OC.nc"
                        }
                    ]
                }
            }
        }
        self.assertEqual(self.normalizer.get_entry_title(attributes), 'V2020245000600.L2_SNPP_OC')

    def test_entry_title_missing_attribute(self):
        """A MetadataNormalizationError must be raised if the raw
        attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_title({})
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_title({'umm': {'foo': 'bar'}})

    def test_summary(self):
        """Test getting the summary"""
        attributes = {
            "umm": {
                "TemporalExtent": {
                    "RangeDateTime": {
                        "BeginningDateTime": "2020-09-01T00:06:00Z",
                        "EndingDateTime": "2020-09-01T00:11:59Z"
                    }
                },
                "Platforms": [
                    {
                        "ShortName": "SUOMI-NPP",
                        "Instruments": [
                            {
                                "ShortName": "VIIRS"
                            }
                        ]
                    }
                ],
                "CollectionReference": {
                    "ShortName": "VIIRSN_L2_OC",
                    "Version": "2018"
                }
            }
        }
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: Platform=SUOMI-NPP, ' +
            'Instrument=VIIRS, Start date=2020-09-01T00:06:00Z;' +
            'Processing level: 2')

    def test_summary_missing_attribute(self):
        """A MetadataNormalizationError must be raised if the raw
        attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_summary({})
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_summary({"umm": {'foo': 'bar'}})

    def test_time_coverage_start(self):
        """Test getting the start of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                "umm": {
                    "TemporalExtent": {
                        "RangeDateTime": {
                            "BeginningDateTime": "2020-09-01T00:06:00Z",
                            "EndingDateTime": "2020-09-01T00:11:59Z"
                        }
                    }
                }
            }),
            datetime(year=2020, month=9, day=1, hour=0, minute=6, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_missing_attribute(self):
        """A MetadataNormalizationError must be raised if the raw
        attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({"umm": {'foo': 'bar'}})

    def test_time_coverage_end(self):
        """Test getting the end of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                "umm": {
                    "TemporalExtent": {
                        "RangeDateTime": {
                            "BeginningDateTime": "2020-09-01T00:06:00Z",
                            "EndingDateTime": "2020-09-01T00:11:59Z"
                        }
                    }
                }
            }),
            datetime(year=2020, month=9, day=1, hour=0, minute=11, second=59, tzinfo=tzutc()))

    def test_time_coverage_end_missing_attribute(self):
        """A MetadataNormalizationError must be raised if the raw
        attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({'umm': {'foo': 'bar'}})

    def test_platform(self):
        """Test getting the platform"""
        with mock.patch('metanorm.utils.get_gcmd_platform') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_platform({'umm': {
                    "Platforms": [
                        {
                            "ShortName": "SUOMI-NPP",
                            "Instruments": [
                                {
                                    "ShortName": "VIIRS"
                                }
                            ]
                        }
                    ]
                }}),
                mock_get_gcmd_method.return_value)
            mock_get_gcmd_method.assert_called_with('SUOMI-NPP')

    def test_platform_missing_attribute(self):
        """A MetadataNormalizationError must be raised if the raw
        attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_platform({})
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_platform({'umm': {'foo': 'bar'}})

    def test_instrument(self):
        """Test getting the instrument"""
        with mock.patch('metanorm.utils.get_gcmd_instrument') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_instrument({'umm': {
                    "Platforms": [
                        {
                            "ShortName": "SUOMI-NPP",
                            "Instruments": [
                                {
                                    "ShortName": "VIIRS"
                                }
                            ]
                        }
                    ]
                }}),
                mock_get_gcmd_method.return_value)
            mock_get_gcmd_method.assert_called_with('VIIRS')

    def test_instrument_missing_attribute(self):
        """A MetadataNormalizationError must be raised if the raw
        attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_instrument({})
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_instrument({'umm': {'foo': 'bar'}})

    def test_location_geometry(self):
        """Test getting the location_geometry"""

        attributes = {
            'umm': {
                "SpatialExtent": {
                    "HorizontalSpatialDomain": {
                        "Geometry": {
                            "BoundingRectangles": [
                                {
                                    "EastBoundingCoordinate": -84.524773,
                                    "SouthBoundingCoordinate": -84.093506,
                                    "NorthBoundingCoordinate": -54.569214,
                                    "WestBoundingCoordinate": 155.812729
                                }
                            ]
                        }
                    }
                }
            }
        }
        expected_wkt = ('POLYGON(('
            '155.812729 -84.093506,'
            '-84.524773 -84.093506,'
            '-84.524773 -54.569214,'
            '155.812729 -54.569214,'
            '155.812729 -84.093506))')

        self.assertEqual(self.normalizer.get_location_geometry(attributes), expected_wkt)

    def test_location_geometry_missing_attribute(self):
        """A MetadataNormalizationError must be raised if the raw
        attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({})
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({'umm': {'foo': 'bar'}})

    def test_get_provider(self):
        """Test getting the provider"""
        with mock.patch('metanorm.utils.get_gcmd_provider') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_provider({"meta": {"provider-id": "OB_DAAC"}}),
                mock_get_gcmd_method.return_value)
            mock_get_gcmd_method.assert_called_with(['OB_DAAC'])

    def test_unknown_provider_returns_none(self):
        """A MetadataNormalizationError must be raised if the provider
        is not found using pythesint
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_provider({"meta": {"provider-id": "something"}})

    def test_provider_missing_attribute(self):
        """A MetadataNormalizationError must be raised if the raw
        attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_provider({})
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_provider({'meta': {'foo': 'bar'}})
