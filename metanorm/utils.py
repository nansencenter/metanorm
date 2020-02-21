"""Utility functions for metadata normalizing"""

from collections import OrderedDict

from django.contrib.gis.geos import GEOSGeometry

import pythesint as pti


UNKNOWN = 'Unknown'


def get_gcmd_provider(potential_provider_attributes):
    """
    Gets a GCMD provider from a name and/or URL, otherwise generate a GCMD provider-like data
    structure
    """
    provider = None
    for attribute in potential_provider_attributes:
        try:
            provider = pti.get_gcmd_provider(attribute)
        except IndexError:
            pass
    return provider

def get_gcmd_like_provider(name=None, url=None):
    """Generate a GCMD provider-like data structure using a name and a URL"""
    # TODO: find a better way to manage the fallback value
    if not name:
        short_name = long_name = UNKNOWN
    else:
        if len(name) < 50:
            short_name = long_name = name
        elif len(name) > 50:
            short_name = name[:50]
            long_name = name if len(name) < 250 else name[:250]
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

def get_gcmd_platform(platform_name):
    """
    Gets a GCMD platform from a platform name, otherwise generate a GCMD platform-like data
    structure
    """
    try:
        gcmd_platform = pti.get_gcmd_platform(platform_name)
    except IndexError:  # TODO: find a better way to manage the fallback value
        gcmd_platform = OrderedDict([
            ('Category', UNKNOWN),
            ('Series_Entity', UNKNOWN),
            ('Short_Name', platform_name if len(platform_name) < 100 else platform_name[:100]),
            ('Long_Name', platform_name if len(platform_name) < 250 else platform_name[:250])
        ])

    return gcmd_platform

def get_gcmd_instrument(instrument_name):
    """
    Gets a GCMD platform from a instrument name, otherwise generate a GCMD instrument-like data
    structure
    """
    try:
        gcmd_instrument = pti.get_gcmd_instrument(instrument_name)
    except IndexError:  # TODO: find a better way to manage the fallback value
        gcmd_instrument = OrderedDict([
            ('Category', UNKNOWN),
            ('Class', UNKNOWN),
            ('Type', UNKNOWN),
            ('Subtype', UNKNOWN),
            ('Short_Name', instrument_name if len(instrument_name) < 60 else instrument_name[:60]),
            ('Long_Name', instrument_name if len(instrument_name) < 200 else instrument_name[:200])
        ])

    return gcmd_instrument


def wkt_polygon_from_wgs84_limits(north, south, east, west):
    """
    Returns a WKT string representation of a simple boundary box delimited by its northernmost
    latitude, southernmost latitude, easternmost longitude and westernmost longitude
    """
    return f"POLYGON(({west} {south},{east} {south},{east} {north},{west} {north},{west} {south}))"

def geometry_from_wkt_string(wkt_string, srid=4326):
    """
    Generates a GEOSGeometry object form a WKT string. The default coordinates reference system is
    EPSG:4326, i.e. WGS 84
    """
    return GEOSGeometry(wkt_string, srid=srid)
