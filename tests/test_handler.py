"""Tests for the metadata handler"""
#pylint: disable=protected-access

import unittest
import unittest.mock as mock

import metanorm.handlers as handlers
import metanorm.normalizers as normalizers


class GeospatialMetadataHandlerTestCase(unittest.TestCase):
    """Test the GeospatialMetadataHandler class"""

    def test_GeoSpatialDefault_normalizer_be_last_in_chain(self):
        """It is mandatory to have 'GeoSpatialDefaultMetadataNormalizer' in the list of normalizers
        (the last one)."""
        handler = handlers.GeospatialMetadataHandler(
            ['test_output_parameter'], ['test_cumulative_parameter'])
        self.assertTrue(
            normalizers.geospatial_defaults.GeoSpatialDefaultMetadataNormalizer
            == handler.NORMALIZERS[-1]
            )

    def test_GeoSpatialDefault_normalizer_is_lost_in_chain(self):
        """ GeoSpatialDefaultMetadataNormalizer normalizer should never be removed from the list of
        normalizers (otherwise, ValueError must be raised). Below list of NORMALIZERS lacks it """
        class TestHandler(handlers.MetadataHandler):
            """testing metadata handler"""
            NORMALIZERS = [
                normalizers.NETCDFCFMetadataNormalizer,
                normalizers.SentinelSAFEMetadataNormalizer,
                normalizers.SentinelOneIdentifierMetadataNormalizer,
                normalizers.ACDDMetadataNormalizer,
            ]
        with self.assertRaises(ValueError):
            TestHandler(['test_output_parameter'], ['test_cumulative_parameter'])

    def test_build_normalizer_chain(self):
        """Instantiate a handler and check the normalizer chain is correctly built"""
        handler = handlers.GeospatialMetadataHandler(
            ['test_output_parameter'], ['test_cumulative_parameter'])

        normalizer = handler._chain
        i = 0
        while normalizer:
            self.assertIsInstance(normalizer, handler.NORMALIZERS[i])
            self.assertEqual(normalizer._output_parameters_names, ['test_output_parameter'])
            self.assertEqual(normalizer._output_cumulative_parameters_names, [
                             'test_cumulative_parameter'])
            normalizer = normalizer.next
            i += 1

    @mock.patch.object(normalizers.BaseMetadataNormalizer, 'normalize', return_value={})
    def test_get_parameters_calls_normalize(self, mock_normalize):
        """Checks that the get_parameters calls the BaseMetadaNormalizer.normalize method"""
        handler = handlers.GeospatialMetadataHandler(
            ['test_output_parameter_name'], ['test_cumulative_parameter_name'])
        _ = handler.get_parameters({})
        mock_normalize.assert_called()
