"""This package contains normalizers which extract the metadata
necessary to instantiate GeoSPaaS Datasets.
All normalizers in this package should inherit from
GeoSPaaSMetadataNormalizer.
"""
import os.path

from .base import GeoSPaaSMetadataNormalizer
from ...utils import export_subclasses

__all__ = []
export_subclasses(__all__, __package__, os.path.dirname(__file__), GeoSPaaSMetadataNormalizer)
