from datetime import date
import psycopg3
import sqlite3


#FUNZIONI PER SQLITE
#FUNZIONI PER CREAZIONE ECOSISTEMA PRODOTTI

def create_table_prodotti(conn):
    cursor=conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prodotto(
    id_prodotto INTEGER AUTOINCREMENT PRIMARY KEY,
    nome_prodotto TEXT UNIQUE NOT NULL,
    tipo TEXT CHECK(tipo IN ('semplice','composto')),
    note TEXT
    );
    ''')
    conn.commit()
    
def create_table_caratteristiche(conn):
    cursor=conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS caratteristiche(
    id_caratteristica INTEGER AUTOINCREMENT PRIMARY KEY,
    nome_caratteristica TEXT UNIQUE NOT NULL,
    tipo_valore TEXT CHECK(tipo_valore IN ('integer','float','date','text'))
    );
    ''')
    conn.commit()
    
def create_table_prodotto_caratteristica(conn):
    cursor=conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prodotto_caratteristica(
    id_prodotto INTEGER NOT NULL, 
    id_caratteristica INTEGER NOT NULL, 
    valore_text TEXT,
    valore_int INTEGER,
    valore_float REAL,
    valore_date DATE,
    unita_di_misura TEXT,
    data_inserimento DATE DEFAULT (DATE('now')),
    PRIMARY KEY (id_prodotto,id_caratteristica),
    FOREIGN KEY (id_caratteristica) REFERENCES caratteristiche(id_caratteristica),
    FOREIGN KEY (id_prodotto) REFERENCES prodotti(id_prodotto) ON DELETE CASCADE
    );
    ''')
    conn.commit()
    
#FUNZIONI PER CREAZIONE ECOSISTEMA PRODOTTI COMPLESSI
    
    
def create_table_composti(conn):
    cursor=conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS composti(
    id_prodotto_composto INTEGER NOT NULL,
    id_prodotto_componente INTEGER NOT NULL,
    quantita REAL,
    unita_misura TEXT,
    descrizione TEXT,
    PRIMARY KEY (id_prodotto_composto,id_prodotto_componente),
    FOREIGN KEY (id_prodotto_composto) REFERENCES prodotti(id_prodotto) ON DELETE CASCADE,
    FOREIGN KEY (id_prodotto_componente) REFERENCES prodotti(id_prodotto)
    );
    ''')
    conn.commit()
    
    #funzione per creazione tabella cronologia
    
def create_table_cronologia(conn):
    cursor=conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cronologia(
    id_cronologia INTEGER PRIMARY KEY AUTOINCREMENT,
    id_prodotto INTEGER NOT NULL,
    id_caratteristica INTEGER,
    id_prodotto_composto INTEGER
    nome_prodotto TEXT,
    nome_caratteristica TEXT,
    nome_prodotto_composto TEXT,
    tipo TEXT CHECK(tipo IN ('semplice','composto')),
    quantita REAL,
    descrizione TEXT,
    operazione TEXT CHECK(operazione IN ('aggiunto','tolto','modificato')),
    valore_text TEXT,
    valore_int INT,
    valore_float REAL,
    valore_date DATE,
    unita_di_misura TEXT,
    data_operazione DATE DEFAULT (DATE('now')),
    note_prodotto TEXT,
    note TEXT,
    id_utente INTEGER,
    nome_utente TEXT
    );
    ''')
    conn.commit()
    
    
    
    #FUNZIONI PER POSTGRES
#FUNZIONI PER CREAZIONE ECOSISTEMA PRODOTTI

def create_table_prodotti_p(conn):
    cursor=conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prodotto(
    id_prodotto SERIAL PRIMARY KEY,
    nome_prodotto TEXT UNIQUE NOT NULL,
    tipo TEXT CHECK(tipo IN ('semplice','composto')),
    note TEXT
    );
    ''')
    conn.commit()
    
def create_table_caratteristiche_p(conn):
    cursor=conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS caratteristiche(
    id_caratteristica SERIAL PRIMARY KEY,
    nome_caratteristica TEXT UNIQUE NOT NULL,
    tipo_valore TEXT CHECK(tipo_valore IN ('integer','float','date','text'))
    );
    ''')
    conn.commit()
    
def create_table_prodotto_caratteristica_p(conn):
    cursor=conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS prodotto_caratteristica(
    id_caratteristica INTEGER NOT NULL, 
    id_prodotto INTEGER NOT NULL, 
    valore_text TEXT,
    valore_int INTEGER,
    valore_float REAL,
    valore_date DATE,
    unita_di_misura TEXT,
    data_inserimento DATE DEFAULT CURRENT_DATE,
    PRIMARY KEY (id_prodotto,id_caratteristica),
    FOREIGN KEY (id_caratteristica) REFERENCES caratteristiche(id_caratteristica),
    FOREIGN KEY (id_prodotto) REFERENCES prodotti(id_prodotto) ON DELETE CASCADE
    );
    ''')
    conn.commit()    
    

    #funzione per creazione tabella cronologia
    
def create_table_cronologia_p(conn):
    cursor=conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cronologia(
    id_cronologia PRIMARY KEY SERIAL,
    id_prodotto INTEGER NOT NULL,
    id_caratteristica INTEGER,
    nome_prodotto TEXT,
    nome_caratteristica TEXT,
    quantita REAL,
    descrizione TEXT,
    operazione TEXT CHECK(operazione IN ('aggiungere','togliere','modificare')),
    valore_text TEXT,
    valore_int INT,
    valore_float REAL,
    valore_date DATE,
    unita_di_misura TEXT,
    data_operazione DATE DEFAULT CURRENT_DATE,
    note_prodotto TEXT,
    note TEXT,
    id_utente INTEGER,
    nome_utente TEXT
    );
    ''')
    conn.commit()