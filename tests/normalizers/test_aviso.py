"""Tests for the AVISOaltimetryMetadataNormalizer normalizer"""
import unittest
from collections import OrderedDict

import metanorm.normalizers as normalizers


class AVISOaltimetryMetadataNormalizerTests(unittest.TestCase):
    """Tests for the well known attributes normalizer"""

    def setUp(self):
        self.metadata = {
            'Conventions':'CF-1.7',
            'Metadata_Conventions':'Unidata Dataset Discovery v1.0',
            'cdm_data_type':'Grid',
            'comment':'Sea Level Anomaly measured by Altimetry and derived variables',
            'contact':'aviso@altimetry.fr',
            'creator_email':'aviso@altimetry.fr',
            'creator_name':'ARCTIC_OCEAN_PROTOTYPE',
            'creator_url':'https://www.aviso.altimetry.fr',
            'history':'Created on 2021-01-08 10:45:52Z by ARCTIC_OCEAN_PROTOTYPE',
            'institution':'CLS,CNES',
            'keywords':'Oceans>Ocean Topography>Sea Surface Height',
            'keywords_vocabulary':'NetCDF COARDS Climate and Forecast Standard Names',
            'platform':'SARAL/CryoSat2/Sentinel3A',
            'processing_level':'L4',
            'Grid':'Subset of Northern Hemisphere 25km EASE2 Grid',
            'title':'DT multi-satellite sea level gridded product',
            'product_version':'1.1',
            'project':'CNES AltiDoppler Glaciologie',
            'reference':'http://aviso.altimetry.fr',
            'source':'Altimetry measurements',
            'time_coverage_duration':'P1032.0D',
            'time_coverage_resolution':'P3.0D',
            'time_coverage_end':'2019-04-29 00:00:00Z',
            'time_coverage_start':'2016-07-01 00:00:00Z',
            'url':'/src/sample/aviso/dt_arctic_multimission_sea_level_20160701_20190429.nc',
            }

        self.normalizer = normalizers.AVISOaltimetryMetadataNormalizer([], [])

    def test_match_metadata(self):
        """ test that Check if the filename exactly correct for using the normalizer """
        self.assertTrue(self.normalizer.match_metadata(self.metadata))

    def test_get_platform(self):
        """ shall return 'SARAL/CryoSat2/Sentinel3A' """
        self.assertEqual(
            self.normalizer.get_platform(self.metadata),
            OrderedDict([('Category', 'Earth Observation Satellites'),
             ('Series_Entity', ''),
             ('Short_Name', ''),
             ('Long_Name', '')]))

    def test_get_instrument(self):
        """ shall return c-sar """
        self.assertEqual(
            self.normalizer.get_instrument(self.metadata),
            OrderedDict([('Category', 'In Situ/Laboratory Instruments'),
             ('Class', 'Data Analysis'),
             ('Type', 'Environmental Modeling'),
             ('Subtype', ''),
             ('Short_Name', 'Computer'),
             ('Long_Name', 'Computer')]))

    def test_get_entry_id(self):
        """ shall return the name of the file of aviso SLA file name """
        self.assertEqual(
                         self.normalizer.get_entry_id(self.metadata),
                         'dt_arctic_multimission_sea_level_20160701_20190429'
                        )

    def test_normalize_wrong_metadata(self):
        """all get_ functions shall return None except get_dataset_parameters which should return []"""
        wrong_meta = {'some': 'metadata'}
        self.assertEqual(self.normalizer.get_platform(wrong_meta), None)
        self.assertEqual(self.normalizer.get_entry_id(wrong_meta), None)
        self.assertEqual(self.normalizer.get_instrument(wrong_meta), None)
