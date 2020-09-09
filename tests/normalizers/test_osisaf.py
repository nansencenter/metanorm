"""Tests for the OSISAF metadata normalizer"""
import unittest
from collections import OrderedDict

import dateutil
from dateutil.tz import tzutc
import metanorm.normalizers as normalizers


class OSISAFMetadataNormalizer(unittest.TestCase):
    """Tests for the OSISAF attributes normalizer"""

    def setUp(self):
        self.normalizer = normalizers.OSISAFMetadataNormalizer([], [])

    def test_summary(self):
        """summary from OSISAFMetadataNormalizer"""

        attributes = {'abstract': 'value_abs'}
        self.assertEqual('value_abs', self.normalizer.get_summary(attributes))

    def test_instrument_from_instrument_type_raw_attribute(self):
        """instrument from OSISAFMetadataNormalizer"""
        attributes = {'instrument_type': 'value_1'}
        # 'instrument_type' must be used in this normalizer
        self.assertEqual(self.normalizer.get_instrument(
            attributes)['Short_Name'], 'value_1')

    def test_instrument_ice_conc(self):
        """instrument from OSISAFMetadataNormalizer in the absence of 'instrument_type' and based
        on 'product_name' """
        attributes = {'product_name': 'osi_saf_ice_conc'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', ''),
                         ('Long_Name', '')])
        )

    def test_instrument_ice_type(self):
        """instrument from OSISAFMetadataNormalizer in the absence of 'instrument_type' and based
        on 'product_name' """
        attributes = {'product_name': 'osi_saf_ice_type'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', ''),
                         ('Long_Name', '')])
        )

    def test_instrument_ice_edge(self):
        """instrument from OSISAFMetadataNormalizer in the absence of 'instrument_type' and based
        on 'product_name' """
        attributes = {'product_name': 'osi_saf_ice_edge'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', ''),
                         ('Long_Name', '')])
        )

    def test_instrument_amsr2ice_conc(self):
        """instrument from OSISAFMetadataNormalizer in the absence of 'instrument_type' and based
        on 'product_name' """
        attributes = {'product_name': 'osi_saf_amsr2ice_conc'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', 'AMSR2'),
                         ('Long_Name', 'Advanced Microwave Scanning Radiometer 2')])
        )

    def test_instrument_lr_ice_drift(self):
        """instrument from OSISAFMetadataNormalizer in the absence of 'instrument_type' and based
        on 'product_name' """
        attributes = {'product_name': 'osi_saf_lr_ice_drift'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', ''),
                         ('Type', ''),
                         ('Subtype', ''),
                         ('Short_Name', ''),
                         ('Long_Name', '')])
        )

    def test_instrument__mr_ice_drift(self):
        """instrument from OSISAFMetadataNormalizer in the absence of 'instrument_type' and based
        on 'product_name' """
        attributes = {'product_name': 'osi_saf_mr_ice_drift'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', 'AVHRR'),
                         ('Long_Name', 'Advanced Very High Resolution Radiometer')])
        )

    def test_instrument_incorrect_product_of_osisaf_project(self):
        """instrument from OSISAFMetadataNormalizer in the absence of 'instrument_type' and based
        on 'product_name'. IF the name of product is not recognized, it shall return unknown """
        attributes = {'product_name': 'osi_saf_2'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Unknown'),
                         ('Class', 'Unknown'),
                         ('Type', 'Unknown'),
                         ('Subtype', 'Unknown'),
                         ('Short_Name', 'Unknown'),
                         ('Long_Name', 'Unknown')])
        )

    def test_instrument_without_any_information_in_raw_attributes(self):
        """instrument from OSISAFMetadataNormalizer in the absence of 'instrument_type' and
        and 'product_name'. It shall return None """
        attributes = {'test': 'test'}
        self.assertIsNone(self.normalizer.get_instrument(attributes))

    def test_platform_based_on_platform_name_raw_attribute(self):
        """platform from OSISAFMetadataNormalizer"""
        attributes = {'platform_name': 'value_1'}
        # 'instrument_type' must be used in this normalizer
        self.assertEqual(self.normalizer.get_platform(
            attributes)['Short_Name'], 'value_1')

    def test_platform_without_any_information_in_raw_attributes(self):
        """ in the absence of 'platform_name' value should be None"""
        attributes = {'activity_type': 'value_2'}
        self.assertIsNone(self.normalizer.get_instrument(attributes))

    def test_platform_2(self):
        """in the absence of 'platform_name' value should be UNKNOWN with GCMD template """
        attributes = {'product_name': 'osi_saf_2'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', ''),
                         ('Short_Name', ''),
                         ('Long_Name', '')])
        )

    def test_time_coverage_start(self):
        """time_coverage_start from OSISAFMetadataNormalizer."""
        attributes = {'start_date': '2020-07-12 00:00:00'}
        self.assertEqual(self.normalizer.get_time_coverage_start(attributes),
                         dateutil.parser.parse("2020-07-12").replace(tzinfo=tzutc()))

    def test_time_coverage_end(self):
        """time_coverage_end from OSISAFMetadataNormalizer."""
        attributes = {'stop_date': '2020-07-14 00:00:00'}
        self.assertEqual(self.normalizer.get_time_coverage_end(attributes),
                         dateutil.parser.parse("2020-07-14").replace(tzinfo=tzutc()))

    def test_location_geometry(self):
        """location_geometry from OSISAFMetadataNormalizer"""
        attributes = {
            'northernsmost_latitude': "9.47472000",
            'southernmost_latitude': "-15.3505001",
            'easternmost_longitude': "-142.755005",
            'westernmost_longitude': "-175.084000"
        }
        expected_geometry = ('POLYGON((' +
             '-175.084000 -15.3505001,' +
             '-142.755005 -15.3505001,' +
             '-142.755005 9.47472000,' +
             '-175.084000 9.47472000,' +
             '-175.084000 -15.3505001))')
        normalizer = normalizers.OSISAFMetadataNormalizer(
            ['location_geometry'], [])
        normalized_params = normalizer.normalize(attributes)
        self.assertIsInstance(normalized_params, dict)
        self.assertTrue('location_geometry' in normalized_params)
        self.assertEqual(normalized_params['location_geometry'], expected_geometry)

    def test_provider(self):
        """provider information from OSISAFMetadataNormalizer """
        attributes = {'institution': 'company1'}
        self.assertEqual(self.normalizer.get_provider(attributes),
                         OrderedDict([('Bucket_Level0', 'Unknown'),
                                      ('Bucket_Level1', 'Unknown'),
                                      ('Bucket_Level2', 'Unknown'),
                                      ('Bucket_Level3', 'Unknown'),
                                      ('Short_Name', 'company1'),
                                      ('Long_Name', 'company1'),
                                      ('Data_Center_URL', 'Unknown'),
                                      ]))

    def test_for_returning_none(self):
        """None should be returned for absurd raw metadata"""
        attributes = {'absurd': 'absurd_meta_data'}
        for param in ['instrument', 'platform', 'time_coverage_start', 'time_coverage_end',
                      'summary', 'provider', 'location_geometry', ]:
            instantiated_method = getattr(self.normalizer, 'get_' + param)
            self.assertIsNone(instantiated_method(attributes))

    def test_gcmd_provider(self):
        """GCMD provider from OSISAFMetadataNormalizer"""
        attributes = {
            'institution': 'NERSC',
        }
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([
                ('Bucket_Level0', 'CONSORTIA/INSTITUTIONS'),
                ('Bucket_Level1', ''),
                ('Bucket_Level2', ''),
                ('Bucket_Level3', ''),
                ('Short_Name', 'NERSC'),
                ('Long_Name', 'Nansen Environmental and Remote Sensing Centre'),
                ('Data_Center_URL', 'http://www.nersc.no/main/index2.php')
            ])
        )

    def test_non_gcmd_provider(self):
        """Non-GCMD provider from OSISAFMetadataNormalizer"""
        attributes = {
            'institution': 'NONGCMD',
        }
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([
                ('Bucket_Level0', 'Unknown'),
                ('Bucket_Level1', 'Unknown'),
                ('Bucket_Level2', 'Unknown'),
                ('Bucket_Level3', 'Unknown'),
                ('Short_Name', 'NONGCMD'),
                ('Long_Name', 'NONGCMD'),
                ('Data_Center_URL', 'Unknown')
            ])
        )

    def test_non_gcmd_provider_long_name(self):
        """
        Non-GCMD provider from OSISAFMetadataNormalizer, with a name longer than 250 characters
        """
        attributes = {
            'institution':
                'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod ' +
                'tempor incididunt ut labore et dolore magna aliqua. Bibendum neque egest' +
                'as congue quisque egestas diam in. Eget magna fermentum iaculis eu non d' +
                'iam phasellus vestibulum lorvgem. Tempor commodo.',
        }
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([
                ('Bucket_Level0', 'Unknown'),
                ('Bucket_Level1', 'Unknown'),
                ('Bucket_Level2', 'Unknown'),
                ('Bucket_Level3', 'Unknown'),
                ('Short_Name', attributes['institution'][:50]),
                ('Long_Name', attributes['institution'][:250]),
                ('Data_Center_URL', 'Unknown')
            ])
        )

    def test_non_gcmd_provider_no_name(self):
        """Non-GCMD provider from ACDDMetadataNormalizer, with no name provided"""
        attributes = {'project': 'test_name'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([
                ('Bucket_Level0', 'Unknown'),
                ('Bucket_Level1', 'Unknown'),
                ('Bucket_Level2', 'Unknown'),
                ('Bucket_Level3', 'Unknown'),
                ('Short_Name', 'test_name'),
                ('Long_Name', 'test_name'),
                ('Data_Center_URL', 'Unknown')
            ])
        )
