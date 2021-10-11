"""Tests for the ESA CCI normalizer"""
import unittest
from collections import OrderedDict
from datetime import datetime
from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from .data import DATASET_PARAMETERS
from metanorm.errors import MetadataNormalizationError


class CEDAESACCIMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the REMSS GMI ftp normalizer"""
    def setUp(self):
        self.normalizer = normalizers.geospaas.CEDAESACCIMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check(
            {'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/'
                    'D001-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}))
        self.assertTrue(self.normalizer.check(
            {'url': 'ftp://ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/'
                    'D001-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

    def test_entry_title(self):
        """entry_title from CEDAESACCIMetadataNormalizer """
        self.assertEqual(self.normalizer.get_entry_title({}), 'ESA SST CCI OSTIA L4 Climatology')

    def test_entry_id(self):
        """entry_id from CEDAESACCIMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/'
                    'D001-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'
        }
        self.assertEqual(self.normalizer.get_entry_id(attributes),
                         'D001-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0')

    def test_entry_id_error(self):
        """a MetadataNormalizationError must be raised when an entry_id cannot be found"""
        # wrong file format
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({'url': 'ftp://foo/bar.txt'})
        # no url attribute
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})

    def test_summary(self):
        """summary from CEDAESACCIMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: This v2.1 SST_cci Climatology Data Record (CDR) consists of Level 4 daily'
            ' climatology files gridded on a 0.05 degree grid.;Processing level: 4;'
            'Product: ESA SST CCI Climatology')

    def test_time_coverage_start(self):
        """time_coverage_start from CEDAESACCIMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/'
                       'D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}),
            datetime(year=1982, month=12, day=31, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_time_coverage_end(self):
        """time_coverage_end from CEDAESACCIMetadataNormalizer"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/'
                       'D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}),
            datetime(year=2010, month=12, day=31, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})

    def test_platform(self):
        """platform from CEDAESACCIMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_platform({}),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', ''),
                         ('Short_Name', ''),
                         ('Long_Name', '')]))

    def test_instrument(self):
        """instrument from CEDAESACCIMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_instrument({}),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', ''),
                         ('Long_Name', '')]))

    def test_location_geometry(self):
        """geometry from CEDAESACCIMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_provider(self):
        """provider from CEDAESACCIMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_provider({}),
            OrderedDict([('Bucket_Level0', 'MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1', ''),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'ESA/CCI'),
                         ('Long_Name', 'Climate Change Initiative, European Space Agency'),
                         ('Data_Center_URL', '')]))

    def test_dataset_parameters(self):
        """dataset_parameters from CEDAESACCIMetadataNormalizer """
        self.assertEqual(self.normalizer.get_dataset_parameters({}), [
            DATASET_PARAMETERS['sea_surface_temperature'],
        ])
