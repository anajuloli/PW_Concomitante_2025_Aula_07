CREATE_TABLE = '''
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    peso REAL NOT NULL,
    altura REAL NOT NULL,
    nivel_atividade TEXT NOT NULL
)
'''

INSERT_USUARIO = '''
INSERT INTO usuarios (nome, email, peso, altura, nivel_atividade)
VALUES (?, ?, ?, ?, ?)
'''

SELECT_USUARIO = '''
SELECT id, nome, email, peso, altura, nivel_atividade
FROM usuarios
WHERE id = ?
'''

SELECT_TODOS_USUARIOS = '''
SELECT id, nome, email, peso, altura, nivel_atividade
FROM usuarios
'''

UPDATE_USUARIO = '''
UPDATE usuarios
SET nome = ?, email = ?, peso = ?, altura = ?, nivel_atividade = ?
WHERE id = ?
'''

DELETE_USUARIO = '''
DELETE FROM usuarios
WHERE id = ?
'''