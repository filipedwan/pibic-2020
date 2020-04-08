import os

from numpy import NaN

from model.atividade import Atividade

from util.utilidades import Util
from util.logger import Logger


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
                        if len(bloco) > 0:  # verifica se exite alguma questão, pois no dataset alguns dados estão faltando
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

