# create_tables.py
import sqlite3

def create_tables():
    conn = sqlite3.connect('alumnos.db')
    cur = conn.cursor()
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS alumnos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            dni TEXT NOT NULL,
            email TEXT NOT NULL,
            edad INTEGER NOT NULL
        )
    ''')
    
    cur.execute('''
        CREATE TABLE IF NOT EXISTS materias (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alumno_id INTEGER,
            materia TEXT NOT NULL,
            turno TEXT NOT NULL,
            profesor TEXT NOT NULL,
            aula TEXT NOT NULL,
            comision TEXT NOT NULL,
            FOREIGN KEY(alumno_id) REFERENCES alumnos(id)
        )
    ''')
    
    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_tables()
