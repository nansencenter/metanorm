"""This module contains handler classes which control how normalizers
are used
"""
import logging

import metanorm.normalizers as normalizers
import metanorm.utils as utils
from .errors import NoNormalizerFound

logger = logging.getLogger(__name__)


class MetadataHandler():
    """Handler which builds a list of of subclasses of a base
    normalizer class
    """

    def __init__(self, base_class=None):
        """Builds a list of normalizers, instantiating one per subclass
        of `base_class`
        """
        if base_class is None:
            base_class = normalizers.MetadataNormalizer

        self.normalizers = [
            normalizer_class()
            for normalizer_class in utils.get_all_subclasses(base_class)
        ]

    def get_parameters(self, raw_metadata):
        """Loop through normalizers and uses the first one whose
        `check()` method returns true to normalize the raw metadata
        """
        for normalizer in self.normalizers:
            if normalizer.check(raw_metadata):
                logger.debug("%s will be used", normalizer.__class__.__name__)
                return normalizer.normalize(raw_metadata)
        raise NoNormalizerFound(f"No matching normalizer was found in {self.normalizers}")
