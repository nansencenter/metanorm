"""
This module contains utilities to convert dataset attributes into parameters which are compatible
with geospaas.catalog Datasets.
It is roughly an implementation of the "chain of responsibility" design pattern:
    - each MetadataNormalizer interprets keywords from a given convention
    - the MetadataHandler instantiates a chain of normalizers through which the attributes of a
      dataset can be processed
"""
import logging

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)
