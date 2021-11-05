"""Base normalizer. Other normalizers should inherit from
MetadataNormalizer
"""

class MetadataNormalizer():
    """Base class for all metadata normalizers"""

    def check(self, raw_metadata):
        """Returns a boolean indicating whether the normalizer is
        capable of handling the raw metadata.
        Only leaf classes should return True
        """
        return False

    def normalize(self, raw_metadata):
        """Normalizes the raw metadata. Should return a dictionary"""
        raise NotImplementedError
