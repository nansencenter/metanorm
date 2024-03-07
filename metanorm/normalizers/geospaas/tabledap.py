"""Normalizer for ERDDAP's tabledap data"""
import dateutil.parser
from collections import OrderedDict

from shapely.geometry import LineString

import metanorm.utils as utils
from .base import GeoSPaaSMetadataNormalizer
from ...errors import MetadataNormalizationError


class TableDAPMetadataNormalizer(GeoSPaaSMetadataNormalizer):
    """Generate the properties of a GeoSPaaS Dataset using tabledap
    attributes
    """

    @staticmethod
    def get_product_attribute(product_metadata, attribute):
        """Extract the value of an attribute from tabledap product
        metadata
        """
        for row in product_metadata['table']['rows']:
            if row[2] == attribute:
                return row[4]
        raise MetadataNormalizationError(f'Could not find product attribute {attribute}')

    @utils.raises(KeyError)
    def check(self, raw_metadata):
        return 'tabledap' in raw_metadata.get('url', '')

    @utils.raises(KeyError)
    def get_entry_title(self, raw_metadata):
        return self.get_product_attribute(raw_metadata['product_metadata'], 'title')

    @utils.raises(KeyError)
    def get_entry_id(self, raw_metadata):
        return raw_metadata['entry_id']

    @utils.raises(KeyError)
    def get_summary(self, raw_metadata):
        return self.get_product_attribute(raw_metadata['product_metadata'], 'summary')

    @utils.raises(KeyError)
    def get_time_coverage_start(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['temporal_coverage'][0])

    @utils.raises(KeyError)
    def get_time_coverage_end(self, raw_metadata):
        return dateutil.parser.parse(raw_metadata['temporal_coverage'][1])

    @utils.raises(KeyError)
    def get_platform(self, raw_metadata):
        source = self.get_product_attribute(raw_metadata['product_metadata'], 'source')
        platform = utils.get_gcmd_platform(source)
        # backwards conpatibility with older GCMD versions
        if platform['Short_Name'] == utils.UNKNOWN and source == 'Argo float':
            return OrderedDict([
              ('Basis', 'Water-based Platforms'),
              ('Category', 'Buoys'),
              ('Sub_Category', 'Unmoored'),
              ('Short_Name', 'Argo-Float'),
              ('Long_Name', '')])
        return platform

    def get_instrument(self, raw_metadata):
        return utils.get_gcmd_instrument('Unknown')

    @utils.raises(KeyError)
    def get_location_geometry(self, raw_metadata):
        return raw_metadata['trajectory']

    @utils.raises(KeyError)
    def get_provider(self, raw_metadata):
        """Returns a GCMD-like provider data structure"""
        institution = self.get_product_attribute(raw_metadata['product_metadata'], 'institution')
        provider = utils.get_gcmd_provider([institution])
        if provider:
            return provider
        else:
            return OrderedDict([
                ('Bucket_Level0', 'CONSORTIA/INSTITUTIONS'),
                ('Bucket_Level1', ''),
                ('Bucket_Level2', ''),
                ('Bucket_Level3', ''),
                ('Short_Name', institution[:100]),
                ('Long_Name', institution[:250]),
                ('Data_Center_URL', '')])
