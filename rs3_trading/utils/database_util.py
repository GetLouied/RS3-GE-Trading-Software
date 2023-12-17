BASE_GE_DATABASE_NAME = r'rs3_{trading_data_type}_data'
BASE_GE_COLUMN_NAMES = ['time', 'item', 'item_name', r'{trading_data_type}']


class RS3TableBuilder:
    def __init__(self, base_database_name: str = BASE_GE_DATABASE_NAME, base_column_names: list = BASE_GE_COLUMN_NAMES):
        self.base_column_names = base_column_names
        self.base_database_name = base_database_name

    def __call__(self, RS_data_type: str):
        return self.base_column_names.format(trading_data_type=RS_data_type), self.base_database_name.format(trading_data_type=RS_data_type)
