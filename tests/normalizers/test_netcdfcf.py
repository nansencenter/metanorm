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
