class Periodo:

    def __init__(self, descricao, path):
        self.descricao = descricao
        self.path = path
        self.turmas = []

    def get_row(self):
        return [self.descricao]

    @staticmethod
    def get_attr_names():
        return list(Periodo('', '').__dict__)[:1]


class Turma:

    def __init__(self, periodo: Periodo, codigo: int, path: str):
        self.periodo = periodo
        self.codigo = codigo
        self.descricao = None
        self.path = path
        self.atividades = []
        self.estudantes = []

    def get_row(self):
        return [self.periodo.descricao, self.codigo, self.descricao]

    @staticmethod
    def get_attr_names():
        return list(Turma(None, 0, '').__dict__)[:3]


class Atividade:

    def __init__(self, turma: Turma, code: int, path: str):
        self.turma = turma
        self.codigo = code
        self.titulo = None
        self.data_inicio = None
        self.data_termino = None
        self.linguagem = None
        self.tipo = None
        self.peso = None
        self.n_blocos = None
        self.blocos = []
        self.path = path

    def get_row(self):
        return [
            self.turma.codigo,
            self.codigo,
            self.titulo,
            self.data_inicio,
            self.data_termino,
            self.linguagem,
            self.tipo,
            self.peso,
            self.n_blocos,
            self.blocos
        ]

    @staticmethod
    def get_attr_names():
        return list(Atividade(None, 0, '').__dict__)[:10]


class Estudante:

    def __init__(self, periodo: Periodo, turma: Turma, code: int, path: str):
        self.periodo = periodo
        self.turma = turma
        self.codigo = code
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
        self.execucoes = []
        self.path = path

    def get_row(self):
        return [
            self.periodo.descricao,
            self.turma.codigo,
            self.codigo,
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
    def get_attr_names():
        return list(Estudante(None, None, 0, '').__dict__)[:15]


class Execucao:

    def __init__(self, periodo: Periodo, turma_id: int, estudante_id: int, atividade_id: int, exercicio_id: int):
        self.periodo = periodo
        self.turma = turma_id
        self.estudante = estudante_id
        self.atividade = atividade_id
        self.exercicio = exercicio_id
        self.tempo_solucao = None
        self.tempo_interacao = None
        self.n_submissoes = None
        self.n_testes = None
        self.n_erros = None
        self.nota_final = None
        self.acertou = None
        self.complexity = None
        self.n_classes = None
        self.n_functions = None
        self.loc = None
        self.lloc = None
        self.sloc = None
        self.single_comments = None
        self.comments = None
        self.multilines = None
        self.blank_lines = None
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

    def get_row(self):
        return [
            self.periodo,
            self.turma,
            self.estudante,
            self.atividade,
            self.exercicio,
            self.tempo_solucao,
            self.tempo_interacao,
            self.n_submissoes,
            self.n_testes,
            self.n_erros,
            self.nota_final,
            self.acertou,
            self.complexity,
            self.n_classes,
            self.n_functions,
            self.loc,
            self.lloc,
            self.sloc,
            self.single_comments,
            self.comments,
            self.multilines,
            self.blank_lines,
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
    def get_attr_names():
        return list(Execucao(None, 0, 0, 0, 0).__dict__)


class Solucao:

    def __init__(self, codigo: int):
        self.codigo = codigo
        self.complexity = None
        self.n_classes = None
        self.n_functions = None
        self.loc = None
        self.lloc = None
        self.sloc = None
        self.single_comments = None
        self.comments = None
        self.multilines = None
        self.blank_lines = None
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

    @staticmethod
    def get_attr_names():
        return list(Solucao(0).__dict__)

    def get_row(self):
        return [
            self.codigo,
            self.complexity,
            self.n_classes,
            self.n_functions,
            self.loc,
            self.lloc,
            self.sloc,
            self.single_comments,
            self.comments,
            self.multilines,
            self.blank_lines,
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


class Erro:

    def __init__(self, name: str, count: int):
        self.periodo = None
        self.turma = None
        self.atividade = None
        self.estudante = None
        self.exercicio = None
        self.tipo = name
        self.ocorrencias = count

    @staticmethod
    def get_attr_names():
        return list(Erro('', 0).__dict__)
