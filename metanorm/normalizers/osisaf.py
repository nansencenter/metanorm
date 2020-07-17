import logging
import re

import dateutil.parser
import pythesint as pti
import metanorm.utils as utils
from dateutil.tz import tzutc
from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class OSISAFMetadataNormalizer(BaseMetadataNormalizer):
    def get_instrument(self, raw_attributes):
        """ returns the suitable instrument based on the filename """
        if set(['instrument_type']).issubset(raw_attributes.keys()):
            return utils.get_gcmd_instrument(raw_attributes['instrument_type'])
        else:
            return None

    def get_platform(self, raw_attributes):
        """ returns the suitable instrument based on the filename """
        if set(['platform_name']).issubset(raw_attributes.keys()):
            return utils.get_gcmd_platform(raw_attributes['platform_name'])
        else:
            return None

    def get_time_coverage_start(self, raw_attributes):
        """ returns the suitable instrument based on the filename """
        if set(['start_date']).issubset(raw_attributes.keys()):
            return dateutil.parser.parse(raw_attributes['start_date'].replace(' ','T'))
        else:
            return None

    def get_time_coverage_end(self, raw_attributes):
        """ returns the suitable instrument based on the filename """
        if set(['stop_date']).issubset(raw_attributes.keys()):
            return dateutil.parser.parse(raw_attributes['stop_date'].replace(' ','T'))
        else:
            return None

    def get_summary(self, raw_attributes):
        """ returns the suitable instrument based on the filename """
        if set(['abstract']).issubset(raw_attributes.keys()):
            return raw_attributes['abstract']
        else:
            return None
    # TODO
    #def get_dataset_parameters(self, raw_attributes):
    #    """ returns the suitable instrument based on the filename """
    #    if set(['product_name']).issubset(raw_attributes.keys()):
    #        if raw_attributes['product_name'][:4]=='':
#
    #        return [pti.get_wkv_variable(raw_attributes['osi_saf_ice_type'])]
    #    else:
    #        return None
