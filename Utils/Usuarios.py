import sqlite3
import bcrypt
from Utils.Resultado import Resultado


class Usuario:
    def __init__(self, con: sqlite3.Connection):
        self.con = con
        self.cur = self.con.cursor()
        self._criar_tabela()

        self.cadastrar_usuario("Joao", "1") #teste
        self.cadastrar_usuario("Lucas", "1") #teste
        self.cadastrar_usuario("Pedro", "1") #teste

    def _criar_tabela(self):
        """Cria a tabela usuarios e adiciona o usuario "sistema" caso ainda nao exista"""

        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT NOT NULL UNIQUE,
                senha TEXT NOT NULL,
                cargo TEXT NOT NULL
            )
        """)
        self.con.commit()

        self.cur.execute(
            "SELECT 1 FROM usuarios WHERE usuario = ?",
            ("Sistema",)
        )
        existe = self.cur.fetchone()

        if not existe:
            hash_senha = self._gerar_hash("123")
            self.cur.execute(
                "INSERT INTO usuarios (usuario, senha, cargo) VALUES (?, ?, ?)",
                ("Sistema", hash_senha, "admin")
            )
            self.con.commit()

    def _gerar_hash(self, senha: str) -> str:
        senha_bytes = senha.encode("utf-8")
        hash_bytes = bcrypt.hashpw(senha_bytes, bcrypt.gensalt())
        return hash_bytes.decode("utf-8")

    def _verificar_senha(self, senha_digitada: str, hash_salvo: str) -> bool:
        return bcrypt.checkpw(
            senha_digitada.encode("utf-8"),
            hash_salvo.encode("utf-8")
        )

    def cadastrar_usuario(self, usuario, senha, cargo="funcionario"):
        hash_senha = self._gerar_hash(senha)

        try:
            self.cur.execute(
                "INSERT INTO usuarios (usuario, senha, cargo) VALUES (?, ?, ?)",
                (usuario, hash_senha, cargo)
            )
            self.con.commit()
            return Resultado(True, "Usuário cadastrado com sucesso", "sucesso")
        except sqlite3.IntegrityError:
            return Resultado(False, "Usuário já existe", "erro")

    def verificar_login(self, usuario:str, senha:str) -> tuple:
        self.cur.execute(
            "SELECT * FROM usuarios WHERE usuario = ?",
            (usuario,)
        )
        resultado = self.cur.fetchone()

        if not resultado:
            return Resultado(False, "Usuario nao encontrado", "info")

        _, nome, hash_salvo, cargo = resultado

        if self._verificar_senha(senha, hash_salvo):
            return True, nome, cargo # retorno inconsistente que vou precisar arrumar dps de definir como vai ser a interface

        return Resultado(False, "")
    
    def alterar_senha(self, usuario: str, senha_atual: str, nova_senha: str):
        self.cur.execute(
            "SELECT senha FROM usuarios WHERE usuario = ?",
            (usuario,)
        )
        resultado = self.cur.fetchone()

        if not resultado:
            return Resultado(False, "Usuário não encontrado", "erro")

        hash_atual = resultado[0]

        if not self._verificar_senha(senha_atual, hash_atual):
            return Resultado(False, "Senha atual incorreta", "aviso")
        
        novo_hash = self._gerar_hash(nova_senha)
        self.cur.execute(
            "UPDATE usuarios SET senha = ? WHERE usuario = ?",
            (novo_hash, usuario)
        )
        self.con.commit()

        return Resultado(True, "Senha alterada com sucesso", "sucesso")


    def listar_usuarios(self):
        self.cur.execute(
            "SELECT usuario, cargo FROM usuarios"
        )
        return self.cur.fetchall()