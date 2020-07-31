"""Normalizer for the CF Standard convention"""

import logging

import pythesint as pti

from .base import BaseMetadataNormalizer

LOGGER = logging.getLogger(__name__)
LOGGER.addHandler(logging.NullHandler())


class NETCDFCFMetadataNormalizer(BaseMetadataNormalizer):
    """Generate the GeoSPaaS Datasetparameters using raw_dataset_parameters attribute"""

    def get_dataset_parameters(self, raw_attributes):
        """ Get the dataset's parameters """
        if set(['raw_dataset_parameters']).issubset(raw_attributes.keys()):
            standardized_dataset_parameters = list()
            for raw_parameter_name in raw_attributes['raw_dataset_parameters']:
                if pti.search_cf_standard_name_list(raw_parameter_name):
                    standardized_dataset_parameters.append(
                        pti.search_cf_standard_name_list(raw_parameter_name)[0])
            return standardized_dataset_parameters
