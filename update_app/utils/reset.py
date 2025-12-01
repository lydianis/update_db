import os
import shutil

def reset_db():
    """Setzt die Datenbank auf den Anfangszustand zurück (db_start.sqlite3 → db.sqlite3)."""
    db_current = 'db.sqlite3'
    db_start = 'db_start.sqlite3'
    
    # Backup der aktuellen DB erstellen (optional)
    if os.path.exists(db_current):
        shutil.copy(db_current, 'db_tmp.sqlite3')
        print(f"Backup erstellt: db_tmp.sqlite3")
    
    # db_start.sqlite3 zu db.sqlite3 kopieren
    if os.path.exists(db_start):
        shutil.copy(db_start, db_current)
        print(f"Datenbank zurückgesetzt: {db_current}")
    else:
        print(f"Fehler: {db_start} nicht gefunden!")

