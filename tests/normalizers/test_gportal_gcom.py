"""Tests for the GPortal GCOM-W normalizer"""
import unittest
from collections import OrderedDict
from datetime import datetime
from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from .data import DATASET_PARAMETERS
from metanorm.errors import MetadataNormalizationError


class GPortalGCOMAMSR2L3MetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the GPortal GCOM-W ftp normalizer"""
    def setUp(self):
        self.normalizer = normalizers.geospaas.GPortalGCOMAMSR2L3MetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2017/12/'
                   'GW1AM2_20171201_01D_EQOA_L3SGSSTLB3300300.h5'
        }))
        self.assertTrue(self.normalizer.check({
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2018/07/'
                   'GW1AM2_20180703_01D_EQOA_L3SGSSTHB3300300.h5'
        }))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

    def test_entry_title(self):
        """entry_title from GPortalGCOMAMSR2L3MetadataNormalizer """
        self.assertEqual(self.normalizer.get_entry_title({}), 'AMSR2-L3 Sea Surface Temperature')

    def test_entry_id(self):
        """entry_id from GPortalGCOMAMSR2L3MetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/'
                   'GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(self.normalizer.get_entry_id(attributes),
                         'GW1AM2_201207031905_134D_L2SGSSTLB3300300')

    def test_entry_id_error(self):
        """a MetadataNormalizationError must be raised when an entry_id cannot be found"""
        # wrong file format
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({'url': 'ftp://foo/bar.txt'})
        # no url attribute
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})

    def test_summary(self):
        """summary from GPortalGCOMAMSR2L3MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: GCOM-W AMSR2 data;Processing level: 3')

    def test_time_coverage_start_day(self):
        """Test getting time_coverage_start from a day file"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/'
                       'GW1AM2_20120702_01D_EQOD_L3SGSSTLB3300300.h5'}),
            datetime(year=2012, month=7, day=2, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_month(self):
        """Test getting time_coverage_start from a month file"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2013/07/'
                       'GW1AM2_20130700_01M_EQMA_L3SGSSTLB3300300.h5'}),
            datetime(year=2013, month=7, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_time_coverage_end_day(self):
        """Test getting time_coverage_end from a day file"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2015/04/'
                       'GW1AM2_20150401_01D_EQOD_L3SGSSTLB3300300.h5'}),
            datetime(year=2015, month=4, day=2, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_month(self):
        """Test getting time_coverage_end from a month file"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2015/04/'
                       'GW1AM2_20150400_01M_EQMD_L3SGSSTLB3300300.h5'}),
            datetime(year=2015, month=5, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})

    def test_platform(self):
        """platform from GPortalGCOMAMSR2L3MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_platform({}),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'GCOM-W1'),
                         ('Long_Name', 'Global Change Observation Mission 1st-Water')]))

    def test_instrument(self):
        """instrument from GPortalGCOMAMSR2L3MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_instrument({}),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', 'AMSR2'),
                         ('Long_Name', 'Advanced Microwave Scanning Radiometer 2')]))

    def test_location_geometry(self):
        """geometry from GPortalGCOMAMSR2L3MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_provider(self):
        """provider from GPortalGCOMAMSR2L3MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_provider({}),
            OrderedDict([('Bucket_Level0', 'GOVERNMENT AGENCIES-NON-US'),
                         ('Bucket_Level1', 'JAPAN'),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'JP/JAXA/EOC'),
                         ('Long_Name', 'Earth Observation Center, Japan Aerospace Exploration '
                                       'Agency, Japan'),
                         ('Data_Center_URL', 'http://www.eorc.jaxa.jp/en/index.html')]))

    def test_dataset_parameters(self):
        """dataset_parameters from GPortalGCOMAMSR2L3MetadataNormalizer """
        self.assertEqual(self.normalizer.get_dataset_parameters({}), [
            DATASET_PARAMETERS['sea_surface_temperature']
        ])
