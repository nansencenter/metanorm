"""Normalizer for the CF Standard convention"""

import logging

import metanorm.utils as utils
from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class NETCDFCFMetadataNormalizer(BaseMetadataNormalizer):
    """ Search and find the corresponding the GeoSPaaS Datasetparameters using
    raw_dataset_parameters attribute """

    def get_dataset_parameters(self, raw_attributes):
        """ Get the dataset's parameters """
        if set(['raw_dataset_parameters']).issubset(raw_attributes.keys()):
            standardized_dataset_parameters = list()
            for raw_parameter_name in raw_attributes['raw_dataset_parameters']:
                try:
                    result = utils.get_cf_or_wkv_standard_name(raw_parameter_name)
                except IndexError:
                    LOGGER.warning("%s parameter could not be normalized")
                else:
                    standardized_dataset_parameters.append(result)
            return standardized_dataset_parameters
        else:
            return []
