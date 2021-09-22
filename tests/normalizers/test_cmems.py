"""Tests for the CMEMS normalizers"""

import unittest
import unittest.mock as mock
from collections import OrderedDict

import metanorm.normalizers as normalizers
from .data import DATASET_PARAMETERS
from metanorm.errors import MetadataNormalizationError

class CMEMSMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the CMEMSMetadataNormalizer base class"""

    def setUp(self):
        self.normalizer = normalizers.geospaas.CMEMSMetadataNormalizer()

    def test_entry_id(self):
        """Test extracting the entry_id from a URL"""
        self.assertEqual(self.normalizer.get_entry_id({'url': 'ftp://foo/bar/baz123.nc'}), 'baz123')
        self.assertEqual(self.normalizer.get_entry_id({'url': 'ftp://foo/bar/baz123.h5'}), 'baz123')
        self.assertEqual(
            self.normalizer.get_entry_id({'url': 'ftp://foo/bar/baz123.nc.gz'}),
            'baz123')
        self.assertEqual(
            self.normalizer.get_entry_id({'url': 'ftp://foo/bar/baz123.h5.gz'}),
            'baz123')

    def test_provider(self):
        """The provider is always CMEMS"""
        self.assertEqual(
            self.normalizer.get_provider({}),
            OrderedDict([('Bucket_Level0', 'MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1', ''),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'CMEMS'),
                         ('Long_Name', 'Copernicus - Marine Environment Monitoring Service'),
                         ('Data_Center_URL', '')]))

    def test_time_coverage(self):
        """Test that the time coverage is extracted using
        utils.find_time_coverage()
        """
        url = 'ftp://foo/bar.nc'
        raw_metadata = {'url': url}
        with mock.patch('metanorm.utils.find_time_coverage') as mock_find_time_coverage:
            mock_find_time_coverage.return_value = ('start', 'end')

            # test time_coverage_start
            self.assertEqual(self.normalizer.get_time_coverage_start(raw_metadata), 'start')
            mock_find_time_coverage.assert_called_with(self.normalizer.time_patterns, url)

            # test time_coverage_end
            self.assertEqual(self.normalizer.get_time_coverage_end(raw_metadata), 'end')
            mock_find_time_coverage.assert_called_with(self.normalizer.time_patterns, url)
