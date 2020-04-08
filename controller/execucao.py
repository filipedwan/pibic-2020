import os
import re

from numpy import NaN
from model.execucao import Execucao

from util.utilidades import Util
from util.logger import Logger


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

                start_date = lines[0].split('#')[0]
                end_date = lines[-1].split('#')[0]

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
        subm = NaN
        test = NaN
        err = NaN
        nota = NaN
        acertou = False

        try:
            with open(path, 'r') as f:
                achou_nota = False

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
                    elif re.search(r"^[a-zA-Z0-9_\.]+Error", line):
                        Util.register_errors(line.split(':')[0])

                try:
                    if nota:
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
