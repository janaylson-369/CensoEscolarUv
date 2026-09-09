from flask import Flask, request

app = Flask(__name__)
import json

with open("src/backend/bd.json", "r", encoding="utf-8") as f:
    instituicoes_db = json.load(f)


# Buscar por ID tipado
@app.get("/instituicoesensino/<int:id>")
def getByInstituicoes(id):
    
    for instituicao in instituicoes_db["instituicoesensino"]:
        if instituicao["id"] == id:
            return instituicao, 200
    return {"error": "Instituição não encontrada"}, 404




@app.post("/instituicoesensino")
def postInstituicoes():
    return {"id": 1, "co_inep": "123456"}, 201


# Listagem de todas as instituições (GET)
@app.get("/instituicoesensino")
def getAllInstituicoes():

    return instituicoes_db, 200


@app.put("/instituicoesensino/<int:id>")
def putInstituicoes(id):
    return {"id": id, "co_inep": "123456"}, 200


@app.delete("/instituicoesensino/<int:id>")
def deleteInstituicoes():
    pass    



def main(args=[]):
    app.run(debug=True)


if __name__ == '__main__':
    main()