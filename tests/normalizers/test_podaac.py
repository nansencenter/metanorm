"""Tests for the PODAAC noramlizer"""

import unittest
import unittest.mock as mock
from collections import OrderedDict
from datetime import datetime, timezone

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


class PODAACMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for PODAACMetadataNormalizer"""

    def setUp(self):
        self.normalizer = normalizers.PODAACMetadataNormalizer()

    def test_check(self):
        """check() should return True when dealing with a PODAAC
        OpenDAP URL
        """
        self.assertTrue(self.normalizer.check({
            'url': 'https://opendap.jpl.nasa.gov/opendap/allData/ghrsst/foo.nc'
        }))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'https://foo/bar.nc'}))

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
        self.assertEqual(self.normalizer.get_entry_id({'url': 'https://foo/bar/baz.nc.gz'}), 'baz')
        self.assertEqual(self.normalizer.get_entry_id({'url': 'https://foo/bar/baz.h5'}), 'baz')
        self.assertEqual(self.normalizer.get_entry_id({'url': 'https://foo/bar/baz.h5.gz'}), 'baz')

    def test_get_entry_id_no_url(self):
        """A MetadataNormalizationError must be raised when the raw
        url attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})

    def test_get_entry_id_url_not_matching(self):
        """A MetadataNormalizationError must be raised when the raw
        url does not have the expected structure
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({'url': 'something'})

    def test_get_summary(self):
        """Test getting the summary"""
        self.assertEqual(
            self.normalizer.get_summary({'summary': 'lorem ipsum', 'processing_level': 'L3C'}),
            'Description: lorem ipsum;Processing level: 3C')

    def test_get_summary_missing_raw_attributes(self):
        """A MetadataNormalizationError must be raised when any of the
        raw attributes used to build the summary is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_summary({'summary': 'lorem ipsum'})
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_summary({'processing_level': 'L3C'})

    def test_get_time_coverage_start(self):
        """Test getting the start of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'time_coverage_start': "20200101T000001"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=0, second=1))
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'time_coverage_start': "20200101T000001Z"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=0, second=1, tzinfo=timezone.utc))
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'time_coverage_start': "2020-01-01T00:00:01"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=0, second=1))
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'time_coverage_start': "2020-01-01T00:00:01Z"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=0, second=1, tzinfo=timezone.utc))

    def test_missing_time_coverage_start(self):
        """A MetadataNormalizationError must be raised when the
        time_coverage_start raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_get_time_coverage_end(self):
        """Test getting the end of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'time_coverage_end': "20200101T000559"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=5, second=59))
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'time_coverage_end': "20200101T000559Z"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=5, second=59, tzinfo=timezone.utc))
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'time_coverage_end': "2020-01-01T00:05:59"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=5, second=59))
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'time_coverage_end': "2020-01-01T00:05:59Z"}),
            datetime(year=2020, month=1, day=1, hour=0, minute=5, second=59, tzinfo=timezone.utc))

    def test_missing_time_coverage_end(self):
        """A MetadataNormalizationError must be raised when the
        time_coverage_end raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})

    def test_get_platform(self):
        """Test getting the platform"""
        with mock.patch('metanorm.utils.get_gcmd_platform') as mock_get_platform:
            mock_get_platform.side_effect = lambda p: {'SENTINEL-1A': 'foo'}[p]
            self.assertEqual(self.normalizer.get_platform({'platform': 'SENTINEL-1A'}), 'foo')

    def test_missing_platform(self):
        """A MetadataNormalizationError must be raised when the
        platform raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_platform({})

    def test_get_instrument(self):
        """Test getting the instrument"""
        with mock.patch('metanorm.utils.get_gcmd_instrument') as mock_get_instrument:
            mock_get_instrument.side_effect = lambda p: {'VIIRS': 'foo'}[p]
            self.assertEqual(self.normalizer.get_instrument({'sensor': 'VIIRS'}), 'foo')

    def test_missing_sensor(self):
        """A MetadataNormalizationError must be raised when the
        sensor raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_instrument({})

    def test_get_location_geometry_from_geospatial_bounds(self):
        """Test getting the location geometry from the
        geospatial_bounds attribute
        """
        geometry = (
            'POLYGON((' +
            '-29.04 61.31,' +
            '-18.32 59.66,' +
            '-20.25 51.06,' +
            '-38.97 55.12,' +
            '-29.04 61.31))')

        self.assertEqual(
            self.normalizer.get_location_geometry({
                'geospatial_bounds': geometry,
                'geospatial_bounds_crs': 'EPSG:3413',
                'easternmost_longitude': '-18.32',
                'westernmost_longitude': '-38.97'
            }),
            'SRID=3413;' + geometry)

        self.assertEqual(
            self.normalizer.get_location_geometry({'geospatial_bounds': geometry}),
            geometry)

    def test_get_location_geometry_from_geospatial_bounds_split_polygon(self):
        """Test getting the location geometry from the
        geospatial_bounds attribute with a polygon crossing the IDL
        """
        geometry = ('POLYGON((' +
            '-148.262 60.400, ' +
            '-147.443 25.982, ' +
            '-177.157 21.480, ' +
            '161.791 52.861, ' +
            '-148.262 60.400))')

        self.assertEqual(
            self.normalizer.get_location_geometry({
                'geospatial_bounds': geometry,
                'easternmost_longitude': '-177.157',
                'westernmost_longitude': '161.791'
            }),
            'MULTIPOLYGON ((('
            '-148.262 60.4, '
            '-147.443 25.982, '
            '-177.157 21.48, '
            '-180 25.71789582937487, '
            '-180 55.60946639437804, '
            '-148.262 60.4)), '
            '((180 25.71789582937487, '
            '161.791 52.861, '
            '180 55.60946639437804, '
            '180 25.71789582937487)))')

    def test_get_location_geometry_from_geospatial_bounds_split_multipolygon(self):
        """Test getting the location geometry from the
        geospatial_bounds attribute with a multipolygon crossing the
        IDL
        """
        geometry = ('MULTIPOLYGON('
            '((-188.525390625 60.37042901631506,'
            '-165.14648437500003 56.46249048388978,'
            '-187.82226562500003 48.283192895483495,'
            '-173.23242187500006 55.92458580482949,'
            '-188.525390625 60.37042901631506)),'
            '((-184.833984375 57.984808019239864,'
            '-177.18749999999997 56.12106042504411,'
            '-185.2734375 52.48278022207825,'
            '-184.833984375 57.984808019239864),'
            '(-181.84570312499997 56.63206372054478,'
            '-184.306640625 55.677584411089526,'
            '-181.49414062499997 54.80068486732236,'
            '-181.84570312499997 56.63206372054478)))')

        self.assertEqual(
            self.normalizer.get_location_geometry({
                'geospatial_bounds': geometry,
                'easternmost_longitude': '-188.525390625',
                'westernmost_longitude': '-165.14648437500003'
            }),
            'MULTIPOLYGON ('
            '((171.474609375 60.37042901631506, '
            '180 58.94535368682163, '
            '180 57.89199918002712, '
            '171.474609375 60.37042901631506)), '
            '((-180 58.94535368682163, '
            '-165.146484375 56.46249048388978, '
            '-180 51.10473353644537, '
            '-180 52.38008427459071, '
            '-173.2324218750001 55.92458580482949, '
            '-180 57.89199918002712, -180 58.94535368682163)), '
            '((180 51.10473353644537, '
            '172.177734375 48.2831928954835, '
            '180 52.38008427459071, '
            '180 51.10473353644537)), '
            '((175.166015625 57.98480801923986, '
            '180 56.80657678152991, '
            '180 54.85557165879511, '
            '174.7265625 52.48278022207825, '
            '175.166015625 57.98480801923986), '
            '(178.154296875 56.63206372054478, '
            '175.693359375 55.67758441108953, '
            '178.505859375 54.80068486732236, '
            '178.154296875 56.63206372054478)), '
            '((-180 56.80657678152991, '
            '-177.1875 56.12106042504411, '
            '-180 54.85557165879511, '
            '-180 56.80657678152991)))')

    def test_get_location_geometry_unsupported_geometry(self):
        """An exception should be raised in case of geometry type which
        is not supported
        """
        geometry = ('LINESTRING(-188.525390625 50, -165.14648437500003 50)')

        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({
                'geospatial_bounds': geometry,
                'easternmost_longitude': '-188.525390625',
                'westernmost_longitude': '-165.14648437500003'
            })

    def test_get_location_geometry_from_bounding_box(self):
        """Test getting the location geometry from the
        "northernmost_latitude", etc... attributes
        """
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

        self.assertEqual(self.normalizer.get_location_geometry(attributes), expected_geometry)

    def test_get_location_geometry_from_bounding_box_split(self):
        """Test getting the location geometry from the
        "northernmost_latitude", etc... attributes in the case where
        it crosses the IDL
        """
        attributes = {
            'northernmost_latitude': "60",
            'southernmost_latitude': "50",
            'easternmost_longitude': "-175",
            'westernmost_longitude': "175"
        }
        expected_geometry = (
            'MULTIPOLYGON (('
            '(180 50, 175 50, 175 60, 180 60, 180 50)), '
            '((-180 60, -175 60, -175 50, -180 50, -180 60)))')

        self.assertEqual(self.normalizer.get_location_geometry(attributes), expected_geometry)

    def test_missing_geometry(self):
        """A MetadataNormalizationError must be raised when the
        geometry raw attributes are missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({})

        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({'northernmost_latitude': '9'})

    def test_get_provider(self):
        """Test getting the provider"""
        self.assertDictEqual(
            self.normalizer.get_provider({}),
            OrderedDict([
                ('Bucket_Level0', 'GOVERNMENT AGENCIES-U.S. FEDERAL AGENCIES'),
                ('Bucket_Level1', 'NASA'),
                ('Bucket_Level2', ''),
                ('Bucket_Level3', ''),
                ('Short_Name', 'NASA/JPL/PODAAC'),
                ('Long_Name',
                 'Physical Oceanography Distributed Active Archive Center, Jet Propulsion '
                 'Laboratory, NASA'),
                ('Data_Center_URL', 'https://podaac.jpl.nasa.gov/')
            ])
        )
