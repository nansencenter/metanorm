"""
This module contains normalizers for different types of metadata. To add a normalizer, create a
class which inherits from BaseMetadataNormalizer. Put it in a new file in the 'normalizers' folder,
and don't forget to write tests!
"""
import importlib
import os.path
import pkgutil
import sys

from .base import BaseMetadataNormalizer, BaseDefaultMetadataNormalizer

__all__ = ['BaseMetadataNormalizer', 'BaseDefaultMetadataNormalizer']
PACKAGE_DIR = os.path.dirname(__file__)

# Import the modules in the 'normalizers' package
for (module_loader, name, is_package) in pkgutil.iter_modules([PACKAGE_DIR]):
    importlib.import_module('.' + name, __package__)

# Make the BaseMetadataNormalizer subclasses available in the 'normalizers' namespace
for cls in BaseMetadataNormalizer.__subclasses__() + BaseDefaultMetadataNormalizer.__subclasses__():
    setattr(sys.modules[__package__], cls.__name__, cls)
    __all__.append(cls.__name__)
