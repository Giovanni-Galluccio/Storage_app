import psycopg3
import sqlite3
from support_functions import connect_database, open_or_create_database, debug_print
from config import config 

#unione delle funzioni di configurazione e creazione/apertura database


def main_connection():
    config=get_config()
    db_name=open_or_create_database()
    
    try:
        connection=connect_database(config, db_name)
        debug_print(f"Connessione al database '{db_name}' riuscita")
        return connection
    
    except Exception as e:
        raise ConnectionError(f"Errore di connessione al database '{db_name}': {e}")
    
if __name__ == "__main__":
    conn=main_connection()
   
    
        

    