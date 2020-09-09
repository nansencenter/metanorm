"""Utility functions for metadata normalizing"""

from collections import OrderedDict

import pythesint as pti


UNKNOWN = 'Unknown'


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

    gcmd_object = None
    # Try to search for the object name
    matching_objects = pti_search_method(keyword)
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
    'grib':'91'
    'amip':'sic'
    'description':"X_area_fraction"

    as the result_values.
    """
    try:
        result_values = pti.get_cf_standard_name(keyword)
    except IndexError:
        result_values = pti.get_wkv_variable(keyword)
    return result_values
