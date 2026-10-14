from Pessoa import Pessoa


class Aluno(Pessoa):
    def __init__(self, cpf, nome, matricula):
        super().__init__(cpf, nome)
        self.matricula = matricula
