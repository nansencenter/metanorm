"""Tests for the base metadata normalizer"""
#pylint: disable=protected-access

import unittest
from collections import OrderedDict

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError
import metanorm.handlers as handlers


class BaseMetadataNormalizerTestCase(unittest.TestCase):
    """
    Tests for the base metadata normalizer. Trivial test normalizers which inherit from the
    BaseMetadataNormalizer are used to test it.
    """

    class TestMetadataNormalizer(normalizers.BaseMetadataNormalizer):
        """
        Class containing trivial attribute methods, used to test the functionalities of the base
        class
        """

        def get_test_parameter(self, raw_attributes):
            """Basic attribute method"""
            return raw_attributes['test_attribute']

    class OtherTestMetadataNormalizer(normalizers.BaseMetadataNormalizer):
        """
        Class containing trivial attribute methods, used to test the functionalities of the base
        class
        """

        def get_other_parameter(self, raw_attributes):
            """Basic attribute method"""
            return raw_attributes['other_attribute']

    def test_instantiation(self):
        """Test the instantiation of a MetadataNormalizer"""
        normalizer = self.TestMetadataNormalizer(['test_parameter'], [])
        self.assertListEqual(
            normalizer._output_parameters_names, ['test_parameter'])

    def test_first_in_chain_normalization(self):
        """
        Test simple normalization of an attribute, as if at the beginning of the normalizing chain.
        The case of last in chain is also tested, since the normalizer's 'next' attribute is None
        """
        parameter_names = ['test_parameter']
        attributes = {'test_attribute': "test_attribute_value"}
        expected_result = {'test_parameter': "test_attribute_value"}

        normalizer = self.TestMetadataNormalizer(parameter_names, [])

        self.assertDictEqual(normalizer.normalize(attributes), expected_result)

    def test_chain_normalization(self):
        """Test chained normalization."""
        parameter_names = ['test_parameter', 'other_parameter']
        attributes = {
            'test_attribute': "test_attribute_value",
            'other_attribute': "other_attribute_value"
        }
        expected_result = {
            'test_parameter': "test_attribute_value",
            'other_parameter': "other_attribute_value"
        }

        normalizer_one = self.TestMetadataNormalizer(parameter_names, [])
        normalizer_two = self.OtherTestMetadataNormalizer(parameter_names, [])
        normalizer_one.next = normalizer_two

        self.assertDictEqual(normalizer_one.normalize(
            attributes), expected_result)

    def test_consistent_dataset_parameters_identification(self):
        """Shall return consistent results for cumulative parameters
        even if the ordering of normalizers are changed"""
        handlers.MetadataHandler.NORMALIZERS = [
            normalizers.NETCDFCFMetadataNormalizer,
            normalizers.OSISAFMetadataNormalizer,
            normalizers.SentinelOneIdentifierMetadataNormalizer,
            normalizers.GeoSpatialDefaultMetadataNormalizer,

        ]
        handler = handlers.MetadataHandler(
            ['platform'], ['dataset_parameters'])

        n = handler._chain
        result = n.normalize(
            {'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1', 'raw_dataset_parameters': ['sea_ice_y_displacement', 'sea_ice_x_displacement']})
        self.assertEqual(len(result['dataset_parameters']), 3)
        self.assertIn(OrderedDict([('standard_name', 'sea_ice_x_displacement'),
                                   ('canonical_units', 'm'),
                                   ('grib', ''),
                                   ('amip', ''),
                                   ('description', '"x" indicates a vector component along the grid x-axis, positive with increasing x. "Displacement" means the change in geospatial position of an object that has moved over time. If possible, the time interval over which the motion took place should be specified using a bounds variable for the time coordinate variable.  A displacement can be represented as a vector. Such a vector should however not be interpreted as describing a rectilinear, constant speed motion but merely as an indication that the start point of the vector is found at the tip of the vector after the time interval associated with the displacement variable.  A displacement does not prescribe a trajectory. Sea ice displacement can be defined as a two-dimensional vector, with no vertical component. An x displacement is calculated from the difference in the moving object\'s grid x coordinate between the start and end of the time interval associated with the displacement variable.')]), result['dataset_parameters'])

        self.assertIn(OrderedDict([('standard_name', 'sea_ice_y_displacement'),
                                   ('canonical_units', 'm'),
                                   ('grib', ''),
                                   ('amip', ''),
                                   ('description', '"y" indicates a vector component along the grid y-axis, positive with increasing y. "Displacement" means the change in geospatial position of an object that has moved over time. If possible, the time interval over which the motion took place should be specified using a bounds variable for the time coordinate variable. A displacement can be represented as a vector. Such a vector should however not be interpreted as describing a rectilinear, constant speed motion but merely as an indication that the start point of the vector is found at the tip of the vector after the time interval associated with the displacement variable.  A displacement does not prescribe a trajectory. Sea ice displacement can be defined as a two-dimensional vector, with no vertical component. A y displacement is calculated from the difference in the moving object\'s grid y coordinate between the start and end of the time interval associated with the displacement variable.')]), result['dataset_parameters'])

        self.assertIn(OrderedDict([('standard_name', 'surface_backwards_scattering_coefficient_of_radar_wave'),
                                   ('long_name', 'Normalized Radar Cross Section'),
                                   ('short_name', 'sigma0'),
                                   ('units', 'm/m'),
                                   ('minmax', '0 0.1'),
                                   ('colormap', 'gray')]), result['dataset_parameters'])

        # Redefinition with another order of normalizers
        handlers.NORMALIZERS = [
            normalizers.SentinelOneIdentifierMetadataNormalizer,
            normalizers.OSISAFMetadataNormalizer,
            normalizers.NETCDFCFMetadataNormalizer,
            normalizers.GeoSpatialDefaultMetadataNormalizer,
        ]
        handler = handlers.MetadataHandler(
            ['platform'], ['dataset_parameters'])

        n = handler._chain
        result = n.normalize(
            {'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1', 'raw_dataset_parameters': ['sea_ice_y_displacement', 'sea_ice_x_displacement']})
        self.assertEqual(len(result['dataset_parameters']), 3)
        self.assertIn(OrderedDict([('standard_name', 'sea_ice_x_displacement'),
                                   ('canonical_units', 'm'),
                                   ('grib', ''),
                                   ('amip', ''),
                                   ('description', '"x" indicates a vector component along the grid x-axis, positive with increasing x. "Displacement" means the change in geospatial position of an object that has moved over time. If possible, the time interval over which the motion took place should be specified using a bounds variable for the time coordinate variable.  A displacement can be represented as a vector. Such a vector should however not be interpreted as describing a rectilinear, constant speed motion but merely as an indication that the start point of the vector is found at the tip of the vector after the time interval associated with the displacement variable.  A displacement does not prescribe a trajectory. Sea ice displacement can be defined as a two-dimensional vector, with no vertical component. An x displacement is calculated from the difference in the moving object\'s grid x coordinate between the start and end of the time interval associated with the displacement variable.')]), result['dataset_parameters'])

        self.assertIn(OrderedDict([('standard_name', 'sea_ice_y_displacement'),
                                   ('canonical_units', 'm'),
                                   ('grib', ''),
                                   ('amip', ''),
                                   ('description', '"y" indicates a vector component along the grid y-axis, positive with increasing y. "Displacement" means the change in geospatial position of an object that has moved over time. If possible, the time interval over which the motion took place should be specified using a bounds variable for the time coordinate variable. A displacement can be represented as a vector. Such a vector should however not be interpreted as describing a rectilinear, constant speed motion but merely as an indication that the start point of the vector is found at the tip of the vector after the time interval associated with the displacement variable.  A displacement does not prescribe a trajectory. Sea ice displacement can be defined as a two-dimensional vector, with no vertical component. A y displacement is calculated from the difference in the moving object\'s grid y coordinate between the start and end of the time interval associated with the displacement variable.')]), result['dataset_parameters'])

        self.assertIn(OrderedDict([('standard_name', 'surface_backwards_scattering_coefficient_of_radar_wave'),
                                   ('long_name', 'Normalized Radar Cross Section'),
                                   ('short_name', 'sigma0'),
                                   ('units', 'm/m'),
                                   ('minmax', '0 0.1'),
                                   ('colormap', 'gray')]), result['dataset_parameters'])


class BaseDefaultMetadataNormalizerTestCase(unittest.TestCase):
    """
    Tests for the base default normalizer. Trivial normalizers which inherit from the base
    normalizers are used to test it.
    """

    class TestMetadataNormalizer(normalizers.BaseMetadataNormalizer):
        """
        Empty normalizer, used to test the functionalities of the base default normalizer
        """

    class TestDefaultMetadataNormalizer(normalizers.BaseDefaultMetadataNormalizer):
        """
        Class containing a trivial parameter method, used to test the functionalities of the base
        default normalizer
        """

        def get_test_parameter(self, raw_attributes):
            """Basic parameter method"""
            return raw_attributes['test_attribute']

    def test_normalize_parameter_with_existing_method(self):
        """
        When a method is defined for a parameter in a default normalizer, it should be used like in
        a standard normalizer
        """
        parameter_names = ['test_parameter']
        attributes = {
            'test_attribute': "test_attribute_value",
        }
        expected_result = {
            'test_parameter': "test_attribute_value",
        }

        normalizer_one = self.TestMetadataNormalizer(parameter_names, [])
        normalizer_two = self.TestDefaultMetadataNormalizer(
            parameter_names, [])
        normalizer_one.next = normalizer_two

        self.assertDictEqual(normalizer_one.normalize(
            attributes), expected_result)

    def test_normalize_parameter_without_existing_method(self):
        """When no method exists for a parameter, it should raise an exception"""
        output_parameter_names = ['other_parameter']
        attributes = {
            'test_attribute': "test_attribute_value",
        }

        normalizer = self.TestDefaultMetadataNormalizer(
            output_parameter_names, [])

        with self.assertRaises(MetadataNormalizationError):
            _ = normalizer.normalize(attributes)
