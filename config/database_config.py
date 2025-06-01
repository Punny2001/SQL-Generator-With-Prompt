import os

class DatabaseConfig:
    db_type: str
    host: str
    port: str
    user: str
    password: str
    database: str
    
    def __init__(self):
        self.db_type = "postgresql"
        self.host = os.getenv("DB_HOST")
        self.port = os.getenv("DB_PORT")
        self.user = os.getenv("DB_USER")
        self.password = os.getenv("DB_PASSWORD")
        self.database = os.getenv("DB_NAME")
