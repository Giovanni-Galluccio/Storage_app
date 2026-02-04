from datetime import datetime, date
import logging
import psycopg3
import sqlite3
import json
import os

logging.basicConfig(level=logging.DEBUG)

def debug_print(msg):
    logging.debug(msg)
    
def debug_input(prompt, default=None):
    if logging.getLogger().isEnabledFor(logging.DEBUG):
        return input(prompt)
    return default

def correct_text(text):
    return text.lower()

def correct_name(text):
    return text.strip().lower()

def correct_date(date_str):
    if not date_str:
        return None
    formats=["%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y"]
    for fmt in formats:
        try:
            return datetime.strptime(date_str.strip(), fmt).date().isoformat()
        except ValueError:
            pass
            raise ValueError("Formato data non valido")
    
    
def today_date():
    return date.today().isoformat()

def norm_int(value):
    if not value or value=="":
        return None
    try:
        return int(value)
    except (ValueError, TypeError):
        raise ValueError("Valore non valido")
        
def norm_float(value):
    if not value:
        return None
    try:
        value=str(value).replace(",",".")
        return float(value)
    except (ValueError, TypeError):
        raise ValueError("Valore non valido")
        
     

    #funzioni di configurazione
    
def configure_postgres():
    host=debug_input("Host(default:localhost):  ", default="localhost")
    try:
        port=int(debug_input("Port(default:5432):  ", default="5432"))
    except ValueError:
        debug_print("Valore Port non valido, uso quello di default.")
        port= 5432
    user=debug_input("Utente(default:admin): ",default="admin")
    password=debug_input("Password(default:1234): ", default="1234")
   
    
    
    return{
        "type":"postgres",
        "host":host,
        "port":port,
        "user":user,
        "password":password
    }

   
def configure_sqlite():
    os.makedirs(base_path, exist_ok=True)
    return {"type":"sqlite", "base_path":"data/"}
    

def setup_config():
    db_type=debug_input("Che tipo di magazzino vuoi fare? 1= locale, 2= da remoto, (default:1)", default="1")
    
    if db_type=="1": config=configure_sqlite()
    else: config=configure_postgres()
    save=debug_input("Vuoi salvare le credenziali? (s/n):  ", default:"n")
    if save.lower()=="s":
        with open("config.json", "w") as f: json.dump(config, f, indent= 4)
            
    return config
        
def load_config():
    try:
        with open("config.json") as f:
            return json.loads(f)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        debug_print("Configurazione danneggiata, reinserire i parametri")
        return None
    
    
    #funzioni connessione database
    
databases= "databases.json"

def load_databases():
    try:
        with open(databases) as f:
            return json.loads(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        debug_print("File di salvataggio danneggiato, reimpostare databases")
        return []
    
def save_databases(db_list):
     with open(databases, "w") as f: json.dump(db_list, f, indent= 4)
    
def open_or_create_database():
    choice=debug_input("Vuoi aprire un magazzino esistente (A) o crearne uno nuovo (C)? ", default="A").lower()
    db_list=load_databases()
    db_name=None
    if choice == "a":
        if not db_list:
            debug_print("Nessun magazzino trovato, devi crearne uno nuovo")
            choice = "c"
        else:
            debug_print("I magazzini sono:")
            for i, db in enumerate(db_list, 1):
                print(f"{i}. {db}")
            while True:
                try:
                    index=int(debug_input("Seleziona il numero del magazzino: "))- 1
                    if 0 <= index < len(db_list): 
                        db_name=db_list[index]
                        break
                    else:
                        print("Numero non valido, riprova.")
                except ValueError: 
                    print("Inserisci un numero valido.")
    if choice == "c":
        db_name=correct_name(debug_input("Come vuoi chiamare il tuo magazzino? (default:magazzino): ", default= default_dbname(db_list)))
        db_list=load_databases()
        if db_name in db_list:
            debug_print(f"Attenzione il nome magazzino {db_name} esiste già!")
        else:
            db_list.append(db_name)
            save_databases(db_list)
            debug_print(f"Magazzino '{db_name}' creato con successo.")
        
    return db_name



def default_dbname(db_list, name="magazzino"):
    count=1
    while f"magazzino_{count}" in db_list:
        count +=1
    return f"magazzino_{count}"
        
       #Funzioni connessione
    
def connect_database(config, db_name=None):
    if config ["type"] == "postgres":
        try:
            conn= psycopg3.connect(
                host=config["host"],
                port=config["port"],
                user=config["user"],
                password=config["password"],
                dbname=db_name
            )
            debug_print(f"Connesso al server: {db_name}")
            return conn
        except psycopg.OperationalError as e:
            raise ConnectionError(f"Errore: {e}")
        except Exception as e:
            raise ConnectionError(f"Errore generico: {e}")
    elif config["type"] == "sqlite":
        path= os.path.join(config.get("base_path",""), db_name+".db")
        try:
            conn=sqlite3.connect(path)
            debug_print(f"Creato in locale: {path}")
            return conn
        except sqlite3.OperationalError as e:
            raise ConnectionError(f"Errore: {e}")
        except Exception as e:
            raise ConnectionError(f"Errore generico:{e}")
    else:
        raise ValueError(f"Tipo di database '{config['type']}' non supportato")