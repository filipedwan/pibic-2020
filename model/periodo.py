from util.Util import Util
from model.turma import Turma
import os


class Periodo:

    def __init__(self, descricao, path):
        self.descricao = descricao
        self.path = path
        self.turmas = Periodo.__get_turmas_periodo(path)

    @staticmethod
    def __get_turmas_periodo(path):
        """
            Retorna uma lista contendo todas as turmas de um período letivo, dado o caminho (diretório) do período.
            Cada turma corresponde a uma pasta dentro do diretório, '220' por exemplo são os dados da turma de número 220.

            Args:
                path (string): caminho absoluto do diretório onde se encontra as turmas do período.

            Returns:
                turmas (list): Todas as turmas do período.

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        turmas = []
        try:
            folders = []

            with os.scandir(path) as entries:  # coleta todas os arquivos ou pastas dentro do diretório do período.
                for entry in entries:
                    if entry.is_dir():  # se a 'entrada' for um diretório (pasta) então corresponde a uma turma válida
                        folders.append(entry.path)

            folders.sort()
            for folder in folders:
                code = int(folder.split('/')[-1])
                turma = Turma(code, folder)
                turma.print_info()

                turmas.append(turma)

        except Exception as e:
            print(f'Erro ao acessar o caminho informado: {path}')
            print(f'Mensagem: {str(e)}')
            Util.count_error()

        return turmas

    def print_info(self):
        """
            Imprime no console as informações de um período.
        """
        print('[{:-^120s}]'.format(f' Periodo: {self.descricao} '))
        print(f'> Pasta: {self.path}\n')
        Util.wait_user_input()
