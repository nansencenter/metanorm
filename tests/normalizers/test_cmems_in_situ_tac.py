"""Tests for the CMEMS in situ TAC metadata normalizer"""
import unittest
import unittest.mock as mock
from collections import OrderedDict
from datetime import datetime

from dateutil.tz import tzutc

import metanorm.normalizers as normalizers


class CMEMSInSituTACMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the CMEMS in situ TAC attributes normalizer"""

    def setUp(self):
        self.normalizer = normalizers.CMEMSInSituTACMetadataNormalizer([], [])

    def test_matches_identifier(self):
        """matches_identifier() should return True if the
        id of the dataset is a CMEMS TAC id.
        """
        self.assertTrue(self.normalizer.matches_identifier({'id': 'NO_TS_TG_OsloTG_20210124'}))
        self.assertTrue(self.normalizer.matches_identifier({'id': 'GL_TS_DB_5100628'}))
        self.assertTrue(self.normalizer.matches_identifier({'id': 'AR_TS_MO_Blakksnes_201812'}))

        self.assertFalse(self.normalizer.matches_identifier({'id': 'A_B_C_D_E'}))
        self.assertFalse(self.normalizer.matches_identifier({'id': 'AB_CD_EF'}))
        self.assertFalse(self.normalizer.matches_identifier({'id': '1B_CD_EF_foo_20201120'}))
        self.assertFalse(self.normalizer.matches_identifier({'id': 'AB_C2_EF_foo_20201120'}))
        self.assertFalse(self.normalizer.matches_identifier({'id': 'AB_CD_34_foo_20201120'}))
        self.assertFalse(self.normalizer.matches_identifier({'id': 'AB_CD_EF_foo_20201120_'}))
        self.assertFalse(self.normalizer.matches_identifier({'id': 'AB_CD_EF_foo_20201120_bar'}))
        self.assertFalse(self.normalizer.matches_identifier({'id': 'NO_AB_TG_OsloTG_20210124'}))
        self.assertFalse(self.normalizer.matches_identifier({'id': 'NO_TS_AB_OsloTG_20210124'}))

    def test_get_entry_id(self):
        """get_entry_id() should return the id of the dataset if it is
        a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=True):
            self.assertEqual(self.normalizer.get_entry_id({'id': 'foo'}), 'foo')

    def test_get_entry_id_no_match(self):
        """get_entry_id() should return None if the id of the dataset
        is not a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=False):
            self.assertIsNone(self.normalizer.get_entry_id({'id': 'foo'}))

    def test_get_summary_from_raw_attributes(self):
        """Get the summary from the raw attributes if possible"""
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=True):
            self.assertEqual(
                self.normalizer.get_summary({'summary': 'foo'}),
                'Description: foo;Processing level: 2;'
                'Product: INSITU_GLO_NRT_OBSERVATIONS_013_030'
            )

    def test_get_summary_default(self):
        """If there is no summary in the attributes (or if it is
        empty), return the default summary
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=True):
            default_summary = (
                'Description: '
                    'Global Ocean - near real-time (NRT) in situ quality controlled observations, '
                    'hourly updated and distributed by INSTAC within 24-48 hours from acquisition '
                    'in average. Data are collected mainly through global networks '
                    '(Argo, OceanSites, GOSUD, EGO) and through the GTS;'
                'Processing level: 2;'
                'Product: INSITU_GLO_NRT_OBSERVATIONS_013_030'
            )
            self.assertEqual(self.normalizer.get_summary({}), default_summary)
            self.assertEqual(self.normalizer.get_summary({'summary': ''}), default_summary)

    def test_get_summary_no_match(self):
        """get_summary() should return None if the id of the dataset
        is not a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=False):
            self.assertIsNone(self.normalizer.get_summary({'summary': 'foo'}))

    def test_get_time_coverage_start(self):
        """get_time_coverage_start() should return the start time
        of the dataset if it has a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=True):
            self.assertEqual(
                self.normalizer.get_time_coverage_start(
                    {'time_coverage_start': '2020-10-21T01:02:03Z'}),
                datetime(year=2020, month=10, day=21, hour=1, minute=2, second=3, tzinfo=tzutc())
            )

    def test_get_time_coverage_start_no_match(self):
        """get_time_coverage_start() should return None if the id of the dataset
        is not a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=False):
            self.assertIsNone(self.normalizer.get_time_coverage_start(
                {'time_coverage_start': '2020-10-20'}))

    def test_get_time_coverage_end(self):
        """get_time_coverage_end() should return the start time
        of the dataset if it has a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=True):
            self.assertEqual(
                self.normalizer.get_time_coverage_end(
                    {'time_coverage_end': '2020-10-21T01:02:03Z'}),
                datetime(year=2020, month=10, day=21, hour=1, minute=2, second=3, tzinfo=tzutc())
            )

    def test_get_time_coverage_end_no_match(self):
        """get_time_coverage_end() should return None if the id of the dataset
        is not a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=False):
            self.assertIsNone(self.normalizer.get_time_coverage_end(
                {'time_coverage_end': '2020-10-20'}))

    def test_get_platform(self):
        """get_platform() should return the platform
        of the dataset if it has a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=True):
            self.assertEqual(
                self.normalizer.get_platform({}),
                OrderedDict([
                    ('Category', 'In Situ Ocean-based Platforms'),
                    ('Series_Entity', ''),
                    ('Short_Name', ''),
                    ('Long_Name', '')
                ])
            )

    def test_get_platform_no_match(self):
        """get_platform() should return None if the id of the dataset
        is not a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=False):
            self.assertIsNone(self.normalizer.get_platform({}))

    def test_get_instrument(self):
        """get_instrument() should return the instrument
        of the dataset if it has a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=True):
            self.assertEqual(
                self.normalizer.get_instrument({}),
                OrderedDict([
                    ('Category', 'In Situ/Laboratory Instruments'),
                    ('Class', ''),
                    ('Type', ''),
                    ('Subtype', ''),
                    ('Short_Name', ''),
                    ('Long_Name', '')
                ])
            )

    def test_get_instrument_no_match(self):
        """get_instrument() should return None if the id of the dataset
        is not a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=False):
            self.assertIsNone(self.normalizer.get_instrument({}))

    def test_get_location_geometry(self):
        """get_location_geometry() should return the location
        of the dataset if it has a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=True):
            self.assertEqual(
                self.normalizer.get_location_geometry({'geometry': 'POINT(10 10)'}),
                'POINT(10 10)'
            )

    def test_get_location_geometry_no_match(self):
        """get_location_geometry() should return None if the id of the dataset
        is not a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=False):
            self.assertIsNone(self.normalizer.get_location_geometry({'geometry': 'POINT(10 10)'}))

    def test_get_provider(self):
        """get_provider() should return the provider
        of the dataset if it has a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=True):
            self.assertEqual(
                self.normalizer.get_provider({}),
                OrderedDict([
                    ('Bucket_Level0', 'MULTINATIONAL ORGANIZATIONS'),
                    ('Bucket_Level1', ''),
                    ('Bucket_Level2', ''),
                    ('Bucket_Level3', ''),
                    ('Short_Name', 'CMEMS'),
                    ('Long_Name', 'Copernicus - Marine Environment Monitoring Service'),
                    ('Data_Center_URL', '')
                ])
            )

    def test_get_provider_no_match(self):
        """get_provider() should return None if the id of the dataset
        is not a CMEMS TAC id
        """
        with mock.patch.object(self.normalizer, 'matches_identifier', return_value=False):
            self.assertIsNone(self.normalizer.get_provider({}))
