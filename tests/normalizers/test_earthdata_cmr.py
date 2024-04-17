"""Tests for the ACDD metadata normalizer"""
import unittest
import unittest.mock as mock
from collections import OrderedDict
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

    def test_entry_id_from_granuleUR(self):
        """Test getting the ID from the GranuleUR field"""
        attributes = {'umm': {'GranuleUR': 'foo'}}
        self.assertEqual(self.normalizer.get_entry_id(attributes), 'foo')

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
        attributes['umm']['CollectionReference']['ShortName'] = 'VIIRSN'
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: Platform=SUOMI-NPP, ' +
            'Instrument=VIIRS, Start date=2020-09-01T00:06:00Z')

    def test_summary_no_platform(self):
        """Test getting a summary when no platform info is available
        """
        attributes = {
            "umm": {
                "TemporalExtent": {
                    "RangeDateTime": {
                        "BeginningDateTime": "2020-09-01T00:06:00Z",
                        "EndingDateTime": "2020-09-01T00:11:59Z"
                    }
                },
                "CollectionReference": {
                    "ShortName": "VIIRSN_L2_OC",
                    "Version": "2018"
                }
            }
        }
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: Start date=2020-09-01T00:06:00Z;Processing level: 2')

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
        unknown_platform = OrderedDict([
            ('Category', 'Unknown'),
            ('Series_Entity', 'Unknown'),
            ('Short_Name', 'Unknown'),
            ('Long_Name', 'Unknown')
        ])
        self.assertDictEqual(self.normalizer.get_platform({}), unknown_platform)
        self.assertDictEqual(self.normalizer.get_platform({'umm': {'foo': 'bar'}}),
                             unknown_platform)

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

    def test_location_geometry_one_bounding_box(self):
        """Test getting the location_geometry from one bounding box"""

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
        expected_wkt = ('GEOMETRYCOLLECTION('
            'POLYGON(('
            '155.812729 -84.093506,'
            '-84.524773 -84.093506,'
            '-84.524773 -54.569214,'
            '155.812729 -54.569214,'
            '155.812729 -84.093506)))')
        self.assertEqual(self.normalizer.get_location_geometry(attributes), expected_wkt)

    def test_location_geometry_multiple_bounding_boxes(self):
        """Test getting the location_geometry from multiple bounding boxes"""

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
                                },
                                {
                                    "EastBoundingCoordinate": 80.0,
                                    "SouthBoundingCoordinate": 50.0,
                                    "NorthBoundingCoordinate": 60.0,
                                    "WestBoundingCoordinate": 70.0
                                }
                            ]
                        }
                    }
                }
            }
        }
        expected_wkt = ('GEOMETRYCOLLECTION('
            'POLYGON(('
            '155.812729 -84.093506,'
            '-84.524773 -84.093506,'
            '-84.524773 -54.569214,'
            '155.812729 -54.569214,'
            '155.812729 -84.093506)),'
            'POLYGON(('
            '70.0 50.0,'
            '80.0 50.0,'
            '80.0 60.0,'
            '70.0 60.0,'
            '70.0 50.0)))')
        self.assertEqual(self.normalizer.get_location_geometry(attributes), expected_wkt)

    def test_location_geometry_gpolygons(self):
        """Test getting the location_geometry from gpolygons"""

        attributes = {
            'umm': {
                "SpatialExtent": {
                    "HorizontalSpatialDomain": {
                        "Geometry": {
                            "GPolygons": [
                                {
                                    'Boundary': {
                                        'Points': [
                                            {'Longitude': 80.0, 'Latitude': 50.0},
                                            {'Longitude': 60.0, 'Latitude': 50.0},
                                            {'Longitude': 60.0, 'Latitude': 70.0},
                                            {'Longitude': 80.0, 'Latitude': 70.0},
                                            {'Longitude': 80.0, 'Latitude': 50.0},
                                        ]
                                    },
                                    'ExclusiveZone': {
                                        'Boundaries': [{
                                            'Points': [
                                                {'Longitude': 75, 'Latitude': 55},
                                                {'Longitude': 65, 'Latitude': 55},
                                                {'Longitude': 65, 'Latitude': 65},
                                                {'Longitude': 75, 'Latitude': 65},
                                                {'Longitude': 75, 'Latitude': 55},
                                            ]
                                        }]
                                    }
                                },
                                {
                                    'Boundary': {
                                        'Points': [
                                            {'Longitude': 20.0, 'Latitude': 40.0},
                                            {'Longitude': 20.0, 'Latitude': 30.0},
                                            {'Longitude': 10.0, 'Latitude': 30.0},
                                            {'Longitude': 20.0, 'Latitude': 40.0},
                                        ]
                                    },
                                }
                            ]
                        }
                    }
                }
            }
        }
        expected_wkt = (
            'GEOMETRYCOLLECTION('
            'POLYGON ((80 50, 60 50, 60 70, 80 70, 80 50), (75 55, 65 55, 65 65, 75 65, 75 55)),'
            'POLYGON ((20 40, 20 30, 10 30, 20 40)))')
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
