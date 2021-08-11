"""
This module contains normalizers for different types of metadata. To add a normalizer, create a
class which inherits from BaseMetadataNormalizer. Put it in a new file in the 'normalizers' folder,
and don't forget to write tests!
"""
import os.path

from .base import BaseMetadataNormalizer, MetadataNormalizer
from ..utils import export_subclasses

__all__ = []
export_subclasses(__all__, __package__, os.path.dirname(__file__), MetadataNormalizer)
export_subclasses(__all__, __package__, os.path.dirname(__file__), BaseMetadataNormalizer)
