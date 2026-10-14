import sqlite3
from flask import g
from apiflask import APIFlask

# app = APIFlask(__name__)
# DB_NAME = "banco.db"


# def get_db():
#     """Abre uma nova conexão se ainda não existir para a requisição atual."""
#     if "db" not in g:
#         g.db = sqlite3.connect(DB_NAME)
#         g.db.row_factory = sqlite3.Row  # Facilita converter para dict
#     return g.db


# @app.teardown_appcontext
# def close_db(exception=None):
#     """Executado automaticamente pelo Flask ao final de cada requisição."""
#     db = g.pop("db", None)
#     if db is not None:
#         db.close()

# @app.get("/avicultores")
# def get_avicultores():
#     db = get_db()
#     cursor = db.cursor()
#     cursor.execute("SELECT * FROM tb_avicultores")
#     rows = cursor.fetchall()

#     avicultores = [dict(row) for row in rows]
#     return avicultores, 200


# @app.post("/avicultores")
# def criar_avicultor(data):
#     db = get_db()
#     with db:  # Garante commit automático aqui
#         cursor = db.cursor()
#         cursor.execute(
#             "INSERT INTO tb_avicultores (nome, nascimento, cpf, caf) VALUES (?, ?, ?, ?)",
#             (data["nome"], data["nascimento"], data["cpf"], data["caf"]),
#         )
#     # E o close() é chamado sozinho ao fim da requisição pelo @app.teardown_appcontext
#     return {"id": cursor.lastrowid}, 201