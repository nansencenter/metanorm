"""Module containing the base class for GeoSPaaS normalizers"""
import pythesint as pti

import metanorm.utils as utils
from metanorm.normalizers.base import MetadataNormalizer


class GeoSPaaSMetadataNormalizer(MetadataNormalizer):
    """Base class for GeoSPaaS normalizers. Defaults are defined here.
    """

    def get_entry_title(self, raw_metadata):
        """Get the entry title from the raw metadata"""
        raise NotImplementedError

    def get_entry_id(self, raw_metadata):
        """Get the entry ID from the raw metadata"""

    def get_summary(self, raw_metadata):
        """Get the summary from the raw metadata"""
        return utils.UNKNOWN

    def get_time_coverage_start(self, raw_metadata):
        """Get the start of the time coverage from the raw metadata"""
        raise NotImplementedError

    def get_time_coverage_end(self, raw_metadata):
        """Get the end of the time coverage from the raw metadata"""
        raise NotImplementedError

    def get_platform(self, raw_metadata):
        """Get the platform from the raw metadata"""
        raise NotImplementedError

    def get_instrument(self, raw_metadata):
        """Get the instrument from the raw metadata"""
        raise NotImplementedError

    def get_location_geometry(self, raw_metadata):
        """Get the location geometry (in WKT or GeoJSON) from the raw
        metadata
        """
        raise NotImplementedError

    def get_provider(self, raw_metadata):
        """Get the provider from the raw metadata"""
        raise NotImplementedError

    @utils.raises(IndexError)
    def get_iso_topic_category(self, raw_metadata):
        """Get the ISO topic category from the raw metadata"""
        return pti.get_iso19115_topic_category('Oceans')

    @utils.raises(IndexError)
    def get_gcmd_location(self, raw_metadata):
        """Get the GCMD location from the raw metadata"""
        return pti.get_gcmd_location('SEA SURFACE')

    def get_dataset_parameters(self, raw_metadata):
        """Get the dataset parameters, if any, from the raw metadata"""
        return []

    def normalize(self, raw_metadata):
        return {
            'entry_title': self.get_entry_title(raw_metadata),
            'entry_id': self.get_entry_id(raw_metadata),
            'summary': self.get_summary(raw_metadata),
            'time_coverage_start': self.get_time_coverage_start(raw_metadata),
            'time_coverage_end': self.get_time_coverage_end(raw_metadata),
            'platform': self.get_platform(raw_metadata),
            'instrument': self.get_instrument(raw_metadata),
            'location_geometry': self.get_location_geometry(raw_metadata),
            'provider': self.get_provider(raw_metadata),
            'iso_topic_category': self.get_iso_topic_category(raw_metadata),
            'gcmd_location': self.get_gcmd_location(raw_metadata),
            'dataset_parameters': self.get_dataset_parameters(raw_metadata)
        }
