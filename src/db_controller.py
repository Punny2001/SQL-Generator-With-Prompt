import psycopg2
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class DatabaseController:
    
    def __init__(self, config):
        self.db_type = config.db_type
        self.host = config.host
        self.port = config.port
        self.user = config.user
        self.password = config.password
        self.database = config.database

        self.conn = None

    def get_db_connection(self):
        if self.conn and not self.conn.closed():
            return self.conn
        try:
            self.conn = psycopg2.connect(
                host = self.host,
                port = self.port,
                user = self.user,
                password = self.password,
                dbname = self.database
            )

            print("Database is connected.")
            return self.conn

        except psycopg2.DatabaseError as e:
            error = f"The database connection was occured an error: {e}"
            logger.error(error)
            return error
        
        except Exception as e:
            error = f"An unexpected error while connecting to the database {e} "
            logger.error(error)
            return error

    def execute_query(self, query: str, include_cols: bool = False):
        conn = None
        cursor = None
        results = None
        
        try:
            self.conn = self.get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute(query)
                columns = tuple([desc[0] for desc in cursor.description]) if include_cols else None
                rows = cursor.fetchall()
                rows.insert(0, columns)
                results = rows.copy()

        except Exception as e:
            error = f"Database error on executing query '{query}': {e}"
            logger.error(error)
            return error
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return results


    def close_connection(self):
        if self.conn and not self.conn.closed:
            self.conn.close()
            self.conn = None
            print("Database connection was closed.")
