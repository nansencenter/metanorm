"""Tests for the metadata handler"""
#pylint: disable=protected-access

import unittest

import metanorm.errors as errors
import metanorm.handlers as handlers
import metanorm.normalizers as normalizers


class MetadataHandlerTestCase(unittest.TestCase):
    """Test the base MetadataHandler class"""

    class TestBaseNormalizer(normalizers.MetadataNormalizer):
        """Base class for test normalizers"""

        def get_foo(self, raw_metadata):
            """Get the 'foo' attribute from raw metadata"""
            raise NotImplementedError

        def get_bar(self, raw_metadata):
            """Get the 'bar' attribute from raw metadata"""
            raise NotImplementedError

        def normalize(self, raw_metadata):
            return {
                'foo': self.get_foo(raw_metadata),
                'bar': self.get_bar(raw_metadata)
            }

    class TestNormalizer1(TestBaseNormalizer):
        """Test normalizer"""
        def check(self, raw_metadata):
            return 'foo' in raw_metadata and 'bar' in raw_metadata

        def get_foo(self, raw_metadata):
            return raw_metadata['foo']

        def get_bar(self, raw_metadata):
            return raw_metadata['bar']


    class TestNormalizer2(TestBaseNormalizer):
        """Test normalizer"""

        def get_foo(self, raw_metadata):
            return raw_metadata['baz']


    class TestNormalizer3(TestNormalizer2):
        """Test normalizer"""

        def check(self, raw_metadata):
            return set(('baz', 'qux', 'quux')).issubset(raw_metadata.keys())

        def get_bar(self, raw_metadata):
            return f"{raw_metadata['qux']}, {raw_metadata['quux']}"


    def setUp(self):
        self.handler = handlers.MetadataHandler(self.TestBaseNormalizer)

    def test_instantiation(self):
        """Test that the handler builds a list of all normalizers which
        inherit from a base class
        """
        self.assertCountEqual(
            (self.TestNormalizer1, self.TestNormalizer2, self.TestNormalizer3),
            (n.__class__ for n in self.handler.normalizers))

    def test_get_parameters(self):
        """Test that the metadata is normalized using the right
        normalizers
        """
        self.assertDictEqual(
            self.handler.get_parameters({'foo': 'value1', 'bar': 'value2'}),
            {'foo': 'value1', 'bar': 'value2'}
        )

        self.assertDictEqual(
            self.handler.get_parameters({
                'baz': 'value3',
                'qux': 'value4',
                'quux': 'value5'
            }),
            {'foo': 'value3', 'bar': 'value4, value5'}
        )

    def test_get_parameters_not_found(self):
        """get_parameters() should raise an exception if not normalizer
        was found for the given metadata
        """
        with self.assertRaises(errors.NoNormalizerFound):
            self.handler.get_parameters({'something': 'something'})
