class Pessoa:
    def __init__(self, nome, idade, cpf):
        self.nome = nome
        self.idade = idade
        self.cpf = cpf
        
    def __str__(self):
        return f"Nome: {self.nome}, Idade: {self.idade}, CPF: {self.cpf}"
    
pessoa1 = Pessoa("joao", 30, "323.455.133-00")
