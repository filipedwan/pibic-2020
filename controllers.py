import os
import csv
import re

from util import Util
from util import Logger
from numpy import NaN

from model import *


class ControllerPeriodo:

    @staticmethod
    def get_periodos(path):
        """
            Retorna uma lista contendo as informações de todos os periodos letivos (pastas) encontrados no dataset Codebench.
            Cada período corresponde a uma pasta, '2017-01' por exemplo são os dados do primeiro período do ano de 2017.

            Args:
                path : string
                    Caminho absoluto do diretório onde se encontra o dataset Codebench.

            Returns:
                periodos : list
                    Uma lista de dicionários contendo as informações dos períodos.
                    @see model.periodo.Periodo

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        periodos = []

        try:
            # coleta todas as 'entradas' (arquivos ou pastas) no caminho informado (path).
            with os.scandir(path) as entries:
                for entry in entries:
                    if entry.is_dir():  # se for uma pasta então corresponde a um período letivo
                        Logger.debug(f'Diretório: {entry.path}')
                        p = Periodo(entry.name, entry.path)
                        periodos.append(p)

        except OSError:
            Logger.error(f'Erro ao acessar o caminho informado: {path}')
            Util.wait_user_input()

        return periodos

    @staticmethod
    def save_periodos(periodos):
        cwd = os.getcwd()
        output_file = f'{cwd}/csv/periodos.csv'
        Logger.info(f'Salvando períodos no arquivo: {output_file}')
        with open(output_file, 'w') as file:
            # cabeçalho do arquivo 'csv'
            file.write(Periodo.get_columns() + os.linesep)
            writter = csv.writer(file)
            for p in periodos:
                writter.writerow(p)


class ControllerTurma:

    @staticmethod
    def get_turmas_periodo(periodo):
        """
            Retorna uma lista contendo todas as turmas de um período letivo, dado o caminho (diretório) do período.
            Cada turma corresponde a uma pasta dentro do diretório, '220' por exemplo são os dados da turma de número 220.

            Returns:
                turmas : list
                    Todas as turmas do período.
                    @see model.turma.Turma

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        turmas = []
        try:
            # coleta todas os arquivos/pastas dentro do diretório do período.
            with os.scandir(periodo.path) as entries:
                for entry in entries:
                    # se a 'entrada' for uma diretório (pasta) então corresponde a uma 'turma'
                    if entry.is_dir():
                        Logger.debug(f'Diretório da turma: {entry.path}')
                        code = int(entry.name)
                        descricao = ControllerTurma.__get_turma_descricao(f'{entry.path}/assessments')
                        turma = Turma(code, descricao, entry.path)
                        # turma.print_info()
                        turmas.append(turma)

        except OSError:
            print(f'Erro ao acessar o caminho informado: {periodo.path}')
            Util.wait_user_input()

        return turmas

    @staticmethod
    def __get_turma_descricao(path):
        """
            Retorna uma string com a descrição de uma turma, obtida de um dos arquivo de atividades (assessments) da turma.

            Args:
                path : string
                    Caminho absoluto do diretório onde se encontra as atividades da turma.

            Returns:
                descricao : string
                    A descrição da turma.

            Error:
                Em caso de erro retorna uma string vazia.
        """
        descricao = None
        try:
            # coleta todas os arquivos/pastas no diretório informado (diretório de atividades da turma)
            with os.scandir(path) as entries:
                for entry in entries:
                    # se a 'entrada' for um arquivo de extensão '.data' então corresponde atividade
                    if entry.is_file() and entry.path.endswith('.data'):
                        with open(entry.path, 'r') as f:
                            # terceira linha eh onde se encontra a descrição da turma
                            # exemplo:
                            # ---- class name: Introdução à Programação de Computadores
                            descricao = f.readlines()[2][17:-1]
                        break

        except OSError:
            Logger.error(f'Erro ao tentar obter a descrição da turma pelo arquivo de atividades: {path}')
            Util.wait_user_input()

        return descricao

    @staticmethod
    def save_turmas(lista_turmas):
        cwd = os.getcwd()
        output_file = f'{cwd}/csv/turmas.csv'
        Logger.info(f'Salvando turmas no arquivo: {output_file}')
        with open(output_file, 'w') as file:
            file.write(Turma.get_columns() + os.linesep)
            writter = csv.writer(file)
            for t in lista_turmas:
                writter.writerow(t)


class ControllerAtividade:

    @staticmethod
    def __get_data_from_file(path):
        """
            Retorna uma lista com os dados da Atividade, obtidos de um arquivo ('.data').

            Args:
                path : string
                    Caminho absoluto do arquivo com as informações da atividade.

            Returns:
                data : list
                    Uma lista com as informações da atividade extraídas do arquivo '.data'.
                    index 0: código da atividade
                    index 1: título da atividade
                    index 2: código da turma
                    index 3: data de ínicio da atividade
                    index 4: data de término da atividade
                    index 5: linguagem de programação usada na atividade
                    index 6: tipo da atividade
                    index 7: peso da atividade
                    index 8: quantidade de blocos de exercícios na atividade
                    index 9: blocos de exercícios da atividade
        """
        data = [NaN, None, NaN, None, None, None, None, NaN, None, []]
        try:
            data[0] = int(path.split('/')[-1][:-5])  # código da atividade

            with open(path, 'r') as f:

                for line in f.readlines():
                    line = line.strip()
                    if line.startswith('---- as'):
                        data[1] = line[23:].strip()
                    elif line.startswith('---- class nu'):
                        data[2] = int(line[19:].strip())
                    elif line.startswith('---- st'):
                        data[3] = line[12:].strip()
                    elif line.startswith('---- en'):
                        data[4] = line[10:].strip()
                    elif line.startswith('---- la'):
                        data[5] = line[15:].strip()
                    elif line.startswith('---- ty'):
                        data[6] = line[11:].strip()
                    elif line.startswith('---- we'):
                        try:
                            data[7] = float(line[13:].strip())
                        except ValueError:
                            Logger.error(f'Erro ao converter o peso da atividade: {line}')
                    elif line.startswith('---- to'):
                        try:
                            data[8] = int(line[22:].strip())
                        except ValueError:
                            Logger.error(f'Erro ao converter número total de exercícios da atividade: {line}')
                    elif line.startswith('---- ex'):
                        bloco = line[18:].strip()
                        if len(
                                bloco) > 0:  # verifica se exite alguma questão, pois no dataset alguns dados estão faltando
                            # testa se realmente corresponde a um bloco de exercícios, blocos são separados por 'or'
                            if ' or ' in bloco:
                                # separa os códigos dos exercícios do bloco
                                bloco = bloco.split(' or ')
                                bloco = [int(x) for x in bloco]  # converte os códigos dos exercícios em inteiro
                                bloco.sort()
                            else:
                                bloco = int(bloco)

                            data[-1].append(bloco)

        except OSError:
            Logger.error(f'Erro ao acessar o arquivo da atividade: {path}')
            Util.wait_user_input()

        return data

    @staticmethod
    def get_atividades(turma):
        """
            Recupera todas as atividades realizadas naquela turma.
            Cada turma possui informações sobre os alunos e atividades.
            As atividades estão localizadas dentro da pasta 'assessments', dentro do diretório da turma.
            Cada atividade corresponde a um arquivo de extensão '.data'.

            Args:
                turma : Turma
                    A turma da qual deve-se recupera as atividades
                    @see model.turma.Turma

            Returns:
                atividades : list
                    Uma lista com todas as atividades encontradas no diretório da turma.
                    @see model.atividade.Atividade

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        atividades = []

        try:
            # coleta todas os arquivos/pastas dentro do diretório de atividades da turma
            with os.scandir(f'{turma.path}/assessments') as entries:
                for entry in entries:
                    # se a 'entrada' for um arquivo de extensão '.data', então corresponde a uma atividade.
                    if entry.is_file() and entry.path.endswith('.data'):
                        Logger.debug(f'Arquivo de Atividade: {entry.path}')
                        data = ControllerAtividade.__get_data_from_file(entry.path)

                        atividade = Atividade(
                            data[0],
                            data[1],
                            entry.path,
                            data[2],
                            data[3],
                            data[4],
                            data[5],
                            data[6],
                            data[7],
                            data[8],
                            data[9]
                        )
                        data.clear()
                        del data

                        # atividade.print_info()
                        atividades.append(atividade)

        except OSError:
            Logger.error(f'Erro ao acessar diretório de atividades: {turma.path}/assessements')
            Util.wait_user_input()

        return atividades

    @staticmethod
    def save_atividades(atividades):
        cwd = os.getcwd()
        output_file = f'{cwd}/csv/atividades.csv'
        Logger.info(f'Salvando atividades no arquivo: {output_file}')
        with open(output_file, 'w') as file:
            # cabeçalho do arquivo 'csv'
            file.write(Atividade.get_columns() + os.linesep)
            writter = csv.writer(file)
            for a in atividades:
                writter.writerow(a)


class ControllerEstudante:

    @staticmethod
    def get_estudantes(turma):
        """
            Recupera todas os estudantes (usuários) matriculados naquela turma.
            Cada turma possui informações sobre os alunos e atividades.
            Os alunos estão localizadas dentro da pasta 'users', dentro do diretório da turma.
            Cada aluno possui suas informações dentro de uma pasta nomeada com seu 'id'.

            Returns:
                estudantes : list
                    Todos os estudantes matriculados na turma.
                    @see model.estudante.Estudante

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        estudantes = []

        try:

            # coleta todas os arquivos/pastas no diretório de 'estudantes' informado
            with os.scandir(f'{turma.path}/users') as entries:
                for entry in entries:
                    # se a 'entrada' for um diretório, então corresponde as informações de um 'estudante'.
                    if entry.is_dir():
                        Logger.debug(f'Arquivo de estudante: {entry.path}')

                        data = ControllerEstudante.__get_data_from_file(f'{entry.path}/user.data')

                        estudante = Estudante(
                            int(entry.name),
                            entry.path,
                            data[0],
                            data[1],
                            data[2],
                            data[3],
                            data[4],
                            data[5],
                            data[6],
                            data[7],
                            data[8],
                            data[9],
                            data[10],
                            data[11]
                        )

                        data.clear()
                        del data

                        # estudante.print_info()
                        estudantes.append(estudante)

        except OSError:
            Logger.error(f'Erro ao acessar o diretório de estudantes: {turma.path}/users')
            Util.wait_user_input()

        return estudantes

    @staticmethod
    def __get_data_from_file(path):
        """
            Retorna os dados referentes ao estudante de dentro do arquivo 'user.data'

            Args:
                path : string
                    Caminho absoluto do arquivo do arquivo 'user.data' que contém as informações do estudante.

            Returns:
                data : list
                    Uma lista com as informações extraídas do arquivo 'user.data'.
                    index 0: código do curso do estudante
                    index 1: nome do curso do estudante
                    index 2: código da instituição de ensino superior
                    index 3: nome da instituição de ensino superior
                    index 4: nome da instituição de ensino médio
                    index 5: tipo da instituição de ensino médio
                    index 6: turno em que o estudante cursou o ensino médio
                    index 7: ano de graduação no ensino médio
                    index 8: sexo do estudante
                    index 9: ano de nascimento do estudante
                    index 10: estado civil
                    index 11: 'True' se o estudante possui filhos, 'False' caso contrário

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        data = [NaN, None, NaN, None, None, None, None, NaN, None, NaN, None, None]
        try:
            with open(path, 'r') as f:
                for index, line in enumerate(f.readlines(), start=0):
                    line = line.strip()
                    if line.startswith('---- cou') and index == 1:
                        try:
                            data[0] = int(ControllerEstudante.__get_property_value(line))
                        except ValueError:
                            Logger.error(f'Erro ao obter código do curso do estudante: {line}')
                    elif line.startswith('---- cou') and index == 2:
                        data[1] = ControllerEstudante.__get_property_value(line)
                    elif line.startswith('---- in') and index == 3:
                        try:
                            data[2] = int(ControllerEstudante.__get_property_value(line))
                        except ValueError:
                            Logger.error(f'Erro ao obter código do curso do estudante: {line}')
                    elif line.startswith('---- in') and index == 4:
                        data[3] = ControllerEstudante.__get_property_value(line)
                    elif line.startswith('---- hi'):
                        data[4] = ControllerEstudante.__get_property_value(line)
                    elif line.startswith('---- sch'):
                        data[5] = ControllerEstudante.__get_property_value(line)
                    elif line.startswith('---- shi'):
                        data[6] = ControllerEstudante.__get_property_value(line)
                    elif line.startswith('---- gr'):
                        try:
                            data[7] = int(ControllerEstudante.__get_property_value(line))
                        except ValueError:
                            Logger.error(f'Erro ao obter ano de graduação no ensino médio: {line}')
                    elif line.startswith('---- sex'):
                        data[8] = ControllerEstudante.__get_property_value(line)
                    elif line.startswith('---- year o'):
                        try:
                            data[9] = int(ControllerEstudante.__get_property_value(line))
                        except ValueError:
                            Logger.error(f'Erro ao obter ano de nascimento: {line}')
                    elif line.startswith('---- civ'):
                        data[10] = ControllerEstudante.__get_property_value(line)
                    elif line.startswith('---- hav'):
                        if ControllerEstudante.__get_property_value(line) == 'yes':
                            data[-1] = True
                        else:
                            data[-1] = False

        except OSError:
            Logger.error(f'Erro ao acessar o arquivo de estudante: {path}')
            Util.wait_user_input()

        return data

    @staticmethod
    def __get_property_value(text):
        idx = text.find(':')
        if idx >= 0:
            return text.strip()[idx+2:]
        return None

    @staticmethod
    def save_estudantes(lista_estudantes):
        cwd = os.getcwd()
        output_file = f'{cwd}/csv/estudantes.csv'
        Logger.info(f'Salvando estudantes no arquivo: {output_file}')
        with open(output_file, 'w') as file:
            # cabeçalho do arquivo 'csv'
            file.write(Estudante.get_columns() + os.linesep)
            writter = csv.writer(file)
            for e in lista_estudantes:
                writter.writerow(e)


class ControllerExecucao:

    @staticmethod
    def __get_codemirror_dates(path):
        """
            Retorna as datas de início e término da tentativa de solucionar um exercício, obtidas a partir do arquivo de 'log' do CodeMirror.

            Args:
                path : string
                    Caminho absoluto do arquivo de 'log' com as informações do CodeMirror.

            Returns:
                (start_date, end_date) : tuple(string, string)
                    Uma Tupla contendo as datas de início e término da tentativa de solucionar o exercício.

            Error:
                Em caso de erro retorna uma tupla com duas strings vazias.
        """
        start_date = None
        end_date = None

        try:
            with open(path, 'r') as f:
                lines = f.readlines()

                start_date = lines[0]
                end_date = lines[-1]

                start_date = start_date[:start_date.find('#')]
                end_date = end_date[:end_date.find('#')]

                lines.clear()
                del lines
        except OSError:
            Logger.error('Erro ao tentar recuperar dados do CodeMirror!')

        return start_date, end_date

    @staticmethod
    def __get_data_from_file(path):
        """
            Retorna os dados referentes as execuções (tentativas de solução) de um exercício a partir do arquivo '.log'

            Args:
                path : string
                    Caminho absoluto do arquivo de 'log' com as informações das execuções feitas pelo estudante.

            Returns:
                data : list
                    Uma lista com as informações extraídas do arquivo de 'log'.
                    index 0: número de submissões
                    index 1: número de testes
                    index 2: número de erros
                    index 3: nota final
                    index 4: True (acertou o exercício) / False (errou o exercício)

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        subm = 0
        test = 0
        err = 0
        nota = 0.0
        acertou = False

        try:
            with open(path, 'r') as f:
                achou_nota = False

                erros = []

                for line in f.readlines():
                    line = line.strip()

                    if achou_nota:
                        nota = line
                        achou_nota = False

                    if line.startswith('== S'):
                        subm += 1
                    elif line.startswith('== T'):
                        test += 1
                    elif line.startswith('-- ER'):
                        err += 1
                    elif line.startswith('-- GRAD'):
                        achou_nota = True
                    elif re.search(r"^([\w_\.]+Error)", line):
                        m = re.match(r"^([\w_\.]+Error)", line)
                        if m:
                            erros.append(m.group(0))

                if len(erros):
                    Util.register_errors(erros)

                try:
                    if isinstance(nota, str):
                        nota = float(nota[:-1])
                    if nota > 99.99:
                        acertou = True
                except TypeError:
                    Logger.error(f'Erro ao tentar obter nota do estudante, na linha: {nota}')
                except ValueError:
                    Logger.error(f'Erro ao tentar obter nota do estudante, na linha: {nota}')

        except OSError:
            Logger.error(f'Erro ao tentar ler arquivo de execução: {path}')

        return [subm, test, err, nota, acertou]

    @staticmethod
    def get_execucoes(estudante):
        """
            Recupera todas as execuções feitas por um estudante para as atividades na turma que ele participou
            Cada estudante possui um registro de execuções para cada questão.
            As execuções estão localizadas dentro da pasta 'executions', dentro do diretório do estudante.
            As execuções de uma determinada questão corresponde a um arquivo de extensão '.log',
            e cujo nome é formado pela composição do código da atividade e do código da questão, separados por um 'underscore'.

            Args:
                estudante : Estudante
                    O estudante cujas execuções devem ser recuperadas
                    @see model.estudante.Estudante

            Returns:
                execucoes : list
                    Todas as execuções realizadas por um estudante, para as questões selecionadas em atividades que o estudante resolveu.
                    @see model.execucao.Execucao

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        execucoes = []

        try:
            # coleta todas os arquivos/pastas dentro do diretório de execuções do aluno
            with os.scandir(f'{estudante.path}/executions') as entries:
                for entry in entries:
                    # se a 'entrada' for um arquivo de extensão '.log', então corresponde as execuções de uma questão.
                    if entry.is_file() and entry.path.endswith('.log'):
                        Logger.debug(f'Arquivo de execução: {entry.path}')

                        # divide o nome do arquivo obtendo os códigos da atividade e exercício.
                        aid, eid, *_ = entry.name[:-4].split('_')
                        data = ControllerExecucao.__get_data_from_file(entry.path)
                        data_inicio, data_termino = ControllerExecucao.__get_codemirror_dates(f'{estudante.path}/codemirror/{entry.name}')

                        execucao = Execucao(
                            int(aid),
                            int(eid),
                            data_inicio,
                            data_termino,
                            data[0],
                            data[1],
                            data[2],
                            data[3],
                            data[4]
                        )

                        # execucao.print_info()
                        execucoes.append(execucao)

        except OSError:
            Logger.error(f'Erro ao acessar o diretório de execuções: {estudante.path}/executions')
            Util.wait_user_input()

        return execucoes

    @staticmethod
    def __get_property_value(text):
        idx = text.find(':')
        if idx > 0:
            return text.strip()[:idx]
        return None

    @staticmethod
    def save_execucoes(lista_execucoes):
        cwd = os.getcwd()
        output_file = f'{cwd}/csv/execucoes.csv'
        Logger.info(f'Salvando execuções no arquivo: {output_file}')
        with open(output_file, 'w') as file:
            # cabeçalho do arquivo 'csv'
            file.write(Execucao.get_columns() + os.linesep)
            writter = csv.writer(file)
            for e in lista_execucoes:
                writter.writerow(e)
