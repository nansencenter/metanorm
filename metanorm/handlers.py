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
    # THE LAST NORMALIZER MUST INHERIT FROM BaseDefaultMetadataNormalizer
    NORMALIZERS = []

    def __init__(self, output_parameter_names=None, output_cumulative_parameter_names=None):
        """Builds a chain of normalizers for the given parameter names"""
        if output_parameter_names is None and output_cumulative_parameter_names is None:
            raise ValueError((
                "Either output_parameter_names or output_cumulative_parameter_names "
                "should be specified"))

        if not isinstance(self.NORMALIZERS[-1]([]), normalizers.base.BaseDefaultMetadataNormalizer):
            raise ValueError(
                "The last normalizer must inherit from 'BaseDefaultMetadataNormalizer'")

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
        normalizers.CPOMaltimetryMetadataNormalizer,
        normalizers.AVISOaltimetryMetadataNormalizer,
        normalizers.URLMetadataNormalizer,
        normalizers.CMEMSInSituTACMetadataNormalizer,
        normalizers.NETCDFCFMetadataNormalizer,
        normalizers.SentinelSAFEMetadataNormalizer,
        normalizers.SentinelOneIdentifierMetadataNormalizer,
        normalizers.CreodiasEOFinderMetadataNormalizer,
        normalizers.EarthdataCMRMetadataNormalizer,
        normalizers.ACDDMetadataNormalizer,
        normalizers.OSISAFMetadataNormalizer,
        normalizers.GeoSpatialWellKnownMetadataNormalizer,
        normalizers.GeoSpatialDefaultMetadataNormalizer,
    ]
