from util.logger import Logger
from util.utilidades import Util

from model.periodo import Periodo

import os


class ControllerPeriodo:

    @staticmethod
    def carrega_periodos(path):
        """
            Retorna uma lista contendo as informações de todos os periodos letivos (pastas) encontrados no dataset Codebench.
            Cada período corresponde a uma pasta, '2017-01' por exemplo são os dados do primeiro período do ano de 2017.

            Args:
                path (string): caminho absoluto do diretório onde se encontra o dataset Codebench.

            Returns:
                periodos (list): Uma lista de dicionários contendo as informações dos períodos.

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        periodos = []

        # noinspection PyBroadException
        try:
            # coleta todas as 'entradas' (arquivos ou pastas) no caminho informado (path).
            with os.scandir(path) as entries:
                folders = []  # lista que irá guardar todas as pastas encontradas no caminho informado (path).
                for entry in entries:
                    # entry: name, path, is_dir(), is_file(), stat
                    if entry.is_dir():  # se for uma pasta então corresponde a um período letivo
                        folders.append(entry.path)

                folders.sort()  # ordena as pastas (períodos)
                for folder in folders:  # percorre cada pasta (período) coletando informações

                    descricao = folder.split('/')[-1]

                    p = Periodo(descricao, folder)
                    p.print_info()

                    periodos.append(p)

                    # utilidades.wait_key()
                    # utilidades.clear_console()

        except Exception as e:
            Logger.error(f'Erro ao acessar o caminho informado: {path}')
            Util.count_error()
            Util.wait_user_input()

        return periodos
