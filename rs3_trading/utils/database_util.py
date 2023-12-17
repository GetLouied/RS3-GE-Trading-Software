BASE_GE_DATABASE_NAME = r'rs3_{trading_data_type}_data'


class RS3TableDataType:
    Prices = 'price'
    Volumes = 'volume'


class RS3TableNameBuilder:
    def __init__(self, base_database_name: str = BASE_GE_DATABASE_NAME):
        self.base_database_name = base_database_name

    def __call__(self, RS_data_type: str):
        return self.base_database_name.format(trading_data_type=RS_data_type)
