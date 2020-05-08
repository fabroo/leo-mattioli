import sqlite3
import os



def agregarUsuario():
    KNOWN_FACES = './fotos'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "testdb.db")
    conn  = sqlite3.connect(db_path)
    c = conn.cursor()
    name = str(input('Nuevo nombre: '))
    hayFotos = False
    for dirname in os.listdir(KNOWN_FACES):
        if dirname == name:
            hayFotos = True
    if hayFotos:
        print('Ya hay fotos tuyas entrenadas.')
    else:
        print('No hay fotos tuyas. Recuerda cargarlas cuando termines de crear tu cuenta.')
    contra = int(input('Tu contraseña: '))
    c.execute(f'''INSERT INTO residents VALUES ({contra},'{name}')''')
    conn.commit()

