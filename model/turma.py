class Turma:

    def __init__(self, codigo, descricao, path):
        self.id = codigo
        self.descricao = descricao
        self.path = path

    def print_info(self):
        """
             Imprime no console as informações de uma turma.
        """
        print(f'\t> Turma [{self.id}]: {self.descricao}')
        print(f'\t> Pasta: {self.path}\n')
