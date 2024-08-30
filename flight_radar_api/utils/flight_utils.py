from FlightRadar24 import FlightRadar24API


def get_region_bounds(api: FlightRadar24API):
    def get_subregion(regions_dict: dict):
        for region in regions_dict:
            if 'subzones' in regions_dict[region]:
                subregion = regions_dict[region]['subzones']
                yield from get_subregion(subregion)
            else:
                yield regions_dict[region], region

    zones = api.get_zones()

    return get_subregion(zones)

