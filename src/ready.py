from connections import main_connections
from schema import create_table_prodotti, create_table_caratteristiche, create_table_prodotto_caratteristica, create_table_composti, create_table_cronologia, create_table_prodotti_p, create_table_caratteristiche_p, create_table_prodotto_caratteristica_p, create_table_cronologia_p
from support_functions import debug_print

#funzione per la creazione del setup tabelle

def setup_database():
    conn, config=main_connections()
    
    if config['type']=='sqlite':
        create_table_prodotti(conn)
        create_table_caratteristiche(conn)
        create_table_prodotto_caratteristica(conn)
        create_table_composti(conn)
        create_table_cronologia(conn)
        
    elif config['type']=='postgres':
        create_table_prodotti_p(conn)
        create_table_caratteristiche_p(conn)
        create_table_prodotto_caratteristica_p(conn)
        create_table_composti(conn)
        create_table_cronologia_p(conn)
        
    else:
        raise ValueError(f"Tipo di DB non supportato:{config['type']}")
        
    conn.close()
    
if __name__=='__main__':
    setup_database()
    debug_print('Magazzino pronto e tabelle create')
        