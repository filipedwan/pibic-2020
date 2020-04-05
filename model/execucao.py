class Execucao:

    def __init__(self, atividade_id, exercicio_id, n_submissoes, n_testes, n_erros, nota, acertou):
        self.atividade_id = atividade_id
        self.exercicio_id = exercicio_id
        self.n_submissoes = n_submissoes
        self.n_testes = n_testes
        self.n_erros = n_erros
        self.nota_final = nota
        self.acertou = acertou

    def print_info(self):
        """
           Imprime as informações da execução da questão no console
        """
        print(f'\t\t- Atividade [{self.atividade_id}]: Q{self.exercicio_id}')
        print('\t\t- Nº Submissões: {:03d}\n'.format(self.n_submissoes))
        print('\t\t- Nº Testes: {:03d}\n'.format(self.n_testes))
        print('\t\t- Nº Erros: {:03d}\n'.format(self.n_erros))
        print('\t\t- Nº Testes: {:.2f}\n'.format(self.nota_final))
        print('\t\t- Acertou? {}\n'.format('Sim' if self.acertou else 'Não'))
