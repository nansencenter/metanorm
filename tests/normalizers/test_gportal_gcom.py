"""Tests for the GPortal GCOM-W normalizer"""
import unittest
import unittest.mock as mock
from datetime import datetime
from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


class GPortalGCOMWAMSR2MetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the GPortal GCOM-W ftp normalizer"""
    def setUp(self):
        self.normalizer = normalizers.geospaas.GPortalGCOMWAMSR2MetadataNormalizer()

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
        self.assertTrue(self.normalizer.check({
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L1R/2/2020/02/'
                   'GW1AM2_202002011046_045A_L1SGRTBR_2220220.h5'
        }))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

    def test_entry_title(self):
        """entry_title from GPortalGCOMWAMSR2MetadataNormalizer """
        self.assertEqual(self.normalizer.get_entry_title({}), 'GCOM-W AMSR2')

    def test_entry_id(self):
        """entry_id from GPortalGCOMWAMSR2MetadataNormalizer """
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
        """summary from GPortalGCOMWAMSR2MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_summary({
                'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2017/12/'
                       'GW1AM2_20171201_01D_EQOA_L3SGSSTLB3300300.h5'
            }),
            'Description: GCOM-W AMSR2 data;Processing level: 3')
        self.assertEqual(
            self.normalizer.get_summary({
                'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L1R/2/2020/02/'
                       'GW1AM2_202002011046_045A_L1SGRTBR_2220220.h5'
            }),
            'Description: GCOM-W AMSR2 data;Processing level: 1R')

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
        """geometry from GPortalGCOMWAMSR2MetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')
