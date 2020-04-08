import os

from model.turma import Turma

from util.utilidades import Util
from util.logger import Logger


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
