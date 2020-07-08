"""Tests for the filename metadata normalizer"""
import datetime
import unittest
from collections import OrderedDict

import metanorm.normalizers as normalizers


class SentinelOneIdentifierMetadataNormalizerTestCase(unittest.TestCase):
    """
    Test case for the SentinelIdentifierMetadataNormalizerTestCase,
    mainly extract the data from file name
    """

    def setUp(self):
        DATASET_PARAMETER_NAMES = [
            "entry_id",
            "platform",
            "instrument",
            "time_coverage_start",
            "time_coverage_end",
            "provider"
        ]
        self.normalizer = normalizers.sentinel1_identifier.SentinelOneIdentifierMetadataNormalizer(
            DATASET_PARAMETER_NAMES)

    def tearDown(self):
        self.normalizer = None

    def test_none_identification_for_incorrect_filename(self):
        """ Shall return None from the incorrect sentinel Identifier """
        result_normalization = self.normalizer.normalize(
            {'Identifier': 'S1A_EW_GRDM_XXSDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(result_normalization['platform'], None)
        self.assertEqual(result_normalization['entry_id'], None)
        self.assertEqual(result_normalization['time_coverage_start'], None)
        self.assertEqual(result_normalization['time_coverage_end'], None)

    def test_start_and_end_time_of_filename(self):
        """ Shall return the start and end time and extraction them from the filename """
        result_normalization = self.normalizer.normalize(
            {'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(result_normalization['time_coverage_start'], datetime.datetime(
            2015, 7, 2, 17, 29, 54))
        self.assertEqual(result_normalization['time_coverage_end'], datetime.datetime(
            2015, 7, 2, 17, 30, 54))

    def test_platform_identification(self):
        """ Shall return the correct sentinel based on the filename """
        result_normalization = self.normalizer.normalize(
            {'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertDictEqual(
            result_normalization['platform'],
            OrderedDict([
                ('Category', 'Earth Observation Satellites'),
                ('Series_Entity', 'SENTINEL-1'),
                ('Short_Name', 'SENTINEL-1A'),
                ('Long_Name', 'SENTINEL-1A')
            ])
        )

    def test_instrument_identification(self):
        """ Shall return the correct sentinel instrument based on the filename """
        result_normalization = self.normalizer.normalize(
            {'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertDictEqual(
            result_normalization['instrument'],
            OrderedDict([
                ('Category', 'Earth Remote Sensing Instruments'),
                ('Class', 'Active Remote Sensing'),
                ('Type', 'Imaging Radars'),
                ('Subtype', ''),
                ('Short_Name', 'C-SAR'),
                ('Long_Name', 'C-Band Synthetic Aperture Radar')
            ])
        )

    def test_provider_identification(self):
        """ Shall return the correct sentinel provider based on the filename """
        result_normalization = self.normalizer.normalize(
            {'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertDictEqual(
            result_normalization['provider'],
            OrderedDict([
                ('Bucket_Level0', 'MULTINATIONAL ORGANIZATIONS'),
                ('Bucket_Level1', ''),
                ('Bucket_Level2', ''),
                ('Bucket_Level3', ''),
                ('Short_Name', 'ESA/EO'),
                ('Long_Name', 'Observing the Earth, European Space Agency'),
                ('Data_Center_URL', 'http://www.esa.int/esaEO/')
            ])
        )

    def test_entry_id_identification(self):
        """ Shall return the correct sentinel Identifier based on the filename """
        result_normalization = self.normalizer.normalize(
            {'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(
            result_normalization['entry_id'],
            'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'
        )

    def test_return_none_for_incorrect_raw_attribute(self):
        """ Shall return None based on non-recognizable raw attribute """
        result_normalization = self.normalizer.normalize(
            {'Iifi': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(
            result_normalization['entry_id'], None)
