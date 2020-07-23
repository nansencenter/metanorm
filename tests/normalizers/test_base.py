"""Tests for the base metadata normalizer"""
#pylint: disable=protected-access

import unittest

import metanorm.normalizers as normalizers
from metanorm.errors import MetadataNormalizationError


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
        normalizer = self.TestMetadataNormalizer(['test_parameter'],[])
        self.assertListEqual(normalizer._output_parameter_names, ['test_parameter'])

    def test_first_in_chain_normalization(self):
        """
        Test simple normalization of an attribute, as if at the beginning of the normalizing chain.
        The case of last in chain is also tested, since the normalizer's 'next' attribute is None
        """
        parameter_names = ['test_parameter']
        attributes = {'test_attribute': "test_attribute_value"}
        expected_result = {'test_parameter': "test_attribute_value"}

        normalizer = self.TestMetadataNormalizer(parameter_names,[])

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

        normalizer_one = self.TestMetadataNormalizer(parameter_names,[])
        normalizer_two = self.OtherTestMetadataNormalizer(parameter_names,[])
        normalizer_one.next = normalizer_two

        self.assertDictEqual(normalizer_one.normalize(attributes), expected_result)


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

        normalizer_one = self.TestMetadataNormalizer(parameter_names,[])
        normalizer_two = self.TestDefaultMetadataNormalizer(parameter_names,[])
        normalizer_one.next = normalizer_two

        self.assertDictEqual(normalizer_one.normalize(attributes), expected_result)

    def test_normalize_parameter_without_existing_method(self):
        """When no method exists for a parameter, it should raise an exception"""
        output_parameter_names = ['other_parameter']
        attributes = {
            'test_attribute': "test_attribute_value",
        }

        normalizer = self.TestDefaultMetadataNormalizer(output_parameter_names,[])

        with self.assertRaises(MetadataNormalizationError):
            _ = normalizer.normalize(attributes)
