

class Aluno(Pessoa):
    def __init__(self, nome, idade, cpf, matricula):
        super().__init__(nome, idade, cpf)
        self.matricula = matricula
        
    def __str__(self):
        return f"{super().__str__()}, Matrícula: {self.matricula}"