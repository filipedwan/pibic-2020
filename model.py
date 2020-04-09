class Periodo:

    def __init__(self, descricao, path):
        self.descricao = descricao
        self.path = path

    def print_info(self):
        """
            Imprime no console as informações de um período.
        """
        print('[{:-^120s}]'.format(f' Periodo: {self.descricao} '))
        print(f'> Pasta: {self.path}\n')

    @staticmethod
    def get_columns():
        return 'periodo'


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

    @staticmethod
    def get_columns():
        return 'periodo,turma_id,turma_descricao'


class Atividade:

    def __init__(
        self,
        codigo,
        titulo,
        path,
        turma_id,
        data_inicio,
        data_termino,
        linguagem,
        tipo,
        peso,
        n_questoes,
        blocos_ex
    ):
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

    @staticmethod
    def get_columns():
        return 'turma_id,atividade_id,titulo,tipo,linguagem,peso,data_inicio,data_termino,n_blocos,blocos'

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


class Estudante:

    def __init__(self,
                 codigo,
                 path,
                 curso_id,
                 curso_nome,
                 instituicao_id,
                 instituicao_nome,
                 escola_nome,
                 escola_tipo,
                 escola_turno,
                 escola_ano_grad,
                 sexo,
                 ano_nascimento,
                 estado_civil,
                 tem_filhos):
        self.id = codigo
        self.path = path
        self.curso_id = curso_id
        self.curso_nome = curso_nome
        self.instituicao_id = instituicao_id
        self.instituicao_nome = instituicao_nome
        self.escola_nome = escola_nome
        self.escola_tipo = escola_tipo
        self.escola_turno = escola_turno
        self.escola_ano_grad = escola_ano_grad
        self.sexo = sexo
        self.ano_nascimento = ano_nascimento
        self.estado_civil = estado_civil
        self.tem_filhos = tem_filhos

    def print_info(self):
        # TODO: doc
        print(f'\t\t- Aluno [{self.id}]')
        print(f'\t\t- Curso [{self.curso_id}]: {self.curso_nome}')
        print(f'\t\t- Instituição [{self.instituicao_id}]: {self.instituicao_nome}')
        print(f'\t\t- Escola: {self.escola_nome}, {self.escola_tipo}, {self.escola_turno}, {self.escola_ano_grad}')
        print(f'\t\t- Nascimento: {self.ano_nascimento}')
        print(f'\t\t- Sexo: {self.sexo}')
        print(f'\t\t- Estado civil: {self.estado_civil}')
        print(f'\t\t- Tem Filhos: {self.tem_filhos}\n')

    @staticmethod
    def get_columns():
        return 'periodo,turma_id,estudante_id,curso_id,curso_nome,instituicao_id,instituicao_nome,escola_nome,escola_tipo,escola_turno,escola_ano_grad,sexo,ano_nascimento,estado_civil,tem_filhos'


class Execucao:

    def __init__(
            self,
            atividade_id,
            exercicio_id,
            data_inicio,
            data_termino,
            n_submissoes,
            n_testes,
            n_erros,
            nota,
            acertou,

    ):
        self.atividade_id = atividade_id
        self.exercicio_id = exercicio_id
        self.data_inicio = data_inicio
        self.data_termino = data_termino
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
        print('\t\t- Iniciou em: {}\n'.format(self.data_inicio))
        print('\t\t- Terminou em: {}\n'.format(self.data_termino))
        print('\t\t- Nº Submissões: {:03d}\n'.format(self.n_submissoes))
        print('\t\t- Nº Testes: {:03d}\n'.format(self.n_testes))
        print('\t\t- Nº Erros: {:03d}\n'.format(self.n_erros))
        print('\t\t- Nº Testes: {:.2f}\n'.format(self.nota_final))
        print('\t\t- Acertou? {}\n'.format('Sim' if self.acertou else 'Não'))

    @staticmethod
    def get_columns():
        return 'periodo,turma_id,estudante_id,atividade_id,exercicio_id,data_inicio,data_termino,n_submissoes,n_testes,n_erros,nota_final,acertou'

