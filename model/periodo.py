from util.utilidades import Util
from model.turma import Turma
import os


class Periodo:

    def __init__(self, descricao, path):
        self.descricao = descricao
        self.path = path

    def print_info(self):
        """
            Imprime no console as informações de um período.
        """
        print('[{:-^120s}]'.format(f' Periodo: {self.descricao} '))
        print(f'> Pasta: {self.path}\n')
