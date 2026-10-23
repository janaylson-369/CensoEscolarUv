from flask import jsonify,  request
from models.instituicaoensino import InstituicaoEnsino, InstituicaoEnsinoSchema
from models.usuarios import Usuarios
from helpers.file.json import read,write
from pathlib import Path
from marshmallow import ValidationError
from helpers.database import get_connexao
from helpers.application import app
from http import HTTPStatus


BASE_DIR = Path(__file__).resolve().parent
arquivoUsuarios = BASE_DIR / "usuarios.json"


instituicao_schema = InstituicaoEnsinoSchema()
instituicoes_schema = InstituicaoEnsinoSchema(many=True)

def row_to_instituicao(row):
    return InstituicaoEnsino(
        id=row[0],
        no_entidade=row[1],
        co_entidade=row[2],
        no_uf=row[3],
        sg_uf=row[4],
        co_uf=row[5],
        no_municipio=row[6],
        co_municipio=row[7],
        nu_ano_censo=row[8],
        qt_mat_bas=row[9],
        qt_mat_inf=row[10],
        qt_mat_fund=row[11],
        qt_mat_med=row[12],
        qt_mat_prof=row[13],
        qt_mat_eja=row[14],
        qt_mat_esp=row[15],
        created=row[16],
        ativo=row[17]
    )


def listarUsuarios():
    dataset = read(arquivoUsuarios)
    usuarioss = [Usuarios(
        row["id"], row["nome"], row["idade"], row["cpf"]) for row in dataset]
    return usuarioss

def salvaUsuarios(usuarios):
    write(arquivoUsuarios, [usr.toDict() for usr in usuarios])
    


@app.route("/health")
def health():
    return {"health": "ok"}, HTTPStatus.OK

@app.get("/instituicoesensino")
def getAllInstituicoes():
    # Abrir a conexão com o banco de dados.
    connexao = get_connexao()
    cursor = connexao.cursor()
    # Executar as DML de consulta
    cursor.execute("""
        SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, 
               no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, 
               qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, 
               qt_mat_eja, qt_mat_esp, created, ativo
        FROM tb_instituicao_ensino
        WHERE ativo = 1""")
    rows = cursor.fetchall()
    instituicoes = [row_to_instituicao(row) for row in rows]
    
    return jsonify(instituicoes_schema.dump(instituicoes)), HTTPStatus.OK

@app.get("/instituicoesensino/<int:id>")
def getByIdInstituicoes(id):
    conn = get_connexao()
    cursor = conn.cursor()
    cursor.execute("""
                SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, 
                no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, 
                qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, 
                qt_mat_eja, qt_mat_esp, created, ativo
                FROM tb_instituicao_ensino WHERE id = ? AND ativo = 1""", (id,))
    row = cursor.fetchone()

    if row is None:
        return {"mensagem": "instituição de ensino não encontrada"}, HTTPStatus.NOT_FOUND

    instituicao = row_to_instituicao(row)
    return jsonify(instituicao_schema.dump(instituicao)), HTTPStatus.OK

@app.post("/instituicoesensino")
def postInstituicoes():
    try: 
        data = instituicao_schema.load(request.get_json(), partial=False)
        connexao = get_connexao()
        with connexao:
            cursor = connexao.cursor()
            cursor.execute(
                """
                INSERT INTO tb_instituicao_ensino (
                    no_entidade, co_entidade, no_uf, sg_uf, co_uf, 
                    no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, 
                    qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, 
                    qt_mat_eja, qt_mat_esp
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
                RETURNING id, created
                """,(data["no_entidade"], data["co_entidade"], data["no_uf"],
                     data["sg_uf"], data["co_uf"], data["no_municipio"],
                     data["co_municipio"], data["nu_ano_censo"], data["qt_mat_bas"],
                     data["qt_mat_inf"], data["qt_mat_fund"], data["qt_mat_med"],
                     data["qt_mat_prof"], data["qt_mat_eja"], data["qt_mat_esp"])
            )
            resultset = cursor.fetchone()
            id_novo = resultset[0]
            created_novo = resultset[1]

        instituicao = InstituicaoEnsino(**data, id=id_novo, created=created_novo)
        
        return jsonify(instituicao_schema.dump(instituicao)), HTTPStatus.CREATED
    except ValidationError as err:
            return {"erro": "dado invalido", "campos": err.messages}, HTTPStatus.BAD_REQUEST



@app.put("/instituicoesensino/<int:id>")
def putInstituicoes(id):
    dados = request.get_json()
    if not dados:
        return {"erro": "Nenhum dado informado"}, HTTPStatus.BAD_REQUEST

    try:
        dados_validados = instituicao_schema.load(dados, partial=True)
    except ValidationError as err:
        return {"erro": "dados invalidos", "campos": err.messages}, HTTPStatus.BAD_REQUEST

    connexao = get_connexao()
    cursor = connexao.cursor()
    cursor.execute("""
        SELECT id, no_entidade, co_entidade, no_uf, sg_uf, co_uf, 
               no_municipio, co_municipio, nu_ano_censo, qt_mat_bas, 
               qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, 
               qt_mat_eja, qt_mat_esp, created, ativo
        FROM tb_instituicao_ensino
        WHERE id = ? AND ativo = 1 """, (id,))
    row = cursor.fetchone()

    if row is None:
        return {"erro": "não encontrei nada bixo"}, HTTPStatus.NOT_FOUND

    instituicao = row_to_instituicao(row)

    instituicao.no_entidade = dados_validados.get("no_entidade", instituicao.no_entidade)
    instituicao.co_entidade = dados_validados.get("co_entidade", instituicao.co_entidade)
    instituicao.qt_mat_bas = dados_validados.get("qt_mat_bas", instituicao.qt_mat_bas)

    with connexao:
        cursor.execute(
            """
            UPDATE tb_instituicao_ensino
            SET no_entidade = ?, co_entidade = ?, qt_mat_bas = ?
            WHERE id = ? AND ativo = 1
            """,(instituicao.no_entidade, instituicao.co_entidade, instituicao.qt_mat_bas, id)
        )

    return jsonify(instituicao_schema.dump(instituicao)), HTTPStatus.OK


@app.delete("/instituicoesensino/<int:id>")
def deleteInstituicoes(id):
    
    connexao = get_connexao()
    with connexao:
        cursor = connexao.cursor()
        cursor.execute("UPDATE tb_instituicao_ensino SET ativo = 0 WHERE id = ? AND ativo = 1", (id,))
        apagado = cursor.rowcount

    return jsonify({"mensagem": f"coluna ativo: {apagado} o registro com ID: {id} foi apagado"}), HTTPStatus.OK



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
