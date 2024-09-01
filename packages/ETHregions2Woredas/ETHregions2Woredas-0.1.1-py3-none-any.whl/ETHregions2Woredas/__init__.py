import json
import pkg_resources

# Load data from JSON file
data_path = pkg_resources.resource_filename('ETHregions2Woredas', 'data.json')
with open(data_path) as f:
    REGIONS_DATA = json.load(f)

# Load data from JSON file
# with open('ETHregions2Woredas/data.json') as f:
#     REGIONS_DATA = json.load(f)

def get_all_regions():
    return list(REGIONS_DATA.keys())

def get_all_zones():
    return {region: list(zones.keys()) for region, zones in REGIONS_DATA.items()}

def get_zones_by_region(region_name):
    return list(REGIONS_DATA.get(region_name, {}).keys())

def get_woredas_by_zone(zone_name):
    for zones in REGIONS_DATA.values():
        if zone_name in zones:
            return zones[zone_name]
    return []

def get_woredas_by_region(region_name):
    return [woreda for zones in REGIONS_DATA.get(region_name, {}).values() for woreda in zones]

def get_woredas_by_region_and_zone(region_name, zone_name):
    return REGIONS_DATA.get(region_name, {}).get(zone_name, [])

def get_region_by_woreda(woreda_name):
    for region, zones in REGIONS_DATA.items():
        for zone, woredas in zones.items():
            if woreda_name in woredas:
                return region
    return None

def get_region_by_zone(zone_name):
    for region, zones in REGIONS_DATA.items():
        if zone_name in zones:
            return region
    return None

def get_zone_by_woreda(woreda_name):
    for zones in REGIONS_DATA.values():
        for zone, woredas in zones.items():
            if woreda_name in woredas:
                return zone
    return None

def get_all_woredas():
    return [woreda for zones in REGIONS_DATA.values() for woreda_list in zones.values() for woreda in woreda_list]