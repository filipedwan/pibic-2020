import os
from numpy import NaN

from model.estudante import Estudante

from util.utilidades import Util
from util.logger import Logger


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
                    if line.startswith('---- cou') and index == 0:
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

        except OSError:
            Logger.error(f'Erro ao acessar o arquivo de estudante: {path}')
            Util.wait_user_input()

        return data

    @staticmethod
    def __get_property_value(text):
        # TODO: doc
        value = str(text).split(':')[-1].strip()
        return value

