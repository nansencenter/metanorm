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
        handler = handlers.GeospatialMetadataHandler(['test_output_parameter_names'],['test_repetitive_parameter'])

        normalizer = handler._chain
        i = 0
        while normalizer:
            self.assertIsInstance(normalizer, handler.NORMALIZERS[i])
            self.assertEqual(normalizer._output_parameter_names, ['test_output_parameter_names'])
            normalizer = normalizer.next
            i += 1

    @mock.patch.object(normalizers.BaseMetadataNormalizer, 'normalize', return_value={})
    def test_get_parameters_calls_normalize(self, mock_normalize):
        """Checks that the get_parameters calls the BaseMetadaNormalizer.normalize method"""
        handler = handlers.GeospatialMetadataHandler(['test_output_parameter_names'],['test_cumulative_parameter_names'])
        _ = handler.get_parameters({})
        mock_normalize.assert_called()

class OrderingOfNormalizer(unittest.TestCase):
    """Tests for the ordering of normalizers. """

    def test_dataset_parameters(self):
        """Shall return consistent results for cumulative parameters
        even if the ordering of normalizers are changed"""
        handler = handlers.GeospatialMetadataHandler(['platform'],['dataset_parameters'])
        handler.NORMALIZERS = [
        normalizers.OSISAFMetadataNormalizer,
        normalizers.SentinelSAFEMetadataNormalizer,
        normalizers.SentinelOneIdentifierMetadataNormalizer,
        normalizers.ACDDMetadataNormalizer,
        normalizers.GeoSpatialWellKnownMetadataNormalizer,
        normalizers.GeoSpatialDefaultMetadataNormalizer,
        ]
        n = handler._chain
        result=n.normalize({'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1', 'product_name':'osi_saf_mr_ice_drift'})
        self.assertEqual(len(result['dataset_parameters']),3)
        self.assertIn('sea_ice_y_displacement',[i['standard_name'] for i in result['dataset_parameters']])
        self.assertIn('sea_ice_x_displacement',[i['standard_name'] for i in result['dataset_parameters']])
        self.assertIn('surface_backwards_scattering_coefficient_of_radar_wave',[i['standard_name'] for i in result['dataset_parameters']])
        #Redefinition with another order of normalizers
        handler = handlers.GeospatialMetadataHandler(['platform'],['dataset_parameters'])
        handler.NORMALIZERS = [
        normalizers.SentinelSAFEMetadataNormalizer,
        normalizers.SentinelOneIdentifierMetadataNormalizer,
        normalizers.ACDDMetadataNormalizer,
        normalizers.OSISAFMetadataNormalizer,
        normalizers.GeoSpatialWellKnownMetadataNormalizer,
        normalizers.GeoSpatialDefaultMetadataNormalizer,
        ]
        n = handler._chain
        result=n.normalize({'Identifier': 'S1A_EW_GRDM_1SDH_20150702T172954_20150702T173054_006635_008DA5_55D1', 'product_name':'osi_saf_mr_ice_drift'})
        self.assertEqual(len(result['dataset_parameters']),3)
        self.assertIn('sea_ice_y_displacement',[i['standard_name'] for i in result['dataset_parameters']])
        self.assertIn('sea_ice_x_displacement',[i['standard_name'] for i in result['dataset_parameters']])
        self.assertIn('surface_backwards_scattering_coefficient_of_radar_wave',[i['standard_name'] for i in result['dataset_parameters']])
