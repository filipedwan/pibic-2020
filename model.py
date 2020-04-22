class Periodo:

    def __init__(self, descricao, path):
        self.descricao = descricao
        self.path = path

    def get_row(self):
        return [self.descricao]

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

    def __init__(self, periodo, codigo, path):
        self.periodo = periodo
        self.id = codigo
        self.path = path
        self.descricao = None

    def print_info(self):
        """
             Imprime no console as informações de uma turma.
        """
        print(f'\t> Turma [{self.id}]: {self.descricao}')
        print(f'\t> Pasta: {self.path}\n')

    def get_row(self):
        return [self.id, self.descricao, self.periodo.descricao]

    @staticmethod
    def get_columns():
        return 'turma_id,turma_descricao,periodo'


class Atividade:

    def __init__(self, turma, codigo, path):
        self.turma = turma
        self.id = codigo
        self.path = path
        self.titulo = None
        self.data_inicio = None
        self.data_termino = None
        self.linguagem = None
        self.tipo = None
        self.peso = None
        self.n_blocos = None
        self.blocos = []

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
        print('\t\t- Nº Questões: {:02d}'.format(self.n_blocos))
        print(f'\t\t- Questões: {self.blocos}\n')

    def get_row(self):
        return [
            self.turma.id,
            self.id,
            self.titulo,
            self.tipo,
            self.linguagem,
            self.peso,
            self.data_inicio,
            self.data_termino,
            self.n_blocos,
            self.blocos
        ]

    @staticmethod
    def get_columns():
        return 'turma_id,atividade_id,titulo,tipo,linguagem,peso,data_inicio,data_termino,n_blocos,blocos'


class Estudante:

    def __init__(self, periodo, turma, codigo, path):
        self.periodo = periodo
        self.turma = turma
        self.id = codigo
        self.path = path
        self.curso_id = None
        self.curso_nome = None
        self.instituicao_id = None
        self.instituicao_nome = None
        self.escola_nome = None
        self.escola_tipo = None
        self.escola_turno = None
        self.escola_ano_grad = None
        self.sexo = None
        self.ano_nascimento = None
        self.estado_civil = None
        self.tem_filhos = None

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

    def get_row(self):
        return [
            self.periodo.descricao,
            self.turma.id,
            self.id,
            self.curso_id,
            self.curso_nome,
            self.instituicao_id,
            self.instituicao_nome,
            self.escola_nome,
            self.escola_tipo,
            self.escola_turno,
            self.escola_ano_grad,
            self.sexo,
            self.ano_nascimento,
            self.estado_civil,
            self.tem_filhos
        ]

    @staticmethod
    def get_columns():
        return 'periodo,turma_id,estudante_id,curso_id,curso_nome,instituicao_id,instituicao_nome,escola_nome,escola_tipo,escola_turno,escola_ano_grad,sexo,ano_nascimento,estado_civil,tem_filhos'


class Execucao:

    def __init__(self, periodo, turma_id, estudante_id, atividade_id, exercicio_id):
        self.periodo = periodo
        self.turma_id = turma_id
        self.estudante_id = estudante_id
        self.atividade_id = atividade_id
        self.exercicio_id = exercicio_id
        self.data_inicio = None
        self.data_termino = None
        self.n_submissoes = None
        self.n_testes = None
        self.n_erros = None
        self.nota_final = None
        self.acertou = None
        self.total_complexity = None
        self.n_functions = None
        self.n_classes = None
        self.loc = None
        self.lloc = None
        self.sloc = None
        self.comments = None
        self.multi = None
        self.single_comments = None
        self.blank = None
        self.h1 = None
        self.h2 = None
        self.N1 = None
        self.N2 = None
        self.vocabulary = None
        self.length = None
        self.calculated_length = None
        self.volume = None
        self.difficulty = None
        self.effort = None
        self.bugs = None
        self.time = None

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

    def get_row(self):
        return [
            self.periodo,
            self.turma_id,
            self.estudante_id,
            self.atividade_id,
            self.exercicio_id,
            self.data_inicio,
            self.data_termino,
            self.n_submissoes,
            self.n_testes,
            self.n_erros,
            self.nota_final,
            self.acertou,
            self.total_complexity,
            self.n_functions,
            self.n_classes,
            self.loc,
            self.lloc,
            self.sloc,
            self.comments,
            self.multi,
            self.single_comments,
            self.blank,
            self.h1,
            self.h2,
            self.N1,
            self.N2,
            self.vocabulary,
            self.length,
            self.calculated_length,
            self.volume,
            self.difficulty,
            self.effort,
            self.bugs,
            self.time,
        ]

    @staticmethod
    def get_columns():
        return 'periodo,turma_id,estudante_id,atividade_id,exercicio_id,data_inicio,data_termino,n_submissoes,n_testes,'\
            'n_erros,nota_final,acertou,total_complexity,n_functions,n_classes,loc,lloc,sloc,comments,multi,single_comments,'\
            'blank,h1,h2,N1,N2,vocabulary,length,calculated_length,volume,difficulty,effort,bugs,time'


class Metricas:

    @staticmethod
    def get_columns():
        return 'complexity,n_funcoes,n_classes,loc,lloc,sloc,comments,multi,single_comments,blank,h1,h2,N1,N2,vocabulary,length,calc_length,volume,difficulty,effort,bugs,time'
