from support_functions import debug_print, debug_input, correct_name, correct_date, norm_int, norm_float, correct_text
from datetime import date
import sqlite3
import psycop3
 
#creazione file jason dove verranno aggiunti man mano tutti gli insert dei prodotti e caratteristiche così da avere una raccolta da 
#poter usare come suggerimenti durante le ricerche
    
suggerimento_prodotto='prodotto.json'
suggerimento_car='caratteristica.json'

def load_sugg_prodotto():
    try:
        with open(suggerimento_prodotto) as f:
            return json.loads(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        debug_print("File di salvataggio danneggiato, reimpostare suggerimenti")
        return []
    
def save_sugg_prodotto(pr_list):
     with open(suggerimento_prodotto, "w") as f: json.dump(pr_list, f, indent= 4)
            
      
            
def load_suggerimento_car():
    try:
        with open(suggerimento_car) as f:
            return json.loads(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        debug_print("File di salvataggio danneggiato, reimpostare suggerimenti")
        return []
    
def save_sugg_prodotto(cr_list):
     with open(suggerimento_car, "w") as f: json.dump(cr_list, f, indent= 4)
            
#creazione 
            
evento={
    'id_prodotto':None,
    'id_caratteristica':None,
    'id_prodotto_composto':None,
    'nome_prodotto':None, 
    'nome_caratteristica':None,
    'nome_prodotto_composto':None,
    'tipo':None,
    'quantita':None,
    'descrizione':None,
    'operazione':None,
    'valore_text':None,
    'valore_int':None,
    'valore_float':None,
    'valore_date':None,
    'unita_di_misura':None,
    'note_prodotto':None,
    'id_utente':None,
    'utente':None
}                       
    
# funzione per riconoscere il tipo di database(visto che si basa su due possibili scelte remoto/locale)

def db_type():
    if 'sqlite' in str(type(conn)):
        db_type='sqlite' 
        mancante="?"
    else:
        db_type='postgres'
        mancante="%s"
    return db_type, mancante

#creazione caratteristica e possibilità di dargli un tipo di valore ed inserire dopo quel valore in prodotto-caratteristica

def insert_caratteristica():
    cursor=conn.cursor()
    db_type, mancante=db_type()
   
    while True:
        nome=debug_input("Quale caratteristica vuoi aggiungere('stop' per uscire'): ")
        nome_caratteristica=correct_name(nome)
        debug_print("Scegli di che tipo è(opzionale):")
        debug_print("1) Numero intero")
        debug_print("2) Numero decimale")
        debug_print("3) Data")
        debug_print("4) Testo")
        debug_print("5) Nulla")
        scelta=debug_input("Inserisci un numero: ")
        if scelta==1:
            tipo_valore='integer'
        elif scelta==2:
            tipo_valore='float'
        elif scelta==3:
            tipo_valore='date'
        elif scelta==4:
            tipo_valore='text'
        elif scelta==5:
            tipo_valore=None
        else:
            debug_print('Perfavore inserire un numero della lista!')
            continue
            
            
        nome_check=f"SELECT id_caratteristica FROM caratteristiche WHERE nome_caratteristica={mancante}"
    
        cursor.execute(nome_check,(nome_caratteristica,))
        risultato=cursor.fetchone()
        if risultato:
            print(f"'{nome}' già presente nel magazzino")
            id_prodotto=risultato[0]
        else:
            if db_type=='sqlite':
                cursor.execute(f"""
                INSERT INTO caratteristiche (nome_caratteristica, tipo_valore) VALUES ({mancante}, {mancante})
                """    ,(nome_caratteristica, tipo_valore))
                id_caratteristica=cursor.lastrowid
            else:
                cursor.execute(f"""
                INSERT INTO caratteristiche (nome_caratteristica, tipo_valore) VALUES ({mancante}, {mancante})
                RETURNING id_caratteristica"""    ,(nome_caratteristica, tipo_valore))
                id_caratteristica=result[0] if result else None
            
            
        if tipo_valore is not None:
            
            while True:
                valore=debug_input("Inserisci il valore per '{nome}'('stop' per uscire): ")
                if valore.lower=='stop':
                    break
                elif tipo_valore=='integer':
                    try:
                        valore_int=norm_int(valore)
                        unita_misura=debug_input("Unità di misura(opzionale): ")
                        return valore_int, unita_misura
                    except:
                        print("Valore non valido, riprova")
                elif tipo_valore=='float':
                    try:
                        valore_float=norm_float(valore)
                        unita_misura=debug_input("Unità di misura(opzionale): ")
                        return valore_float, unita_misura
                    except:
                        print("Valore non valido, riprova")
                elif tipo_valore=='date':
                    try:
                        valore_date=correct_date(valore)
                        return valore_date
                    except:
                        print("Valori inseriti non validi, riprova")
                        
                elif tipo_valore=='text':
                    valore_text=correct_text(valore)
                    return valore_text
                
        cursor.execute(f"INSERT INTO prodotto_caratteristica(id_prodotto, id_caratteristica, valore_text, valore_int, valore_float, valore_date, unita_di_misura ) VALUES ({mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante})",(id_prodotto, id_caratteristica, valore_text, valore_int, valore_float, valore_date, unita_misura)
                       conn.commit()
        #salvataggio in cronologia, visto che viene inglobata poi in insert_prodotto viene salvata con nome ed id_prodotto              
        evento=evento.copy()
        evento['id_prodotto']=id_prodotto
        evento['nome_prodotto']=nome_prodotto
        if id_caratteristica is not None:
            evento['id_caratteristica']=id_caratteristica
        elif nome_caratteristica is not None:
            evento['id_caratteristica']=id_caratteristica
        elif valore_text is not None:
            evento['valore_text']=valore_text
        elif valore_int is not None:
            evento['valore_int']=valore_int
        elif valore_float is not None:
            evento['valore_float']=valore_float
        elif valore_date is not None:
            evento['valore_date']=valore_date
        elif unita_misura is not None:
            evento['unita_misura']=unita_misura
                                      
        cronologia_prodotto(evento)
        
        #salvataggio in lista suggerimenti
        cr_list=load_suggerimento_car()
        pr_list.append(nome_caratteristica)
        save_sugg_prodotto(cr_list)              
            
 # funzione per l'aggiunta a cronologia usando l'evento creato in precedenza                                           
                       
def cronologia_prodotto(evento):
     db_type, mancante=db_type()
     cursor=conn.cursor()
     cursor.execute("""
     INSERT INTO cronologia (id_prodotto, id_caratteristica,id_prodotto_composto, nome_prodotto, nome_caratteristica, nome_prodotto_composto, quantita, descrizione, operazione, valore_text, valore_int, valore_float, valore_date, unita_di_misura, note_prodotto, id_utente, utente) VALUES ({mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante}, {mancante})
     """, (
         evento.get('id_prodotto'),
         evento.get('id_caratteristica'),
         evento.get('id_prodotto_composto'),
         evento.get('nome_prodotto'),
         evento.get('nome_caratteristica'),
         evento.get('nome_prodotto_composto'),
         evento.get('tipo'),
         evento.get('quantita'), 
         evento.get('descrizione'), 
         evento.get('operazione'), 
         evento.get('valore_text'), 
         evento.get('valore_int'), 
         evento.get('valore_float'), 
         evento.get('valore_date'), 
         evento.get('unita_di_misura')
         evento.get('note_prodotto')
         evento.get('id_utente')
         evento.get('utente') ))
                       conn.commit()
     
#funzione per recuperare l'id prodotto dal nome, servirà per ricerche ma anche per inserire note postume
                       
def get_id_prodotto(nome_prodotto=None):
    db_type, mancante=db_type()
    if nome_prodotto is None:
        nome_prodotto=debug_input("Inserisci il nome del prodotto: ")
    nome_prodotto=correct_name(nome_prodotto)
    cursor=conn.cursor()
    cursor.execute(f"SELECT id_prodotto FROM prodotti WHERE nome_prodotto={mancante}", (nome_prodotto,))
    result=cursor.fetchone()
    if result:
        return result[0]
    else:
        print(f"{nome_prodotto} non trovato!")
        return None
                       
 #come sopra solo per note cronologia                      
        
def get_id_prodotto_cronologia(nome_prodotto=None):
    db_type, mancante=db_type()
    if nome_prodotto is None:
        nome_prodotto=debug_input("Inserisci il nome del prodotto: ")
    nome_prodotto=correct_name(nome_prodotto)
    cursor=conn.cursor()
    cursor.execute(f"SELECT id_prodotto FROM cronologia WHERE nome_prodotto={mancante}", (nome_prodotto,))
    result=cursor.fetchone()
    if result:
        return result[0]
    else:
        print(f"{nome_prodotto} non trovato!")
        return None
                       
  #funzione di inserimento note sia all'interno che all'esterno dei vari insert
                       
def gestione_note(id_prodotto=None, nome_prodotto=None):
    if id_prodotto is None:
        id_prodotto=get_id_prodotto(nome_prodotto)
    
    note=debug_input("Scrivi pure la tua nota: ")
    note=correct_text(nota)
                       
    db_type, mancante=db_type()
    cursor=conn.cursor
    cursor.execute(f"UPDATE prodotti SET note={mancante} WHERE id_prodotto={mancante}", (note, id_prodotto))
    conn.commit()
    debug_print("Successo")
    evento=evento.copy()
    evento['note_prodotto']=note
    evento['id_prodotto']=id_prodotto
    evento['nome_prodotto']=nome_prodotto
    cronologia_prodotto(evento)                   
                       
    #funzione per inserire prodotto
def insert_prodotto():
    cursor=conn.cursor()
    nome=debug_input('Cosa vuoi aggiungere al magazzino?: ')
    nome_prodotto=correct_name(nome)
    db_type, mancante=db_type()
   
    query_insert=f"""
        INSERT INTO prodotti (nome_prodotto, tipo, note) VALUES ({mancante}, 'semplice', {mancante})
        """    
    nome_check=f"SELECT id_prodotto FROM prodotti WHERE nome_prodotto={mancante}"
    
    cursor.execute(nome_check,(nome_prodotto,))
    risultato=cursor.fetchone()
    if risultato:
        print(f"'{nome}' già presente nel magazzino")
        id_prodotto=risultato[0]
    else:
        if db_type=='sqlite':
            cursor.execute(f"""
            INSERT INTO prodotti (nome_prodotto, tipo, note) VALUES ({mancante}, 'semplice', {mancante})
            """    ,(nome_prodotto, note))
            id_prodotto=cursor.lastrowid
        else:
            cursor.execute(f"""
            INSERT INTO prodotti (nome_prodotto, tipo, note) VALUES ({mancante}, 'semplice', {mancante})
            RETURNING id_prodotto"""    ,(nome_prodotto, note))
            result=cursor.fetchone()
            if not result:
                       raise Exception("Errore di recupero ID!")
            id_prodotto=result[0]
        conn.commit()
        debug_print(f"Prodotto '{nome}' inserito con ID {id_prodotto}.")
    #inserimento in cronologia
    evento=evento.copy()
    evento['id_prodotto']=id_prodotto
    evento['nome_prodotto']=nome_prodotto
    evento['tipo']='semplice'
    evento['operazione']='aggiunto'
    cronologia_prodotto(evento)
    #aggiunge le funzioni per cronologia, note e lista suggerimenti
    insert_caratteristica()
    gestione_note(id_prodotto, nome_prodotto)
    pr_list=load_sugg_prodotto()
    pr_list.append(nome_prodotto)
    save_sugg_prodotto(pr_list) 
    
    return id_prodotto
 
   #funzione per correlazione tra prodotto composto a vari prodotti semplici(componenti)                    
def correlazioni(id_prodotto, nome_prodotto):
    cursor=conn.cursor
    db_type, mancante=db_type()
    
    while True:
        nome_componente=correct_name(debug_input("Inserisci il nome del prodotto da aggiungere al composto(opzionale): "))
        if nome_componente == "":
            break
        id_componente=get_id_prodotto(nome_prodotto=nome_componente)
        quantita=norm_float(debug_input("Quantità(opzionale): "))
        unita=correct_name(debug_input("Unità di misura(opzionale): "))
        descrizione=correct_text(debug_input("Vuoi aggiungere una descrizione?: "))
        cursor.execute(f" INSERT INTO composti(id_prodotto_composto, id_prodotto_componente, quantita, unita_di_misura, descrizione) VALUES ({mancante}, {mancante},{mancante},{mancante},{mancante})",(id_prodotto, id_componente, quantita, unita, descrizione))
        conn.commit()
        debug_print(f"{nome_componente} aggiunto con successo a {nome_composto}")
        evento=evento.copy()
        evento.update({
            'id_prodotto'=id_componente
            'nome_prodotto'=nome_componente
            'id_prodotto_composto'=id_prodotto,
            'nome_prodotto_composto'=nome_prodotto,
            'quantita'=quantita
            'descrizione'=descrizione
            'operazione'='aggiunto'
            'unita_di_misura'=unita
        })
        cronologia_prodotto(evento)               
                       
                       
                       
   #insert del prodotto composto                    
                       
def insert_prodotto_composto():
    cursor=conn.cursor()
    nome=debug_input('Cosa vuoi aggiungere al magazzino?: ')
    nome_prodotto=correct_name(nome)
    db_type, mancante=db_type()
   
    query_insert=f"""
        INSERT INTO prodotti (nome_prodotto, tipo, note) VALUES ({mancante}, 'composto', {mancante})
        """    
    nome_check=f"SELECT id_prodotto FROM prodotti WHERE nome_prodotto={mancante}"
    
    cursor.execute(nome_check,(nome_prodotto,))
    risultato=cursor.fetchone()
    if risultato:
        print(f"'{nome}' già presente nel magazzino")
        id_prodotto=risultato[0]
    else:
        if db_type=='sqlite':
            cursor.execute(f"""
            INSERT INTO prodotti (nome_prodotto, tipo, note) VALUES ({mancante}, 'semplice', {mancante})
            """    ,(nome_prodotto, note))
            id_prodotto=cursor.lastrowid
        else:
            cursor.execute(f"""
            INSERT INTO prodotti (nome_prodotto, tipo, note) VALUES ({mancante}, 'semplice', {mancante})
            RETURNING id_prodotto"""    ,(nome_prodotto, note))
            result=cursor.fetchone()
            if not result:
                       raise Exception("Errore di recupero ID!")
            id_prodotto=result[0]
        conn.commit()
        debug_print(f"Prodotto '{nome}' inserito con ID {id_prodotto}.")
    #inserimento in cronologia del prodotto composto
    evento=evento.copy()
    evento['id_prodotto']=id_prodotto
    evento['nome_prodotto']=nome_prodotto
    evento['tipo']='composto'
    evento['operazione']='aggiunto'
    cronologia_prodotto(evento)
    #aggiunta di eventuali caratteristiche
    insert_caratteristica()
    gestione_note(id_prodotto, nome_prodotto)
    #varie correlazioni tra prodotti
    correlazioni(id_prodotto_composto, nome_prodotto_composto)
    #salvataggi per lista suggerimenti
    pr_list=load_sugg_prodotto()
    pr_list.append(nome_prodotto)
    save_sugg_prodotto(pr_list) 
    
    return id_prodotto                      
#funzione per aggiungere note in cronologia
                       
def note_cronologia(nome_prodotto=None):
    cursor=conn.cursor()
    db_type, mancante=db_type()
                       
    if nome_prodotto is None:
        nome=debug_input('Dove vuoi aggiungere la nota?: ')
        nome_prodotto=correct_name(nome)
    
    id_prodotto=get_id_prodotto_cronologia(nome_prodotto)
    note=correct_text(debug_input("Inserisci la tua nota: "))
    cursor.execute("""
    INSERT INTO cronologia (id_prodotto, nome_prodotto, note) VALUES ({mancante}, {mancante}, {mancante})""", (id_prodotto, nome_prodotto, note))
    conn.commit()
    debug_print("Nota aggiunta con successo.")
                       
                       
