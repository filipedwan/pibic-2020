from typing import List


class CSVEntity:
    """Interface que especifica os métodos de uma Entidade que possa ser salva num arquivo '.csv' (dataset)."""

    def as_row(self) -> List:
        """Retorna valores dos atributos da Entidade numa lista (row), para então serem salvos no dataset."""
        pass

    @staticmethod
    def get_csv_header() -> List[str]:
        """Retorna uma lista com o nome de todos os atributos da Entidade, que devam ser salvas no dataset (csv file header)."""
        pass


class Periodo(CSVEntity):
    """Entidade que representa um Período letivo."""

    def __init__(self, descricao: str, path: str):
        """
        Método Construtor.

        :param descricao: Descrição do Período, composta pelo ano e número do semestre.
        :param path: Caminho absoluto para o diretório do Período, dentro do dataset Codebench.
        """
        self.descricao = descricao
        self.path = path
        self.turmas = []

    def as_row(self) -> List:
        return [self.descricao]

    @staticmethod
    def get_csv_header():
        return list(Periodo(None, None).__dict__)[:-2]


class Turma(CSVEntity):
    """Entidade que representa uma Turma de Estudantes num :class:`Periodo` letivo."""

    def __init__(self, periodo: Periodo, codigo: int, path: str):
        """
        Método Construtor.

        :param periodo: O Periodo letivo em que a Turma ocorrreu.
        :param codigo: O código númerico único da Turma.
        :param path: Caminho absoluto para o diretório da Turma dentro do dataset do Codebench
        """
        self.periodo = periodo
        self.codigo = codigo
        self.descricao = None
        self.path = path
        self.atividades = []
        self.estudantes = []

    def as_row(self) -> List:
        return [
            self.periodo.descricao,
            self.codigo,
            self.descricao
        ]

    @staticmethod
    def get_csv_header():
        return list(Turma(Periodo(None, None), 0, None).__dict__)[:-3]


class Atividade(CSVEntity):
    """Entidade que representa uma Atividade realizada numa :class:`Turma`."""

    def __init__(self, turma: Turma, codigo: int, path: str):
        """
        Método Construtor.

        :param turma: A Turma em que a Atividade foi realizada.
        :param codigo: Código numérico único da Atividade.
        :param path: Caminho absoluto para o arquivo com as informações da Atividade (.data).
        """
        self.periodo = turma.periodo
        self.turma = turma
        self.codigo = codigo
        self.titulo = None
        self.data_inicio = None
        self.data_termino = None
        self.linguagem = None
        self.tipo = None
        self.peso = None
        self.n_blocos = None
        self.blocos = []
        self.path = path

    def as_row(self) -> List:
        return [
            self.periodo.descricao,
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
    def get_csv_header():
        return list(Atividade(Turma(Periodo('', ''), 0, ''), 0, '').__dict__)[:-1]


class Estudante(CSVEntity):
    """Entidade que representa um Estudante matriculado numa :class:`Turma`."""

    def __init__(self, periodo: Periodo, turma: Turma, codigo: int, path: str):
        """
        Método Construtor

        :param periodo: O Período letivo em que a turma ocorreu.
        :param turma: A Turma na qual o Estudante está matriculado.
        :param codigo: Código numérico único do Estudante.
        :param path: Caminho absoluto para o diretório com as informações do Estudante no dataset Codebench.
        """
        self.periodo = periodo
        self.turma = turma
        self.codigo = codigo
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

    def as_row(self) -> List:
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
    def get_csv_header() -> List[str]:
        return list(Estudante(None, None, 0, '').__dict__)[:-2]


class Execucao(CSVEntity):
    """
    Entidade que representa as Execuções do Código de um :class:`Estudante` na tentativa de resolver um Exercício proposto numa :class:`Atividade`.

    Contém informações sobre:
        - Quantidade de Submissões feitas pelo Estudante, :property:`Estudante.n_submissoes.
        - Quantidade de Testes feitos pelo Estudante.
        - Quantidade de Erros acusados pelo Interpretador Python durante as Submissões/Testes.
        - Tempo de Implementação descontado intervalos de 5 min (inatividade).
        - Tempo de Implementação Total.
        - Métricas de Complexidade de Código (McCabe).
        - Métricas de Software (Halstead).
        - Métricas Brutas de Código.
    """

    def __init__(self, periodo: Periodo, turma: Turma, estudante: Estudante, atividade: Atividade, exercicio_codigo: int):
        """
        Método Construtor.

        :param periodo: O Periodo letivo em que a Atividade ocorreu.
        :param turma: A Turma em que o Estudante estava matriculado.
        :param estudante: O Estudante que fez as Execuções.
        :param atividade: Código numérico único da Atividade do Exercício.
        :param exercicio_codigo: Código numérico único do Exercício que o Estudante tentava resolver.
        """
        self.periodo = periodo
        self.turma = turma
        self.estudante = estudante
        self.atividade = atividade
        self.exercicio = exercicio_codigo
        self.t_implementacao = None
        self.t_interacao = None
        self.n_submissoes = None
        self.n_testes = None
        self.n_erros = None
        self.t_execucao = None
        self.nota_final = None
        self.acertou = None
        self.metricas = None

    def as_row(self) -> List:
        return [
            self.periodo.descricao,
            self.turma.codigo,
            self.estudante.codigo,
            self.atividade.codigo,
            self.exercicio,
            self.t_implementacao,
            self.t_interacao,
            self.n_submissoes,
            self.n_testes,
            self.n_erros,
            self.t_execucao,
            self.nota_final,
            self.acertou,
            self.metricas.complexity,
            self.metricas.n_classes,
            self.metricas.n_functions,
            self.metricas.loc,
            self.metricas.lloc,
            self.metricas.sloc,
            self.metricas.single_comments,
            self.metricas.comments,
            self.metricas.multilines,
            self.metricas.blank_lines,
            self.metricas.h1,
            self.metricas.h2,
            self.metricas.N1,
            self.metricas.N2,
            self.metricas.h,
            self.metricas.N,
            self.metricas.calculated_N,
            self.metricas.volume,
            self.metricas.difficulty,
            self.metricas.effort,
            self.metricas.bugs,
            self.metricas.time
        ]

    @staticmethod
    def get_csv_header() -> List[str]:
        return list(Execucao(None, None, None, None, 0).__dict__)[:-1]+list(Metricas().__dict__)


class Solucao(CSVEntity):
    """
    Entidade que representa métricas de uma :class:`Solucao` proposta por um Professor para um Exercício

    Contém informações sobre:
        - Métricas de Complexidade de Código (McCabe).
        - Métricas de Software (Halstead).
        - Métricas Brutas de Código.
    """

    def __init__(self, codigo: int):
        """
        Método Construtor

        :param codigo: Código numérico único do Exercicio da Solução.
        """
        self.codigo = codigo
        self.metricas = Metricas()

    @staticmethod
    def get_csv_header() -> List[str]:
        return list(Solucao(0).__dict__)[:-1]+list(Metricas().__dict__)

    def as_row(self) -> List:
        return [
            self.codigo,
            self.metricas.complexity,
            self.metricas.n_classes,
            self.metricas.n_functions,
            self.metricas.loc,
            self.metricas.lloc,
            self.metricas.sloc,
            self.metricas.single_comments,
            self.metricas.comments,
            self.metricas.multilines,
            self.metricas.blank_lines,
            self.metricas.h1,
            self.metricas.h2,
            self.metricas.N1,
            self.metricas.N2,
            self.metricas.h,
            self.metricas.N,
            self.metricas.calculated_N,
            self.metricas.volume,
            self.metricas.difficulty,
            self.metricas.effort,
            self.metricas.bugs,
            self.metricas.time
        ]


class Erro(CSVEntity):
    """Entidade que representa a contagem de Erros de um mesmo Tipo, acusados pelo Interpretador Python, enquanto um :class:`Estudante` tentava resolver um Exercício."""

    def __init__(self, tipo: str, count: int):
        """
        Método Construtor

        :param tipo: Tipo (descrição do erro) segundo a nomenclatura do Interpretador Python.
        :param count: Quantidade de ocorrências do Erro enquanto o Estudante tentava resolver o Exercício.
        """
        self.periodo = None
        self.turma = None
        self.atividade = None
        self.estudante = None
        self.exercicio = None
        self.tipo = tipo
        self.ocorrencias = count

    def as_row(self) -> List:
        return [
            self.periodo.descricao,
            self.turma.codigo,
            self.atividade.codigo,
            self.estudante.codigo,
            self.exercicio,
            self.tipo,
            self.ocorrencias
        ]

    @staticmethod
    def get_csv_header() -> List[str]:
        return list(Erro('', 0).__dict__)


class Metricas:
    """Classe que representa as métricas de código extraídas usando o módulo 'radon'"""

    def __init__(self):
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
        self.h = None
        self.N = None
        self.calculated_N = None
        self.volume = None
        self.difficulty = None
        self.effort = None
        self.bugs = None
        self.time = None
