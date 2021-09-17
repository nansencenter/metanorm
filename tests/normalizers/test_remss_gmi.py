"""Tests for the REMSS GMI normalizer"""
import unittest
from collections import OrderedDict
from datetime import datetime
from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from .data import DATASET_PARAMETERS


class REMSSGMIMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the REMSS GMI ftp normalizer"""
    def setUp(self):
        self.normalizer = normalizers.geospaas.REMSSGMIMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check(
            {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140601v8.2.gz'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

    def test_entry_title(self):
        """entry_title from REMSSGMIMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_entry_title({}),
            'Atmosphere parameters from Global Precipitation Measurement Microwave Imager')

    def test_entry_id(self):
        """entry_id from REMSSGMIMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140603v8.2.gz'}
        self.assertEqual(self.normalizer.get_entry_id(attributes),
                         'f35_20140603v8.2')

    def test_summary(self):
        """summary from REMSSGMIMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: GMI is a dual-polarization, multi-channel, conical-scanning, passive '
            'microwave radiometer with frequent revisit times.;Processing level: 3')

    def test_time_coverage_start_month_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_201406v8.2.gz'}),
            datetime(year=2014, month=6, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_single_day_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140604v8.2.gz'}),
            datetime(year=2014, month=6, day=4, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_week_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/weeks/f35_20140614v8.2.gz'}),
            datetime(year=2014, month=6, day=8, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_3d3_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140630v8.2_d3d.gz'}),
            datetime(year=2014, month=6, day=28, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_single_day_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140620v8.2.gz'}),
            datetime(year=2014, month=6, day=21, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_month_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_201406v8.2.gz'}),
            datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_week_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/weeks/f35_20140614v8.2.gz'}),
            datetime(year=2014, month=6, day=15, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_3d3_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140630v8.2_d3d.gz'}),
            datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_platform(self):
        """platform from REMSSGMIMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_platform({}),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'GPM'),
                         ('Long_Name', 'Global Precipitation Measurement')]))

    def test_instrument(self):
        """instrument from REMSSGMIMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_instrument({}),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', 'GMI'),
                         ('Long_Name', 'Global Precipitation Measurement Microwave Imager')]))

    def test_location_geometry(self):
        """geometry from REMSSGMIMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_location_geometry({}),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_provider(self):
        """provider from REMSSGMIMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_provider({}),
            OrderedDict([('Bucket_Level0', 'COMMERCIAL'),
                         ('Bucket_Level1', ''),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'RSS'),
                         ('Long_Name', 'Remote Sensing Systems'),
                         ('Data_Center_URL', 'http://www.remss.com/')]))

    def test_dataset_parameters(self):
        """dataset_parameters from REMSSGMIMetadataNormalizer """
        self.assertEqual(self.normalizer.get_dataset_parameters({}), [
            DATASET_PARAMETERS['wind_speed'],
            DATASET_PARAMETERS['atmosphere_mass_content_of_water_vapor'],
            DATASET_PARAMETERS['atmosphere_mass_content_of_cloud_liquid_water'],
            DATASET_PARAMETERS['rainfall_rate'],
        ])
