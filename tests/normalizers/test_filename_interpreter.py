"""Tests for the default metadata normalizer"""
import datetime
import unittest
from collections import OrderedDict

import metanorm.normalizers as normalizers


class GeoSpatialDefaultMetadataNormalizerTestCase(unittest.TestCase):
    """
    Test case for the GeoSpatialDefaultMetadataNormalizer, mainly checking default values and raised
    exceptions
    """

    def setUp(self):
        DATASET_PARAMETER_NAMES = ["entry_id",
                                   "platform",
                                   "instrument",
                                   "time_coverage_start",
                                   "time_coverage_end",
                                   "provider"
                                   ]
        self.normalizer = normalizers.filename_interpreter.SentinelFilenameInterpreterNormalizer(
            DATASET_PARAMETER_NAMES)

    def tearDown(self):
        self.normalizer = None

    def test_start_and_end_time_of_filename(self):
        """ Shall return the start and end time and extraction them from the filename """
        result_normalization = self.normalizer.normalize(
            {'entry_id': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(result_normalization['time_coverage_start'], datetime.datetime(
            2015, 7, 2, 17, 29, 54))
        self.assertEqual(result_normalization['time_coverage_end'], datetime.datetime(
            2015, 7, 2, 17, 30, 54))

    def test_platform_identification(self):
        """ Shall return the correct sentinel based on the filename """
        result_normalization = self.normalizer.normalize(
            {'entry_id': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertDictEqual(
            result_normalization['platform'],
            OrderedDict([
                ('Category', 'Earth Observation Satellites'),
                ('Series_Entity', 'SENTINEL-1'),
                ('Short_Name', 'SENTINEL-1A'),
                ('Long_Name', 'SENTINEL-1A')
            ])
        )
