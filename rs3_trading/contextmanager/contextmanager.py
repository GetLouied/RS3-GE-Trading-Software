import duckdb


class DuckDBCM:
    def __init__(self, file_name: str):
        self.file_name = file_name
        self.connection = duckdb.connect(self.file_name)

    def __enter__(self):
        return self.connection.cursor()

    def __exit__(self, exc_type, exc_value, traceback):
        self.connection.commit()
        self.connection.close()