"""Tests for the base metadata normalizer"""
#pylint: disable=protected-access

import unittest

import metanorm.normalizers as normalizers


class MetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the base metadata normalizer
    """

    def test_check(self):
        """check() should always return False on base classes"""
        self.assertFalse(normalizers.MetadataNormalizer().check({}))

    def test_abstract_normalize(self):
        """normalize() should raise a NotImplementedError"""
        with self.assertRaises(NotImplementedError):
            normalizers.MetadataNormalizer().normalize({})
