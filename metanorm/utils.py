"""Utility functions for metadata normalizing"""

import importlib
import functools
import pkgutil
import sys
from collections import OrderedDict
from datetime import datetime, timedelta

import pythesint as pti
from dateutil.tz import tzutc

from .errors import MetadataNormalizationError

UNKNOWN = 'Unknown'


# Field names commonly used in the 'summary' attribute
SUMMARY_FIELDS = {
    'description': 'Description',
    'processing_level': 'Processing level',
    'product': 'Product',
}


# Key: valid pythesint search keyword
# Value: iterable of aliases
PYTHESINT_KEYWORD_TRANSLATION = {
    # instruments
    'OLCI': ('OL',),
    'SLSTR': ('SL',),
    # platforms
    'METEOSAT-10': ('MSG3',),
    'METEOSAT-11': ('MSG4',),
    'METEOSAT-8': ('MSG1',),
    'METEOSAT-9': ('MSG2',),
    'METOP-B': ('METOP_B',),
    'Sentinel-1A': ('S1A',),
    'Sentinel-1B': ('S1B',),
    'Sentinel-2A': ('S2A',),
    'Sentinel-2B': ('S2B',),
    'Sentinel-3A': ('S3A',),
    'Sentinel-3B': ('S3B',),
    # providers
    'ESA/EO': ('ESA',),
    'OB.DAAC': ('OB_DAAC',)
}


def translate_pythesint_keyword(translation_dict, alias):
    """Get a valid pythesint search keyword from known aliases"""
    for valid_keyword, aliases in translation_dict.items():
        if alias in aliases:
            return valid_keyword
    return alias


def get_gcmd_provider(potential_provider_attributes, additional_keywords=None):
    """
    Get a GCMD provider from a name and/or URL, otherwise return None
    """
    provider = None
    for attribute in potential_provider_attributes:
        provider = gcmd_search('provider', attribute, additional_keywords)
        if provider:
            break
    return provider


def export_subclasses(all, package, package_dir, base_class):
    """Append `base_class` and all of its subclasses declared in
    modules in `package_dir` to `all`. This is meant to be used in
    __init__.py files to make normalizer classes easily importable.
    """
    all.append(base_class.__name__)

    # Import the modules in the package
    for (_, name, _) in pkgutil.iter_modules([package_dir]):
        importlib.import_module('.' + name, package)

    # Make the base_class subclasses available
    # in the 'package' namespace
    for cls in base_class.__subclasses__():
        setattr(sys.modules[package], cls.__name__, cls)
        all.append(cls.__name__)

def raises(exceptions):
    """Decorator for methods which get an attribute from metadata.
    Makes it possible to declare which exception(s) are thrown when the
    raw metadata does not have the expected structure.
    `exceptions` can be an exception class or a tuple of exception
    classes. If any of these exceptions is raised by the method,
    a MetadataNormalizationError with a (hopefully) clear error message
    is raised from this exception.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(self, raw_metadata):
            try:
                return func(self, raw_metadata)
            except exceptions as error:
                raise MetadataNormalizationError(
                    f"{func.__name__} was unable to process the following metadata: {raw_metadata}"
                ) from error
        return wrapper
    return decorator

def get_gcmd_like_provider(name=None, url=None):
    """Generate a GCMD provider-like data structure using a name and a URL"""
    # TODO: find a better way to manage the fallback value
    if not name:
        short_name = long_name = UNKNOWN
    else:
        short_name = name[:50]
        long_name = name[:250]
    provider = OrderedDict([
        ('Bucket_Level0', UNKNOWN),
        ('Bucket_Level1', UNKNOWN),
        ('Bucket_Level2', UNKNOWN),
        ('Bucket_Level3', UNKNOWN),
        ('Short_Name', short_name),
        ('Long_Name', long_name),
        ('Data_Center_URL', url if url else UNKNOWN)
    ])

    return provider


def get_gcmd_platform(platform_name, additional_keywords=None):
    """
    Gets a GCMD platform from a platform name, otherwise generate a GCMD platform-like data
    structure
    """
    gcmd_platform = gcmd_search('platform', platform_name, additional_keywords)

    if not gcmd_platform:  # TODO: find a better way to manage the fallback value
        gcmd_platform = OrderedDict([
            ('Category', UNKNOWN),
            ('Series_Entity', UNKNOWN),
            ('Short_Name', platform_name[:100]),
            ('Long_Name', platform_name[:250])
        ])

    return gcmd_platform


def get_gcmd_instrument(instrument_name, additional_keywords=None):
    """
    Gets a GCMD instrument from an instrument name, otherwise generate a GCMD instrument-like data
    structure.
    """
    gcmd_instrument = gcmd_search('instrument', instrument_name, additional_keywords)

    if not gcmd_instrument:
        gcmd_instrument = OrderedDict([
            ('Category', UNKNOWN),
            ('Class', UNKNOWN),
            ('Type', UNKNOWN),
            ('Subtype', UNKNOWN),
            ('Short_Name', instrument_name[:60]),
            ('Long_Name', instrument_name[:200])
        ])

    return gcmd_instrument


def gcmd_search(vocabulary_name, keyword, additional_keywords=None):
    """
    Search for GCMD objects using the provided vocabulary name and keywords.
    Returns None if nothing was found.
    """
    pti_search_method = getattr(pti, f"search_gcmd_{vocabulary_name}_list")
    pti_get_method = getattr(pti, f"get_gcmd_{vocabulary_name}")

    translated_keyword = translate_pythesint_keyword(PYTHESINT_KEYWORD_TRANSLATION, keyword)

    gcmd_object = None
    # Try to search for the object name
    matching_objects = pti_search_method(translated_keyword)
    matching_objects_length = len(matching_objects)

    if matching_objects_length == 1:
        gcmd_object = matching_objects[0]
    # If more than one is found, look for the additional keywords
    # in the search results to narrow it down
    elif matching_objects_length > 1 and additional_keywords:
        restricted_search = restrict_gcmd_search(matching_objects, additional_keywords)
        restricted_search_length = len(restricted_search)
        if restricted_search_length == 1:
            gcmd_object = restricted_search[0]

    if not gcmd_object:
        # If the additional keywords did not manage to narrow down the search enough, or if no
        # additional keyword was provided, try the strict `get_` method from pythesint
        try:
            gcmd_object = pti_get_method(keyword)
        except IndexError:
            pass

    return gcmd_object


def restrict_gcmd_search(gcmd_objects, keywords):
    """Restricts a list of GCMD objects using a list of keywords to search"""
    restricted_search = gcmd_objects.copy()
    restricted_search_length = len(restricted_search)

    for keyword in keywords:
        keyword_search = [
            gcmd_object for gcmd_object in restricted_search
            if keyword.lower() in str(gcmd_object).lower()
        ]
        keyword_search_length = len(keyword_search)
        if keyword_search_length > 0 and keyword_search_length < restricted_search_length:
            restricted_search = keyword_search
            restricted_search_length = keyword_search_length

    return restricted_search


def wkt_polygon_from_wgs84_limits(north, south, east, west):
    """
    Returns a WKT string representation of a simple boundary box delimited by its northernmost
    latitude, southernmost latitude, easternmost longitude and westernmost longitude
    """
    return f"POLYGON(({west} {south},{east} {south},{east} {north},{west} {north},{west} {south}))"


def get_cf_or_wkv_standard_name(keyword):
    """return the values of a dataset parameter in a standard way from the
    standards that are defined in the pti package based on the keyword that has been passed to it.
    For example, it returns something like:

    'standard_name':'sea_ice_area_fraction'
    'canonical_units':'1'
    'description':"X_area_fraction"

    as the result_values.
    """
    try:
        result_values = pti.get_cf_standard_name(keyword)
    except IndexError:
        result_values = pti.get_wkv_variable(keyword)
    return result_values


YEARMONTH_REGEX = r'(?P<year>\d{4})(?P<month>\d{2})'
YEARMONTHDAY_REGEX = YEARMONTH_REGEX + r'(?P<day>\d{2})'

def create_datetime(year, month=1, day=1, day_of_year=None, hour=0, minute=0, second=0):
    """Returns a datetime object using the provided arguments.
    Possible argument combinations are:
      - year, month, day(, hour, minute, second)
      - year, day_of_year(, hour, minute, second)
    """
    year = int(year)
    hour = int(hour)
    minute = int(minute)
    second = int(second)

    if day_of_year:
        day_of_year = int(day_of_year)
        first_day = datetime(year, 1, 1, hour, minute, second).replace(tzinfo=tzutc())
        return first_day + timedelta(days=day_of_year-1)
    else:
        month = int(month)
        day = int(day)
        return datetime(year, month, day, hour, minute, second).replace(tzinfo=tzutc())


def dict_to_string(dictionary):
    """Returns a string representation of the dictionary argument.
    The following dictionary:
    {'key1': 'value1', 'key2': 'value2'}
    Will be represented as:
    "key1: value1;key2: value2"
    """
    string = ''
    for key, value in dictionary.items():
        string += f"{key}: {value};"
    return string.rstrip(';')
