# 📦 Storage_app

Database-driven inventory system (Work in Progress)

Questo progetto è una applicazione di gestione magazzino generico
attualmente in fase di sviluppo.

L’obiettivo è costruire un sistema modulare, scalabile e
riutilizzabile, partendo dal backend e dalla logica dati
prima di passare alle interfacce utente.

---

## 🚧 Stato del progetto

🟡 **In corso (early-stage)**

Attualmente il progetto è focalizzato su:
- struttura del database
- gestione delle connessioni
- funzioni di inserimento dati
- preparazione delle query di ricerca

Le parti di interfaccia e API sono pianificate ma non ancora implementate.

---

## 🎯 Obiettivo finale

L’obiettivo a lungo termine è sviluppare:
- un backend solido e riutilizzabile
- un’API per l’accesso ai dati
- applicazioni client:
  - web (browser)
  - desktop
  - mobile (Android / iOS)

con gestione utenti e permessi.

---

## 🧠 Architettura attuale

Il progetto è organizzato in moduli separati per responsabilità.

### 🔹 Configurazione
Gestisce:
- modalità di utilizzo (locale o remoto)
- parametri di connessione

---

### 🔹 Connessione
Responsabile di:
- creazione della connessione al database
- inizializzazione del database se non esistente

---

### 🔹 Schema
Contiene:
- definizione delle tabelle
- struttura del database
- relazioni tra le entità

Tutte le `def` per la creazione delle tabelle sono centralizzate qui.

---

### 🔹 Manage
Contiene le funzioni operative:
- inserimento prodotti
- inserimento caratteristiche
- popolamento delle tabelle
- gestione dei dati

Attualmente include funzioni di inserimento.  
Le query di ricerca sono in fase di sviluppo e verranno integrate
progressivamente nello stesso modulo.

---

### 🔹 Ready (Setup Database)
Modulo di orchestrazione:
- unisce configurazione, connessione e schema
- permette il setup completo del database in un unico passaggio

---

### 🔹 Support Functions
Raccolta di funzioni di supporto condivise:
- utility
- validazioni
- funzioni riutilizzabili
- funzioni di debug


---

## 🧩 Funzionalità implementate (attuali)

- Configurazione ambiente (locale / remoto)
- Connessione e creazione database
- Creazione automatica delle tabelle
- Inserimento prodotti(semplice/composto)
- Inserimento caratteristiche(di qualsiasi genere ed unità di misura)
- Setup centralizzato del database

---

## 🔜 Sviluppi pianificati

- Query di ricerca avanzate
- Gestione utenti e autenticazione
- API REST
- Interfaccia web
- Applicazioni desktop
- Applicazioni mobile (Android / iOS)

---

## 🤖 Uso dell’Intelligenza Artificiale

L’Intelligenza Artificiale viene utilizzata come supporto allo sviluppo:
- per chiarire concetti
- per migliorare la struttura del codice
- come strumento di apprendimento continuo
- senior 'a cui chiedere suggerimenti strategici'
- archivio di codici (molti dei quali nuovi per me)

Il progetto è pensato come esercizio pratico
per consolidare competenze su:
- database
- backend
- architettura software

---

## 📌 Nota finale

Questo repository documenta un progetto reale in evoluzione.
Rispecchia tutta la mia filosofia dell'universatilità, un magazzino virtuale per tutto
dai prodotti semplici, complessi, caratteristiche di tutti i tipi.
Nella creazione mi sono ispirato al mio lavoro con gli alimenti,
quindi alla tracciabilità dei prodotti, però ho voluto renderlo 
universale, quindi utile con ogni tipo di oggetto, da usare sia in ambiente casalingo
che in un vero e prorpio luogo di lavoro con più persone.
Il punto forte, che può essere vista come una fragilità, è la scelta dell'user finale
per praticamente tutto, dalla password al tipo di caratteristica senza rendere alcun passaggio 
obbligatorio, se non quelli principali(database e prodotto).

La struttura è pensata per crescere nel tempo
e verrà aggiornata man mano che nuove funzionalità verranno aggiunte.

