class Usuarios():
    def __init__(self, id, nome, idade, cpf):
        self.id = id
        self.nome = nome
        self.idade = idade
        self.cpf = cpf

    def toDict(self):
        return {"id": self.id, 
                "nome": self.nome, 
                "idade": self.idade, 
                "cpf": self.cpf}