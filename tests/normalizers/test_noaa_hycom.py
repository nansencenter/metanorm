"""Tests for the NOAA HYCOM normalizer"""
import unittest
from collections import OrderedDict
from datetime import datetime
from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from .data import DATASET_PARAMETERS
from metanorm.errors import MetadataNormalizationError


class NOAAHYCOMMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the REMSS GMI ftp normalizer"""
    def setUp(self):
        self.normalizer = normalizers.geospaas.NOAAHYCOMMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check(
            {'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

    def test_entry_title(self):
        """entry_title from NOAAHYCOMMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_entry_title({}),
            'Global Hybrid Coordinate Ocean Model (HYCOM)')

    def test_entry_id(self):
        """entry_id from NOAAHYCOMMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_entry_id({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_regp17_2020122000_t168.nc.gz'
            }),
            'hycom_glb_regp17_2020122000_t168')
        self.assertEqual(self.normalizer.get_entry_id({
            'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                   'hycom_glb_sfc_u_2020121900_t000.nc.gz'
        }),
            'hycom_glb_sfc_u_2020121900_t000')

    def test_entry_id_error(self):
        """a MetadataNormalizationError must be raised when an entry_id cannot be found"""
        # wrong file format
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({'url': 'ftp://foo/bar.txt'})
        # no url attribute
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})

    def test_summary(self):
        """summary from NOAAHYCOMMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_summary({}),
            'Description: This system provides 4-day forecasts at 3-hour time steps, updated at '
            '00Z daily. Navy Global HYCOM has a resolution of 1/12 degree in the horizontal and '
            'uses hybrid (isopycnal/sigma/z-level) coordinates in the vertical. The output is '
            'interpolated onto a regular 1/12-degree grid horizontally and 40 standard depth '
            'levels.;'
            'Processing level: 4;'
            'Product: HYCOM')

    def test_time_coverage_start_region_000(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_regp01_2020121900_t000.nc.gz'
            }),
            datetime(year=2020, month=12, day=19, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_region_009(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_regp01_2020121900_t009.nc.gz'
            }),
            datetime(year=2020, month=12, day=19, hour=9, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_region_027(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_regp01_2020121900_t027.nc.gz'
            }),
            datetime(year=2020, month=12, day=20, hour=3, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_sfc(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_sfc_u_2020121900_t003.nc.gz'
            }),
            datetime(year=2020, month=12, day=19, hour=3, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_time_coverage_end_region_000(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_regp01_2020121900_t000.nc.gz'
            }),
            datetime(year=2020, month=12, day=19, hour=3, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_region_009(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_regp01_2020121900_t009.nc.gz'
            }),
            datetime(year=2020, month=12, day=19, hour=12, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_region_027(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_regp01_2020121900_t027.nc.gz'
            }),
            datetime(year=2020, month=12, day=20, hour=6, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_sfc(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_sfc_u_2020121900_t003.nc.gz'
            }),
            datetime(year=2020, month=12, day=19, hour=6, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})

    def test_platform(self):
        """platform from NOAAHYCOMMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_platform({}),
            OrderedDict([('Category', 'Models/Analyses'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'OPERATIONAL MODELS'),
                         ('Long_Name', '')]))

    def test_instrument(self):
        """instrument from NOAAHYCOMMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_instrument({}),
            OrderedDict([('Category', 'In Situ/Laboratory Instruments'),
                         ('Class', 'Data Analysis'),
                         ('Type', 'Environmental Modeling'),
                         ('Subtype', ''),
                         ('Short_Name', 'Computer'),
                         ('Long_Name', 'Computer')]))

    def test_geometry_hycom_region1(self):
        """Should return the proper geometry"""
        attributes = {
            'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                   'hycom_glb_regp01_2020121900_t030.nc.gz'
        }
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-100.04 70.04, -100.04 -0.04, -49.96 -0.04, -49.96 70.04, -100.04 70.04))'
        )

    def test_geometry_hycom_region6(self):
        """Should return the proper geometry"""
        attributes = {
            'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                   'hycom_glb_regp06_2020121900_t030.nc.gz'
        }
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((149.96 70.04, 149.96 9.96, 210.04 9.96, 210.04 70.04, 149.96 70.04))'
        )

    def test_geometry_hycom_region7(self):
        """Should return the proper geometry"""
        attributes = {
            'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                   'hycom_glb_regp07_2020121900_t030.nc.gz'
        }
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-150.04 60.04, -150.04 9.96, -99.96 9.96, -99.96 60.04, -150.04 60.04))'
        )

    def test_geometry_hycom_region17(self):
        """Should return the proper geometry"""
        attributes = {
            'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                   'hycom_glb_regp17_2020121900_t030.nc.gz'
        }
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180.04 80.02,-180.04 59.98,-119.96 59.98,-119.96 80.02,-180.04 80.02))'
        )

    def test_geometry_hycom_sfc(self):
        """Should return the proper geometry"""
        attributes = {
            'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                   'hycom_glb_sfc_u_2020121900_t030.nc.gz'
        }
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'
        )

    def test_unknown_geometry(self):
        """An exception should be raised if no geometry can be found"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({'url': 'http://foo'})

    def test_provider(self):
        """provider from NOAAHYCOMMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_provider({}),
            OrderedDict([
                ('Bucket_Level0', 'GOVERNMENT AGENCIES-U.S. FEDERAL AGENCIES'),
                ('Bucket_Level1', 'DOC'),
                ('Bucket_Level2', 'NOAA'),
                ('Bucket_Level3', ''),
                ('Short_Name', 'DOC/NOAA/NWS/NCEP'),
                ('Long_Name',
                 'National Centers for Environmental Prediction, National Weather Service, NOAA, '
                 'U.S. Department of Commerce'),
                ('Data_Center_URL', 'http://www.ncep.noaa.gov/')]))

    def test_dataset_parameters(self):
        """dataset_parameters from NOAAHYCOMMetadataNormalizer """
        self.assertEqual(self.normalizer.get_dataset_parameters({}), [
            DATASET_PARAMETERS['sea_water_salinity'],
            DATASET_PARAMETERS['sea_water_temperature'],
            DATASET_PARAMETERS['sea_water_salinity_at_bottom'],
            DATASET_PARAMETERS['sea_water_temperature_at_bottom'],
            DATASET_PARAMETERS['sea_surface_height_above_geoid'],
            DATASET_PARAMETERS['eastward_sea_water_velocity'],
            DATASET_PARAMETERS['northward_sea_water_velocity'],
        ])
