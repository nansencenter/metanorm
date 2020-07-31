import unittest
import metanorm.normalizers as normalizers
from collections import OrderedDict
import unittest.mock as mock
import pythesint as pti

class OSISAFMetadataNormalizer(unittest.TestCase):
    """Tests for the NETCDFCF normalizer"""

    def setUp(self):
        self.normalizer = normalizers.NETCDFCFMetadataNormalizer([], [])

    @mock.patch.object(pti, 'search_cf_standard_name_list',return_value=[{'standard_name':'sea_ice_area_fraction', 'amip':'sic'}])
    def test_dataset_parameters(self, mock_normalize):
        """ dataset_parameters from OSISAFMetadataNormalizer. Shall return the proper value
         (one of "concentration", "type" or "drift") """
        attributes = {'raw_dataset_parameters': ['sea_ice_y_displacement','sea_ice_x_displacement']}

        self.assertEqual(self.normalizer.get_dataset_parameters(attributes)[0],
                         {'standard_name':'sea_ice_area_fraction', 'amip':'sic'})
