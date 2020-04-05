class Atividade:

    def __init__(self, codigo, titulo, path, turma_id, data_inicio, data_termino, linguagem, tipo, peso, n_questoes, blocos_ex):
        self.id = codigo
        self.path = path
        self.titulo = titulo
        self.turma_id = turma_id
        self.data_inicio = data_inicio
        self.data_termino = data_termino
        self.linguagem = linguagem
        self.tipo = tipo
        self.peso = peso
        self.n_questoes = n_questoes
        self.blocos_ex = blocos_ex

    def print_info(self):
        """
           Imprime as informações da ativida no console
        """
        print(f'\t\t- Atividade [{self.id}]: {self.titulo}')
        print(f'\t\t- Arquivo: {self.path}')
        print(f'\t\t- De {self.data_inicio} até {self.data_termino}')
        print(f'\t\t- Linguagem: {self.linguagem}')
        print(f'\t\t- Tipo: {self.tipo}')
        print('\t\t- Peso: {:.2f}'.format(self.peso))
        print('\t\t- Nº Questões: {:02d}'.format(self.n_questoes))
        print(f'\t\t- Questões: {self.blocos_ex}\n')
