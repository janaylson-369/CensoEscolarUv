from flask import Flask, request
from models.instituicaoensino import InstituicaoEnsino
from models.usuarios import Usuarios
from helpers.file.json import read,write
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
arquivoD = BASE_DIR / "instituicoes.json"
arquivoUsuarios = BASE_DIR / "usuarios.json"

def listar():
    # Ler o arquivo json.
    dataset = read(arquivoD)
    # Converter o json -> InsitituicaoEnsino.
    instituicoesEnsino = [InstituicaoEnsino(
        row["id"], row["no_entidade"], row["co_entidade"], row["qt_mat_bas"]) for row in dataset]
    # Retorna a lista de InstituicoesEnsino.
    return instituicoesEnsino

def salva(instituicoes):
    write(arquivoD, [inst.toDict() for inst in instituicoes])
    
def listarUsuarios():
    dataset = read(arquivoUsuarios)
    usuarioss = [Usuarios(
        row["id"], row["nome"], row["idade"], row["cpf"]) for row in dataset]
    return usuarioss

def salvaUsuarios(usuarios):
    write(arquivoUsuarios, [usr.toDict() for usr in usuarios])
    
    

app = Flask(__name__)


@app.route("/")
def index():
    return {"versao": "0.0.1"}, 200


@app.route("/health")
def health():
    return {"health": "ok"}, 200


# GETS
@app.get("/instituicoesensino")
def getAllInstituicoes():
    
    co_entidade = request.args.get("co_entidade")
    
    return [
        inst.toDict() for inst in listar() 
        if not co_entidade or int(inst.co_entidade) == int(co_entidade)], 200


@app.get("/instituicoesensino/<int:id>")
def getByIdInstituicoes(id):
    institi = listar()
    a = [i.toDict() for i in institi if int(i.id) == id]
    if not a:
        return { "erro":"não encontrei bixo."}, 404
    return a[0] , 200


@app.post("/instituicoesensino")
def postInstituicoes():
    dados = request.get_json()

    instituicoes = listar()
    
    nova_inst = InstituicaoEnsino(
        id= dados.get("id"),
        no_entidade=dados.get("no_entidade"),
        co_entidade=dados.get("co_entidade"),
        qt_mat_bas=dados.get("qt_mat_bas")
    )
    
    instituicoes.append(nova_inst)
    salva(instituicoes)
    
    return nova_inst.toDict()


@app.put("/instituicoesensino/<int:id>")
def putInstituicoes(id):
    dados = request.get_json()
    
    institi = listar()
    a = next((inst for inst in institi if int(inst.id) == id), None)
    
    if not a:
        return { "erro":"não encontrei bixo."}, 404
        
    a.no_entidade = dados.get("no_entidade", a.no_entidade)
    a.co_entidade = dados.get("co_entidade", a.co_entidade)
    a.qt_mat_bas = dados.get("qt_mat_bas", a.qt_mat_bas)
    
    salva(institi)
    return {"messagem": "atualizado man"}, 200


@app.delete("/instituicoesensino/<int:id>")
def deleteInstituicoes(id):
    instituicoes = listar()
    resto_dalista = [i for i in instituicoes if int(i.id) != id]
    
    salva(resto_dalista)
    return {"mensagem": "instituição apagada olha no arquivo"}, 200




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
