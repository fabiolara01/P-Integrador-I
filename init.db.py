import sqlite3

connection  = sqlite3.connect('database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()

cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Reclamação', 'Conteudo da reclamação')
            )
cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
            ('Elogio', 'Content for the second post')
            )
cur.execute("INSERT INTO posts (title, contato, email, content, tipo) VALUES (?, ?, ?, ?, ?)",
            ('Fabio', '991323344', 'fabio@fabiocombr', 'prof de capoeira', 'V' )
            )
cur.execute("INSERT INTO posts (title, contato, email, content, tipo) VALUES (?, ?, ?, ?, ?)",
            ('Mateus', '991990000', 'mateusmateuscombr', 'jogador de futebol', 'V')
            )
connection.commit()
connection.close()
