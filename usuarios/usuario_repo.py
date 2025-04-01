from typing import List, Optional
import sqlite3
from usuarios.usuario import Usuario
from usuarios import usuario_sql as sql
from util import get_db_connection

class UsuarioRepo:
    def __init__(self):
        self._criar_tabela()

    def _criar_tabela(self):
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.CREATE_TABLE)
        except sqlite3.Error as e:
            print(f"Erro ao criar tabela: {e}")

    def adicionar(self, usuario: Usuario) -> Optional[int]:
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.INSERT_USUARIO, (usuario.nome, usuario.email, usuario.peso, 
                                                   usuario.altura, usuario.nivel_atividade))
                return cursor.lastrowid
        except sqlite3.Error as e:
            print(f"Erro ao adicionar usuário: {e}")
            return None

    def obter(self, usuario_id: int) -> Optional[Usuario]:
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.SELECT_USUARIO, (usuario_id,))
                row = cursor.fetchone()
                if row:
                    return Usuario(id=row[0], nome=row[1], email=row[2], peso=row[3], 
                                  altura=row[4], nivel_atividade=row[5])
                return None
        except sqlite3.Error as e:
            print(f"Erro ao obter usuário {usuario_id}: {e}")
            return None

    def obter_todos(self) -> List[Usuario]:
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.SELECT_TODOS_USUARIOS)
                rows = cursor.fetchall()
                return [Usuario(id=row[0], nome=row[1], email=row[2], peso=row[3], 
                               altura=row[4], nivel_atividade=row[5]) for row in rows]
        except sqlite3.Error as e:
            print(f"Erro ao obter todos os usuários: {e}")
            return []

    def atualizar(self, usuario: Usuario) -> bool:
        if usuario.id is None:
            print("Erro: Usuário sem ID não pode ser atualizado.")
            return False
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.UPDATE_USUARIO, (usuario.nome, usuario.email, usuario.peso, 
                                                   usuario.altura, usuario.nivel_atividade, usuario.id))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao atualizar usuário {usuario.id}: {e}")
            return False

    def excluir(self, usuario_id: int) -> bool:
        try:
            with get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(sql.DELETE_USUARIO, (usuario_id,))
                return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Erro ao excluir usuário {usuario_id}: {e}")
            return False