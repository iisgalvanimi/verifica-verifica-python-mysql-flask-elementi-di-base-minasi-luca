import sqlite3

# Funzione per creare la connessione al DB
def connect_db():
    return sqlite3.connect("insetti.db")

# Commit 1: Creare il database e caricare i dati iniziali
def create_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS insetti (
        id INTEGER PRIMARY KEY,
        nome_comune TEXT,
        ordine TEXT,
        dimensioni TEXT,
        alimentazione TEXT,
        habitat TEXT
    )
    """)
    
    # Dati iniziali
    insetti = [
        {"Nome comune": "Farfalla", "Ordine": "Lepidoptera", "Dimensioni": "2-10cm", "Alimentazione": "Nettare", "Habitat": "Giardini"},
        {"Nome comune": "Ape", "Ordine": "Hymenoptera", "Dimensioni": "1-2cm", "Alimentazione": "Nettare", "Habitat": "Fiori"},
        {"Nome comune": "Formica", "Ordine": "Hymenoptera", "Dimensioni": "2-5mm", "Alimentazione": "Nettare", "Habitat": "Insetti, Semi"},
        {"Nome comune": "Scarafaggio", "Ordine": "Blattodea", "Dimensioni": "1-5cm", "Alimentazione": "Resti organici", "Habitat": "Case"},
        {"Nome comune": "Mosca", "Ordine": "Diptera", "Dimensioni": "5-10mm", "Alimentazione": "Liquidi zuccherini", "Habitat": "Rifiuti"},
        {"Nome comune": "Zanzara", "Ordine": "Diptera", "Dimensioni": "5-10mm", "Alimentazione": "Sangue", "Habitat": "Ambienti umidi"},
        {"Nome comune": "Coccinella", "Ordine": "Coleoptera", "Dimensioni": "5-10mm", "Alimentazione": "Afidi", "Habitat": "Piante"},
        {"Nome comune": "Libellula", "Ordine": "Odonata", "Dimensioni": "5-10cm", "Alimentazione": "Altri insetti", "Habitat": "Acqua dolce"},
        {"Nome comune": "Grillo", "Ordine": "Orthoptera", "Dimensioni": "2-5cm", "Alimentazione": "Piante", "Habitat": "Terreno"},
        {"Nome comune": "Cavalletta", "Ordine": "Orthoptera", "Dimensioni": "3-5cm", "Alimentazione": "Piante", "Habitat": "Campi"}
    ]
    
    # Inserire i dati iniziali nel database
    for insetto in insetti:
        cursor.execute("""
        INSERT INTO insetti (nome_comune, ordine, dimensioni, alimentazione, habitat) 
        VALUES (?, ?, ?, ?, ?)
        """, (insetto["Nome comune"], insetto["Ordine"], insetto["Dimensioni"], insetto["Alimentazione"], insetto["Habitat"]))
    
    conn.commit()
    conn.close()


def fetch_all_insetti():
    try:
        conn = connect_db()  # Connetti al database
        cursor = conn.cursor()  # Crea il cursore per eseguire le query
        cursor.execute("SELECT * FROM insetti")  # Esegui la query
        rows = cursor.fetchall()  # Recupera tutti i risultati
        conn.close()  # Chiudi la connessione al database
        return rows  # Restituisci i risultati

    except sqlite3.Error as e:
        print(f"Errore nel recupero dei dati dal database: {e}")
        return None  # Se c'è un errore, restituisci None

# Commit 3: Inserire nuovi elementi nel DB
def insert_insetto():
    nome_comune = input("Nome comune: ")
    ordine = input("Ordine: ")
    dimensioni = input("Dimensioni: ")
    alimentazione = input("Alimentazione: ")
    habitat = input("Habitat: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO insetti (nome_comune, ordine, dimensioni, alimentazione, habitat) 
    VALUES (?, ?, ?, ?, ?)
    """, (nome_comune, ordine, dimensioni, alimentazione, habitat))
    conn.commit()
    conn.close()
    print("Insetto inserito con successo!")

def delete_insetto():
    try:
        # Chiedi all'utente di inserire l'ID dell'insetto da eliminare
        id_insetto = int(input("Inserisci l'ID dell'insetto da eliminare: "))
        
        # Connessione al database
        conn = connect_db()
        cursor = conn.cursor()

        # Verifica se l'ID esiste
        cursor.execute("SELECT * FROM insetti WHERE id = ?", (id_insetto,))
        insetto = cursor.fetchone()
        
        if insetto is None:
            print(f"Nessun insetto trovato con l'ID {id_insetto}.")
        else:
            # Elimina l'insetto con l'ID specificato
            cursor.execute("DELETE FROM insetti WHERE id = ?", (id_insetto,))
            conn.commit()
            print(f"Insetto con ID {id_insetto} eliminato con successo!")

        # Chiudi la connessione
        conn.close()
    
    except ValueError:
        print("Errore: L'ID deve essere un numero intero valido.")
    
    except sqlite3.Error as e:
        print(f"Errore nel database: {e}")

    