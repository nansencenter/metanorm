"""Tests for the filename metadata normalizer"""
import datetime
import unittest
from collections import OrderedDict
from dateutil.tz import tzutc

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
            "provider",
            "dataset_parameters"
        ]
        self.normalizer = normalizers.sentinel1_identifier.SentinelOneIdentifierMetadataNormalizer(
            DATASET_PARAMETER_NAMES, [])
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
            2015, 7, 2, 17, 29, 54, tzinfo=tzutc()))
        self.assertEqual(result_normalization['time_coverage_end'], datetime.datetime(
            2015, 7, 2, 17, 30, 54, tzinfo=tzutc()))

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
                ('Short_Name', 'SENTINEL-1 C-SAR'),
                ('Long_Name', '')])
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

    def test_parameters_identification(self):
        """ Shall return the correct sentinel1 parameter based on the filename """
        result_normalization = self.normalizer.normalize(
            {'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(
            result_normalization['dataset_parameters'],
            [
                OrderedDict([
                    ('standard_name', 'surface_backwards_scattering_coefficient_of_radar_wave'),
                    ('canonical_units', '1'),
                    ('grib', ''),
                    ('amip', ''),
                    ('description', 'The scattering/absorption/attenuation coefficient is assumed to be an integral over all wavelengths, unless a coordinate of radiation_wavelength is included to specify the wavelength. Scattering of radiation is its deflection from its incident path without loss of energy. Backwards scattering refers to the sum of scattering into all backward angles i.e. scattering_angle exceeding pi/2 radians. A scattering_angle should not be specified with this quantity.')
                ])
            ])

    def test_return_none_for_incorrect_raw_attribute(self):
        """ Shall return None based on non-recognizable raw attribute """
        result_normalization = self.normalizer.normalize(
            {'Iifi': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(
            result_normalization['entry_id'], None)

    def test_return_proper_output_of_regex_based_on_different_raw_attribute_situation(self):
        """ Shall return None based on situation of specific character inside the Identifier attribute """

        result_normalization = self.normalizer.match_identifier(
            {'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(result_normalization['type'], "GRD")
        self.assertEqual(result_normalization['resolution'], "M")
        self.assertEqual(result_normalization['mode'], "EW")
        self.assertEqual(result_normalization['orbit'], "006635")
        self.assertEqual(result_normalization['mission_id'], "008DA5")
        self.assertEqual(result_normalization['product_id'], "55D1")
        self.assertEqual(result_normalization['processing_level'], "1")
        self.assertEqual(result_normalization['class'], "S")
        self.assertEqual(result_normalization['polarization'], "DH")
        self.assertEqual(result_normalization['time_coverage_start'], "20150702T172954")
        self.assertEqual(result_normalization['time_coverage_end'], "20150702T173054")

        result_normalization = self.normalizer.match_identifier(
            {'Identifier': 'S1A_EW____M_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(result_normalization['type'], "___")

        result_normalization = self.normalizer.match_identifier(
            {'Identifier': 'S1A_EW_GRD__1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(result_normalization['resolution'], "_")

        result_normalization = self.normalizer.match_identifier(
            {'Identifier': 'S1A____GRD__1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(result_normalization['mode'], "__")

        result_normalization = self.normalizer.match_identifier(
            {'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054________008DA5_55D1'})
        self.assertEqual(result_normalization['orbit'], "______")

        result_normalization = self.normalizer.match_identifier(
            {'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635________55D1'})
        self.assertEqual(result_normalization['mission_id'], "______")

        result_normalization = self.normalizer.match_identifier(
            {'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_____'})
        self.assertEqual(result_normalization['product_id'], "____")

        result_normalization = self.normalizer.match_identifier(
            {'Identifier': 'S1A_EW_GRDM__SDH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(result_normalization['processing_level'], "_")

        result_normalization = self.normalizer.match_identifier(
            {'Identifier': 'S1A_EW_GRDM_1_DH_20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(result_normalization['class'], "_")

        result_normalization = self.normalizer.match_identifier(
            {'Identifier': 'S1A_EW_GRDM_1S___20150702T172954_20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(result_normalization['polarization'], "__")

        result_normalization = self.normalizer.match_identifier(
            {'Identifier': 'S1A_EW_GRDM_1S___________________20150702T173054_006635_008DA5_55D1'})
        self.assertEqual(result_normalization['time_coverage_start'], "_______________")

        result_normalization = self.normalizer.match_identifier(
            {'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_________________006635_008DA5_55D1'})
        self.assertEqual(result_normalization['time_coverage_end'], "_______________")
