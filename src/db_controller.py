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

    def get_db_connection(self):
        try:
            connection = psycopg2.connect(
                host = self.host,
                port = self.port,
                user = self.user,
                password = self.password,
                dbname = self.database
            )

            return connection

        except psycopg2.DatabaseError as e:
            logger.error(f"The database connection was occured an error: {e}")
            return None
        
        except Exception as e:
            logger.error(f"An unexpected error while connecting to the database {e} ")
            return None

    def execute_query(self, query: str, include_cols: bool = False):
        conn = None
        cursor = None
        results = None
        
        try:
            conn = self.get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute(query)
                columns = tuple([desc[0] for desc in cursor.description]) if include_cols else None
                rows = cursor.fetchall()
                rows.insert(0, columns)
                results = rows.copy()

        except Exception as e:
            logger.error(f"Database error on executing query '{query}': {e}")
            return None
        
        finally:
            if cursor:
                cursor.close()
            if conn:
                conn.close()
            return results

       
