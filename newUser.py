import sqlite3
import os
from random import randint

import smtplib
from email.mime.text import MIMEText

def agregarUsuario(dni, name, mail, companyId):
    def randomPass(n):
        a = ''
        for i in range(n):
            b = str(randint(0,9))
            a +=b
        c = int(a)
        return c


    KNOWN_FACES = './fotos'
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, "testdb.db")
    conn  = sqlite3.connect(db_path)
    c = conn.cursor()
    # dni = str(input('Tu DNI: '))
    # name = str(input('Nuevo nombre: '))
    # mail = str(input("Tu E-Mail: "))

    c.execute(f'''SELECT dni FROM residents WHERE company = '{companyId}' ''')
    dniList = c.fetchall()
    dniListClean = []
    for el in dniList:
        el = str(el)
        el = el[:-2]
        el = el[1:]
    dniListClean.append(el)
    if dni in dniListClean:
        hayFotos = False
        for dirname in os.listdir(KNOWN_FACES):
            if dirname == dni:
                hayFotos = True
        if hayFotos:
            print('Ya hay fotos tuyas entrenadas.')
        else:
            print('No hay fotos tuyas. Recuerda cargarlas cuando termines de crear tu cuenta.')
        
        contra = randomPass(7)

        c.execute(f''' UPDATE residents SET name = '{name}', password = {contra}, email = '{mail}'  WHERE dni = {int(dni)} ''')
        print('Bienvenido ' + name + ', con DNI: '+ dni +', y E-Mail: '+ mail + '. Se te asignó la contraseña: ' + str(contra))
        conn.commit()
        
        # context = ssl.SSLContext(ssl.PROTOCOL_SSLv3)

        smtp_ssl_host = 'smtp.gmail.com'  # smtp.mail.yahoo.com
        smtp_ssl_port = 465
        username = 'mattiolilearning@gmail.com'
        password = 'mattioli123'
        sender = 'mattiolilearning@gmail.com'
        targets = mail

        msg = MIMEText(f'Buenas Tardes, señor usuario. Sele informa que mi nombre es lionel mesi asuser vicio \nEn esta ocasion vengo a decirle que su contraseña es: {str(contra)}\nNo seas facha y cuidala porque si no te hacen el rancho y no esta bueno eso, me paso una vez y no lo recomiendo dale wachin te mando besos, saludame a la nena de mi parte\nBesos!')
        msg['Subject'] = 'Cuenta nueva registrada en Mattioli Learning'
        msg['From'] = sender
        msg['To'] = targets

        server = smtplib.SMTP_SSL(smtp_ssl_host, smtp_ssl_port)
        server.login(username, password)
        server.sendmail(sender, targets, msg.as_string())
        server.quit()
       
        return True
    else:
        print(' no estas autorizado aca mirey')
        return False
        
    

