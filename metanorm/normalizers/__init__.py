"""This package contains normalizers for different types of metadata.
To add a normalizer, create a class which inherits from
MetadataNormalizer. Put it in a new module in the 'normalizers' folder,
and don't forget to write tests!
"""
import os.path

from .base import MetadataNormalizer
from ..utils import export_subclasses

__all__ = []
export_subclasses(__all__, __package__, os.path.dirname(__file__), MetadataNormalizer)
