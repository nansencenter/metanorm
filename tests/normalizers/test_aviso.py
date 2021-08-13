"""Tests for the AVISO altimetry normalizer"""

import unittest
import unittest.mock as mock
from collections import OrderedDict
from datetime import datetime, timezone

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


class AVISOAltimetryMetadataNormalizerTests(unittest.TestCase):
    """Tests for the AVISOaltimetryMetadataNormalizer normalizer"""

    def setUp(self):
        self.normalizer = normalizers.AVISOAltimetryMetadataNormalizer()

    def test_check(self):
        """check() should return True when dealing with an AVISO
        altimetry dataset
        """
        self.assertTrue(self.normalizer.check({
            'creator_url': 'https://www.aviso.altimetry.fr',
            'creator_email': 'aviso@altimetry.fr'
        }))

        self.assertTrue(self.normalizer.check({
            'creator_url': 'http://www.aviso.altimetry.fr',
            'creator_email': 'aviso@altimetry.fr'
        }))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({
            'creator_url': 'https://foo/bar.nc',
            'creator_email': 'aviso@altimetry.fr'
        }))
        self.assertFalse(self.normalizer.check({
            'creator_url': 'http://www.aviso.altimetry.fr',
            'creator_email': 'foo@bar.fr'
        }))
        self.assertFalse(self.normalizer.check({'creator_url': 'http://www.aviso.altimetry.fr'}))
        self.assertFalse(self.normalizer.check({'creator_email': 'aviso@altimetry.fr'}))

    def test_get_entry_title(self):
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
            self.normalizer.get_summary({'comment': 'lorem ipsum', 'processing_level': 'L3C'}),
            'Description: lorem ipsum;Processing level: 3C')

    def test_get_summary_missing_raw_attributes(self):
        """A MetadataNormalizationError must be raised when any of the
        raw attributes used to build the summary is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_summary({'comment': 'lorem ipsum'})
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
        self.assertDictEqual(
            self.normalizer.get_platform({}),
            OrderedDict([
                ('Category', 'Earth Observation Satellites'),
                ('Series_Entity', ''),
                ('Short_Name', ''),
                ('Long_Name', '')])
        )

    def test_get_instrument(self):
        """Test getting the instrument"""
        self.assertDictEqual(
            self.normalizer.get_instrument({}),
            OrderedDict([
                ('Category', 'Earth Remote Sensing Instruments'),
                ('Class', 'Active Remote Sensing'),
                ('Type', 'Altimeters'),
                ('Subtype', ''),
                ('Short_Name', ''),
                ('Long_Name', '')])
        )

    def test_get_location_geometry(self):
        """Test getting the geometry"""
        self.assertEqual(self.normalizer.get_location_geometry({'geometry': 'wkt'}), 'wkt')

    def test_missing_geometry(self):
        """A MetadataNormalizationError must be raised when the
        geometry raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({})

    def test_get_provider(self):
        """Test getting the provider"""
        self.assertDictEqual(
            self.normalizer.get_provider({}),
            OrderedDict([
                ('Bucket_Level0', 'COMMERCIAL'),
                ('Bucket_Level1', ''),
                ('Bucket_Level2', ''),
                ('Bucket_Level3', ''),
                ('Short_Name', 'AVISO'),
                ('Long_Name',
                'Archiving, Validation and Interpretation of Satellite Oceanographic Data'),
                ('Data_Center_URL', 'http://www.aviso.oceanobs.com/')])
        )
