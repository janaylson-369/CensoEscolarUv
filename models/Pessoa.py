class Pessoa():
    def __init__(self, cpf, nome):
        self.cpf = cpf
        self.nome = nome

    def __str__(self):
        return f"<Pessoa: {self.cpf}, {self.nome}>"


pessoa = Pessoa("00011122233", "João da Silva")
print(pessoa)
