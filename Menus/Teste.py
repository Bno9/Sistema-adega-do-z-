import sqlite3

con = sqlite3.connect("estoque.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER,
    preco REAL
)
""")

cur.execute("INSERT INTO produtos (nome, quantidade, preco) VALUES (?, ?, ?)",
            ("Cerveja", 10, 5.50))

con.commit()

cur.execute("SELECT * FROM produtos")
for row in cur.fetchall():
    print(row)

con.close()
