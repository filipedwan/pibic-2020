import re

from util import Util
from datetime import datetime, timedelta

from radon.visitors import ComplexityVisitor
from radon.raw import analyze
from radon.metrics import h_visit

from parser import *
from model import *


class CodebenchExtractor:
    """
    Classe Extratora das Entidades do dataset Codebench
    """

    # extensão dos arquivos de informações das 'Atividades' de uma 'Turma'
    __atividade_file_extension = '.data'
    # nome do arquivo de informações de 'Estudante'
    __estudante_file_name = 'user.data'
    # extensão do arquivo de log do CodeMirror
    __codemirror_file_extension = '.log'
    # extensão do arquivo de código-fonte das soluções dos 'Estudantes'
    __exercices_file_extension = '.py'
    # extensão do arquivo de código-fonte das soluções dos 'Professores
    __solution_extension = '.code'
    # tempo de inatividade
    __inactivity_threshold = timedelta(minutes=5)

    @staticmethod
    def extract_periodos(path: str) -> List[Periodo]:
        """
        Retorna uma lista de todos os :class:`Periodo` letivos encontrados no dataset Codebench.

        Cada Período corresponde a uma pasta dentro do diretório do dataset Codebench.

        Exemplo de uso:
            periodos = CodebenchExtractor.extract_periodos('cb_dataset_v1.11/')

            for periodo in periodos:
                print(periodo)
            ...

        :param path: Caminho absoluto para o diretório do dataset do Codebench.
        :type path: str
        """
        periodos = []
        # recupera todas as 'entradas' (arquivos ou pastas) no caminho informado (path).
        with os.scandir(path) as entries:
            for entry in entries:
                with os.scandir(entry.path) as folders:
                    for folder in folders:
                        Logger.info(f'Extraindo informações de Perído: {folder.name}')
                        p = Periodo(folder.name, folder.path)
                        periodos.append(p)
        return periodos

    @staticmethod
    def __extract_turma_descricao_from_file(path: str, turma: Turma):
        """
        Recupera a descrição da :class:`Turma`, a partir de um dos arquivo de :class:`Atividade` (assessments).
        A descrição da turma é então atribuída a propriedade 'descricao' da 'Turma'.

        ---- classe name: [descrição]

        :param path: Caminho absoluto para o diretório de atividades da Turma
        :type path: str
        :param turma: Objeto que irá armazenar a descrição da Turma.
        :type turma: Turma
        """
        # coleta todas os arquivos/pastas no diretório informado (diretório de atividades da turma)
        with os.scandir(path) as entries:
            for entry in entries:
                # se a 'entrada' for um arquivo de extensão '.data' então corresponde atividade
                if entry.is_file() and entry.path.endswith(CodebenchExtractor.__atividade_file_extension):
                    with open(entry.path, 'r') as f:
                        Logger.info(f'Extraindo descrição da Turma no arquivo: {entry.path}')
                        line = f.readline()
                        while line:
                            # ---- class name: Introdução à Programação de Computadores
                            if line.startswith('---- class name:'):
                                turma.descricao = line.strip()[17:]
                                break
                            line = f.readline()
                    break

    @staticmethod
    def extract_turmas(periodo: Periodo):
        """
        Retorna uma lista contendo todas as :class:`Turma` de um :class:`Período` letivo.

        Cada Turma corresponde a uma pasta dentro do diretório do Período:
            - '220': Turma 220
            - '221': Turma 221 ...

        As turmas encontradas são salvas no período (periodo.turma)

        Exemplo de uso:
            CodebenchExtractor.extract_turmas(periodo)

            for turma in periodo.turmas:
                print(turma)
            ...

        :param periodo: O Período letivo do qual devem ser recuperadas as Turmas.
        :type periodo: Periodo
        """
        # coleta todas os arquivos/pastas dentro do diretório do período.
        with os.scandir(periodo.path) as folders:
            for folder in folders:
                # se a 'entrada' for uma diretório (pasta) então corresponde a uma 'turma'
                if folder.is_dir():
                    Logger.info(f'Extraindo informações de Turma: {folder.name} {periodo.descricao}')
                    code = int(folder.name)
                    turma = Turma(periodo, code, folder.path)
                    CodebenchExtractor.__extract_turma_descricao_from_file(f'{folder.path}/assessments', turma)
                    periodo.turmas.append(turma)

    @staticmethod
    def __extract_atividade_info_from_file(path: str, atividade: Atividade):
        """
        Recupera as informações da :class:`Atividade` de um arquivo ('.data').

        As informações extraídas são salvas na 'atividade'.

        :param path: Caminho absoluto para o arquivo de dados da Atividade.
        :type path: str
        :param atividade: Objeto que irá armazenar as informações retiradas do arquivo.
        :type atividade: Atividade
        """
        with open(path, 'r') as f:
            Logger.info(f'Extraindo informações da Atividade no arquivo: {path}')
            for line in f.readlines():
                if line.startswith('---- as'):
                    atividade.titulo = line[23:].strip()
                elif line.startswith('---- st'):
                    atividade.data_inicio = line[12:].strip()
                elif line.startswith('---- en'):
                    atividade.data_termino = line[10:].strip()
                elif line.startswith('---- la'):
                    atividade.linguagem = line[15:].strip()
                elif line.startswith('---- ty'):
                    atividade.tipo = line[11:].strip()
                elif line.startswith('---- we'):
                    atividade.peso = float(line[13:].strip())
                elif line.startswith('---- to'):
                    atividade.n_blocos = int(line[22:].strip())
                elif line.startswith('---- ex'):
                    bloco = line[18:].strip()
                    if len(bloco) > 0:  # verifica se exite alguma questão, pois no dataset alguns dados estão faltando
                        # testa se realmente corresponde a um bloco de exercícios, blocos são separados por 'or'
                        if ' or ' in bloco:
                            # separa os códigos dos exercícios do bloco
                            bloco = bloco.split(' or ')
                            bloco = [int(x) for x in bloco]  # converte os códigos dos exercícios em inteiro
                            bloco.sort()
                        else:
                            bloco = int(bloco)
                        atividade.blocos.append(bloco)

    @staticmethod
    def extract_atividades(turma: Turma):
        """
        Recupera uma lista com todas as :class:`Atividade` realizadas numa dada :class:`Turma`.

        Cada turma possui informações sobre os estudantes e atividades.

        Cada atividade corresponde a um arquivo de extensão '.data'.

        Os arquivos das atividades estão localizadas dentro do diretório da turma, na pasta 'assessments'.

        As atividades encontradas são salvas na turma (turma.atividades)

        Exemplos de uso:
            CodebenchExtractor.extract_atividades(turma)

            for atividade in turma.atividades:
                print(atividade)
            ...

        :param turma: A Turma das Atividades.
        :type turma: Turma
        """
        # coleta todas os arquivos/pastas dentro do diretório de atividades da turma
        with os.scandir(f'{turma.path}/assessments') as arquivos:
            for arquivo in arquivos:
                # se a 'entrada' for um arquivo de extensão '.data', então corresponde a uma atividade.
                if arquivo.is_file() and arquivo.path.endswith(CodebenchExtractor.__atividade_file_extension):
                    Logger.info(f'Extraindo informações de Atividade: {arquivo.name}')
                    code = int(arquivo.path.split('/')[-1].replace(CodebenchExtractor.__atividade_file_extension, ''))
                    atividade = Atividade(turma, code, arquivo.path)
                    CodebenchExtractor.__extract_atividade_info_from_file(arquivo.path, atividade)
                    turma.atividades.append(atividade)

    @staticmethod
    def __extract_estudante_info_from_file(path: str, estudante: Estudante):
        """
        Extrai as informações referentes ao :class:`Estudante` do arquivo 'user.data'.

        As informações são salvas no objeto 'estudante' passado como parametro.

        :param path: Caminho absoluto do arquivo 'user.data' com as informações do Estudante.
        :type path: str
        :param estudante: Objeto que irá armazenar as informações retiradas do arquivo.
        :type estudante: Estudante
        """
        with open(path, 'r') as f:
            Logger.info(f'Extraindo informações do Estudante no arquivo: {path}')
            for index, line in enumerate(f.readlines(), start=0):
                line = line.strip()
                if line.startswith('---- cou') and index == 1:
                    estudante.curso_id = int(CodebenchExtractor.__get_property_value(line))
                elif line.startswith('---- cou') and index == 2:
                    estudante.curso_nome = CodebenchExtractor.__get_property_value(line)
                elif line.startswith('---- in') and index == 3:
                    estudante.instituicao_id = int(CodebenchExtractor.__get_property_value(line))
                elif line.startswith('---- in') and index == 4:
                    estudante.instituicao_nome = CodebenchExtractor.__get_property_value(line)
                elif line.startswith('---- hi'):
                    estudante.escola_nome = CodebenchExtractor.__get_property_value(line)
                elif line.startswith('---- sch'):
                    estudante.escola_tipo = CodebenchExtractor.__get_property_value(line)
                elif line.startswith('---- shi'):
                    estudante.escola_turno = CodebenchExtractor.__get_property_value(line)
                elif line.startswith('---- gr'):
                    estudante.escola_ano_grad = int(CodebenchExtractor.__get_property_value(line))
                elif line.startswith('---- sex'):
                    estudante.sexo = CodebenchExtractor.__get_property_value(line)
                elif line.startswith('---- year o'):
                    estudante.ano_nascimento = int(CodebenchExtractor.__get_property_value(line))
                elif line.startswith('---- civ'):
                    estudante.estado_civil = CodebenchExtractor.__get_property_value(line)
                elif line.startswith('---- hav'):
                    estudante.tem_filhos = True if CodebenchExtractor.__get_property_value(line) == 'yes' else False

    @staticmethod
    def __get_property_value(text: str):
        """
        Recebe uma linha de texto do arquivo de informações do estudante contendo uma chave e valor.

        Retorna somente o valor associado a aquela chave. Cada linha possui uma chave separada de seu valor por ':'.

        :param text: Linha de texto com a chave e valor.
        :type text: str
        :return: O valor encontrado na linha de texto ou 'None'.
        """
        idx = text.find(':')
        if idx >= 0:
            return text.strip()[idx + 2:]
        return None

    @staticmethod
    def extract_estudantes(turma: Turma):
        """
        Recupera uma lista com todos os :class:`Estudante` de uma :class:`Turma`.

        Cada turma possui informações sobre os estudantes e atividades.

        As informações dos estudantes estão localizadas dentros de pastas nomeadas com o código do estudante.

        Essas pastas estão localizadas dentro da pasta 'users' no diretório da turma.

        Os estudantes encontrados são salvos na turma (turma.estudantes)

        Exemplo de uso:
            CodebenchExtractor.extract_estudantes(turma)

            for estudante in turma.estudantes:
                print(estudante)
            ...

        :param turma: A Turma (disciplina) na qual os Estudantes estão matriculados.
        :type turma: Turma
        """
        # coleta todas os arquivos/pastas no diretório de 'estudantes' informado
        with os.scandir(f'{turma.path}/users') as folders:
            for folder in folders:
                # se a 'entrada' for um diretório, então corresponde a pasta de um 'estudante'.
                if folder.is_dir():
                    Logger.info(f'Extraindo informações do Estudante: {folder.name}')
                    estudante = Estudante(turma.periodo, turma, int(folder.name), folder.path)
                    CodebenchExtractor.__extract_estudante_info_from_file(
                        f'{folder.path}/{CodebenchExtractor.__estudante_file_name}', estudante)
                    turma.estudantes.append(estudante)

    @staticmethod
    def __get_code_metrics(codigo: str):
        """
        Recupera as métricas de um código Python.

        McCabe's (Complexidade)
            - complexity: Complexidade Total
            - n_classes: Quantidade de Classes
            - n_functions: Quantidade de Funções
        Métricas Brutas (Código)
            - loc: Número Total de Linhas
            - lloc: Número de Linhas Lógicas de Código
            - sloc: Número de Linhas de Código
            - comments: Número de Comentários
            - single_comments: Número de Comentários Simples
            - multilines: Número de Multi-line Strings
            - blank_lines: Número de Linhas em Branco
        Halstead (Métricas de SW)
            - h1: Número de Operadores Distintos
            - h2: Número de Operandos Distintos
            - N1: Número Total de Operadores
            - N2: Número Total de Operandos
            - vocabulary: Vocabulário (h = h1 + h2)
            - length: Tamanho (N = N1 + N2)
            - calculated_length: Tamanho Calculado (h1 * log2(h1) + h2 * log2(h2))
            - volume: Volume (V = N * log2(h))
            - difficulty: Dificuldade (D = h1/2 * N2/h2)
            - effort: Esforço (E = D * V)
            - time: Tempo (T = E / 18 segundos)
            - bugs: Bugs (B = V / 3000), estivativa de erros na implementação

        :param path: Caminho absoluto para o arquivo de código fonte (.py).
        :type path: str
        :return: As métricas que puderam ser extraídas do código.
        """
        metricas = Metricas()
        try:
            v = ComplexityVisitor.from_code(codigo)
            metricas.complexity = v.complexity
            metricas.n_functions = len(v.functions)
            metricas.n_classes = len(v.functions)
        except Exception as e:
            pass

        try:
            a = analyze(codigo)
            metricas.loc = a.loc
            metricas.lloc = a.lloc
            metricas.sloc = a.sloc
            metricas.blank_lines = a.blank
            metricas.multilines = a.multi
            metricas.comments = a.comments
            metricas.single_comments = a.single_comments
        except Exception as e:
            pass

        try:
            h = h_visit(codigo)
            metricas.h1 = h.total.h1
            metricas.h2 = h.total.h2
            metricas.N1 = h.total.N1
            metricas.N2 = h.total.N2
            metricas.h = h.total.vocabulary
            metricas.N = h.total.length
            metricas.calculated_N = h.total.calculated_length
            metricas.volume = h.total.volume
            metricas.difficulty = h.total.difficulty
            metricas.effort = h.total.effort
            metricas.bugs = h.total.bugs
            metricas.time = h.total.time
        except Exception as e:
            pass

        return metricas

    @staticmethod
    def __extract_solution_interval(path: str, execucao: Execucao):
        """
        Calcula os tempos de implementação e interação utilizando como limites os intervalos definidos na Atividade.

        O tempo de implementação é o tempo gasto pelo usuário enquanto o editor do CodeMirror estiver em foco, descontados os intervalos de inatividade.

        O tempo de interação é o tempo total gasto pelo usuário interagindo com o editor do CodeMirror.

        :param path: Caminho absoluto do arquivo de 'log' com as informações do CodeMirror.
        :type path: str
        :param execucao: Objeto que irá armazenar as informações obtidas do arquivo de 'log' do CodeMirror.
        :type execucao: Execucao
        """
        with open(path, 'r') as f:
            Logger.info(f'Calculando tempos des implementação e interação: {path}')
            # datas de inicio e termino da atividade, servem como limites para o calculo do tempo e solução
            at_dti = datetime.strptime(execucao.atividade.data_inicio, '%Y-%m-%d %H:%M')
            at_dtf = datetime.strptime(execucao.atividade.data_termino, '%Y-%m-%d %H:%M')

            execucao.t_implementacao = timedelta(0)
            execucao.t_interacao = timedelta(0)

            # percorremos o arquivo de log até os eventos terem um datetime maior que o do inicio da atividade
            lines = f.readlines()
            i = 0
            size = len(lines)
            while i < size:
                try:
                    start_datetime, _, _ = CodebenchExtractor.__get_event_info(lines[i])
                    if start_datetime >= at_dti:
                        break
                except Exception:
                    pass
                i += 1

            while i < size:
                end_datetime = None

                # buscamos então o evento de focus
                while i < size:
                    i += 1
                    try:
                        start_datetime, event_name, _ = CodebenchExtractor.__get_event_info(lines[i])
                        if event_name == 'focus':
                            break
                        # se o evento for uma 'sumissão' correta ou o datetime do evento for maior que o datetime de termino da atividade
                        # finalizamos o calculo do tempo de solução
                        if event_name == 'submit' and event_msg.startswith('Congr'):
                            start_datetime = None
                            i = size
                    except Exception:
                        pass

                # efetuamos o somatório dos intervalos enquanto o editor do CodeMirror possuir foco
                while i < size:
                    i += 1
                    try:
                        # se temos o datetime de um evento anterior, podemos calcular o intervalo de tempo entre os eventos
                        end_datetime, event_name, event_msg = CodebenchExtractor.__get_event_info(lines[i])
                        if event_name == 'blur':
                            break
                    except Exception:
                        pass

                if not end_datetime:
                    break
                if end_datetime > at_dtf:
                    break

                if start_datetime <= end_datetime:
                    interval = (end_datetime - start_datetime)
                    if interval < CodebenchExtractor.__inactivity_threshold:
                        execucao.t_implementacao += interval
                    execucao.t_interacao += interval

    @staticmethod
    def __get_event_info(linha):
        date, _, linha = linha.partition('#')
        name, _, msg = linha.partition('#')
        # data e hora do evento desconsiderando os milisegundos
        date = datetime.strptime(date, '%Y-%m-%d %H:%M:%S.%f')
        return date, name, msg

    @staticmethod
    def __get_float_value(line):
        value = 0.0
        try:
            value = float(line)
        except Exception:
            pass
        return value

    @staticmethod
    def __extract_code(lines, i):
        codigo = []
        while not lines[i].startswith('-- '):
            codigo.append(lines[i])
            i += 1
        return codigo

    @staticmethod
    def __get_error_name(lines, i):
        while not lines[i].startswith('*-*'):
            m = re.match(r"^([\w_\.]+Error)", lines[i])
            if m:
                return m.group(0)
            i += 1
        return None

    @staticmethod
    def __extract_executions_count(path: str, execucao: Execucao):
        """
        Recupera as informações de submissões, testes e erros do arquivo de 'log' das tentativas de solução de um exercício.

        As informações sobre submissões, testes e erros são salvos no objeto 'execucao'.

        :param path: Caminho absoluto do arquivo de 'log' com as informações das execuções feitas pelo estudante.
        :type path: str
        :param execucao: Objeto que irá armazenar as informações obtidas do arquivo de 'log' do Codebench.
        :type execucao: model.Execucao
        """
        error_names = []
        with open(path, 'r') as f:
            execucao.n_submissoes = 0
            execucao.n_testes = 0
            execucao.n_erros = 0
            execucao.nota_final = 0.0

            i = 0
            lines = f.readlines()
            size = len(lines)

            while i < size:
                if lines[i].startswith('== S'):
                    code = None
                    execucao.t_execucao = None
                    execucao.acertou = False
                    execucao.n_submissoes += 1
                    i += 1
                    while not lines[i].startswith('*-*'):
                        if lines[i].startswith('-- CODE'):
                            code = CodebenchExtractor.__extract_code(lines, i + 1)
                            i += len(code) + 1
                        elif lines[i].startswith('-- EXEC'):
                            execucao.t_execucao = CodebenchExtractor.__get_float_value(lines[i + 1].strip())
                            i += 2
                        elif lines[i].startswith('-- GRAD'):
                            execucao.nota_final = CodebenchExtractor.__get_float_value(lines[i + 1].strip()[:-1])
                            i += 2
                        elif lines[i].startswith('-- ERROR'):
                            i += 3
                            execucao.n_erros += 1
                            error_names.append(CodebenchExtractor.__get_error_name(lines, i))
                        else:
                            i += 1
                    if execucao.nota_final > 99.99:
                        execucao.acertou = True
                        execucao.metricas = CodebenchExtractor.__get_code_metrics(''.join(code))
                        i = size
                elif lines[i].startswith('== T'):
                    execucao.n_testes += 1
                    while not lines[i].startswith('*-*'):
                        if lines[i].startswith('-- ERROR'):
                            i += 3
                            execucao.n_erros += 1
                            error_names.append(CodebenchExtractor.__get_error_name(lines, i))
                        else:
                            i += 1
                i += 1

        erros_count = Util.count_errors(error_names, execucao)
        if len(erros_count):
            CSVParser.salvar_erros(erros_count)

    @staticmethod
    def extract_execucoes(estudante: Estudante):
        """
        Recupera todas as :class:`Execucoes` feitas por um :class:`Estudante` tentando solucionar um Exercício de uma :class:`Atividade`.

        As execuções estão localizadas dentro da pasta 'executions', dentro do diretório do estudante.

        Cada estudante possui um registro de execuções para cada exercício.

        As execuções de uma determinada questão corresponde a um arquivo de extensão '.log', e cujo nome é formado pela composição do código da atividade e do código da questão, separados por um 'underscore'.

        As execuções encontradas são salvas no objeto estudante (estudante.execucoes).

        Exemplo de uso:
            CodebenchExtractor.extract_execucoes(estudante)

            for execucao in estudante.execucoes:
                print(execucao)
            ...

        :param estudante: O estudante cujas execuções devem ser recuperadas.
        :type estudante: Estudante
        """
        # transforma a lista de atividades da turma num dicionário, utilizando o código da turma como 'chave' (key)
        # isto facilita a obtenção do intervalo da atividade no cálculo dos tempos de implementação e interação
        atividades = {a.codigo: a for a in estudante.turma.atividades}
        # coleta todas os arquivos/pastas dentro do diretório de execuções do aluno
        with os.scandir(f'{estudante.path}/executions') as arquivos:
            for arquivo in arquivos:
                # se a 'entrada' for um arquivo de extensão '.log', então corresponde as execuções de uma questão.
                if arquivo.is_file() and arquivo.path.endswith(CodebenchExtractor.__codemirror_file_extension):
                    Logger.info(f'Extraindo informações de Execução: {arquivo.name}')
                    # divide o nome do arquivo obtendo os códigos da atividade e exercício.
                    atividade_code, exercicio_code, *_ = arquivo.name.replace(
                        CodebenchExtractor.__codemirror_file_extension, '').split('_')
                    atividade = atividades.get(int(atividade_code), None)
                    execucao = Execucao(estudante.periodo, estudante.turma, estudante, atividade, int(exercicio_code))

                    CodebenchExtractor.__extract_executions_count(arquivo.path, execucao)

                    codemirror_file = f'{estudante.path}/codemirror/{arquivo.name}'
                    if os.path.exists(codemirror_file):
                        CodebenchExtractor.__extract_solution_interval(codemirror_file, execucao)
                    else:
                        Logger.warn(f'Arquivo de execução não encontrado: {codemirror_file}')

                    if not execucao.metricas:
                        code_file = arquivo.name.replace(CodebenchExtractor.__codemirror_file_extension,
                                                         CodebenchExtractor.__exercices_file_extension)
                        code_file = f'{estudante.path}/codes/{code_file}'
                        if os.path.exists(code_file):
                            with open(code_file) as f:
                                codigo = ''.join(f.readlines())
                                execucao.metricas = CodebenchExtractor.__get_code_metrics(codigo)
                        else:
                            Logger.warn(f'Arquivo de código fonte não encontrado: {code_file}')

                    estudante.execucoes.append(execucao)

    @staticmethod
    def extract_solucoes(path: str):
        """
        Extrai as métricas das soluções dos exercícios propostas pelos Professores.

        As soluções estão salvas com a extensão '.code'.

        Exemplo de uso:
            solucoes = CodebenchExtractor.extract_solucoes([solutions_path])

            for solucao in solucoes:
                print(solucao)
            ...

        :param path: Caminho absoluto para a pasta onde se encontram as soluções.
        :type path: str
        :return: Lista de Soluções e suas métricas
        """
        solucoes = []
        # coleta todas os arquivos/pastas dentro do diretório de execuções do aluno
        with os.scandir(path) as arquivos:
            for arquivo in arquivos:
                # se a 'entrada' for um arquivo de extensão '.code', então corresponde as execuções de uma questão.
                if arquivo.is_file() and arquivo.path.endswith(CodebenchExtractor.__solution_extension):
                    Logger.info(f'Extraindo métricas da Solução: {arquivo.path}')
                    solucao = Solucao(int(arquivo.name.replace(CodebenchExtractor.__solution_extension, '')))
                    with open(arquivo.path, 'r') as f:
                        codigo = ''.join(f.readlines())
                        solucao.metricas = CodebenchExtractor.__get_code_metrics(codigo)
                    solucoes.append(solucao)

        return solucoes
