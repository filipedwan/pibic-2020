from util.logger import Logger
from util.utilidades import Util

from model.periodo import Periodo

import os


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
