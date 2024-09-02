"""Variable reference for Zampy."""

from pint import UnitRegistry
from zampy.datasets.dataset_protocol import Variable


def unit_registration() -> UnitRegistry:
    """Create unit registration for all custom units."""
    unit_registry = UnitRegistry()
    unit_registry.define("fraction = [] = frac = kilogram_per_kilogram")
    unit_registry.define("percent = 1e-2 frac = pct")
    unit_registry.define("ppm = 1e-6 fraction")
    unit_registry.define("degree_north = degree = degree_N = degreeN")
    unit_registry.define("degree_east = degree = degree_E = degreeE")
    unit_registry.define("watt_per_square_meter = watt/meter**2")
    unit_registry.define("joule_per_square_meter = joule/meter**2")
    unit_registry.define("kilogram_per_square_meter = kilogram/(meter**2)")
    unit_registry.define(
        "kilogram_per_square_meter_second = kilogram/(meter**2*second)"
    )
    unit_registry.define("milimeter_per_second = watt/meter**2")
    unit_registry.define("dimensionless = []")
    return unit_registry


unit_registry = unit_registration()
# By default, we use the variable names and units following the CF convention:
# https://cfconventions.org/Data/cf-standard-names/current/build/cf-standard-name-table.html


VARIABLE_REFERENCE = (
    Variable("air_temperature", unit_registry.kelvin),
    Variable("dewpoint_temperature", unit_registry.kelvin),
    Variable("relative_humidity", unit_registry.percent),
    Variable("surface_pressure", unit_registry.pascal),
    Variable("eastward_component_of_wind", unit_registry.meter_per_second),
    Variable("northward_component_of_wind", unit_registry.meter_per_second),
    Variable("surface_solar_radiation_downwards", unit_registry.watt_per_square_meter),
    Variable(
        "surface_thermal_radiation_downwards", unit_registry.watt_per_square_meter
    ),
    Variable("total_precipitation", unit_registry.millimeter_per_second),
    Variable(
        "specific_humidity",
        unit_registry.fraction,
        desc="Mass fraction of water in air.",
    ),
    Variable("height_of_vegetation", unit_registry.meter),
    Variable(
        "height_of_vegetation_standard_deviation",
        unit_registry.meter,
        desc="Uncertainty of the 'height_of_vegetation' variable.",
    ),
    Variable("co2_concentration", unit_registry.kilogram_per_kilogram),
    Variable("altitude", unit_registry.meter),
    Variable("latitude", unit=unit_registry.degree_north),
    Variable("longitude", unit=unit_registry.degree_east),
    Variable("elevation", unit=unit_registry.meter),
    Variable("leaf_area_index", unit=unit_registry.fraction),
    Variable("land_cover", unit=unit_registry.dimensionless),
    Variable("soil_temperature", unit=unit_registry.kelvin),
    Variable("soil_moisture", unit=unit_registry.kilogram_per_square_meter),
)

VARIABLE_REFERENCE_LOOKUP = {var.name: var for var in VARIABLE_REFERENCE}
