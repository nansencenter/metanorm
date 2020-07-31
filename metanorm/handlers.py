"""
Handler class for normalizers. It is possible to create a custom handler which uses a custom list
of normalizers: just inherit from MetadataHandler and override the NORMALIZERS class attribute.

This is roughly an implementation of the "chain of responsibility" design pattern:
    - each MetadataNormalizer interprets keywords from a given convention
    - the MetadataHandler instantiates a chain of normalizers through which the attributes of a
      dataset can be processed
"""
import logging

import metanorm.normalizers as normalizers

LOGGER = logging.getLogger(__name__)


class MetadataHandler():
    """Base handler"""
    # This list should be ordered by decreasing priority, and
    # THE LAST NORMALISER MUST INHERIT FROM BaseDefaultMetadataNormalizer
    NORMALIZERS = []

    def __init__(self, output_parameter_names, output_cumulative_parameter_names):
        """Builds a chain of normalizers for the given parameter names"""
        if not isinstance(self.NORMALIZERS[-1]([], [],), normalizers.geospatial_defaults.BaseDefaultMetadataNormalizer):
            raise ValueError(
                "'BaseDefaultMetadataNormalizer' class must be inherited for the last one in the list of normalizers in 'MetadataHandler' class")

        self._chain = last_normalizer = self.NORMALIZERS[0](
            output_parameter_names, output_cumulative_parameter_names)

        for normalizer_class in self.NORMALIZERS[1:]:
            current_normalizer = normalizer_class(
                output_parameter_names, output_cumulative_parameter_names)
            last_normalizer.next = current_normalizer
            last_normalizer = current_normalizer

    def get_parameters(self, raw_attributes):
        """Loop through normalizers to try and get a value for each parameter"""
        return self._chain.normalize(raw_attributes)


class GeospatialMetadataHandler(MetadataHandler):
    """Geospatial metadata handler"""
    NORMALIZERS = [
        normalizers.NETCDFCFMetadataNormalizer,
        normalizers.SentinelSAFEMetadataNormalizer,
        normalizers.SentinelOneIdentifierMetadataNormalizer,
        normalizers.ACDDMetadataNormalizer,
        normalizers.OSISAFMetadataNormalizer,
        normalizers.GeoSpatialWellKnownMetadataNormalizer,
        normalizers.GeoSpatialDefaultMetadataNormalizer,
    ]
