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
                turmas (list): Todas as turmas do período.

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        turmas = []
        try:
            folders = []

            # coleta todas os arquivos/pastas dentro do diretório do período.
            with os.scandir(periodo.path) as entries:
                for entry in entries:
                    # se a 'entrada' for uma diretório (pasta) então corresponde a uma 'turma'
                    if entry.is_dir():
                        folders.append(entry.path)

            folders.sort()

            # cria uma 'turma' para cada diretório encontrado
            for folder in folders:
                code = int(folder.split('/')[-1])
                descricao = ControllerTurma.__get_turma_descricao(f'{folder}/assessments')
                turma = Turma(code, descricao, folder)
                # turma.print_info()

                turmas.append(turma)

        except Exception as e:
            print(f'Erro ao acessar o caminho informado: {periodo.path}')
            print(f'Mensagem: {str(e)}')
            Util.count_error()

        return turmas

    # noinspection PyBroadException
    @staticmethod
    def __get_turma_descricao(path):
        """
            Retorna uma string com a descrição de uma turma, obtida de um dos arquivo de atividades (assessments) da turma.

            Args:
                path (string): caminho absoluto do diretório onde se encontra as atividades da turma.

            Returns:
                descricao (string): A descrição da turma.

            Error:
                Em caso de erro retorna uma string vazia.
        """
        descricao = ''
        arquivo = None
        try:

            # assessment_path: caminho para alguma atividade da turma
            assessment_path = ''

            # coleta todas os arquivos/pastas no diretório informado (diretório de atividades da turma)
            with os.scandir(path) as entries:
                for entry in entries:
                    # se a 'entrada' for um arquivo de extensão '.data' então corresponde atividade
                    if entry.is_file() and entry.path.endswith('.data'):
                        assessment_path = entry.path
                        break

            # obtemos a descrição da turma que se encontra dentro do arquivo da atividade
            arquivo = open(assessment_path, 'r')

            # terceira linha eh onde se encontra a descrição da turma
            # exemplo:
            # ---- class name: Introdução à Programação de Computadores
            descricao = arquivo.readlines()[2][17:-1]

        except Exception as e:
            Logger.error(f'Erro ao acessar o caminho informado: {path}')
            Util.count_error()
        finally:
            if arquivo is not None:
                arquivo.close()

        return descricao

