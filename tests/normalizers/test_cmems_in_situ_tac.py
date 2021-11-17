"""Tests for the CMEMS in situ TAC metadata normalizer"""
import unittest
from collections import OrderedDict
from datetime import datetime

from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


class CMEMSInSituTACMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the CMEMS in situ TAC attributes normalizer"""

    def setUp(self):
        self.normalizer = normalizers.CMEMSInSituTACMetadataNormalizer()

    def test_check(self):
        """check() should return True if the
        id of the dataset is a CMEMS TAC id.
        """
        self.assertTrue(self.normalizer.check({'id': 'NO_TS_TG_OsloTG_20210124'}))
        self.assertTrue(self.normalizer.check({'id': 'GL_TS_DB_5100628'}))
        self.assertTrue(self.normalizer.check({'id': 'AR_TS_MO_Blakksnes_201812'}))
        self.assertTrue(self.normalizer.check({'id': 'GL_TS_DC_7300658_201606'}))
        self.assertTrue(self.normalizer.check({'id': 'GL_TV_HF_HFR-TirLig-Total_201703'}))

        self.assertFalse(self.normalizer.check({'id': 'A_B_C_D_E'}))
        self.assertFalse(self.normalizer.check({'id': 'AB_CD_EF'}))
        self.assertFalse(self.normalizer.check({'id': '1B_CD_EF_foo_20201120'}))
        self.assertFalse(self.normalizer.check({'id': 'AB_C2_EF_foo_20201120'}))
        self.assertFalse(self.normalizer.check({'id': 'AB_CD_34_foo_20201120'}))
        self.assertFalse(self.normalizer.check({'id': 'AB_CD_EF_foo_20201120_'}))
        self.assertFalse(self.normalizer.check({'id': 'AB_CD_EF_foo_20201120_bar'}))
        self.assertFalse(self.normalizer.check({'id': 'NO_AB_TG_OsloTG_20210124'}))
        self.assertFalse(self.normalizer.check({'id': 'NO_TS_AB_OsloTG_20210124'}))

    def test_get_entry_title(self):
        """Test getting the title"""
        self.assertEqual(self.normalizer.get_entry_title({'title': 'foo'}), 'foo')

    def test_missing_title(self):
        """A MetadataNormalizationError should be raised if the raw title
        is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_title({})

    def test_get_entry_id(self):
        """Test getting the ID"""
        self.assertEqual(self.normalizer.get_entry_id({'id': 'foo'}), 'foo')

    def test_missing_id(self):
        """A MetadataNormalizationError should be raised if the raw id
        is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})

    def test_get_summary_013_030_from_raw_attributes(self):
        """Get the summary from the raw attributes for the 013_030
        product
        """
        url = '/foo/INSITU_GLO_NRT_OBSERVATIONS_013_030/dataset.nc'
        self.assertEqual(
            self.normalizer.get_summary({'summary': 'foo', 'url': url}),
            'Description: foo;Processing level: 2;'
            'Product: INSITU_GLO_NRT_OBSERVATIONS_013_030'
        )

    def test_get_summary_013_048_from_raw_attributes(self):
        """Get the summary from the raw attributes for the 013_048
        product
        """
        url = '/foo/INSITU_GLO_UV_NRT_OBSERVATIONS_013_048/dataset.nc'
        self.assertEqual(
            self.normalizer.get_summary({'summary': 'foo', 'url': url}),
            'Description: foo;Processing level: 2;'
            'Product: INSITU_GLO_UV_NRT_OBSERVATIONS_013_048'
        )

    def test_get_summary_unknown_from_raw_attributes(self):
        """Get the summary from the raw attributes for an unknown
        product
        """
        url = '/foo/bar/dataset.nc'
        self.assertEqual(
            self.normalizer.get_summary({'summary': 'foo', 'url': url}),
            'Description: foo;Processing level: 2;'
            'Product: Unknown'
        )

    def test_get_summary_013_030_default(self):
        """If there is no summary in the attributes (or if it is
        empty), return the default summary for the 013_030 product
        """
        url = '/foo/INSITU_GLO_NRT_OBSERVATIONS_013_030/dataset.nc'
        default_summary = (
            'Description: '
                'Global Ocean - near real-time (NRT) in situ quality controlled observations, '
                'hourly updated and distributed by INSTAC within 24-48 hours from acquisition '
                'in average. Data are collected mainly through global networks '
                '(Argo, OceanSites, GOSUD, EGO) and through the GTS;'
            'Processing level: 2;'
            'Product: INSITU_GLO_NRT_OBSERVATIONS_013_030'
        )
        self.assertEqual(self.normalizer.get_summary({'url': url}), default_summary)
        self.assertEqual(
            self.normalizer.get_summary({'summary': '', 'url': url}),
            default_summary)
        self.assertEqual(
            self.normalizer.get_summary({'summary': '  ', 'url': url}),
            default_summary)

    def test_get_summary_013_048_default(self):
        """If there is no summary in the attributes (or if it is
        empty), return the default summary for the 013_048 product
        """
        url = '/foo/INSITU_GLO_UV_NRT_OBSERVATIONS_013_048/dataset.nc'
        default_summary = (
            'Description: '
                'This product is entirely dedicated to ocean current data observed in '
                'near-real time. Surface current data from 2 different types of instruments'
                ' are distributed: velocities calculated along the trajectories of drifting'
                ' buoys from the DBCP’s Global Drifter Program, and velocities measured by '
                'High Frequency radars from the European High Frequency radar Network;'
            'Processing level: 2;'
            'Product: INSITU_GLO_UV_NRT_OBSERVATIONS_013_048'
        )
        self.assertEqual(self.normalizer.get_summary({'url': url}), default_summary)
        self.assertEqual(
            self.normalizer.get_summary({'summary': '', 'url': url}),
            default_summary)
        self.assertEqual(
            self.normalizer.get_summary({'summary': '  ', 'url': url}),
            default_summary)

    def test_get_summary_unknown_default(self):
        """If there is no summary in the attributes (or if it is
        empty), return the default summary for an unknown product
        """
        url = '/foo/bar/dataset.nc'
        default_summary = (
            'Description: CMEMS in situ TAC data;'
            'Processing level: 2;'
            'Product: Unknown'
        )
        self.assertEqual(self.normalizer.get_summary({'url': url}), default_summary)
        self.assertEqual(
            self.normalizer.get_summary({'summary': '', 'url': url}),
            default_summary)
        self.assertEqual(
            self.normalizer.get_summary({'summary': '  ', 'url': url}),
            default_summary)

    def test_get_time_coverage_start(self):
        """get_time_coverage_start() should return the start time of
        the dataset
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'time_coverage_start': '2020-10-21T01:02:03Z'}),
            datetime(year=2020, month=10, day=21, hour=1, minute=2, second=3, tzinfo=tzutc())
        )

    def test_missing_time_coverage_start(self):
        """A MetadataNormalizationError must be raised when the
        time_coverage_start raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_get_time_coverage_end(self):
        """get_time_coverage_end() should return the start time
        of the dataset
        """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'time_coverage_end': '2020-10-21T01:02:03Z'}),
            datetime(year=2020, month=10, day=21, hour=1, minute=2, second=3, tzinfo=tzutc())
        )

    def test_missing_time_coverage_end(self):
        """A MetadataNormalizationError must be raised when the
        time_coverage_end raw attribute is missing
        """
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})

    def test_get_platform(self):
        """get_platform() should return the platform
        of the dataset
        """
        self.assertEqual(
            self.normalizer.get_platform({}),
            OrderedDict([
                ('Category', 'In Situ Ocean-based Platforms'),
                ('Series_Entity', ''),
                ('Short_Name', ''),
                ('Long_Name', '')
            ]))

    def test_get_instrument(self):
        """get_instrument() should return the instrument
        of the dataset
        """
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

    def test_get_location_geometry(self):
        """get_location_geometry() should return the location
        of the dataset
        """
        self.assertEqual(
            self.normalizer.get_location_geometry({'geometry': 'POINT(10 10)'}), 'POINT(10 10)')

    def test_missing_geometry(self):
        """An empty string must be returned when the geometry raw
        attribute is missing
        """
        self.assertEqual(self.normalizer.get_location_geometry({}), '')

    def test_get_provider(self):
        """get_provider() should return the provider
        of the dataset
        """
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
            ]))
