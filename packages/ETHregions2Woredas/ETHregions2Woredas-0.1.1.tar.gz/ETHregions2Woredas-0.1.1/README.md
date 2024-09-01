# ETHRegions2Woredas Package

A Python package that provides a complete list of regions, zones, and woredas.

## Installation

You can install the package using pip:

```bash
pip install ETHRegions2Woredas

```

## USAGE

Here's how to use the package:

```python
from ETHRegions2Woredas import (
    get_all_regions,
    get_all_zones,
    get_zones_by_region,
    get_woredas_by_zone,
    get_woredas_by_region,
    get_woredas_by_region_and_zone,
    get_region_by_woreda,
    get_region_by_zone,
    get_zone_by_woreda,
    get_all_woredas,
)

# Get all regions
regions = get_all_regions()
print("All Regions:", regions)

# Get all zones
zones = get_all_zones()
print("All Zones:", zones)

# Get zones by specific region
zones_in_region = get_zones_by_region('Amhara')
print("Zones in Amhara:", list(zones_in_region))

# Get woredas by specific zone
woredas_in_zone = get_woredas_by_zone('South Wollo Zone')
print("Woredas in South Wollo Zone:", woredas_in_zone)

# Get woredas by specific region
woredas_in_region = get_woredas_by_region('Amhara')
print("Woredas in Amhara:", woredas_in_region)

# Get woredas by specific region and zone
woredas_in_region_zone = get_woredas_by_region_and_zone('Amhara', 'South Wollo Zone')
print("Woredas in Amhara and South Wollo Zone:", woredas_in_region_zone)

# Get region by specific woreda
region_of_woreda = get_region_by_woreda('Amhara Sayint')
print("Region of Amhara Sayint:", region_of_woreda)

# Get region by specific zone
region_of_zone = get_region_by_zone('South Wollo Zone')
print("Region of South Wollo Zone:", region_of_zone)

# Get zone by specific woreda
zone_of_woreda = get_zone_by_woreda('Amhara Sayint')
print("Zone of Amhara Sayint:", zone_of_woreda)

# Get all woredas
all_woredas = get_all_woredas()
print("All Woredas:", all_woredas)
```