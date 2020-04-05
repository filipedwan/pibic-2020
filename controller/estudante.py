import os

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
                estudantes (lista): Todos os estudantes matriculados na turma.

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
                        Logger.debug(f'Arquivo: {entry.path}')
                        data = ControllerEstudante.__get_file_data(f'{entry.path}/user.data')
                        estudante = Estudante(int(entry.name),
                                              entry.path,
                                              data.get('curso_id', 0),
                                              data.get('curso_nome', ''),
                                              data.get('instituicao_id', 0),
                                              data.get('instituicao_nome', ''),
                                              data.get('escola_nome', ''),
                                              data.get('escola_tipo', ''),
                                              data.get('escola_turno', ''),
                                              data.get('escola_ano_grad', 0),
                                              data.get('sexo', ''),
                                              data.get('ano_nascimento', 0),
                                              data.get('estado_civil', ''),
                                              data.get('tem_filhos', False))
                        data.clear()
                        del data

                        # estudante.print_info()
                        Logger.info(f'Estudante encontrado!')
                        estudantes.append(estudante)

        except OSError:
            Logger.error(f'Erro ao acessar o diretório de estudantes: {turma.path}/users')
            Util.wait_user_input()

        return estudantes

    @staticmethod
    def __get_file_data(path):
        # TODO: doc
        arquivo = None
        data = dict()

        try:
            arquivo = open(path, 'r')
            lines = arquivo.readlines()

            for index, line in enumerate(lines, start=1):
                line = line.lower().strip()
                if index == 2 and line.startswith('---- course id:'):
                    data['curso_id'] = int(ControllerEstudante.__get_property_value(line))
                elif index == 3 and line.startswith('---- course name:'):
                    data['curso_nome'] = ControllerEstudante.__get_property_value(line)
                elif index == 4 and line.startswith('---- institution id:'):
                    data['instituicao_id'] = int(ControllerEstudante.__get_property_value(line))
                elif index == 5 and line.startswith('---- institution name:'):
                    data['instituicao_nome'] = ControllerEstudante.__get_property_value(line)
                elif index == 7 and line.startswith('---- high school name:'):
                    data['escola_nome'] = ControllerEstudante.__get_property_value(line)
                elif index == 8 and line.startswith('---- school type:'):
                    data['escola_tipo'] = ControllerEstudante.__get_property_value(line)
                elif index == 9 and line.startswith('---- shift:'):
                    data['escola_turno'] = ControllerEstudante.__get_property_value(line)
                elif index == 10 and line.startswith('---- graduation year:'):
                    data['escola_ano_grad'] = int(ControllerEstudante.__get_property_value(line))
                elif index == 28 and line.startswith('---- sex:'):
                    data['sexo'] = ControllerEstudante.__get_property_value(line)
                elif index == 29 and line.startswith('---- year of birth:'):
                    data['ano_nascimento'] = int(ControllerEstudante.__get_property_value(line))
                elif index == 30 and line.startswith('---- civil status:'):
                    data['estado_civil'] = ControllerEstudante.__get_property_value(line)
                elif index == 31 and line.startswith('---- have kids:'):
                    data['tem_filhos'] = True if ControllerEstudante.__get_property_value(line) == 'yes' else False

        except OSError:
            Logger.error(f'Erro ao acessar o arquivo de estudante: {path}')
            Util.wait_user_input()
        finally:
            if arquivo is not None:
                arquivo.close()

        return data

    @staticmethod
    def __get_property_value(text):
        # TODO: doc
        value = str(text).split(':')[-1].strip()
        return value

