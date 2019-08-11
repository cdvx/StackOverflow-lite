
import psycopg2

class DatabaseConnection:
    """Class to manage database connection"""

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(DatabaseConnection, cls).__new__(cls)
        return cls.instance

    def __init__(self, url=None):
        self.db_url = url
        if self.db_url:
            try:
                self.connection = psycopg2.connect(self.db_url, sslmode='allow')
                self.connection.autocommit = True
                self.cursor = self.connection.cursor()
            except Exception as e: #pragma: no cover
                print("Cannot connect to database", e)
        else: #pragma: no cover
            print('Could not connect to database\nReason: Database url not provided!')
