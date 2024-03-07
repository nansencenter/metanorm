"""Tests for the tabledap normalizer"""

import unittest
import unittest.mock as mock
from collections import OrderedDict
from datetime import datetime, timezone

import metanorm.normalizers as normalizers
import metanorm.utils as utils
from metanorm.errors import MetadataNormalizationError


class TableDAPMetadataNormalizerTests(unittest.TestCase):
    """Tests for TableDAPMetadataNormalizer"""

    def setUp(self):
        self.normalizer = normalizers.TableDAPMetadataNormalizer()
        self.empty_raw_metadata = {'product_metadata': {'table': {'rows': []}}}
        self.raw_metadata = {
            'entry_id': '123456',
            'url': 'http://foo/tabledap/bar.json',
            'temporal_coverage': ('2023-01-01T00:00:00Z', '2023-01-01T12:47:13Z'),
            'trajectory': 'LINESTRING (1 2, 3 4)',
            'product_metadata': {
                'table': {
                    'columnNames': [
                        "Row Type", "Variable Name", "Attribute Name", "Data Type", "Value"],
                    'rows': [
                        ["attribute", "NC_GLOBAL", "cdm_altitude_proxy", "String", "pres"],
                        ["attribute", "NC_GLOBAL", "cdm_data_type", "String", "TrajectoryProfile"],
                        ["attribute", "NC_GLOBAL", "time_coverage_end", "String",
                         "2026-12-27T14:48:20Z"],
                        ["attribute", "NC_GLOBAL", "time_coverage_start", "String",
                         "1997-07-28T20:26:20Z"],
                        ["attribute", "NC_GLOBAL", "title", "String", "Argo Float Measurements"],
                        ["attribute", "NC_GLOBAL", "summary", "String",
                         "Argo float vertical profiles from Coriolis Global Data Assembly Centres"],
                        ["attribute", "NC_GLOBAL", "source", "String", "Argo float"],
                        ["attribute", "NC_GLOBAL", "institution", "String", "Argo"],
                    ]
                }
            }
        }

    def test_get_product_attribute(self):
        """Test getting the value of an attribute from a tabledap
        product's metadata
        """
        self.assertEqual(
            normalizers.TableDAPMetadataNormalizer.get_product_attribute(
                self.raw_metadata['product_metadata'], 'cdm_data_type'),
            'TrajectoryProfile')
        with self.assertRaises(MetadataNormalizationError):
            normalizers.TableDAPMetadataNormalizer.get_product_attribute(
                self.raw_metadata['product_metadata'], 'foo')

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check(self.raw_metadata))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': ''}))
        self.assertFalse(self.normalizer.check({'url': '/foo/bar/baz.nc'}))

    def test_get_entry_title(self):
        """Test getting the title"""
        self.assertEqual(self.normalizer.get_entry_title(self.raw_metadata),
                         'Argo Float Measurements')

    def test_missing_title(self):
        """A MetadataNormalizationError should be raised if the raw title
        is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_title(self.empty_raw_metadata)

    def test_get_entry_id(self):
        """Test getting the ID"""
        self.assertEqual(self.normalizer.get_entry_id(self.raw_metadata), '123456')

    def test_entry_id_error(self):
        """A MetadataNormalizationError should be raised if ID is not found
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id(self.empty_raw_metadata)

    def test_summary(self):
        """Test getting the summary"""
        self.assertEqual(
            self.normalizer.get_summary(self.raw_metadata),
            'Argo float vertical profiles from Coriolis Global Data Assembly Centres')

    def test_get_time_coverage_start(self):
        """Test getting the start of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start(self.raw_metadata),
            datetime(year=2023, month=1, day=1, tzinfo=timezone.utc))

    def test_missing_time_coverage_start(self):
        """A MetadataNormalizationError must be raised when the
        time_coverage_start raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start(self.empty_raw_metadata)

    def test_get_time_coverage_end(self):
        """Test getting the end of the time coverage"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end(self.raw_metadata),
            datetime(year=2023, month=1, day=1, hour=12, minute=47, second=13, tzinfo=timezone.utc))

    def test_missing_time_coverage_end(self):
        """A MetadataNormalizationError must be raised when the
        time_coverage_end raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end(self.empty_raw_metadata)

    def test_gcmd_platform(self):
        """Test getting the platform"""
        with mock.patch('metanorm.utils.get_gcmd_platform') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_platform(self.raw_metadata),
                mock_get_gcmd_method.return_value)
            mock_get_gcmd_method.assert_called_with('Argo float')

    def test_gcmd_platform_unknow(self):
        """Test getting the platform with GCMD versions that don't
        support ARGO floats
        """
        with mock.patch('metanorm.utils.get_gcmd_platform') as mock_get_gcmd_method:
            mock_get_gcmd_method.return_value = {'Short_Name': utils.UNKNOWN}
            self.assertEqual(
                self.normalizer.get_platform(self.raw_metadata),
                OrderedDict([
                    ('Basis', 'Water-based Platforms'),
                    ('Category', 'Buoys'),
                    ('Sub_Category', 'Unmoored'),
                    ('Short_Name', 'Argo-Float'),
                    ('Long_Name', '')]))

    def test_gcmd_instrument(self):
        """Test getting the instrument"""
        self.assertEqual(
            self.normalizer.get_instrument(self.raw_metadata),
            OrderedDict([
                ('Category', utils.UNKNOWN),
                ('Class', utils.UNKNOWN),
                ('Type', utils.UNKNOWN),
                ('Subtype', utils.UNKNOWN),
                ('Short_Name', 'Unknown'),
                ('Long_Name', 'Unknown')]))

    def test_gcmd_provider(self):
        """Test getting the provider"""
        with mock.patch('metanorm.utils.get_gcmd_provider') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_provider(self.raw_metadata),
                mock_get_gcmd_method.return_value)

    def test_gcmd_provider_unknow(self):
        """Test getting the provider with GCMD versions that don't
        support ARGO floats
        """
        with mock.patch('metanorm.utils.get_gcmd_provider', return_value=None):
            self.assertEqual(
                self.normalizer.get_provider(self.raw_metadata),
                OrderedDict([
                    ('Bucket_Level0', 'CONSORTIA/INSTITUTIONS'),
                    ('Bucket_Level1', ''),
                    ('Bucket_Level2', ''),
                    ('Bucket_Level3', ''),
                    ('Short_Name', 'Argo'),
                    ('Long_Name', 'Argo'),
                    ('Data_Center_URL', '')]))

    def test_get_location_geometry(self):
        """get_location_geometry() should return the location
        of the dataset
        """
        self.assertEqual(
            self.normalizer.get_location_geometry(self.raw_metadata),
            'LINESTRING (1 2, 3 4)')
