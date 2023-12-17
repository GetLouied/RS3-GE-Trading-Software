BASE_URL = r'https://runescape.wiki/?title=Module:{data_type}/data.json&action=raw&ctype=application%2Fjson'


class RSDataType:
    Prices = 'GEPrices'
    Volumes = 'GEVolumes'


class RS3UrlBuilder:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url

    def __call__(self, RS_data_type: str):
        return self.base_url.format(data_type=RS_data_type)
