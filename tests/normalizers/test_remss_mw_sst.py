"""Tests for the REMSS MW SST normalizer"""
import unittest
import unittest.mock as mock
from datetime import datetime
from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


class REMSSMWSSTMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the REMSS MW SST ftp normalizer"""
    def setUp(self):
        self.normalizer = normalizers.geospaas.REMSSMWSSTMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check(
            {'url': 'https://data.remss.com/SST/daily/mw/v05.1/netcdf/2024/'
                    '20240108120000-REMSS-L4_GHRSST-SSTfnd-MW_OI-GLOB-v02.0-fv05.1.nc'}))
        self.assertTrue(self.normalizer.check(
            {'url': 'ftp://ftp.remss.com/SST/daily/mw/v05.1/netcdf/2024/'
                    '20240108120000-REMSS-L4_GHRSST-SSTfnd-MW_OI-GLOB-v02.0-fv05.1.nc'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

    def test_entry_title(self):
        """entry_title from REMSSMWSSTMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_entry_title({}),
            'Sea surface temperature from passive microwave sensors')

    def test_entry_id(self):
        """entry_id from REMSSMWSSTMetadataNormalizer """
        attributes = {'url': 'https://data.remss.com/SST/daily/mw/v05.1/netcdf/2024/'
                             '20240108120000-REMSS-L4_GHRSST-SSTfnd-MW_OI-GLOB-v02.0-fv05.1.nc'}
        self.assertEqual(self.normalizer.get_entry_id(attributes),
                         '20240108120000-REMSS-L4_GHRSST-SSTfnd-MW_OI-GLOB-v02.0-fv05.1')

    def test_entry_id_error(self):
        """a MetadataNormalizationError must be raised when an entry_id cannot be found"""
        # wrong file format
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({'url': 'ftp://foo/bar.txt'})
        # no url attribute
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})

    def test_summary(self):
        """summary from REMSSMWSSTMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: Sea surface temperature from TMI, AMSR-E, AMSR2, WindSat, GMI;'
            'Processing level: 4')

    def test_time_coverage_start(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'https://data.remss.com/SST/daily/mw/v05.1/netcdf/2024/'
                        '20240108120000-REMSS-L4_GHRSST-SSTfnd-MW_OI-GLOB-v02.0-fv05.1.nc'}),
            datetime(year=2024, month=1, day=8, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_time_coverage_end(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'https://data.remss.com/SST/daily/mw/v05.1/netcdf/2024/'
                        '20240108120000-REMSS-L4_GHRSST-SSTfnd-MW_OI-GLOB-v02.0-fv05.1.nc'}),
            datetime(year=2024, month=1, day=9, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})

    def test_gcmd_platform(self):
        """Test getting the platform"""
        with mock.patch('metanorm.utils.get_gcmd_platform') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_platform({}),
                mock_get_gcmd_method.return_value)

    def test_gcmd_instrument(self):
        """Test getting the instrument"""
        with mock.patch('metanorm.utils.get_gcmd_instrument') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_instrument({}),
                mock_get_gcmd_method.return_value)

    def test_gcmd_provider(self):
        """Test getting the provider"""
        with mock.patch('metanorm.utils.get_gcmd_provider') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_provider({}),
                mock_get_gcmd_method.return_value)

    def test_location_geometry(self):
        """geometry from REMSSMWSSTMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_dataset_parameters(self):
        """dataset_parameters from CEDAESACCIMetadataNormalizer """
        with mock.patch('metanorm.utils.create_parameter_list') as mock_get_gcmd_method:
            self.assertEqual(
                self.normalizer.get_dataset_parameters({}),
                mock_get_gcmd_method.return_value)
