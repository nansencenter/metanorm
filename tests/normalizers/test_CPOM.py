"""Tests for the CPOMaltimetryMetadataNormalizer normalizer"""
import unittest
from collections import OrderedDict
from datetime import datetime

import metanorm.normalizers as normalizers
from dateutil.tz import tzutc


class CPOMAltimetryMetadataNormalizerTests(unittest.TestCase):
    """Tests for the well known attributes normalizer"""

    def setUp(self):
        self.metadata = {'url':'/src/sample/cpom/CPOM_DOT.nc'}
        self.normalizer = normalizers.CPOMaltimetryMetadataNormalizer([], [])

    def test_match_metadata(self):
        """ test that Check if the filename exactly correct for using the normalizer """
        self.assertTrue(self.normalizer.match_metadata(self.metadata))

    def test_get_platform(self):
        """ shall return 'OPERATIONAL MODELS' """
        self.assertEqual(self.normalizer.get_platform(self.metadata),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', ''),
                         ('Short_Name', ''),
                         ('Long_Name', '')
                        ])
                        )

    def test_get_instrument(self):
        """ shall return "computer" """
        self.assertEqual(self.normalizer.get_instrument(self.metadata),
                         OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                                      ('Class', 'Active Remote Sensing'),
                                      ('Type', 'Altimeters'),
                                      ('Subtype', ''),
                                      ('Short_Name', ''),
                                      ('Long_Name', '')
                                     ])
                        )

    def test_get_entry_id(self):
        """ shall return the name of the file of CPOM SLA file name """
        self.assertEqual(self.normalizer.get_entry_id(self.metadata), 'CPOM_DOT')

    def test_get_time_coverage_start(self):
        """shall return the proper starting time for hardcoded normalizer """
        self.assertEqual(self.normalizer.get_time_coverage_start(self.metadata),
                         datetime(year=2003, month=1, day=1, tzinfo=tzutc())
                        )

    def test_get_time_coverage_end(self):
        """shall return the proper ending time for hardcoded normalizer """
        self.assertEqual(self.normalizer.get_time_coverage_end(self.metadata),
                         datetime(year=2015, month=1, day=1, tzinfo=tzutc())
                        )

    def test_get_entry_title(self):
        """ shall return 'CPOM SLA' """
        self.assertEqual(self.normalizer.get_entry_title(self.metadata), 'CPOM SLA')

    def test_get_provider(self):
        """ shall return CPOM provider """
        self.assertEqual(self.normalizer.get_provider(self.metadata),
            OrderedDict([
                ('Bucket_Level0', 'ACADEMIC'),
                ('Bucket_Level1', ''),
                ('Bucket_Level2', ''),
                ('Bucket_Level3', ''),
                ('Short_Name', 'UC-LONDON/CPOM'),
                ('Long_Name', ''),
                ('Data_Center_URL', 'http://www.cpom.ucl.ac.uk/cpom_ucl_only/data_resources.html')
                        ])
                        )

    def test_get_parameters(self):
        """ shall return 'sea_surface_height_above_sea_level' """
        self.assertCountEqual(self.normalizer.get_dataset_parameters(self.metadata),
                              [OrderedDict([
                                  ('standard_name', 'sea_surface_height_above_sea_level'),
                                  ('long_name', 'Sea Surface Anomaly'),
                                  ('short_name', 'SSA'),
                                  ('units', 'm'),
                                  ('minmax', '-100 100'),
                                  ('colormap', 'jet')
                              ])]
                             )

    def test_normalize_wrong_metadata(self):
        """
        all get_ functions shall return None except get_dataset_parameters which should return []
        """
        wrong_meta = {'some': 'metadata'}
        self.assertEqual(self.normalizer.get_platform(wrong_meta), None)
        self.assertEqual(self.normalizer.get_instrument(wrong_meta), None)
        self.assertEqual(self.normalizer.get_entry_id(wrong_meta), None)
        self.assertEqual(self.normalizer.get_entry_title(wrong_meta), None)
        self.assertEqual(self.normalizer.get_time_coverage_start(wrong_meta), None)
        self.assertEqual(self.normalizer.get_time_coverage_end(wrong_meta), None)
        self.assertEqual(self.normalizer.get_provider(wrong_meta), None)
        self.assertEqual(self.normalizer.get_dataset_parameters(wrong_meta), [])
