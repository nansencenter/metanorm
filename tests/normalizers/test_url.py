"""Tests for the URL normalizer """
import unittest
from collections import OrderedDict
from datetime import datetime

from dateutil.tz import tzutc
import metanorm.normalizers as normalizers


class URLMetadataNormalizerTestCase(unittest.TestCase):
    """Tests for the URL normalizer"""
    @classmethod
    def setUpClass(cls):
        cls.normalizer = normalizers.URLMetadataNormalizer([], [])

    DATASET_PARAMETERS = {
        'atmosphere_mass_content_of_cloud_liquid_water': OrderedDict([
            ('standard_name', 'atmosphere_mass_content_of_cloud_liquid_water'),
            ('canonical_units', 'kg m-2'),
            ('definition',
             '"Content" indicates a quantity per unit area. The "atmosphere content"'
             ' of a quantity refers to the vertical integral from the surface to the top of the '
             'atmosphere. For the content between specified levels in the atmosphere, standard '
             'names including content_of_atmosphere_layer are used. "Cloud liquid water" refers to '
             'the liquid phase of cloud water. A diameter of 0.2 mm has been suggested as an upper '
             'limit to the size of drops that shall be regarded as cloud drops; larger drops fall '
             'rapidly enough so that only very strong updrafts can sustain them. Any such division '
             'is somewhat arbitrary, and active cumulus clouds sometimes contain cloud drops much '
             'larger than this. '
             'Reference: AMS Glossary http://glossary.ametsoc.org/wiki/Cloud_drop.')]),
        'atmosphere_mass_content_of_water_vapor': OrderedDict([
            ('standard_name', 'atmosphere_mass_content_of_water_vapor'),
            ('canonical_units', 'kg m-2'),
            ('definition',
             '"Content" indicates a quantity per unit area. The "atmosphere content"'
             ' of a quantity refers to the vertical integral from the surface to the top of the '
             'atmosphere. For the content between specified levels in the atmosphere, standard '
             'names including content_of_atmosphere_layer are used. Atmosphere water vapor content '
             'is sometimes referred to as "precipitable water", although this term does not imply '
             'the water could all be precipitated.')]),
        'barotropic_eastward_sea_water_velocity': OrderedDict([
            ('standard_name', 'barotropic_eastward_sea_water_velocity'),
            ('canonical_units', 'm s-1'),
            ('definition',
             'A velocity is a vector quantity. "Eastward" indicates a vector component which is '
             'positive when directed eastward (negative westward).')]),
        'barotropic_northward_sea_water_velocity': OrderedDict([
            ('standard_name', 'barotropic_northward_sea_water_velocity'),
            ('canonical_units', 'm s-1'),
            ('definition',
             'A velocity is a vector quantity. "Northward" indicates a vector component which is '
             'positive when directed northward (negative southward).')]),
        'cell_thickness': OrderedDict([
            ('standard_name', 'cell_thickness'),
            ('canonical_units', 'm'),
            ('definition',
             '"Thickness" means the vertical extent of a layer. '
             '"Cell" refers to a model grid-cell.')]),
        'eastward_sea_ice_velocity': OrderedDict([
            ('standard_name', 'eastward_sea_ice_velocity'),
            ('canonical_units', 'm s-1'),
            ('definition',
             'A velocity is a vector quantity. "Eastward" indicates a vector component which is '
             'positive when directed eastward (negative westward). Sea ice velocity is defined as a'
             ' two-dimensional vector, with no vertical component. "Sea ice" means all ice floating'
             ' in the sea which has formed from freezing sea water, rather than by other processes'
             ' such as calving of land ice to form icebergs.')]),
        'eastward_sea_water_velocity': OrderedDict([
            ('standard_name', 'eastward_sea_water_velocity'),
            ('canonical_units', 'm s-1'),
            ('definition',
             'A velocity is a vector quantity. "Eastward" indicates a vector component which is '
             'positive when directed eastward (negative westward).')]),
        'ice_coverage': OrderedDict([
            ('standard_name', 'ice_coverage'),
            ('long_name', 'Ice coverage'),
            ('short_name', 'ice_coverage'),
            ('units', 'na'),
            ('minmax', '0 1'),
            ('colormap', 'jet')]),
        'ice_temperature': OrderedDict([
            ('standard_name', 'ice_temperature'),
            ('long_name', 'Ice temperature'),
            ('short_name', 'ice_temperature'),
            ('units', 'celsius'),
            ('minmax', '-100 0'),
            ('colormap', 'jet')]),
        'ice_thickness': OrderedDict([
            ('standard_name', 'ice_thickness'),
            ('long_name', 'Ice thickness'),
            ('short_name', 'ice_thickness'),
            ('units', 'm'),
            ('minmax', '0 100'),
            ('colormap', 'jet')]),
        'ice_uvelocity': OrderedDict([
            ('standard_name', 'ice_uvelocity'),
            ('long_name', 'Eastward sea ice velocity'),
            ('short_name', 'ice_uvelocity'),
            ('units', 'm s-1'),
            ('minmax', '-10 10'),
            ('colormap', 'jet')]),
        'icd_vvelocity': OrderedDict([
            ('standard_name', 'icd_vvelocity'),
            ('long_name', 'Northward sea ice velocity'),
            ('short_name', 'ice_vvelocity'),
            ('units', 'm s-1'),
            ('minmax', '-10 10'),
            ('colormap', 'jet')]),
        'model_level_number_at_sea_floor': OrderedDict([
            ('standard_name', 'model_level_number_at_sea_floor'),
            ('canonical_units', '1'),
            ('definition',
             'The quantity with standard name model_level_number_at_sea_floor is the depth of the '
             'ocean expressed in model levels. This could be a non-integer value because some ocean'
             ' models use partial cells close to the sea floor.  For example, if this field were '
             '23.4 at some location, it would mean the water column at that point comprised 23 full'
             ' model levels plus 40% occupancy of the lowest (24th) gridcell.')]),
        'northward_sea_ice_velocity': OrderedDict([
            ('standard_name', 'northward_sea_ice_velocity'),
            ('canonical_units', 'm s-1'),
            ('definition',
             'A velocity is a vector quantity. "Northward" indicates a vector '
             'component which is positive when directed northward (negative southward). Sea ice '
             'velocity is defined as a two-dimensional vector, with no vertical component. '
             '"Sea ice" means all ice floating in the sea which has formed from freezing sea water,'
             ' rather than by other processes such as calving of land ice to form icebergs.')]),
        'northward_sea_water_velocity': OrderedDict([
            ('standard_name', 'northward_sea_water_velocity'),
            ('canonical_units', 'm s-1'),
            ('definition',
             'A velocity is a vector quantity. "Northward" indicates a vector component which is '
             'positive when directed northward (negative southward).')]),
        'ocean_mixed_layer_thickness_defined_by_sigma_theta': OrderedDict([
            ('standard_name', 'ocean_mixed_layer_thickness_defined_by_sigma_theta'),
            ('canonical_units', 'm'),
            ('definition',
             'The ocean mixed layer is the upper part of the ocean, regarded as being well-mixed.  '
             'The base of the mixed layer defined by "temperature", "sigma", "sigma_theta", '
             '"sigma_t" or vertical diffusivity is the level at which the quantity indicated '
             'differs from its surface value by a certain amount. A coordinate variable or scalar '
             'coordinate variable with standard name sea_water_sigma_theta_difference can be used '
             'to specify the sigma_theta criterion that determines the layer thickness. Sigma-theta'
             ' of sea water is the potential density (i.e. the density when moved adiabatically to '
             'a reference pressure) of water having the same temperature and salinity, minus 1000 '
             'kg m-3. "Thickness" means the vertical extent of a layer.')]),
        'ocean_mixed_layer_thickness': OrderedDict([
            ('standard_name', 'ocean_mixed_layer_thickness'),
            ('canonical_units', 'm'),
            ('definition',
             'The ocean mixed layer is the upper part of the ocean, regarded as being well-mixed. '
             'Various criteria are used to define the mixed layer; this can be specified by using a'
             ' standard name of ocean_mixed_layer_defined_by_X. "Thickness" means the vertical '
             'extent of a layer.')]),
        'rainfall_rate': OrderedDict([
            ('standard_name', 'rainfall_rate'),
            ('canonical_units', 'm s-1'),
            ('definition',
             'The lifting condensation level is the height at which the relative humidity of an air'
             ' parcel cooled by dry adiabatic lifting would reach 100%. A coordinate variable of '
             'original_air_pressure_of_lifted_parcel should be specified to indicate the starting '
             'height of the lifted parcel.')]),
        'sea_floor_depth_below_geoid': OrderedDict([
            ('standard_name', 'sea_floor_depth_below_geoid'),
            ('canonical_units', 'm'),
            ('definition',
             '"Depth_below_X" means the vertical distance below the named surface X. The geoid is a'
             ' surface of constant geopotential with which mean sea level would coincide if the '
             'ocean were at rest. (The volume enclosed between the geoid and the sea floor equals '
             'the mean volume of water in the ocean). In an ocean GCM the geoid is the surface of '
             'zero depth, or the rigid lid if the model uses that approximation. To specify which '
             'geoid or geopotential datum is being used as a reference level, a grid_mapping '
             'variable should be attached to the data variable as described in Chapter 5.6 of the '
             'CF Convention.')]),
        'sea_ice_area_fraction': OrderedDict([
            ('standard_name', 'sea_ice_area_fraction'),
            ('canonical_units', '1'),
            ('definition',
             '"Area fraction" is the fraction of a grid cell\'s horizontal area that has some '
             'characteristic of interest. It is evaluated as the area of interest divided by the '
             'grid cell area. It may be expressed as a fraction, a percentage, or any other '
             'dimensionless representation of a fraction. Sea ice area fraction is area of the sea '
             'surface occupied by sea ice. It is also called "sea ice concentration". "Sea ice" '
             'means all ice floating in the sea which has formed from freezing sea water, rather '
             'than by other processes such as calving of land ice to form icebergs.')]),
        'sea_ice_thickness': OrderedDict([
            ('standard_name', 'sea_ice_thickness'),
            ('canonical_units', 'm'),
            ('definition',
             '"Thickness" means the vertical extent of a layer. "Sea ice" means all ice floating in'
             ' the sea which has formed from freezing sea water, rather than by other processes '
             'such as calving of land ice to form icebergs.')]),
        'sea_surface_height_above_geoid': OrderedDict([
            ('standard_name', 'sea_surface_height_above_geoid'),
            ('canonical_units', 'm'),
            ('definition', '"Height_above_X" means the vertical distance above the named surface X.'
            ' "Sea surface height" is a time-varying quantity. The geoid is a surface of constant '
            'geopotential with which mean sea level would coincide if the ocean were at rest. (The '
            'volume enclosed between the geoid and the sea floor equals the mean volume of water in'
            ' the ocean). In an ocean GCM the geoid is the surface of zero depth, or the rigid lid '
            'if the model uses that approximation. To specify which geoid or geopotential datum is '
            'being used as a reference level, a grid_mapping variable should be attached to the '
            'data variable as described in Chapter 5.6 of the CF Convention. By definition of the '
            'geoid, the global average of the time-mean sea surface height (i.e. mean sea level) '
            'above the geoid must be zero. The standard name for the height of the sea surface '
            'above mean sea level is sea_surface_height_above_mean_sea_level. The standard name for'
            ' the height of the sea surface above the reference ellipsoid is '
            'sea_surface_height_above_reference_ellipsoid.')]),
        'sea_surface_height_above_sea_level': OrderedDict([
            ('standard_name', 'sea_surface_height_above_sea_level'),
            ('long_name', 'Sea Surface Anomaly'),
            ('short_name', 'SSA'),
            ('units', 'm'),
            ('minmax', '-100 100'),
            ('colormap', 'jet')]),
        'sea_surface_temperature': OrderedDict([
            ('standard_name', 'sea_surface_temperature'),
            ('canonical_units', 'K'),
            ('definition',
             'Sea surface temperature is usually abbreviated as "SST". It is the temperature of sea'
             ' water near the surface (including the part under sea-ice, if any). More specific '
             'terms, namely sea_surface_skin_temperature, sea_surface_subskin_temperature, and '
             'surface_temperature are available for the skin, subskin, and interface temperature. '
             'respectively. For the temperature of sea water at a particular depth or layer, a data'
             ' variable of sea_water_temperature with a vertical coordinate axis should be '
             'used.')]),
        'sea_surface_salinity': OrderedDict([('standard_name', 'sea_surface_salinity'),
             ('canonical_units', '1e-3'),
             ('definition',
              'Sea surface salinity is the salt content of sea water close to the sea surface, '
              'often on the Practical Salinity Scale of 1978. However, the unqualified term '
              '\'salinity\' is generic and does not necessarily imply any particular method of '
              'calculation. The units of salinity are dimensionless and the units attribute should '
              'normally be given as 1e-3 or 0.001 i.e. parts per thousand. Sea surface salinity is '
              'often abbreviated as "SSS". For the salinity of sea water at a particular depth or '
              'layer, a data variable of "sea_water_salinity" or one of the more precisely defined '
              'salinities should be used with a vertical coordinate axis. There are standard names '
              'for the precisely defined salinity quantities: sea_water_knudsen_salinity, S_K (used'
              ' for salinity observations between 1901 and 1966), sea_water_cox_salinity, S_C (used'
              ' for salinity observations between 1967 and 1977), sea_water_practical_salinity, S_P'
              ' (used for salinity observations from 1978 to the present day), '
              'sea_water_absolute_salinity, S_A, sea_water_preformed_salinity, S_*, and '
              'sea_water_reference_salinity. Practical Salinity is reported on the Practical '
              'Salinity Scale of 1978 (PSS-78), and is usually based on the electrical '
              'conductivity of sea water in observations since the 1960s. Conversion of data '
              'between the observed scales follows: S_P = (S_K - 0.03) * (1.80655 / 1.805) and '
              'S_P = S_C, however the accuracy of the latter is dependent on whether chlorinity or '
              'conductivity was used to determine the S_C value, with this inconsistency driving '
              'the development of PSS-78. The more precise standard names should be used where '
              'appropriate for both modelled and observed salinities. In particular, the use of '
              'sea_water_salinity to describe salinity observations made from 1978 onwards is now '
              'deprecated in favor of the term sea_water_practical_salinity which is the salinity '
              'quantity stored by national data centers for post-1978 observations. The only '
              'exception to this is where the observed salinities are definitely known not to be '
              'recorded on the Practical Salinity Scale. The unit "parts per thousand" was used for'
              ' sea_water_knudsen_salinity and sea_water_cox_salinity.')]),
        'sea_water_potential_density': OrderedDict([
            ('standard_name', 'sea_water_potential_density'),
            ('canonical_units', 'kg m-3'),
            ('definition',
             'Sea water potential density is the density a parcel of sea water would have if moved '
             'adiabatically to a reference pressure, by default assumed to be sea level pressure. '
             'To specify the reference pressure to which the quantity applies, provide a scalar '
             'coordinate variable with standard name reference_pressure. The density of a substance'
             ' is its mass per unit volume. For sea water potential density, if 1000 kg m-3 is '
             'subtracted, the standard name sea_water_sigma_theta should be chosen instead.')]),
        'sea_water_potential_temperature': OrderedDict([
            ('standard_name', 'sea_water_potential_temperature'),
            ('canonical_units', 'K'),
            ('definition',
             'Sea water potential temperature is the temperature a parcel of sea water would have '
             'if moved adiabatically to sea level pressure.')]),
        'sea_water_potential_temperature_at_sea_floor': OrderedDict([
            ('standard_name', 'sea_water_potential_temperature_at_sea_floor'),
            ('canonical_units', 'K'),
            ('definition',
             'Potential temperature is the temperature a parcel of air or sea water would have if '
             'moved adiabatically to sea level pressure. The potential temperature at the sea floor'
             ' is that adjacent to the ocean bottom, which would be the deepest grid cell in an '
             'ocean model and within the benthic boundary layer for measurements.')]),
        'sea_water_salinity': OrderedDict([
            ('standard_name', 'sea_water_salinity'),
            ('canonical_units', '1e-3'),
            ('definition',
             'Sea water salinity is the salt content of sea water, often on the Practical Salinity'
             ' Scale of 1978. However, the unqualified term \'salinity\' is generic and does not '
             'necessarily imply any particular method of calculation. The units of salinity are '
             'dimensionless and the units attribute should normally be given as 1e-3 or 0.001 i.e. '
             'parts per thousand. There are standard names for the more precisely defined salinity '
             'quantities: sea_water_knudsen_salinity, S_K (used for salinity observations between '
             '1901 and 1966),  sea_water_cox_salinity, S_C (used for salinity observations between '
             '1967 and 1977), sea_water_practical_salinity, S_P (used for salinity observations '
             'from 1978 to the present day), sea_water_absolute_salinity, S_A, '
             'sea_water_preformed_salinity, S_*, and sea_water_reference_salinity. Practical '
             'Salinity is reported on the Practical Salinity Scale of 1978 (PSS-78), and is usually'
             ' based on the electrical conductivity of sea water in observations since the 1960s. '
             'Conversion of data between the observed scales follows: '
             'S_P = (S_K - 0.03) * (1.80655 / 1.805) and S_P = S_C, however the accuracy of the '
             'latter is dependent on whether chlorinity or conductivity was used to determine the '
             'S_C value, with this inconsistency driving the development of PSS-78. The more '
             'precise standard names should be used where appropriate for both modelled and '
             'observed salinities. In particular, the use of sea_water_salinity to describe '
             'salinity observations made from 1978 onwards is now deprecated in favor of the term '
             'sea_water_practical_salinity which is the salinity quantity stored by national data '
             'centers for post-1978 observations. The only exception to this is where the observed '
             'salinities are definitely known not to be recorded on the Practical Salinity Scale. '
             'The unit "parts per thousand" was used for sea_water_knudsen_salinity and '
             'sea_water_cox_salinity.')]),
        'sea_water_salinity_at_bottom': OrderedDict([
            ('standard_name', 'sea_water_salinity_at_bottom'),
            ('long_name', 'Sea water salinity at bottom'),
            ('short_name', 'salinity_bottom'),
            ('units', 'psu'),
            ('minmax', '0 50'),
            ('colormap', 'jet')]),
        'sea_water_temperature': OrderedDict([
            ('standard_name', 'sea_water_temperature'),
            ('canonical_units', 'K'),
            ('definition',
             'Sea water temperature is the in situ temperature of the sea water. To specify the '
             'depth at which the temperature applies use a vertical coordinate variable or scalar '
             'coordinate variable. There are standard names for sea_surface_temperature, '
             'sea_surface_skin_temperature, sea_surface_subskin_temperature and '
             'sea_surface_foundation_temperature which can be used to describe data located at the '
             'specified surfaces. For observed data, depending on the period during which the '
             'observation was made, the measured in situ temperature was recorded against standard '
             '"scales". These historical scales include the International Practical Temperature '
             'Scale of 1948 (IPTS-48; 1948-1967), the International Practical Temperature Scale of '
             '1968 (IPTS-68, Barber, 1969; 1968-1989) and the International Temperature Scale of '
             '1990 (ITS-90, Saunders 1990; 1990 onwards). Conversion of data between these scales '
             'follows t68 = t48 - (4.4 x 10e-6) * t48(100 - t - 48); t90 = 0.99976 * t68. '
             'Observations made prior to 1948 (IPTS-48) have not been documented and therefore a '
             'conversion cannot be certain. Differences between t90 and t68 can be up to 0.01 at '
             'temperatures of 40 C and above; differences of 0.002-0.007 occur across the standard '
             'range of ocean temperatures (-10 - 30 C). The International Equation of State of '
             'Seawater 1980 (EOS-80, UNESCO, 1981) and the Practical Salinity Scale (PSS-78) were '
             'both based on IPTS-68, while the Thermodynamic Equation of Seawater 2010 (TEOS-10) is'
             ' based on ITS-90. References: Barber, 1969, doi: 10.1088/0026-1394/5/2/001; UNESCO, '
             '1981; Saunders, 1990, WOCE Newsletter, 10, September 1990.')]),
        'sea_water_temperature_at_bottom': OrderedDict([
            ('standard_name', 'sea_water_temperature_at_bottom'),
            ('long_name', 'Sea water temperature at bottom'),
            ('short_name', 'water_temp_bottom'),
            ('units', 'celsius'),
            ('minmax', '-2 40'),
            ('colormap', 'jet')]),
        'surface_geostrophic_eastward_sea_water_velocity': OrderedDict([
            ('standard_name', 'surface_geostrophic_eastward_sea_water_velocity'),
            ('canonical_units', 'm s-1'),
            ('definition',
             'The surface called "surface" means the lower boundary of the atmosphere. A velocity '
             'is a vector quantity. "Eastward" indicates a vector component which is positive when '
             'directed eastward (negative westward). "Geostrophic" indicates that geostrophic '
             'balance is assumed, i.e. that the pressure gradient force and the Coriolis force are '
             'balanced and the large scale fluid flow is parallel to the isobars. The quantity with'
             ' standard name surface_geostrophic_eastward_sea_water_velocity is the sum of a '
             'variable part, '
             'surface_geostrophic_eastward_sea_water_velocity_assuming_mean_sea_level_for_geoid, '
             'and a constant part due to the stationary component of ocean circulation.')]),
        'surface_geostrophic_eastward_sea_water_velocity_assuming_mean_sea_level_for_geoid': (
            OrderedDict([
            ('standard_name',
             'surface_geostrophic_eastward_sea_water_velocity_assuming_mean_sea_level_for_geoid'),
            ('canonical_units', 'm s-1'),
            ('definition',
             'The surface called "surface" means the lower boundary of the atmosphere. A velocity '
             'is a vector quantity. "Eastward" indicates a vector component which is positive when '
             'directed eastward (negative westward). "Geostrophic" indicates that geostrophic '
             'balance is assumed, i.e. that the pressure gradient force and the Coriolis force are '
             'balanced and the large scale fluid flow is parallel to the isobars. "Mean sea level" '
             'means the time mean of sea surface elevation at a given location over an arbitrary '
             'period sufficient to eliminate the tidal signals. The geoid is a surface of constant '
             'geopotential with which mean sea level would coincide if the ocean were at rest. (The'
             ' volume enclosed between the geoid and the sea floor equals the mean volume of water '
             'in the ocean.) In an ocean GCM the geoid is the surface of zero depth, or the rigid '
             'lid if the model uses that approximation. The quantity with standard name '
             'surface_geostrophic_eastward_sea_water_velocity_assuming_mean_sea_level_for_geoid is '
             'the variable part of surface_geostrophic_eastward_sea_water_velocity. The assumption '
             'that sea level is equal to the geoid means that the stationary component of ocean '
             'circulation is equal to zero.')])),
        'surface_geostrophic_northward_sea_water_velocity': OrderedDict([
            ('standard_name', 'surface_geostrophic_northward_sea_water_velocity'),
            ('canonical_units', 'm s-1'),
            ('definition',
             'The surface called "surface" means the lower boundary of the atmosphere. A velocity '
             'is a vector quantity. "Northward" indicates a vector component which is positive when'
             ' directed northward (negative southward). "Geostrophic" indicates that geostrophic '
             'balance is assumed, i.e. that the pressure gradient force and the Coriolis force are '
             'balanced and the large scale fluid flow is parallel to the isobars. The quantity with'
             ' standard name surface_geostrophic_northward_sea_water_velocity is the sum of a '
             'variable part, '
             'surface_geostrophic_northward_sea_water_velocity_assuming_mean_sea_level_for_geoid, '
             'and a constant part due to the stationary component of ocean circulation.')]),
        'surface_geostrophic_northward_sea_water_velocity_assuming_mean_sea_level_for_geoid': (
            OrderedDict([
            ('standard_name',
             'surface_geostrophic_northward_sea_water_velocity_assuming_mean_sea_level_for_geoid'),
            ('canonical_units', 'm s-1'),
            ('definition',
             'The surface called "surface" means the lower boundary of the atmosphere. A velocity '
             'is a vector quantity. "Northward" indicates a vector component which is positive when'
             ' directed northward (negative southward). "Geostrophic" indicates that geostrophic '
             'balance is assumed, i.e. that the pressure gradient force and the Coriolis force are '
             'balanced and the large scale fluid flow is parallel to the isobars. "Mean sea level" '
             'means the time mean of sea surface elevation at a given location over an arbitrary '
             'period sufficient to eliminate the tidal signals. The geoid is a surface of constant '
             'geopotential with which mean sea level would coincide if the ocean were at rest. (The'
             ' volume enclosed between the geoid and the sea floor equals the mean volume of water '
             'in the ocean.) In an ocean GCM the geoid is the surface of zero depth, or the rigid '
             'lid if the model uses that approximation. The quantity with standard name '
             'surface_geostrophic_northward_sea_water_velocity_assuming_mean_sea_level_for_geoid is'
             ' the variable part of surface_geostrophic_northward_sea_water_velocity. The '
             'assumption that sea level is equal to the geoid means that the stationary component '
             'of ocean circulation is equal to zero.')])),
        'wind_speed': OrderedDict([
            ('standard_name', 'wind_speed'),
            ('canonical_units', 'm s-1'),
            ('definition',
             'Speed is the magnitude of velocity. Wind is defined as a two-dimensional (horizontal)'
             ' air velocity vector, with no vertical component. (Vertical motion in the atmosphere '
             'has the standard name upward_air_velocity.) The wind speed is the magnitude of the '
             'wind velocity.')]),
        'surface_boundary_layer_thickness': OrderedDict([
            ('standard_name', 'surface_boundary_layer_thickness'),
            ('long_name', 'Surface boundary layer thickness'),
            ('short_name', 'surface_boundary_layer_thickness'),
            ('units', 'm'),
            ('minmax', '0 5000'),
            ('colormap', 'jet')])
    }

    def test_time_coverage_start_remss_month_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_201406v8.2.gz'}),
            datetime(year=2014, month=6, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_remss_single_day_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140604v8.2.gz'}),
            datetime(year=2014, month=6, day=4, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_remss_week_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/weeks/f35_20140614v8.2.gz'}),
            datetime(year=2014, month=6, day=8, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_remss_3d3_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140630v8.2_d3d.gz'}),
            datetime(year=2014, month=6, day=28, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_ceda(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}),
            datetime(year=1982, month=12, day=31, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_jaxa(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_20120702_01D_EQOD_L3SGSSTLB3300300.h5'}),
            datetime(year=2012, month=7, day=2, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_jaxa_month_file(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2013/07/GW1AM2_20130700_01M_EQMA_L3SGSSTLB3300300.h5'}),
            datetime(year=2013, month=7, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024/2016/03/mercatorpsy4v3r1_gl12_mean_20160303_R20160316.nc'}),
            datetime(year=2016, month=3, day=3, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024_3dinst_so(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-so/2019/04/mercatorpsy4v3r1_gl12_so_20190403_18h_R20190404.nc'}),
            datetime(year=2019, month=4, day=3, hour=18, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024_3dinst_thetao(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-thetao/2020/04/mercatorpsy4v3r1_gl12_thetao_20200404_18h_R20200405.nc'}),
            datetime(year=2020, month=4, day=4, hour=18, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024_3dinst_uovo(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-uovo/2020/04/mercatorpsy4v3r1_gl12_uovo_20200403_06h_R20200404.nc'}),
            datetime(year=2020, month=4, day=3, hour=6, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024_hourly_merged_uv(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-hourly-merged-uv/2019/05/SMOC_20190515_R20190516.nc'}),
            datetime(year=2019, month=5, day=15, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024_hourly_t_u_v_ssh(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-hourly-t-u-v-ssh/2020/05/mercatorpsy4v3r1_gl12_hrly_20200511_R20200520.nc'}),
            datetime(year=2020, month=5, day=11, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_phy_001_024_monthly(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-monthly/2018/mercatorpsy4v3r1_gl12_mean_201807.nc'}),
            datetime(year=2018, month=7, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046/dataset-duacs-nrt-global-merged-allsat-phy-l4/2019/04/nrt_global_allsat_phy_l4_20190403_20200320.nc'}),
            datetime(year=2019, month=4, day=2, hour=12, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_multiobs_glo_phy_nrt_015_003_daily(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/dataset-uv-nrt-daily/2020/03/dataset-uv-nrt-daily_20200301T0000Z_P20200307T0000.nc'}),
            datetime(year=2020, month=3, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_multiobs_glo_phy_nrt_015_003_monthly(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/dataset-uv-nrt-monthly/2020/dataset-uv-nrt-monthly_202004T0000Z_P20200506T0000.nc'}),
            datetime(year=2020, month=4, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_multiobs_glo_phy_nrt_015_003_hourly(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/dataset-uv-nrt-hourly/2020/09/dataset-uv-nrt-hourly_20200906T0000Z_P20200912T0000.nc'}),
            datetime(year=2020, month=9, day=6, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_medsea_analysis_forecast_phy_006_013_daily_mean(self):
        """Should return the proper starting time for a daily mean file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'
               'med00-cmcc-cur-an-fc-d/2020/06/'
               '20200601_d-CMCC--RFVL-MFSeas5-MEDATL-b20200616_an-sv06.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'url': url}),
            datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_medsea_analysis_forecast_phy_006_013_hourly_mean(self):
        """Should return the proper starting time for an hourly mean file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'
               'med00-cmcc-cur-an-fc-h/2020/06/'
               '20200601_h-CMCC--RFVL-MFSeas5-MEDATL-b20200616_an-sv06.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'url': url}),
            datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_medsea_analysis_forecast_phy_006_013_hourly_mean_hts(self):
        """Should return the proper starting time for an hts hourly mean file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'
               'med00-cmcc-cur-an-fc-hts/2020/06/'
               '20200601_hts-CMCC--RFVL-MFSeas5-MEDATL-b20200616_an-sv06.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_start({'url': url}),
            datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_medsea_analysis_forecast_phy_006_013_month(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'
                        'med00-cmcc-cur-an-fc-m/2020/'
                        '20200601_m-CMCC--RFVL-MFSeas5-MEDATL-b20200714_an-sv06.00.nc'}),
            datetime(year=2020, month=6, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_ibi_analysis_forecast_phys_005_001_15min(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT15M-m/2020/12/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_15minav_20201212_20201212_R20201221_AN04.nc'
            }),
            datetime(year=2020, month=12, day=12, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_ibi_analysis_forecast_phys_005_001_daily(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-3D_P1D-m/2021/05/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01dav_20210503_20210503_R20210510_AN06.nc'
            }),
            datetime(year=2021, month=5, day=3, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_ibi_analysis_forecast_phys_005_001_hourly(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT1H-m/2019/11/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav_20191112_20191112_R20191113_AN07.nc'
            }),
            datetime(year=2019, month=11, day=12, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_ibi_analysis_forecast_phys_005_001_hourly3d(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-3D_PT1H-m/2021/08/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav3D_20210815_20210815_R20210816_HC01.nc'
            }),
            datetime(year=2021, month=8, day=15, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_ibi_analysis_forecast_phys_005_001_monthly(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-3D_P1M-m/2019/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01mav_20191001_20191031_R20191031_AN01.nc'
            }),
            datetime(year=2019, month=10, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_hycom_region_000(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_regp01_2020121900_t000.nc.gz'
            }),
            datetime(year=2020, month=12, day=19, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_hycom_region_009(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_regp01_2020121900_t009.nc.gz'
            }),
            datetime(year=2020, month=12, day=19, hour=9, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_hycom_region_027(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_regp01_2020121900_t027.nc.gz'
            }),
            datetime(year=2020, month=12, day=20, hour=3, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_hycom_sfc(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_sfc_u_2020121900_t003.nc.gz'
            }),
            datetime(year=2020, month=12, day=19, hour=3, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_start_rtofs_3dz_daily(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20210519/'
                'rtofs_glo_3dz_n024_daily_3zsio.nc'
            }),
            datetime(year=2021, month=5, day=20, tzinfo=tzutc()))

    def test_time_coverage_start_rtofs_3dz_6hourly(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20210518/'
                'rtofs_glo_3dz_f042_6hrly_hvr_US_east.nc'
            }),
            datetime(year=2021, month=5, day=19, hour=18, tzinfo=tzutc()))

    def test_time_coverage_start_rtofs_2ds(self):
        """Should return the proper starting time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20210518/'
                'rtofs_glo_2ds_f062_prog.nc'
            }),
            datetime(year=2021, month=5, day=20, hour=14, tzinfo=tzutc()))

    def test_time_coverage_end_remss_single_day_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140620v8.2.gz'}),
            datetime(year=2014, month=6, day=21, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_remss_month_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_201406v8.2.gz'}),
            datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_remss_week_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/weeks/f35_20140614v8.2.gz'}),
            datetime(year=2014, month=6, day=15, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_remss_3d3_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140630v8.2_d3d.gz'}),
            datetime(year=2014, month=7, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_ceda(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}),
            datetime(year=2010, month=12, day=31, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_jaxa_single_day_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2015/04/GW1AM2_20150401_01D_EQOD_L3SGSSTLB3300300.h5'}),
            datetime(year=2015, month=4, day=2, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_jaxa_month_file(self):
        """shall return the propert end time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2015/04/GW1AM2_20150400_01M_EQMD_L3SGSSTLB3300300.h5'}),
            datetime(year=2015, month=5, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024/2016/03/mercatorpsy4v3r1_gl12_mean_20160303_R20160316.nc'}),
            datetime(year=2016, month=3, day=4, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024_3dinst_so(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-so/2019/04/mercatorpsy4v3r1_gl12_so_20190403_18h_R20190404.nc'}),
            datetime(year=2019, month=4, day=3, hour=18, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024_3dinst_thetao(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-thetao/2020/04/mercatorpsy4v3r1_gl12_thetao_20200404_18h_R20200405.nc'}),
            datetime(year=2020, month=4, day=4, hour=18, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024_3dinst_uovo(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-3dinst-uovo/2020/04/mercatorpsy4v3r1_gl12_uovo_20200403_06h_R20200404.nc'}),
            datetime(year=2020, month=4, day=3, hour=6, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024_hourly_merged_uv(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-hourly-merged-uv/2019/05/SMOC_20190515_R20190516.nc'}),
            datetime(year=2019, month=5, day=16, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024_hourly_t_u_v_ssh(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-hourly-t-u-v-ssh/2020/05/mercatorpsy4v3r1_gl12_hrly_20200511_R20200520.nc'}),
            datetime(year=2020, month=5, day=12, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_phy_001_024_monthly(self):
        """shall return the propert starting time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024/global-analysis-forecast-phy-001-024-monthly/2018/mercatorpsy4v3r1_gl12_mean_201807.nc'}),
            datetime(year=2018, month=8, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """shall return the propert ending time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046/dataset-duacs-nrt-global-merged-allsat-phy-l4/2019/04/nrt_global_allsat_phy_l4_20190403_20200320.nc'}),
            datetime(year=2019, month=4, day=3, hour=12, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_multiobs_glo_phy_nrt_015_003_daily(self):
        """shall return the propert ending time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/dataset-uv-nrt-daily/2020/03/dataset-uv-nrt-daily_20200302T0000Z_P20200307T0000.nc'}),
            datetime(year=2020, month=3, day=3, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_multiobs_glo_phy_nrt_015_003_monthly(self):
        """shall return the propert ending time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/dataset-uv-nrt-monthly/2020/dataset-uv-nrt-monthly_202004T0000Z_P20200506T0000.nc'}),
            datetime(year=2020, month=5, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_multiobs_glo_phy_nrt_015_003_hourly(self):
        """shall return the propert ending time for hardcoded normalizer """
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003/dataset-uv-nrt-hourly/2020/09/dataset-uv-nrt-hourly_20200906T0000Z_P20200918T0000.nc'}),
            datetime(year=2020, month=9, day=7, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_medsea_analysis_forecast_phy_006_013_daily_mean(self):
        """Should return the proper ending time for a daily mean file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'
               'med00-cmcc-cur-an-fc-d/2020/06/'
               '20200601_d-CMCC--RFVL-MFSeas5-MEDATL-b20200616_an-sv06.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'url': url}),
            datetime(year=2020, month=6, day=2, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_medsea_analysis_forecast_phy_006_013_hourly_mean(self):
        """Should return the proper ending time for an hourly mean file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'
               'med00-cmcc-cur-an-fc-h/2020/06/'
               '20200601_h-CMCC--RFVL-MFSeas5-MEDATL-b20200616_an-sv06.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'url': url}),
            datetime(year=2020, month=6, day=2, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_medsea_analysis_forecast_phy_006_013_hourly_mean_hts(self):
        """Should return the proper ending time for an hts hourly mean file"""
        url = ('ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'
               'med00-cmcc-cur-an-fc-hts/2020/06/'
               '20200601_hts-CMCC--RFVL-MFSeas5-MEDATL-b20200616_an-sv06.00.nc')
        self.assertEqual(
            self.normalizer.get_time_coverage_end({'url': url}),
            datetime(year=2020, month=6, day=2, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_medsea_analysis_forecast_phy_006_013_month(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end(
                {'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'
                        'med00-cmcc-cur-an-fc-m/2020/'
                        '20200601_m-CMCC--RFVL-MFSeas5-MEDATL-b20200714_an-sv06.00.nc'}),
            datetime(year=2020, month=7, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_ibi_analysis_forecast_phys_005_001_15min(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT15M-m/2020/12/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_15minav_20201212_20201212_R20201221_AN04.nc'
            }),
            datetime(year=2020, month=12, day=13, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_ibi_analysis_forecast_phys_005_001_daily(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-3D_P1D-m/2021/05/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01dav_20210503_20210503_R20210510_AN06.nc'
            }),
            datetime(year=2021, month=5, day=4, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_ibi_analysis_forecast_phys_005_001_hourly(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT1H-m/2019/11/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav_20191112_20191112_R20191113_AN07.nc'
            }),
            datetime(year=2019, month=11, day=13, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_ibi_analysis_forecast_phys_005_001_hourly3d(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-3D_PT1H-m/2021/08/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav3D_20210815_20210815_R20210816_HC01.nc'
            }),
            datetime(year=2021, month=8, day=16, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_ibi_analysis_forecast_phys_005_001_monthly(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                       'cmems_mod_ibi_phy_anfc_0.027deg-3D_P1M-m/2019/'
                       'CMEMS_v5r1_IBI_PHY_NRT_PdE_01mav_20191001_20191031_R20191031_AN01.nc'
            }),
            datetime(year=2019, month=11, day=1, hour=0, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_hycom_region_000(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_regp01_2020121900_t000.nc.gz'
            }),
            datetime(year=2020, month=12, day=19, hour=3, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_hycom_region_009(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_regp01_2020121900_t009.nc.gz'
            }),
            datetime(year=2020, month=12, day=19, hour=12, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_hycom_region_027(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_regp01_2020121900_t027.nc.gz'
            }),
            datetime(year=2020, month=12, day=20, hour=6, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_hycom_sfc(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                       'hycom_glb_sfc_u_2020121900_t003.nc.gz'
            }),
            datetime(year=2020, month=12, day=19, hour=6, minute=0, second=0, tzinfo=tzutc()))

    def test_time_coverage_end_rtofs_3dz_daily(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20210519/'
                'rtofs_glo_3dz_n024_daily_3zsio.nc'
            }),
            datetime(year=2021, month=5, day=20, tzinfo=tzutc()))

    def test_time_coverage_end_rtofs_3dz_6hourly(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_end({
                'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20210518/'
                'rtofs_glo_3dz_f042_6hrly_hvr_US_east.nc'
            }),
            datetime(year=2021, month=5, day=19, hour=18, tzinfo=tzutc()))

    def test_time_coverage_end_rtofs_2ds(self):
        """Should return the proper ending time"""
        self.assertEqual(
            self.normalizer.get_time_coverage_start({
                'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/rtofs.20210518/'
                'rtofs_glo_2ds_f062_prog.nc'
            }),
            datetime(year=2021, month=5, day=20, hour=14, tzinfo=tzutc()))

    def test_instrument_jaxa(self):
        """instrument from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', 'AMSR2'),
                         ('Long_Name', 'Advanced Microwave Scanning Radiometer 2')])
        )

    def test_instrument_remss(self):
        """instrument from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', 'GMI'),
                         ('Long_Name', 'Global Precipitation Measurement Microwave Imager')])
        )

    def test_instrument_ceda(self):
        """instrument from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Passive Remote Sensing'),
                         ('Type', 'Spectrometers/Radiometers'),
                         ('Subtype', 'Imaging Spectrometers/Radiometers'),
                         ('Short_Name', ''),
                         ('Long_Name', '')])
        )

    def test_instrument_global_analysis_forecast_phy_001_024(self):
        """instrument from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'In Situ/Laboratory Instruments'),
                         ('Class', 'Data Analysis'),
                         ('Type', 'Environmental Modeling'),
                         ('Subtype', ''),
                         ('Short_Name', 'Computer'),
                         ('Long_Name', 'Computer')])
        )

    def test_instrument_multiobs_glo_phy_nrt_015_003(self):
        """instrument from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Active Remote Sensing'),
                         ('Type', 'Altimeters'),
                         ('Subtype', ''),
                         ('Short_Name', ''),
                         ('Long_Name', '')])
        )

    def test_instrument_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """instrument from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'Earth Remote Sensing Instruments'),
                         ('Class', 'Active Remote Sensing'),
                         ('Type', 'Altimeters'),
                         ('Subtype', ''),
                         ('Short_Name', ''),
                         ('Long_Name', '')])
        )

    def test_instrument_medsea_analysis_forecast_phy_006_013(self):
        """Should return the proper instrument"""
        attributes = {'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'In Situ/Laboratory Instruments'),
                         ('Class', 'Data Analysis'),
                         ('Type', 'Environmental Modeling'),
                         ('Subtype', ''),
                         ('Short_Name', 'Computer'),
                         ('Long_Name', 'Computer')])
        )

    def test_instrument_ibi_analysis_forecast_phys_005_001(self):
        """Should return the proper instrument"""
        attributes = {'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'In Situ/Laboratory Instruments'),
                         ('Class', 'Data Analysis'),
                         ('Type', 'Environmental Modeling'),
                         ('Subtype', ''),
                         ('Short_Name', 'Computer'),
                         ('Long_Name', 'Computer')])
        )

    def test_instrument_hycom(self):
        """Should return the proper instrument"""
        attributes = {'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'In Situ/Laboratory Instruments'),
                         ('Class', 'Data Analysis'),
                         ('Type', 'Environmental Modeling'),
                         ('Subtype', ''),
                         ('Short_Name', 'Computer'),
                         ('Long_Name', 'Computer')])
        )

    def test_instrument_rtofs(self):
        """Should return the proper instrument"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'}
        self.assertEqual(
            self.normalizer.get_instrument(attributes),
            OrderedDict([('Category', 'In Situ/Laboratory Instruments'),
                         ('Class', 'Data Analysis'),
                         ('Type', 'Environmental Modeling'),
                         ('Subtype', ''),
                         ('Short_Name', 'Computer'),
                         ('Long_Name', 'Computer')])
        )

    def test_platform_jaxa(self):
        """platform from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'GCOM-W1'),
                         ('Long_Name', 'Global Change Observation Mission 1st-Water')])
        )

    def test_platform_remss(self):
        """platform from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'GPM'),
                         ('Long_Name', 'Global Precipitation Measurement')])
        )

    def test_platform_ceda(self):
        """platform from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category', 'Earth Observation Satellites'),
                         ('Series_Entity', ''),
                         ('Short_Name', ''),
                         ('Long_Name', '')])
        )

    def test_platform_global_analysis_forecast_phy_001_024(self):
        """platform from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category','Models/Analyses'),
                        ('Series_Entity',''),
                        ('Short_Name','OPERATIONAL MODELS'),
                        ('Long_Name','')])
        )

    def test_platform_multiobs_glo_phy_nrt_015_003(self):
        """platform from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category','Earth Observation Satellites'),
                        ('Series_Entity',''),
                        ('Short_Name',''),
                        ('Long_Name','')])
        )

    def test_platform_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """platform from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category','Earth Observation Satellites'),
                        ('Series_Entity',''),
                        ('Short_Name',''),
                        ('Long_Name','')])
        )

    def test_platform_medsea_analysis_forecast_phy_006_013(self):
        """Should return the proper platform"""
        attributes = {'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category', 'Models/Analyses'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'OPERATIONAL MODELS'),
                         ('Long_Name', '')])
        )

    def test_platform_ibi_analysis_forecast_phys_005_001(self):
        """Should return the proper platform"""
        attributes = {'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category', 'Models/Analyses'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'OPERATIONAL MODELS'),
                         ('Long_Name', '')])
        )

    def test_platform_hycom(self):
        """Should return the proper platform"""
        attributes = {'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category', 'Models/Analyses'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'OPERATIONAL MODELS'),
                         ('Long_Name', '')])
        )

    def test_platform_rtofs(self):
        """Should return the proper platform"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'}
        self.assertEqual(
            self.normalizer.get_platform(attributes),
            OrderedDict([('Category', 'Models/Analyses'),
                         ('Series_Entity', ''),
                         ('Short_Name', 'OPERATIONAL MODELS'),
                         ('Long_Name', '')])
        )

    def test_provider_jaxa(self):
        """provider from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0', 'GOVERNMENT AGENCIES-NON-US'),
                         ('Bucket_Level1', 'JAPAN'),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'JP/JAXA/EOC'),
                         ('Long_Name', 'Earth Observation Center, Japan Aerospace Exploration Agency, Japan'),
                         ('Data_Center_URL', 'http://www.eorc.jaxa.jp/en/index.html')])
        )

    def test_provider_remss(self):
        """provider from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0', 'COMMERCIAL'),
                         ('Bucket_Level1', ''),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'RSS'),
                         ('Long_Name', 'Remote Sensing Systems'),
                         ('Data_Center_URL', 'http://www.remss.com/')])
    )

    def test_provider_ceda(self):
        """provider from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0', 'MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1', ''),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'ESA/CCI'),
                         ('Long_Name', 'Climate Change Initiative, European Space Agency'),
                         ('Data_Center_URL', '')])
        )

    def test_provider_global_analysis_forecast_phy_001_024(self):
        """provider from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0','MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1',''),
                         ('Bucket_Level2',''),
                         ('Bucket_Level3',''),
                         ('Short_Name','CMEMS'),
                         ('Long_Name','Copernicus - Marine Environment Monitoring Service'),
                         ('Data_Center_URL','')])
        )

    def test_provider_multiobs_glo_phy_nrt_015_003(self):
        """provider from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0','MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1',''),
                         ('Bucket_Level2',''),
                         ('Bucket_Level3',''),
                         ('Short_Name','CMEMS'),
                         ('Long_Name','Copernicus - Marine Environment Monitoring Service'),
                         ('Data_Center_URL','')])
        )

    def test_provider_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """provider from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0','MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1',''),
                         ('Bucket_Level2',''),
                         ('Bucket_Level3',''),
                         ('Short_Name','CMEMS'),
                         ('Long_Name','Copernicus - Marine Environment Monitoring Service'),
                         ('Data_Center_URL','')])
        )

    def test_provider_medsea_analysis_forecast_phy_006_013(self):
        """Should return the proper provider"""
        attributes = {'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0','MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1',''),
                         ('Bucket_Level2',''),
                         ('Bucket_Level3',''),
                         ('Short_Name','CMEMS'),
                         ('Long_Name','Copernicus - Marine Environment Monitoring Service'),
                         ('Data_Center_URL','')])
        )

    def test_provider_ibi_analysis_forecast_phys_005_001(self):
        """Should return the proper provider"""
        attributes = {'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([('Bucket_Level0', 'MULTINATIONAL ORGANIZATIONS'),
                         ('Bucket_Level1', ''),
                         ('Bucket_Level2', ''),
                         ('Bucket_Level3', ''),
                         ('Short_Name', 'CMEMS'),
                         ('Long_Name', 'Copernicus - Marine Environment Monitoring Service'),
                         ('Data_Center_URL', '')])
        )

    def test_provider_hycom(self):
        """Should return the proper provider"""
        attributes = {'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([
                ('Bucket_Level0', 'GOVERNMENT AGENCIES-U.S. FEDERAL AGENCIES'),
                ('Bucket_Level1', 'DOC'),
                ('Bucket_Level2', 'NOAA'),
                ('Bucket_Level3', ''),
                ('Short_Name', 'DOC/NOAA/NWS/NCEP'),
                ('Long_Name',
                 'National Centers for Environmental Prediction, National Weather Service, NOAA, '
                 'U.S. Department of Commerce'),
                ('Data_Center_URL', 'http://www.ncep.noaa.gov/')])
        )

    def test_provider_rtofs(self):
        """Should return the proper provider"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'}
        self.assertEqual(
            self.normalizer.get_provider(attributes),
            OrderedDict([
                ('Bucket_Level0', 'GOVERNMENT AGENCIES-U.S. FEDERAL AGENCIES'),
                ('Bucket_Level1', 'DOC'),
                ('Bucket_Level2', 'NOAA'),
                ('Bucket_Level3', ''),
                ('Short_Name', 'DOC/NOAA/NWS/NCEP'),
                ('Long_Name',
                 'National Centers for Environmental Prediction, National Weather Service, NOAA, '
                 'U.S. Department of Commerce'),
                ('Data_Center_URL', 'http://www.ncep.noaa.gov/')])
        )

    def test_dataset_parameters_jaxa(self):
        """dataset_parameters from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [self.DATASET_PARAMETERS['sea_surface_temperature']]
        )

    def test_dataset_parameters_remss(self):
        """dataset_parameters from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/'}
        self.assertEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['wind_speed'],
            self.DATASET_PARAMETERS['atmosphere_mass_content_of_water_vapor'],
            self.DATASET_PARAMETERS['atmosphere_mass_content_of_cloud_liquid_water'],
            self.DATASET_PARAMETERS['rainfall_rate'],
        ])

    def test_dataset_parameters_ceda(self):
        """dataset_parameters from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['sea_surface_temperature']
        ])

    def test_dataset_parameters_phy_001_024(self):
        """dataset_parameters from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [
                self.DATASET_PARAMETERS['sea_water_potential_temperature_at_sea_floor'],
                self.DATASET_PARAMETERS['ocean_mixed_layer_thickness_defined_by_sigma_theta'],
                self.DATASET_PARAMETERS['sea_ice_area_fraction'],
                self.DATASET_PARAMETERS['sea_ice_thickness'],
                self.DATASET_PARAMETERS['sea_water_salinity'],
                self.DATASET_PARAMETERS['sea_water_potential_temperature'],
                self.DATASET_PARAMETERS['eastward_sea_water_velocity'],
                self.DATASET_PARAMETERS['eastward_sea_ice_velocity'],
                self.DATASET_PARAMETERS['northward_sea_water_velocity'],
                self.DATASET_PARAMETERS['northward_sea_ice_velocity'],
                self.DATASET_PARAMETERS['sea_surface_height_above_geoid']
            ]
        )

    def test_dataset_parameters_multiobs_glo_phy_nrt_015_003(self):
        """dataset_parameters from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [
                self.DATASET_PARAMETERS['eastward_sea_water_velocity'],
                self.DATASET_PARAMETERS['northward_sea_water_velocity'],
            ]
        )

    def test_dataset_parameters_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """dataset_parameters from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [
                self.DATASET_PARAMETERS['sea_surface_height_above_geoid'],
                self.DATASET_PARAMETERS['sea_surface_height_above_sea_level'],
                self.DATASET_PARAMETERS['surface_geostrophic_eastward_sea_water_velocity'],
                self.DATASET_PARAMETERS['surface_geostrophic_eastward_sea_water_velocity_'
                                        'assuming_mean_sea_level_for_geoid'],
                self.DATASET_PARAMETERS['surface_geostrophic_northward_sea_water_velocity'],
                self.DATASET_PARAMETERS['surface_geostrophic_northward_sea_water_velocity_'
                                        'assuming_mean_sea_level_for_geoid'],
            ]
        )

    def test_dataset_parameters_medsea_analysis_forecast_phy_006_013_cur(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/med00-cmcc-cur'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes), [
                self.DATASET_PARAMETERS['eastward_sea_water_velocity'],
                self.DATASET_PARAMETERS['northward_sea_water_velocity']
            ]
        )

    def test_dataset_parameters_medsea_analysis_forecast_phy_006_013_mld(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/med00-cmcc-mld'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes), [
                self.DATASET_PARAMETERS['ocean_mixed_layer_thickness_defined_by_sigma_theta']
            ]
        )

    def test_dataset_parameters_medsea_analysis_forecast_phy_006_013_sal(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/med00-cmcc-sal'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [self.DATASET_PARAMETERS['sea_water_salinity']]
        )

    def test_dataset_parameters_medsea_analysis_forecast_phy_006_013_ssh(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/med00-cmcc-ssh'}
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [self.DATASET_PARAMETERS['sea_surface_height_above_geoid']]
        )

    def test_dataset_parameters_medsea_analysis_forecast_phy_006_013_tem(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/med00-cmcc-tem'}
        self.assertEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['sea_water_potential_temperature_at_sea_floor'],
            self.DATASET_PARAMETERS['sea_water_potential_temperature']
        ])

    def test_dataset_parameters_medsea_analysis_forecast_phy_006_013_mask_bathy(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/" +
                   "MEDSEA_ANALYSIS_FORECAST_PHY_006_013-statics/MED-MFC_006_013_mask_bathy.nc"
        }
        self.assertEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['model_level_number_at_sea_floor'],
            self.DATASET_PARAMETERS['sea_floor_depth_below_geoid'],
        ])

    def test_dataset_parameters_medsea_analysis_forecast_phy_006_013_coordinates(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': "ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/" +
                   "MEDSEA_ANALYSIS_FORECAST_PHY_006_013-statics/MED-MFC_006_013_coordinates.nc"
        }
        self.assertEqual(
            self.normalizer.get_dataset_parameters(attributes),
            [self.DATASET_PARAMETERS['cell_thickness']]
        )

    def test_dataset_parameters_ibi_analysis_forecast_phys_005_001_15min(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                   'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT15M-m/2020/12/'
                   'CMEMS_v5r1_IBI_PHY_NRT_PdE_15minav_20201212_20201212_R20201221_AN04.nc'
        }
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['sea_surface_height_above_geoid'],
            self.DATASET_PARAMETERS['eastward_sea_water_velocity'],
            self.DATASET_PARAMETERS['northward_sea_water_velocity']
        ])

    def test_dataset_parameters_ibi_analysis_forecast_phys_005_001_daily(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                    'cmems_mod_ibi_phy_anfc_0.027deg-3D_P1D-m/2021/05/'
                    'CMEMS_v5r1_IBI_PHY_NRT_PdE_01dav_20210503_20210503_R20210510_AN06.nc'
        }
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['sea_water_potential_temperature'],
            self.DATASET_PARAMETERS['sea_water_salinity'],
            self.DATASET_PARAMETERS['eastward_sea_water_velocity'],
            self.DATASET_PARAMETERS['northward_sea_water_velocity'],
            self.DATASET_PARAMETERS['sea_surface_height_above_geoid'],
            self.DATASET_PARAMETERS['ocean_mixed_layer_thickness_defined_by_sigma_theta'],
            self.DATASET_PARAMETERS['sea_water_potential_temperature_at_sea_floor'],
        ])

    def test_dataset_parameters_ibi_analysis_forecast_phys_005_001_hourly(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                    'cmems_mod_ibi_phy_anfc_0.027deg-2D_PT1H-m/2019/11/'
                    'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav_20191112_20191112_R20191113_AN07.nc'
        }
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['sea_water_potential_temperature'],
            self.DATASET_PARAMETERS['eastward_sea_water_velocity'],
            self.DATASET_PARAMETERS['northward_sea_water_velocity'],
            self.DATASET_PARAMETERS['barotropic_eastward_sea_water_velocity'],
            self.DATASET_PARAMETERS['barotropic_northward_sea_water_velocity'],
            self.DATASET_PARAMETERS['sea_surface_height_above_geoid'],
            self.DATASET_PARAMETERS['ocean_mixed_layer_thickness_defined_by_sigma_theta'],

        ])

    def test_dataset_parameters_ibi_analysis_forecast_phys_005_001_hourly3d(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                    'cmems_mod_ibi_phy_anfc_0.027deg-3D_PT1H-m/2021/08/'
                    'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav3D_20210815_20210815_R20210816_HC01.nc'
        }
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['sea_water_potential_temperature'],
            self.DATASET_PARAMETERS['sea_water_salinity'],
            self.DATASET_PARAMETERS['eastward_sea_water_velocity'],
            self.DATASET_PARAMETERS['northward_sea_water_velocity'],
        ])

    def test_dataset_parameters_ibi_analysis_forecast_phys_005_001_monthly(self):
        """Should return the proper dataset parameters"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                   'cmems_mod_ibi_phy_anfc_0.027deg-3D_P1M-m/2019/'
                   'CMEMS_v5r1_IBI_PHY_NRT_PdE_01mav_20191001_20191031_R20191031_AN01.nc'
        }
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['sea_water_potential_temperature'],
            self.DATASET_PARAMETERS['sea_water_salinity'],
            self.DATASET_PARAMETERS['eastward_sea_water_velocity'],
            self.DATASET_PARAMETERS['northward_sea_water_velocity'],
            self.DATASET_PARAMETERS['sea_surface_height_above_geoid'],
            self.DATASET_PARAMETERS['ocean_mixed_layer_thickness_defined_by_sigma_theta'],
            self.DATASET_PARAMETERS['sea_water_potential_temperature_at_sea_floor'],
        ])

    def test_dataset_parameters_hycom_region(self):
        """Should return the proper dataset parameters"""
        attributes = {'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'}
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['sea_water_salinity'],
            self.DATASET_PARAMETERS['sea_water_temperature'],
            self.DATASET_PARAMETERS['sea_water_salinity_at_bottom'],
            self.DATASET_PARAMETERS['sea_water_temperature_at_bottom'],
            self.DATASET_PARAMETERS['sea_surface_height_above_geoid'],
            self.DATASET_PARAMETERS['eastward_sea_water_velocity'],
            self.DATASET_PARAMETERS['northward_sea_water_velocity'],
        ])

    def test_dataset_parameters_rtofs_2ds_diag(self):
        """Should return the proper dataset parameters"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_2ds_f063_diag.nc'}
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['sea_surface_height_above_geoid'],
            self.DATASET_PARAMETERS['barotropic_eastward_sea_water_velocity'],
            self.DATASET_PARAMETERS['barotropic_northward_sea_water_velocity'],
            self.DATASET_PARAMETERS['surface_boundary_layer_thickness'],
            self.DATASET_PARAMETERS['ocean_mixed_layer_thickness'],
        ])

    def test_dataset_parameters_rtofs_2ds_prog(self):
        """Should return the proper dataset parameters"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_2ds_f062_prog.nc'}
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['eastward_sea_water_velocity'],
            self.DATASET_PARAMETERS['northward_sea_water_velocity'],
            self.DATASET_PARAMETERS['sea_surface_temperature'],
            self.DATASET_PARAMETERS['sea_surface_salinity'],
            self.DATASET_PARAMETERS['sea_water_potential_density'],
        ])

    def test_dataset_parameters_rtofs_2ds_ice(self):
        """Should return the proper dataset parameters"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_2ds_f062_ice.nc'}
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['ice_coverage'],
            self.DATASET_PARAMETERS['ice_temperature'],
            self.DATASET_PARAMETERS['ice_thickness'],
            self.DATASET_PARAMETERS['ice_uvelocity'],
            self.DATASET_PARAMETERS['icd_vvelocity'],
        ])

    def test_dataset_parameters_rtofs_3dz(self):
        """Should return the proper dataset parameters"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_3dz_f024_daily_3zsio.nc'}
        self.assertListEqual(self.normalizer.get_dataset_parameters(attributes), [
            self.DATASET_PARAMETERS['eastward_sea_water_velocity'],
            self.DATASET_PARAMETERS['northward_sea_water_velocity'],
            self.DATASET_PARAMETERS['sea_surface_temperature'],
            self.DATASET_PARAMETERS['sea_surface_salinity'],
        ])

    def test_entry_title_jaxa(self):
        """entry_title from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_entry_title(attributes), 'AMSR2-L3 Sea Surface Temperature')

    def test_entry_title_remss(self):
        """entry_title from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/'}
        self.assertEqual(self.normalizer.get_entry_title(attributes),
                         'Atmosphere parameters from Global Precipitation Measurement Microwave Imager')

    def test_entry_title_ceda(self):
        """entry_title from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(self.normalizer.get_entry_title(
            attributes), 'ESA SST CCI OSTIA L4 Climatology')

    def test_entry_title_global_analysis_forecast_phy_001_024(self):
        """entry_title from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'}
        self.assertEqual(
            self.normalizer.get_entry_title(attributes),'GLOBAL OCEAN 1_12 PHYSICS ANALYSIS AND FORECAST UPDATED DAILY')

    def test_entry_title_multiobs_glo_phy_nrt_015_003(self):
        """entry_title from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'}
        self.assertEqual(
            self.normalizer.get_entry_title(attributes),'GLOBAL TOTAL SURFACE AND 15M CURRENT FROM ALTIMETRIC GEOSTROPHIC CURRENT AND MODELED EKMAN CURRENT PROCESSING')

    def test_entry_title_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """entry_title from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'}
        self.assertEqual(
            self.normalizer.get_entry_title(attributes),'GLOBAL OCEAN GRIDDED L4 SEA SURFACE HEIGHTS AND DERIVED VARIABLES NRT')

    def test_entry_title_medsea_analysis_forecast_phy_006_013(self):
        """Should return the proper entry_title"""
        attributes = {'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'}
        self.assertEqual(
            self.normalizer.get_entry_title(attributes),
            'Mediterranean Forecasting System (hydrodynamic-wave model)'
        )

    def test_entry_title_ibi_analysis_forecast_phys_005_001(self):
        """Should return the proper entry_title"""
        attributes = {'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'}
        self.assertEqual(
            self.normalizer.get_entry_title(attributes),
            'Atlantic-Iberian Biscay Irish-Ocean Physics Analysis and Forecast'
        )

    def test_entry_title_hycom(self):
        """Should return the proper entry_title"""
        attributes = {'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'}
        self.assertEqual(
            self.normalizer.get_entry_title(attributes),
            'Global Hybrid Coordinate Ocean Model (HYCOM)'
        )

    def test_entry_title_rtofs(self):
        """Should return the proper entry_title"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'}
        self.assertEqual(
            self.normalizer.get_entry_title(attributes),
            'Global operational Real-Time Ocean Forecast System'
        )

    def test_entry_id_jaxa(self):
        """entry_id from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_entry_id(attributes), 'GW1AM2_201207031905_134D_L2SGSSTLB3300300')

    def test_entry_id_remss(self):
        """entry_id from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/f35_20140603v8.2.gz'}
        self.assertEqual(self.normalizer.get_entry_id(attributes),
                         'f35_20140603v8.2')

    def test_entry_id_ceda(self):
        """entry_id from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(self.normalizer.get_entry_id(
            attributes), 'D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0')

    def test_entry_id_for_unkown_file_type(self):
        """entry_id shall equal to None for an unknown fileformat """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.bb'}
        self.assertEqual(self.normalizer.get_entry_id(
            attributes), None)

    def test_entry_id_for_thredds_met_no_dods(self):
        """entry_id from URLMetadataNormalizer for a dods URL from thredds.met.no"""
        attributes = {
            'url': "https://thredds.met.no/thredds/dodsC/osisaf/met.no/ice/Some/path/to/file/ice_type_sh_polstere-100_multi_201609261200.nc.dods"}
        self.assertEqual(
            self.normalizer.get_entry_id(attributes),
            'ice_type_sh_polstere-100_multi_201609261200')

    def test_entry_id_for_thredds_met_no_fileserver(self):
        """entry_id from URLMetadataNormalizer for a fileServer URL from thredds.met.no"""
        attributes = {
            'url': "https://thredds.met.no/thredds/fileServer/osisaf/met.no/ice/Some/path/to/file/ice_type_sh_polstere-100_multi_201609261200.nc"}
        self.assertEqual(
            self.normalizer.get_entry_id(attributes),
            'ice_type_sh_polstere-100_multi_201609261200')

    def test_entry_id_for_podaac_ingester(self):
        """entry_id from URLMetadataNormalizer for PODAAC metadata"""
        attributes = {
            'url': "https://opendap.jpl.nasa.gov/opendap/Some/path/to/file/20180110000000-OSPO-L2P_GHRSST-SSTsubskin-VIIRS_NPP-ACSPO_V2.61-v02.0-fv01.0.nc"}
        self.assertEqual(self.normalizer.get_entry_id(
            attributes), '20180110000000-OSPO-L2P_GHRSST-SSTsubskin-VIIRS_NPP-ACSPO_V2.61-v02.0-fv01.0')

    def test_entry_id_for_marine_copernicus(self):
        """entry_id from URLMetadataNormalizer for marine copernicus metadata"""
        attributes = {
            'url': "ftp://nrt.cmems-du.eu/Core/Some/path/to/file/20180110000000-OSPO-L2P_GHRSST-SSTsubskin-VIIRS_NPP-ACSPO_V2.61-v02.0-fv01.0.nc"}
        self.assertEqual(self.normalizer.get_entry_id(
            attributes), '20180110000000-OSPO-L2P_GHRSST-SSTsubskin-VIIRS_NPP-ACSPO_V2.61-v02.0-fv01.0')

    def test_entry_id_medsea_analysis_forecast_phy_006_013(self):
        """Should return the proper entry_id"""
        attributes = {'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'
                             'med00-cmcc-sal-an-fc-hts/2019/07/'
                             '20190706_hts-CMCC--PSAL-MFSeas5-MEDATL-b20190101_an-sv06.00.nc'}
        self.assertEqual(
            self.normalizer.get_entry_id(attributes),
            '20190706_hts-CMCC--PSAL-MFSeas5-MEDATL-b20190101_an-sv06.00'
        )

    def test_entry_id_ibi_analysis_forecast_phys_005_001(self):
        """Should return the proper entry_id"""
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'
                    'cmems_mod_ibi_phy_anfc_0.027deg-3D_PT1H-m/2021/08/'
                    'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav3D_20210815_20210815_R20210816_HC01.nc'
        }
        self.assertEqual(
            self.normalizer.get_entry_id(attributes),
            'CMEMS_v5r1_IBI_PHY_NRT_PdE_01hav3D_20210815_20210815_R20210816_HC01'
        )

    def test_entry_id_hycom_region(self):
        """Should return the proper entry_id"""
        attributes = {
            'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                   'hycom_glb_regp17_2020122000_t168.nc.gz'
        }
        self.assertEqual(
            self.normalizer.get_entry_id(attributes),
            'hycom_glb_regp17_2020122000_t168'
        )

    def test_entry_id_hycom_sfc(self):
        """Should return the proper entry_id"""
        attributes = {
            'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                   'hycom_glb_sfc_u_2020121900_t000.nc.gz'
        }
        self.assertEqual(
            self.normalizer.get_entry_id(attributes),
            'hycom_glb_sfc_u_2020121900_t000'
        )

    def test_entry_id_rtofs(self):
        """Should return the proper entry_id"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_3dz_f024_daily_3zsio.nc'}
        self.assertEqual(
            self.normalizer.get_entry_id(attributes),
            '20210518/rtofs_glo_3dz_f024_daily_3zsio'
        )

    def test_geometry_jaxa_the_first_type_of_sst(self):
        """geometry from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_10/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_geometry_jaxa_the_second_type_of_sst(self):
        """geometry from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25/3/2012/07/GW1AM2_201207031905_134D_L2SGSSTLB3300300.h5'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_geometry_phy_001_024(self):
        """geometry from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_geometry_multiobs_glo_phy_nrt_015_003(self):
        """geometry from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_geometry_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """geometry from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_geometry_remss(self):
        """geometry from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_geometry_ceda(self):
        """geometry from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))')

    def test_geometry_medsea_analysis_forecast_phy_006_013(self):
        """Should return the proper geometry"""
        attributes = {'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-17.29 45.98, -17.29 30.18, 36.30 30.18, 36.30 45.98, -17.29 45.98))'
        )

    def test_geometry_ibi_analysis_forecast_phys_005_001(self):
        """Should return the proper geometry"""
        attributes = {'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-19 56, 5 56, 5 26, -19 26, -19 56))'
        )

    def test_geometry_hycom_region1(self):
        """Should return the proper geometry"""
        attributes = {
            'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                   'hycom_glb_regp01_2020121900_t030.nc.gz'
        }
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-100.04 70.04, -100.04 -0.04, -49.96 -0.04, -49.96 70.04, -100.04 70.04))'
        )

    def test_geometry_hycom_region6(self):
        """Should return the proper geometry"""
        attributes = {
            'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                   'hycom_glb_regp06_2020121900_t030.nc.gz'
        }
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((149.96 70.04, 149.96 9.96, 210.04 9.96, 210.04 70.04, 149.96 70.04))'
        )

    def test_geometry_hycom_region7(self):
        """Should return the proper geometry"""
        attributes = {
            'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                   'hycom_glb_regp07_2020121900_t030.nc.gz'
        }
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-150.04 60.04, -150.04 9.96, -99.96 9.96, -99.96 60.04, -150.04 60.04))'
        )

    def test_geometry_hycom_region17(self):
        """Should return the proper geometry"""
        attributes = {
            'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                   'hycom_glb_regp17_2020121900_t030.nc.gz'
        }
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180.04 80.02,-180.04 59.98,-119.96 59.98,-119.96 80.02,-180.04 80.02))'
        )

    def test_geometry_hycom_sfc(self):
        """Should return the proper geometry"""
        attributes = {
            'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'
                   'hycom_glb_sfc_u_2020121900_t030.nc.gz'
        }
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'
        )

    def test_geometry_rtofs_global(self):
        """Should return the proper geometry"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_3dz_f024_daily_3zsio.nc'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            'POLYGON((-180 -90, -180 90, 180 90, 180 -90, -180 -90))'
        )

    def test_geometry_rtofs_us_east(self):
        """Should return the proper geometry"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_3dz_f042_6hrly_hvr_US_east.nc'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            ('POLYGON (('
                '-105.193603515625 0, -40.719970703125 0,'
                '-40.719970703125 79.74808502197266,'
                '-105.193603515625 79.74808502197266,'
                '-105.193603515625 0))')
        )

    def test_geometry_rtofs_us_west(self):
        """Should return the proper geometry"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_3dz_f042_6hrly_hvr_US_west.nc'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            ('POLYGON (('
                '-157.9200439453125 10.02840137481689,'
                '-74.239990234375 10.02840137481689,'
                '-74.239990234375 74.57466888427734,'
                '-157.9200439453125 74.57466888427734,'
                '-157.9200439453125 10.02840137481689))')
        )

    def test_geometry_rtofs_alaska(self):
        """Should return the proper geometry"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'
                             'rtofs.20210518/rtofs_glo_3dz_f042_6hrly_hvr_alaska.nc'}
        self.assertEqual(
            self.normalizer.get_location_geometry(attributes),
            ('POLYGON (('
                '-179.1199951171875 45.77324676513672,'
                '-112.6572265625 45.77324676513672,'
                '-112.6572265625 78.41667938232422,'
                '-179.1199951171875 78.41667938232422,'
                '-179.1199951171875 45.77324676513672))')
        )

    def test_none_for_incorrect_ftp_resource(self):
        """shall return None in the case of incorrect ftp resource (incorrect 'ftp_domain_name')
        and [] for the cumulative ones """
        self.assertEqual([], self.normalizer.get_dataset_parameters({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_entry_title({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_instrument({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_platform({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_provider({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_time_coverage_end({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_time_coverage_start({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_location_geometry({'url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_entry_id({'url': 'ftp://test/'}))

    def test_for_delivering_none_when_lacking_url_in_raw_attributes(self):
        """shall return None in the case of no 'url' field in the raw_attribute dictionary
        and [] for the cumulative ones.
        This test is for asserting the correct behavior of this normalizer inside
        the chain of normalizer in order not to intract with other type of raw_attributes """
        self.assertEqual([], self.normalizer.get_dataset_parameters({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_entry_title({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_instrument({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_platform({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_provider({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_time_coverage_end({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_time_coverage_start({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_location_geometry({'none-url': 'ftp://test/'}))
        self.assertIsNone(self.normalizer.get_entry_id({'none-url': 'ftp://test/'}))

    def test_summary_jaxa_l2(self):
        """summary from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L2.SST'}
        self.assertEqual(
            self.normalizer.get_summary(attributes), 'Processing level: 2')

    def test_summary_jaxa_l3(self):
        """summary from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://ftp.gportal.jaxa.jp/standard/GCOM-W/GCOM-W.AMSR2/L3.SST_25'}
        self.assertEqual(
            self.normalizer.get_summary(attributes), 'Processing level: 3')

    def test_summary_remss(self):
        """summary from URLMetadataNormalizer """
        attributes = {'url': 'ftp://ftp.remss.com/gmi/bmaps_v08.2/y2014/m06/'}
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: GMI is a dual-polarization, multi-channel, conical-scanning, passive '
            'microwave radiometer with frequent revisit times.;Processing level: 3'
        )

    def test_summary_ceda(self):
        """summary from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://anon-ftp.ceda.ac.uk/neodc/esacci/sst/data/CDR_v2/Climatology/L4/v2.1/D365-ESACCI-L4_GHRSST-SSTdepth-OSTIA-GLOB_CDR2.1-v02.0-fv01.0.nc'}
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: This v2.1 SST_cci Climatology Data Record (CDR) consists of Level 4 daily'
            ' climatology files gridded on a 0.05 degree grid.;Processing level: 4;'
            'Product: ESA SST CCI Climatology'
        )

    def test_summary_global_analysis_forecast_phy_001_024(self):
        """summary from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/GLOBAL_ANALYSIS_FORECAST_PHY_001_024'}
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: The Operational Mercator global ocean analysis and forecast system at '
            '1/12 degree is providing 10 days of 3D global ocean forecasts updated daily.;'
            'Processing level: 4;'
            'Product: GLOBAL_ANALYSIS_FORECAST_PHY_001_024'
        )

    def test_summary_multiobs_glo_phy_nrt_015_003(self):
        """summary from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/MULTIOBS_GLO_PHY_NRT_015_003'}
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: This product is a NRT L4 global total velocity field at 0m and 15m.;'
            'Processing level: 4;'
            'Product: MULTIOBS_GLO_PHY_NRT_015_003'
        )

    def test_summary_sealevel_glo_phy_l4_nrt_observations_008_046(self):
        """summary from URLMetadataNormalizer """
        attributes = {
            'url': 'ftp://nrt.cmems-du.eu/Core/SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'}
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: Altimeter satellite gridded Sea Level Anomalies (SLA) computed with '
            'respect to a twenty-year mean.;'
            'Processing level: 4;'
            'Product: SEALEVEL_GLO_PHY_L4_NRT_OBSERVATIONS_008_046'
        )

    def test_summary_medsea_analysis_forecast_phy_006_013(self):
        """Should return the proper summary"""
        attributes = {'url': 'ftp://nrt.cmems-du.eu/Core/MEDSEA_ANALYSIS_FORECAST_PHY_006_013/'}
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: The physical component of the Mediterranean Forecasting System '
            '(Med-Currents) is a coupled hydrodynamic-wave model implemented over the whole '
            'Mediterranean Basin.;'
            'Processing level: 4;'
            'Product: MEDSEA_ANALYSIS_FORECAST_PHY_006_013'
        )

    def test_summary_ibi_analysis_forecast_phys_005_001(self):
        """Should return the proper summary"""
        attributes = {'url': 'ftp://nrt.cmems-du.eu/Core/IBI_ANALYSISFORECAST_PHY_005_001/'}
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: The operational IBI (Iberian Biscay Irish) Ocean Analysis and Forecasting'
            ' system provides a 5-day hydrodynamic forecast including high frequency '
            'processes of paramount importance to characterize regional scale marine '
            'processes.;'
            'Processing level: 4;'
            'Product: IBI_ANALYSISFORECAST_PHY_005_001'
        )

    def test_summary_hycom(self):
        """Should return the proper summary"""
        attributes = {'url': 'ftp://ftp.opc.ncep.noaa.gov/grids/operational/GLOBALHYCOM/Navy/'}
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            'Description: This system provides 4-day forecasts at 3-hour time steps, updated at '
            '00Z daily. Navy Global HYCOM has a resolution of 1/12 degree in the horizontal and '
            'uses hybrid (isopycnal/sigma/z-level) coordinates in the vertical. The output is '
            'interpolated onto a regular 1/12-degree grid horizontally and 40 standard depth '
            'levels.;'
            'Processing level: 4;'
            'Product: HYCOM'
        )

    def test_summary_rtofs(self):
        """Should return the proper summary"""
        attributes = {'url': 'ftp://ftpprd.ncep.noaa.gov/pub/data/nccf/com/rtofs/prod/'}
        self.assertEqual(
            self.normalizer.get_summary(attributes),
            "Description: Real Time Ocean Forecast System (RTOFS) Global is a data-assimilating "
            "nowcast-forecast system operated by the National Weather Service's National "
            "Centers for Environmental Prediction (NCEP).;"
            'Processing level: 4;'
            'Product: RTOFS'
        )
