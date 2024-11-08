import sqlite3


def connect_db():
    return sqlite3.connect("insetti.db")


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
    
   
    for insetto in insetti:
        cursor.execute("""
        INSERT INTO insetti (nome_comune, ordine, dimensioni, alimentazione, habitat) 
        VALUES (?, ?, ?, ?, ?)
        """, (insetto["Nome comune"], insetto["Ordine"], insetto["Dimensioni"], insetto["Alimentazione"], insetto["Habitat"]))
    
    conn.commit()
    conn.close()


def fetch_all_insetti():
    try:
        conn = connect_db() 
        cursor = conn.cursor()  
        cursor.execute("SELECT * FROM insetti") 
        rows = cursor.fetchall() 
        conn.close() 
        return rows  

    except sqlite3.Error as e:
        print(f"Errore nel recupero dei dati dal database: {e}")
        return None  # Se c'è un errore, restituisci None

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
        id_insetto = int(input("Inserisci l'ID dell'insetto da eliminare: "))
        
        
        conn = connect_db()
        cursor = conn.cursor()

        
        cursor.execute("SELECT * FROM insetti WHERE id = ?", (id_insetto,))
        insetto = cursor.fetchone()
        
        if insetto is None:
            print(f"Nessun insetto trovato con l'ID {id_insetto}.")
        else:
           
            cursor.execute("DELETE FROM insetti WHERE id = ?", (id_insetto,))
            conn.commit()
            print(f"Insetto con ID {id_insetto} eliminato con successo!")

       
        conn.close()
    
    except ValueError:
        print("Errore: L'ID deve essere un numero intero valido.")
    
    except sqlite3.Error as e:
        print(f"Errore nel database: {e}")



def filter_insetti():
    caratteristica = input("Inserisci la caratteristica da filtrare (e.g. 'dimensioni' o 'habitat'): ")
    valore = input(f"Inserisci il valore da cercare per {caratteristica}: ")
    
    conn = connect_db()
    cursor = conn.cursor()
    query = f"SELECT * FROM insetti WHERE {caratteristica} LIKE ?"
    cursor.execute(query, ('%' + valore + '%',))
    rows = cursor.fetchall()
    conn.close()
    
    if rows:
        for row in rows:
            print(row)
    else:
        print("Nessun insetto trovato con questa caratteristica.")



def menu():
    while True:
        print("\n*** Menu ***")
        print("1. Carica dati iniziali")
        print("2. Estrai tutti i dati")
        print("3. Inserisci nuovo insetto")
        print("4. Elimina insetto per ID")
        print("5. Filtra insetti per caratteristica")
        print("6. Aggiorna insetto per ID")
        print("7. Esci")

        scelta = input("Scegli un'opzione: ")

        if scelta == "1":
            create_table()
            print("Dati iniziali caricati con successo.")
        elif scelta == "2":
            insetti = fetch_all_insetti()
            for insetto in insetti:
                print(insetto)
        elif scelta == "3":
            insert_insetto()
        elif scelta == "4":
            delete_insetto()
        elif scelta == "5":
            filter_insetti()
        elif scelta == "6":
            update_insetto()
        elif scelta == "7":
            print("Uscita...")
            break
        else:
            print("Opzione non valida. Riprova.")



def update_insetto():
    id_insetto = int(input("Inserisci l'ID dell'insetto da aggiornare: "))
    colonna = input("Quale colonna desideri aggiornare (nome_comune, ordine, dimensioni, alimentazione, habitat)? ")
    nuovo_valore = input(f"Inserisci il nuovo valore per {colonna}: ")

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(f"UPDATE insetti SET {colonna} = ? WHERE id = ?", (nuovo_valore, id_insetto))
    conn.commit()
    conn.close()
    print(f"Insetto aggiornato con successo!")



if __name__ == "__main__":
    menu()


    