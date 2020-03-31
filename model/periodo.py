from util.utilidades import Util
from model.turma import Turma
import os


class Periodo:

    def __init__(self, descricao, path):
        self.descricao = descricao
        self.path = path

    def get_turmas_periodo(self):
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
            with os.scandir(self.path) as entries:
                for entry in entries:
                    # se a 'entrada' for uma diretório (pasta) então corresponde a uma 'turma'
                    if entry.is_dir():
                        folders.append(entry.path)

            folders.sort()

            # cria uma 'turma' para cada diretório encontrado
            for folder in folders:
                code = int(folder.split('/')[-1])
                turma = Turma(code, folder)
                # turma.print_info()

                turmas.append(turma)

        except Exception as e:
            print(f'Erro ao acessar o caminho informado: {self.path}')
            print(f'Mensagem: {str(e)}')
            Util.count_error()

        return turmas

    def print_info(self):
        """
            Imprime no console as informações de um período.
        """
        print('[{:-^120s}]'.format(f' Periodo: {self.descricao} '))
        print(f'> Pasta: {self.path}\n')
