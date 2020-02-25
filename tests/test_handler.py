"""Tests for the metadata handler"""
#pylint: disable=protected-access

import unittest
import unittest.mock as mock

import metanorm.handlers as handlers
import metanorm.normalizers as normalizers


class GeospatialMetadataHandlerTestCase(unittest.TestCase):
    """Test the GeospatialMetadataHandler class"""

    def test_build_normalizer_chain(self):
        """Instantiate a handler and check the normalizer chain is correctly built"""
        handler = handlers.GeospatialMetadataHandler(['test_parameter'])

        normalizer = handler._chain
        i = 0
        while normalizer:
            self.assertIsInstance(normalizer, handler.NORMALIZERS[i])
            self.assertEqual(normalizer._parameter_names, ['test_parameter'])
            normalizer = normalizer.next
            i += 1

    @mock.patch.object(normalizers.BaseMetadataNormalizer, 'normalize', return_value={})
    def test_get_parameters_calls_normalize(self, mock_normalize):
        """Checks that the get_parameters calls the BaseMetadaNormalizer.normalize method"""
        handler = handlers.GeospatialMetadataHandler(['test_parameter'])
        _ = handler.get_parameters({})
        mock_normalize.assert_called()
