from collections import OrderedDict

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
    'latitude': OrderedDict([
        ('standard_name', 'latitude'),
        ('canonical_units', 'degree_north'),
        ('definition',
            'Latitude is positive northward; its units of degree_north (or '
            'equivalent) indicate this explicitly. In a latitude-longitude '
            'system defined with respect to a rotated North Pole, the '
            'standard name of grid_latitude should be used instead of '
            'latitude. Grid latitude is positive in the grid-northward '
            'direction, but its units should be plain degree.')]),
    'longitude': OrderedDict([
        ('standard_name', 'longitude'),
        ('canonical_units', 'degree_east'),
        ('definition',
            'Longitude is positive eastward; its units of degree_east (or '
            'equivalent) indicate this explicitly. In a latitude-longitude '
            'system defined with respect to a rotated North Pole, the '
            'standard name of grid_longitude should be used instead of '
            'longitude. Grid longitude is positive in the grid-eastward '
            'direction, but its units should be plain degree.')]),
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
    'projection_x_coordinate': OrderedDict([
        ('standard_name', 'projection_x_coordinate'),
        ('canonical_units', 'm'),
        ('definition',
            '"x" indicates a vector component along the grid x-axis, when '
            'this is not true longitude, positive with increasing x. '
            'Projection coordinates are distances in the x- and y-directions '
            'on a plane onto which the surface of the Earth has been '
            'projected according to a map projection. The relationship '
            'between the projection coordinates and latitude and longitude '
            'is described by the grid_mapping.')]),
    'projection_y_coordinate': OrderedDict([
        ('standard_name', 'projection_y_coordinate'),
        ('canonical_units', 'm'),
        ('definition',
            '"y" indicates a vector component along the grid y-axis, when this is not true '
            'latitude, positive with increasing y. Projection coordinates are distances in the '
            'x- and y-directions on a plane onto which the surface of the Earth has been projected '
            'according to a map projection. The relationship between the projection coordinates and'
            ' latitude and longitude is described by the grid_mapping.')]),
    'rainfall_rate': OrderedDict([
        ('standard_name', 'rainfall_rate'),
        ('canonical_units', 'm s-1'),
        ('definition',
            'The lifting condensation level is the height at which the relative humidity of an air'
            ' parcel cooled by dry adiabatic lifting would reach 100%. A coordinate variable of '
            'original_air_pressure_of_lifted_parcel should be specified to indicate the starting '
            'height of the lifted parcel.')]),
    'sea_binary_mask': OrderedDict([
        ('standard_name', 'sea_binary_mask'),
        ('canonical_units', '1'),
        ('definition',
            'X"_binary_mask" has 1 where condition X is met, 0 elsewhere. 1 = sea, 0 = land.')]),
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
    'sea_ice_x_velocity': OrderedDict([
        ('standard_name', 'sea_ice_x_velocity'),
        ('canonical_units', 'm s-1'),
        ('definition',
            'A velocity is a vector quantity. "x" indicates a vector '
            'component along the grid x-axis, positive with increasing x. '
            '"Sea ice" means all ice floating in the sea which has formed '
            'from freezing sea water, rather than by other processes such as '
            'calving of land ice to form icebergs.')]),
    'sea_ice_y_velocity': OrderedDict([
        ('standard_name', 'sea_ice_y_velocity'),
        ('canonical_units', 'm s-1'),
        ('definition',
            'A velocity is a vector quantity. "y" indicates a vector '
            'component along the grid y-axis, positive with increasing y. '
            '"Sea ice" means all ice floating in the sea which has formed '
            'from freezing sea water, rather than by other processes such as '
            'calving of land ice to form icebergs.')]),
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
    'surface_snow_thickness': OrderedDict([
        ('standard_name', 'surface_snow_thickness'),
        ('canonical_units', 'm'),
        ('definition',
            'Surface snow refers to the snow on the solid ground or on '
            'surface ice cover, but excludes, for example, falling '
            'snowflakes and snow on plants. "Thickness" means the vertical '
            'extent of a layer. Unless indicated in the cell_methods '
            'attribute, a quantity is assumed to apply to the whole area of '
            'each horizontal grid box. Previously, the qualifier where_type '
            'was used to specify that the quantity applies only to the part '
            'of the grid box of the named type. Names containing the '
            'where_type qualifier are deprecated and newly created data '
            'should use the cell_methods attribute to indicate the '
            'horizontal area to which the quantity applies.')]),
    'time': OrderedDict([
        ('standard_name', 'time'),
        ('canonical_units', 's'),
        ('definition',
            'Atmosphere upward absolute vorticity is the sum of the '
            'atmosphere upward relative vorticity and the vertical component '
            'of vorticity due to the Earth’s rotation. In contrast, the '
            'quantity with standard name '
            "atmosphere_upward_relative_vorticity excludes the Earth's "
            'rotation. Vorticity is a vector quantity. "Upward" indicates a '
            'vector component which is positive when directed upward '
            '(negative downward). A positive value of '
            'atmosphere_upward_absolute_vorticity indicates anticlockwise '
            'rotation when viewed from above.')]),
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
