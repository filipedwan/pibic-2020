class Atividade:

    def __init__(self, codigo, titulo, turma_id, data_inicio, data_termino, linguagem, tipo, peso, n_questoes, blocos_ex):
        self.id = codigo
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
        print('\t\t- Atividade [{}]: {}'.format(self.atividade_id, self.titulo))
        print('\t\t- De {} até {}'.format(self.data_inicio, self.data_termino))
        print('\t\t- Linguagem: {}'.format(self.linguagem))
        print('\t\t- Tipo: {}'.format(self.tipo))
        print('\t\t- Peso: {:.2f}'.format(self.peso))
        print('\t\t- Nº Questões: {}'.format(self.n_questoes))
        print('\t\t- Questões: {}\n'.format(self.blocos_ex))
