import unittest
import metanorm.normalizers as normalizers
from collections import OrderedDict
import unittest.mock as mock
import pythesint as pti
import metanorm.utils as utils

class OSISAFMetadataNormalizer(unittest.TestCase):
    """Tests for the NETCDFCF normalizer"""

    def setUp(self):
        self.normalizer = normalizers.NETCDFCFMetadataNormalizer([], [])

    @mock.patch.object(utils, 'get_cf_or_wkv_standard_name',
    return_value={'standard_name':'test1', 'amip':'test2'})
    def test_dataset_parameters(self, mock_normalize):
        """ dataset_parameters from OSISAFMetadataNormalizer. Shall return the proper value
         (sea_ice_area_fraction) and corresponding fields of it("standard_name" and "amip") """
        attributes = {'raw_dataset_parameters': ['sea_ice_y_displacement','sea_ice_x_displacement']}

        self.assertEqual(self.normalizer.get_dataset_parameters(attributes),
                         [{'standard_name':'test1', 'amip':'test2'},
                         {'standard_name':'test1', 'amip':'test2'}])

    @mock.patch.object(pti, 'get_wkv_variable',
    return_value={'standard_name':'test1', 'amip':'test2'})
    def test_dataset_parameters(self, mock_normalize):
        """ Shall return values from "get_wkv_variable" function in the case of no value from
        "get_cf_standard_name" function """
        self.assertEqual(utils.get_cf_or_wkv_standard_name("dummy"),
                         {'standard_name':'test1', 'amip':'test2'})

    def test_incorrect_dataset_parameters(self):
        """ in the case of incorrect value inside 'raw_dataset_parameters' it shall pass and always
        return an empty list """
        attributes = {'raw_dataset_parameters': ['false_standard_name']}
        self.assertEqual(self.normalizer.get_dataset_parameters(attributes), [])

        attributes = {'testing_dictionary_key': ['dummy_standard_name']}
        self.assertEqual(self.normalizer.get_dataset_parameters(attributes), [])
