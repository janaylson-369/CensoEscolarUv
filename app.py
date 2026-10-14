from flask import Flask, jsonify, render_template, request
from models.instituicaoensino import InstituicaoEnsino, InstituicaoEnsinoSchema
from models.usuarios import Usuarios
from helpers.file.json import read,write
from pathlib import Path
import sqlite3
from marshmallow import ValidationError
from helpers.database import get_connection, close_db
from http import HTTPStatus


BASE_DIR = Path(__file__).resolve().parent
arquivoD = BASE_DIR / "instituicoes.json"
arquivoUsuarios = BASE_DIR / "usuarios.json"


app = Flask(__name__)
#  fechamento automatico da conexão
app.teardown_appcontext(close_db)

#Marshmallow
instituicao_schema = InstituicaoEnsinoSchema()
instituicoes_schema = InstituicaoEnsinoSchema(many=True)


def listarUsuarios():
    dataset = read(arquivoUsuarios)
    usuarioss = [Usuarios(
        row["id"], row["nome"], row["idade"], row["cpf"]) for row in dataset]
    return usuarioss

def salvaUsuarios(usuarios):
    write(arquivoUsuarios, [usr.toDict() for usr in usuarios])
    


@app.route('/')
def index():
    conn = get_connection()
    posts = conn.execute('SELECT * FROM posts').fetchall()
    return render_template('index.html', posts=posts)


@app.route("/health")
def health():
    return {"health": "ok"}, 200



@app.get("/instituicoesensino")
def getAllInstituicoes():
    # Abrir a conexão com o banco de dados.
    connection = get_connection()
    cursor = connection.cursor()
    # Executar as DML de consulta
    cursor.execute(f'SELECT * FROM tb_instituicao_ensino WHERE ativo = 1')
    dataset = cursor.fetchall()
    
    instituicoes = instituicoes_schema.dump([dict(row) for row in dataset])
    
    return jsonify(instituicoes), HTTPStatus.OK



@app.get("/instituicoesensino/<int:id>")
def getByIdInstituicoes(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tb_instituicao_ensino WHERE id = ? AND ativo = 1', (id,))
    row = cursor.fetchone()

    if row is None:
        return {'mensagem': 'Instituição de ensino não encontrada'}, HTTPStatus.NOT_FOUND

    resultado = instituicao_schema.dump(dict(row))
    
    return jsonify(resultado), HTTPStatus.OK


@app.post("/instituicoesensino")
def postInstituicoes():
    try: 
        data = instituicao_schema.load(request.get_json(), partial=False)
        connection = get_connection()
        with connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO tb_instituicao_ensino (no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) RETURNING id, created',
                        (data.get("no_entidade"), data.get("co_entidade"), data.get("no_uf"),
                        data.get("sg_uf"), data.get("co_uf"), data.get("no_municipio"),
                        data.get("co_municipio"), data.get("nu_ano_censo"), data.get("qt_mat_bas"),
                        data.get("qt_mat_inf"), data.get("qt_mat_fund"), data.get("qt_mat_med"),
                        data.get("qt_mat_prof"), data.get("qt_mat_eja"), data.get("qt_mat_esp")))

            resultset = cursor.fetchone()
            
    except ValidationError as err:
        return { "erro": "Dados inválidos", "campos": err.messages}, 400

    return jsonify({"id": resultset["id"],"created": resultset["created"],**data}), HTTPStatus.CREATED



@app.put("/instituicoesensino/<int:id>")
def putInstituicoes(id):
    dados = request.get_json()
    if not dados:
        return {"erro": "Nenhum dado informado"}, HTTPStatus.BAD_REQUEST

    try:
        dados_validados = instituicao_schema.load(dados, partial=True)
    except ValidationError as err:
        return {"erro": "Dados inválidos", "campos": err.messages}, HTTPStatus.BAD_REQUEST
    
    connexao = get_connection()
    cursor = connexao.cursor()
    cursor.execute('SELECT * FROM tb_instituicao_ensino WHERE id = ? AND ativo = 1', (id,))
    row = cursor.fetchone()
    
    if row is None:
        return {"erro": "não encontrei bixo."}, HTTPStatus.NOT_FOUND
    
    no_entidade = dados_validados.get("no_entidade", row["no_entidade"])
    co_entidade = dados_validados.get("co_entidade", row["co_entidade"])
    qt_mat_bas = dados_validados.get("qt_mat_bas", row["qt_mat_bas"])

    with connexao:
        cursor.execute('UPDATE tb_instituicao_ensino SET no_entidade = ?, co_entidade = ?, qt_mat_bas = ? WHERE id = ? AND ativo = 1 RETURNING *',
            (no_entidade, co_entidade, qt_mat_bas, id))
        atualizado = cursor.fetchone()

    return jsonify(instituicao_schema.dump(dict(atualizado))), HTTPStatus.OK


@app.delete("/instituicoesensino/<int:id>")
def deleteInstituicoes(id):
    
    connexao = get_connection()
    with connexao:
        cursor = connexao.cursor()
        cursor.execute('UPDATE tb_instituicao_ensino SET ativo = 0 WHERE id = ? AND ativo = 1', (id,))

    apagado = cursor.rowcount

    return jsonify({"mensagem": f"Coluna ativo: {apagado} esse registro com ID: {id} foi apagado"}), HTTPStatus.OK




# USUARIOS
@app.post("/usuarios")
def postUsuarios():
    dados = request.get_json()

    usuarios = listarUsuarios()
    
    novo_usuario = Usuarios(
        id=dados.get("id"),
        nome=dados.get("nome"),
        idade=dados.get("idade"),
        cpf=dados.get("cpf")
    )
    
    usuarios.append(novo_usuario)
    salvaUsuarios(usuarios)
    
    return novo_usuario.toDict()


@app.put("/usuarios/<int:id>")
def putUsuarios(id):
    dados = request.get_json()
    
    usuarios = listarUsuarios()
    a = next((usr for usr in usuarios if int(usr.id) == id), None)
    
    if not a:
        return { "erro":"não encontrei bixo."}, 404
     
    a.nome = dados.get("nome", a.nome)
    a.idade = dados.get("idade", a.idade)
    a.cpf = dados.get("cpf", a.cpf)
    
    salvaUsuarios(usuarios)
    return {"messagem": "atualizado man"}, 200


@app.delete("/usuarios/<int:id>")
def deleteUsuarios(id):
    usuarios = listarUsuarios()
    resto_dalista = [u for u in usuarios if int(u.id) != id]
    
    salvaUsuarios(resto_dalista)
    return {"mensagem": "usuario apagado olha no arquivo"}, 200

@app.get("/usuarios/<int:id>")
def getByIdUsuarios(id):
    usuarios = listarUsuarios()
    a = [u.toDict() for u in usuarios if int(u.id) == id]
    if not a:
        return { "erro":"não encontrei bixo."}, 404
    return a[0] , 200

def main(arg=[]):
    app.run(debug=True)


if __name__ == '__main__':
    main()
