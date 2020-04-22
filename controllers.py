import os
import csv
import re

from typing import List

from util import Util
from util import Logger
from numpy import NaN

from radon.visitors import ComplexityVisitor
from radon.raw import analyze
from radon.metrics import h_visit

from model import *


class ControllerPeriodo:

    @staticmethod
    def get_periodos(path: str):
        """
        Retorna uma lista contendo as informações de todos os Periodos letivos (pastas) encontrados no dataset Codebench.
        Cada Período corresponde a uma pasta, '2017-01' por exemplo são os dados do primeiro período do ano de 2017.

        :param path: Caminho absoluto para o diretório do dataset do Codebench.
        :type path: str
        """
        periodos = []
        # coleta todas as 'entradas' (arquivos ou pastas) no caminho informado (path).
        with os.scandir(path) as entries:
            for entry in entries:
                if entry.is_dir():  # se for uma pasta então corresponde a um período letivo
                    Logger.debug(f'Diretório do período: {entry.path}')
                    p = Periodo(entry.name, entry.path)
                    periodos.append(p)
        return periodos

    @staticmethod
    def save_periodos(periodos: List[Periodo], path: str):
        """
        Salva a lista de Turmas num arquivo no formato CSV.

        :param periodos: Lista de Turmas a serem salvas, :class:`model.Turma`.
        :type periodos: List[Periodo]
        :param path: Caminho absoluto do arquivo CSV onde as Turmas devam ser salvas.
        :type path: str
        """
        Logger.info(f'Salvando períodos no arquivo: {path}')
        with open(path, 'a') as file:
            writter = csv.writer(file)
            for p in periodos:
                writter.writerow(p.get_row())


class ControllerTurma:

    @staticmethod
    def __get_turma_descricao(path: str, turma: Turma):
        """
        Recupera a descrição da Turma, a partir de um dos arquivo de Atividades (assessments).
        A descrição é armazenada como um atributo do parâmetro 'turma'.

        :param path: Caminho absoluto para o diretório de atividades da Turma
        :type path: str
        :param turma: Objeto que irá armazenar a descrição da Turma, :class:`Turma`.
        :type turma: Turma
        """
        # coleta todas os arquivos/pastas no diretório informado (diretório de atividades da turma)
        with os.scandir(path) as entries:
            for entry in entries:
                # se a 'entrada' for um arquivo de extensão '.data' então corresponde atividade
                if entry.is_file() and entry.path.endswith('.data'):
                    with open(entry.path, 'r') as f:
                        # terceira linha eh onde se encontra a descrição da turma
                        # exemplo:
                        # ---- class name: Introdução à Programação de Computadores
                        turma.descricao = f.readlines()[2][17:-1]
                    break

    @staticmethod
    def get_turmas_periodo(periodo: Periodo):
        """
        Retorna uma lista contendo todas as Turmas de um Período letivo, dado o caminho (diretório) do período.
        Cada Turma corresponde a uma pasta dentro do diretório, '220' por exemplo são os dados da Turma de número 220.

        :param periodo:  O Período letivo do qual devem ser recuperadas as Turmas, :class:`Periodo`.
        :type periodo: Periodo
        """
        turmas = []
        # coleta todas os arquivos/pastas dentro do diretório do período.
        with os.scandir(periodo.path) as entries:
            for entry in entries:
                # se a 'entrada' for uma diretório (pasta) então corresponde a uma 'turma'
                if entry.is_dir():
                    try:
                        Logger.debug(f'Diretório da turma: {entry.path}')
                        code = int(entry.name)
                        turma = Turma(periodo, code, entry.path)
                        ControllerTurma.__get_turma_descricao(f'{entry.path}/assessments', turma)
                        turmas.append(turma)
                    except Exception as e:
                        print(f'Erro ao recuperar dados da turma: {entry.path}\nErro: {str(e)}')
                        Util.wait_user_input()
        return turmas

    @staticmethod
    def save_turmas(turmas: List[Turma], path: str):
        """
        Salva a lista de Turmas num arquivo no formato CSV.

        :param turmas: Lista de Turmas a serem salvas, :class:`model.Turma`.
        :type turmas: List[Turma]
        :param path: Caminho absoluto do arquivo CSV onde as Turmas devam ser salvas.
        :type path: str
        """
        Logger.info(f'Salvando turmas no arquivo: {path}')
        with open(path, 'a') as file:
            writter = csv.writer(file)
            for turma in turmas:
                writter.writerow(turma.get_row())


class ControllerAtividade:

    @staticmethod
    def __get_data_from_file(path: str, atividade: Atividade):
        """
        Recupera as informações da Atividade de um arquivo ('.data').
        As informações são salvas no objeto 'atividade' passado como parametro.

        :param path: Caminho absoluto para o arquivo de dados da Atividade.
        :type path: str
        :param atividade: Objeto que irá armazenar as informações retiradas do arquivo, :class:`Atividade`.
        :type atividade: Atividade
        """
        with open(path, 'r') as f:
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
    def get_atividades(turma: Turma):
        """
        Recupera uma lista com todas as Atividades realizadas numa dada Turma.
        Cada Turma possui informações sobre os Estudantes e Atividades.
        As Atividades estão localizadas dentro da pasta 'assessments', que fica dentro do diretório da Turma.
        Cada Atividade corresponde a um arquivo de extensão '.data'.

        :param turma: A Turma das Atividades, :class:`model.Turma`.
        :type turma: Turma
        """
        atividades = []
        # coleta todas os arquivos/pastas dentro do diretório de atividades da turma
        with os.scandir(f'{turma.path}/assessments') as entries:
            for entry in entries:
                # se a 'entrada' for um arquivo de extensão '.data', então corresponde a uma atividade.
                if entry.is_file() and entry.path.endswith('.data'):
                    try:
                        Logger.debug(f'Arquivo de Atividade: {entry.path}')
                        code = int(entry.path.split('/')[-1][:-5])
                        atividade = Atividade(
                            turma,
                            code,
                            entry.path
                        )
                        ControllerAtividade.__get_data_from_file(entry.path, atividade)
                        atividades.append(atividade)
                    except Exception:
                        Logger.error(f'Erro obter atividade: {entry.path}')
                        Util.wait_user_input()
        return atividades

    @staticmethod
    def save_atividades(atividades: List[Atividade], path: str):
        """
        Salva a lista de atividades num arquivo no formato CSV.

        :param atividades: Lista de atividades a serem salvas, :class:`Atividade`
        :type atividades: List[Atividade]
        :param path: Caminho absoluto do arquivo CSV onde as atividades devam ser salvas.
        :type path: str
        """
        Logger.info(f'Salvando atividades no arquivo: {path}')
        with open(path, 'a') as file:
            writter = csv.writer(file)
            for atividade in atividades:
                writter.writerow(atividade.get_row())


class ControllerEstudante:

    @staticmethod
    def __get_data_from_file(path: str, estudante: Estudante):
        """
        Recupera as informações referentes ao Estudante de dentro do arquivo 'user.data'.
        As informações são salvas no objeto 'estudante' pasado como parametro.

        :param path: Caminho absoluto do arquivo 'user.data' com as informações do Estudante.
        :type path: str
        :param estudante: Objeto que irá armazenar as informações retiradas do arquivo, :class:`Estudante`.
        :type estudante: Estudante
        """
        with open(path, 'r') as f:
            for index, line in enumerate(f.readlines(), start=0):
                line = line.strip()
                if line.startswith('---- cou') and index == 1:
                    estudante.curso_id = int(ControllerEstudante.__get_property_value(line))
                elif line.startswith('---- cou') and index == 2:
                    estudante.curso_nome = ControllerEstudante.__get_property_value(line)
                elif line.startswith('---- in') and index == 3:
                    estudante.instituicao_id = int(ControllerEstudante.__get_property_value(line))
                elif line.startswith('---- in') and index == 4:
                    estudante.instituicao_nome = ControllerEstudante.__get_property_value(line)
                elif line.startswith('---- hi'):
                    estudante.escola_nome = ControllerEstudante.__get_property_value(line)
                elif line.startswith('---- sch'):
                    estudante.escola_tipo = ControllerEstudante.__get_property_value(line)
                elif line.startswith('---- shi'):
                    estudante.escola_turno = ControllerEstudante.__get_property_value(line)
                elif line.startswith('---- gr'):
                    estudante.escola_ano_grad = int(ControllerEstudante.__get_property_value(line))
                elif line.startswith('---- sex'):
                    estudante.sexo = ControllerEstudante.__get_property_value(line)
                elif line.startswith('---- year o'):
                    estudante.ano_nascimento = int(ControllerEstudante.__get_property_value(line))
                elif line.startswith('---- civ'):
                    estudante.estado_civil = ControllerEstudante.__get_property_value(line)
                elif line.startswith('---- hav'):
                    estudante.tem_filhos = True if ControllerEstudante.__get_property_value(line) == 'yes' else False

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
            return text.strip()[idx+2:]
        return None

    @staticmethod
    def get_estudantes(turma: Turma):
        """
        Recupera uma lista com todos Estudantes matriculados nama Tsurma.
        Cada Turma possui informações sobre os Estudantes e Atividades.
        Os Estudantes estão localizadas dentro da pasta 'users', dentro do diretório da turma.
        Cada Estudante possui suas informações dentro de uma pasta nomeada com seu 'id'.

        :param turma: A Turma (disciplina) na qual os Estudantes estão matriculados, :class:`Turma`.
        :type turma: Turma
        :return: Lista de Estudantes encontrados para aquela Turma, :class:`Estudante`.
        """
        estudantes = []
        # coleta todas os arquivos/pastas no diretório de 'estudantes' informado
        with os.scandir(f'{turma.path}/users') as entries:
            for entry in entries:
                # se a 'entrada' for um diretório, então corresponde as informações de um 'estudante'.
                if entry.is_dir():
                    try:
                        Logger.debug(f'Arquivo de estudante: {entry.path}')
                        estudante = Estudante(
                            turma.periodo,
                            turma,
                            int(entry.name),
                            entry.path,
                        )
                        ControllerEstudante.__get_data_from_file(f'{entry.path}/user.data', estudante)
                        estudantes.append(estudante)
                    except Exception:
                        Logger.error(f'Erro ao recuperar dados do estudante: {entry.path}')
                        # Util.wait_user_input()
        return estudantes

    @staticmethod
    def save_estudantes(estudantes: List[Estudante], path: str):
        """
        Salva a lista estudantes num arquivo no formato CSV.

        :param estudantes: Lista de Estudantes a serem salvos, :classe:`Estudante`.
        :type estudantes: List[Estudante]
        :param path: Caminho absoluto do arquivo CSV onde a lista de estudantes deva ser salva.
        :type path: str
        """
        Logger.info(f'Salvando estudantes no arquivo: {path}')
        with open(path, 'a') as file:
            writter = csv.writer(file)
            for estudante in estudantes:
                writter.writerow(estudante.get_row())


class ControllerExecucao:

    @staticmethod
    def __get_code_metrics(path: str, execucao: Execucao):
        """
        Recupera as métricas de código da última solução submetida por um Estudante, nas tentativa de resolver um exercício.
        Salva as métricas encontradas no objeto 'execucao'.

        :param path: Caminho absoluto para o arquivo de código fonte (.py) da solução do Estudante.
        :type path: str
        :param execucao: Objeto que irá armazenar as informações obtidas do arquivo de código fonte, :class:`Execucao`.
        :type execucao: Execucao
        """
        with open(path) as f:
            lines = f.readlines()
            codigo = ''.join(lines)

            v = ComplexityVisitor.from_code(codigo)
            execucao.total_complexity = v.total_complexity
            execucao.n_functions = len(v.functions)
            execucao.n_classes = len(v.functions)

            a = analyze(codigo)
            execucao.loc = a.loc
            execucao.lloc = a.lloc
            execucao.sloc = a.sloc
            execucao.blank = a.blank
            execucao.multi = a.multi
            execucao.comments = a.comments
            execucao.single_comments = a.single_comments

            h = h_visit(codigo)
            execucao.h1 = h.total.h1
            execucao.h2 = h.total.h2
            execucao.N1 = h.total.N1
            execucao.N2 = h.total.N2
            execucao.vocabulary = h.total.vocabulary
            execucao.length = h.total.length
            execucao.calculated_length = h.total.calculated_length
            execucao.volume = h.total.volume
            execucao.difficulty = h.total.difficulty
            execucao.effort = h.total.effort
            execucao.bugs = h.total.bugs
            execucao.time = h.total.time

            lines.clear()
            del lines

    @staticmethod
    def __get_solution_interval(path: str, execucao: Execucao):
        """
        Recupera as datas de início e término da tentativa de solucionar um exercício, obtidas a partir do arquivo de 'log' do CodeMirror.
        Salva essas datas no objeto 'execucao'.

        :param path: Caminho absoluto do arquivo de 'log' com as informações do CodeMirror.
        :type path: str
        :param execucao: Objeto que irá armazenar as informações obtidas do arquivo de 'log' do CodeMirror, :class:`Execucao`.
        :type execucao: Execucao
        """
        with open(path, 'r') as f:
            lines = f.readlines()

            i = 0
            while True:
                m = re.search(
                    r'^((\d{4})-(\d{1,2})-(\d{1,2})) ((\d{2}):(\d{2}):(\d{2}).(\d{3}))',
                    lines[i]
                )
                if m:
                    execucao.data_inicio = m.group(0)
                    break
                i += 1

            i = -1
            while True:
                m = re.search(
                    r'^((\d{4})-(\d{1,2})-(\d{1,2}) (\d{2}):(\d{2}):(\d{2}).(\d{3}))#submit#Congratulations, your code is correct!',
                    lines[i]
                )
                if m:
                    execucao.data_termino = m.group(0)
                    break
                i -= 1

            lines.clear()
            del lines

    @staticmethod
    def __get_submissions(path: str, execucao: Execucao):
        """
        Recupera as informações de submissões, testes e erros do arquivo de 'log' das tentativas de solução de um exercício.
        Salvas as informações, encontradas no arquivo, no objeto 'execucao' passado como parametro.

        :param path: Caminho absoluto do arquivo de 'log' com as informações das execuções feitas pelo estudante.
        :type path: str
        :param execucao: Objeto que irá armazenar as informações obtidas do arquivo de 'log' do Codebench, :class:`Execucao`.
        :type execucao: Execucao
        """
        with open(path, 'r') as f:
            achou_nota = False
            erros = []

            if not execucao.n_submissoes:
                execucao.n_submissoes = 0
            if not execucao.n_testes:
                execucao.n_testes = 0
            if not execucao.n_erros:
                execucao.n_erros = 0

            for line in f.readlines():
                line = line.strip()

                if achou_nota:
                    try:
                        execucao.nota_final = float(line[:-1])
                        execucao.acertou = True if execucao.nota_final > 99.99 else False
                    except TypeError:
                        Logger.error(f'Erro ao tentar obter nota do estudante, na linha: {line}')
                    except ValueError:
                        Logger.error(f'Erro ao tentar obter nota do estudante, na linha: {line}')
                    achou_nota = False

                if line.startswith('== S'):
                    execucao.n_submissoes += 1
                elif line.startswith('== T'):
                    execucao.n_testes += 1
                elif line.startswith('-- ER'):
                    execucao.n_erros += 1
                elif line.startswith('-- GRAD'):
                    achou_nota = True
                elif re.search(r"^([\w_\.]+Error)", line):
                    m = re.match(r"^([\w_\.]+Error)", line)
                    if m:
                        erros.append(m.group(0))
            if len(erros):
                Util.register_errors(erros)

    @staticmethod
    def get_execucoes(estudante: Estudante):
        """
        Recupera todas as execuções feitas por um estudante para as atividades na turma que ele participou.
        Cada estudante possui um registro de execuções para cada questão.
        As execuções estão localizadas dentro da pasta 'executions', dentro do diretório do estudante.
        As execuções de uma determinada questão corresponde a um arquivo de extensão '.log', e cujo nome é formado pela composição do código da atividade e do código da questão, separados por um 'underscore'.

        :param estudante: O estudante cujas execuções devem ser recuperadas, :class:`Estudante`.
        :type estudante: Estudante
        :return: Todas as execuções realizadas por um estudante, para as questões selecionadas em atividades que o estudante resolveu, :py:class:`model.Execucao`.
        """
        execucoes = []
        # coleta todas os arquivos/pastas dentro do diretório de execuções do aluno
        with os.scandir(f'{estudante.path}/executions') as entries:
            for entry in entries:
                # se a 'entrada' for um arquivo de extensão '.log', então corresponde as execuções de uma questão.
                if entry.is_file() and entry.path.endswith('.log'):
                    Logger.debug(f'Arquivo de execução: {entry.path}')

                    # divide o nome do arquivo obtendo os códigos da atividade e exercício.
                    aid, eid, *_ = entry.name[:-4].split('_')
                    execucao = Execucao(
                        estudante.periodo.descricao,
                        estudante.turma.id,
                        estudante.id,
                        int(aid),
                        int(eid)
                    )

                    try:
                        ControllerExecucao.__get_submissions(entry.path, execucao)
                    except Exception:
                        Logger.error(f'Erro ao obter dados das submissões da execução: {entry.path}')

                    try:
                        ControllerExecucao.__get_solution_interval(f'{estudante.path}/codemirror/{entry.name}', execucao)
                    except Exception:
                        Logger.error(f'Erro ao obter dados do intervalo de solução da execução: {estudante.path}/codemirror/{entry.name}')

                    try:
                        ControllerExecucao.__get_code_metrics(f'{estudante.path}/codes/{entry.name[:-4]}.py', execucao)
                    except Exception:
                        Logger.error(f'Erro ao obter métricas de código da execução: {estudante.path}/codes/{entry.name[:-4]}.py')

                    execucoes.append(execucao)
        return execucoes

    @staticmethod
    def save_execucoes(execucoes: List[Execucao], path: str):
        """
        Salva a lista de execuções num arquivo no formato CSV.

        :param execucoes: Lista de Execuções a serem salvas, :class:`Execucao`.
        :type execucoes: List[Execucao]
        :param path: Caminho absoluto do arquivo CSV onde as execuções devem ser salvas.
        :type path: str
        """
        Logger.info(f'Salvando execuções no arquivo: {path}')
        with open(path, 'a') as file:
            writter = csv.writer(file)
            for execucao in execucoes:
                writter.writerow(execucao.get_row())


class ControllerSolucao:

    @staticmethod
    def get_metricas(path: str):
        """
        Recupera matriz (lista de listas) com as métricas extraídas dos exemplos de soluções dos exercícios do Codebench.
        As soluções devem ser salvas em arquivos texto de extensão '.code', e escritas utilizando Linguagem Python.

        :param path: Caminho absoluto para a pasta onde se encontram as soluções.
        :type path: str
        :return: Matriz com as métricas extraídas de cada solução
        """
        metricas_solucoes = []
        # coleta todas os arquivos/pastas dentro do diretório de execuções do aluno
        with os.scandir(f'{path}') as entries:
            for entry in entries:
                # se a 'entrada' for um arquivo de extensão '.log', então corresponde as execuções de uma questão.
                if entry.is_file() and entry.path.endswith('.code'):
                    Logger.debug(f'Arquivo de solução do professor: {entry.path}')
                    try:
                        metricas = ControllerSolucao.__get_metricas(entry.path)
                        metricas.append(str(entry.name[:-4]))
                        metricas_solucoes.append(metricas)
                    except Exception:
                        Logger.error(f'Erro ao recuperar métricas da solução: {entry.path}')
                        # Util.wait_user_input()
        return metricas_solucoes

    @staticmethod
    def save_metricas(metricas: List, path: str):
        """
        Salva a lista de métricas das soluções num arquivo no formato CSV.

        :param metricas: Lista de Métricas a serem salvas.
        :type metricas: list
        :param path: Caminho absoluto do arquivo CSV onde as métricas devem ser salvas.
        :type path: str
        """
        Logger.info(f'Salvando métricas dos professores no arquivo: {path}')
        with open(path, 'w') as file:
            # cabeçalho do arquivo 'csv'
            file.write(Metricas.get_columns() + ',exercicio' + os.linesep)
            writter = csv.writer(file)
            for m in metricas:
                writter.writerow(m)

    @staticmethod
    def __get_metricas(path: str):
        """
        Retorna uma lista com diversas métricas (McCabe's complexity, Halstead e Métricas Brutas) de um arquivo de código-fonte.

        McCabe's
            - Complexidade Total
            - Quantidade de Funções
            - Quantidade de Classes
        Métricas Brutas
            - Número Total de Linhas (LOC)
            - Número de Linhas Lógicas de Código (LLOC)
            - Número de Linhas de Código (SLOC)
            - Número de Comentários
            - Número de Multi-line Strings
            - Número de Comentários Simples
            - Número de Linhas em Branco
        Halstead
            - Número de Operadores Distintos (h1)
            - Número de Operandos Distintos (h2)
            - Número Total de Operadores (N1)
            - Número Total de Operandos (N2)
            - Vocabulário (h = h1 + h2)
            - Tamanho (N = N1 + N2)
            - Tamanho Calculado (h1 * log2(h1) + h2 * log2(h2))
            - Volume (V = N * log2(h))
            - Dificuldade (D = h1/2 * N2/h2)
            - Esforço (E = D * V)
            - Tempo (T = E / 18 segundos)
            - Bugs (B = V / 3000), estivativa de erros na implementação

        :param path: String com o caminho absoluto para o arquivo de código-fonte.
        :type path: str
        :return: Lista com as métricas obtidas.
        """
        with open(path) as f:
            lines = f.readlines()
            codigo = ''.join(lines)
            v = ComplexityVisitor.from_code(codigo)
            a = analyze(codigo)
            h = h_visit(codigo)

            return [
                v.total_complexity,
                len(v.functions),
                len(v.classes),
                a.loc,
                a.lloc,
                a.sloc,
                a.comments,
                a.multi,
                a.single_comments,
                a.blank,
                h.total.h1,
                h.total.h2,
                h.total.N1,
                h.total.N2,
                h.total.vocabulary,
                h.total.length,
                h.total.calculated_length,
                h.total.volume,
                h.total.difficulty,
                h.total.effort,
                h.total.bugs,
                h.total.time
            ]
