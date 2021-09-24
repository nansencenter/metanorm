"""Tests for the NOAA RTOFS normalizer"""
import unittest
from collections import OrderedDict
from datetime import datetime
from dateutil.tz import tzutc

import metanorm.normalizers as normalizers
from .data import DATASET_PARAMETERS
from metanorm.errors import MetadataNormalizationError


class NOAARTOFSMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the NOAA RTOFS ftp normalizer"""
    def setUp(self):
        self.normalizer = normalizers.geospaas.NOAARTOFSMetadataNormalizer()

    def test_check(self):
        """Test the checking condition"""
        self.assertTrue(self.normalizer.check({
            'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                   'rtofs.20210923/rtofs_glo_2ds_f000_diag.nc'}))

        self.assertFalse(self.normalizer.check({}))
        self.assertFalse(self.normalizer.check({'url': 'ftp://foo/bar'}))

    def test_entry_title(self):
        """entry_title from NOAARTOFSMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_entry_title({}),
            'Global operational Real-Time Ocean Forecast System')

    def test_entry_id(self):
        """entry_id from NOAARTOFSMetadataNormalizer """
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_3dz_f024_daily_3zsio.nc'}
        self.assertEqual(
            self.normalizer.get_entry_id(attributes),
            '20210518/rtofs_glo_3dz_f024_daily_3zsio')

    def test_entry_id_error(self):
        """a MetadataNormalizationError must be raised when an entry_id cannot be found"""
        # wrong file format
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({'url': 'ftp://foo/bar.txt'})
        # no url attribute
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_entry_id({})

    def test_summary(self):
        """summary from NOAARTOFSMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_summary({}),
            "Description: Real Time Ocean Forecast System (RTOFS) Global is a data-assimilating "
            "nowcast-forecast system operated by the National Weather Service's National "
            "Centers for Environmental Prediction (NCEP).;"
            "Processing level: 4;"
            "Product: RTOFS")

    def test_time_coverage_start_3dz_daily(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20210519/'
                'rtofs_glo_3dz_n024_daily_3zsio.nc'
            }),
            datetime(year=2021, month=5, day=20, tzinfo=tzutc()))

    def test_time_coverage_start_3dz_6hourly(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20210518/'
                'rtofs_glo_3dz_f042_6hrly_hvr_US_east.nc'
            }),
            datetime(year=2021, month=5, day=19, hour=18, tzinfo=tzutc()))

    def test_time_coverage_start_2ds(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20210518/'
                'rtofs_glo_2ds_f062_prog.nc'
            }),
            datetime(year=2021, month=5, day=20, hour=14, tzinfo=tzutc()))

    def test_time_coverage_start_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_start({})

    def test_time_coverage_end_3dz_daily(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20210519/'
                'rtofs_glo_3dz_n024_daily_3zsio.nc'
            }),
            datetime(year=2021, month=5, day=20, tzinfo=tzutc()))

    def test_time_coverage_end_3dz_6hourly(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20210518/'
                'rtofs_glo_3dz_f042_6hrly_hvr_US_east.nc'
            }),
            datetime(year=2021, month=5, day=19, hour=18, tzinfo=tzutc()))

    def test_time_coverage_end_2ds(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20210518/'
                'rtofs_glo_2ds_f062_prog.nc'
            }),
            datetime(year=2021, month=5, day=20, hour=14, tzinfo=tzutc()))

    def test_time_coverage_end_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_time_coverage_end({})

    def test_platform(self):
        """platform from NOAARTOFSMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_platform({}),
            OrderedDict([('Category', 'Models/Analyses'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'OPERATIONAL MODELS'),
                         ('Long_Name', '')]))

    def test_instrument(self):
        """instrument from NOAARTOFSMetadataNormalizer """
        self.assertEqual(
            self.normalizer.get_instrument({}),
            OrderedDict([('Category', 'In Situ/Laboratory Instruments'),
                         ('Class', 'Data Analysis'),
                         ('Type', 'Environmental Modeling'),
                         ('Subtype', ''),
                         ('Short_Name', 'Computer'),
                         ('Long_Name', 'Computer')]))

    def test_location_geometry_global(self):
        """Should return the proper geometry"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_3dz_f024_daily_3zsio.nc'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'
        )

    def test_location_geometry_us_east(self):
        """Should return the proper geometry"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_3dz_f042_6hrly_hvr_US_east.nc'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            ('POLYGON (('
                '-105.193603515625 0, -40.719970703125 0,'
                '-40.719970703125 79.74808502197266,'
                '-105.193603515625 79.74808502197266,'
                '-105.193603515625 0))'))

    def test_location_geometry_us_west(self):
        """Should return the proper geometry"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_3dz_f042_6hrly_hvr_US_west.nc'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            ('POLYGON (('
                '-157.9200439453125 10.02840137481689,'
                '-74.239990234375 10.02840137481689,'
                '-74.239990234375 74.57466888427734,'
                '-157.9200439453125 74.57466888427734,'
                '-157.9200439453125 10.02840137481689))'))

    def test_location_geometry_alaska(self):
        """Should return the proper geometry"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_3dz_f042_6hrly_hvr_alaska.nc'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            ('POLYGON (('
                '-179.1199951171875 45.77324676513672,'
                '-112.6572265625 45.77324676513672,'
                '-112.6572265625 78.41667938232422,'
                '-179.1199951171875 78.41667938232422,'
                '-179.1199951171875 45.77324676513672))'))

    def test_geometry_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_location_geometry({})

    def test_provider(self):
        """provider from NOAARTOFSMetadataNormalizer """
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

    def test_dataset_parameters_rtofs_2ds_diag(self):
        """Should return the proper dataset parameters"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_2ds_f063_diag.nc'}
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            DATASET_PARAMETERS['sea_surface_height_above_geoid'],
            DATASET_PARAMETERS['barotropic_eastward_sea_water_velocity'],
            DATASET_PARAMETERS['barotropic_northward_sea_water_velocity'],
            DATASET_PARAMETERS['surface_boundary_layer_thickness'],
            DATASET_PARAMETERS['ocean_mixed_layer_thickness'],
        ])

    def test_dataset_parameters_rtofs_2ds_prog(self):
        """Should return the proper dataset parameters"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_2ds_f062_prog.nc'}
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            DATASET_PARAMETERS['eastward_sea_water_velocity'],
            DATASET_PARAMETERS['northward_sea_water_velocity'],
            DATASET_PARAMETERS['sea_surface_temperature'],
            DATASET_PARAMETERS['sea_surface_salinity'],
            DATASET_PARAMETERS['sea_water_potential_density'],
        ])

    def test_dataset_parameters_rtofs_2ds_ice(self):
        """Should return the proper dataset parameters"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_2ds_f062_ice.nc'}
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            DATASET_PARAMETERS['ice_coverage'],
            DATASET_PARAMETERS['ice_temperature'],
            DATASET_PARAMETERS['ice_thickness'],
            DATASET_PARAMETERS['ice_uvelocity'],
            DATASET_PARAMETERS['icd_vvelocity'],
        ])

    def test_dataset_parameters_rtofs_3dz(self):
        """Should return the proper dataset parameters"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_3dz_f024_daily_3zsio.nc'}
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            DATASET_PARAMETERS['eastward_sea_water_velocity'],
            DATASET_PARAMETERS['northward_sea_water_velocity'],
            DATASET_PARAMETERS['sea_surface_temperature'],
            DATASET_PARAMETERS['sea_surface_salinity'],
        ])

    def test_dataset_parameters_missing_attribute(self):
        """An exception must be raised if the attribute is missing"""
        with self.assertRaises(MetadataNormalizationError):
            self.normalizer.get_dataset_parameters({})
