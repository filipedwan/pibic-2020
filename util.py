import os
import logging
from datetime import datetime

from model import *

from collections import Counter


class Util:

    # função que pausa o console aguardando o usuário teclar [ENTER]
    @staticmethod
    def wait_user_input():
        input('{:^15s}'.format('Tecle [ENTER]...'))

    # função que limpa a tela do console
    @staticmethod
    def clear_console():
        os.system('clear')

    @staticmethod
    def count_errors(error_names, execucao: Execucao):
        """
        Contabiliza a quantidade de ocorrências de cada Tipo de Erro na lista.

        :param execucao: A Execução onde os Erros ocorreram
        :param error_names: Lista com os Tipos de Erros (com repetições).
        :return: Uma lista com os Erros e suas Ocorrências (quantidade).
        """
        c = Counter(error_names)

        erros = []
        for name in c.keys():
            e = Erro(name, c[name])
            e.periodo = execucao.periodo
            e.turma = execucao.turma
            e.atividade = execucao.atividade
            e.estudante = execucao.estudante
            e.exercicio = execucao.exercicio
            erros.append(e)

        return erros


class Logger:

    __path = os.getcwd() + '/logs'
    __cblogger = None

    @staticmethod
    def configure():
        logging.basicConfig(level=logging.INFO)

        if not os.path.exists(Logger.__path):
            os.mkdir(Logger.__path)

        formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')
        data_hoje = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        if not Logger.__cblogger:
            Logger.__cblogger = logging.getLogger('cblogger')

            dfh = logging.FileHandler(f'{Logger.__path}/{data_hoje}_debug.log')
            dfh.setLevel(level=logging.DEBUG)
            dfh.setFormatter(formatter)
            Logger.__cblogger.addHandler(dfh)

            ifh = logging.FileHandler(f'{Logger.__path}/{data_hoje}_info.log')
            ifh.setLevel(level=logging.INFO)
            ifh.setFormatter(formatter)
            Logger.__cblogger.addHandler(ifh)

            wfh = logging.FileHandler(f'{Logger.__path}/{data_hoje}_warn.log')
            wfh.setLevel(level=logging.WARNING)
            wfh.setFormatter(formatter)
            Logger.__cblogger.addHandler(wfh)

            efh = logging.FileHandler(f'{Logger.__path}/{data_hoje}_error.log')
            efh.setLevel(level=logging.ERROR)
            efh.setFormatter(formatter)
            Logger.__cblogger.addHandler(efh)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(level=logging.INFO)
            console_handler.setFormatter(formatter)
            Logger.__cblogger.addHandler(console_handler)

    @staticmethod
    def debug(msg: str):
        Logger.__cblogger.debug(msg)

    @staticmethod
    def info(msg: str):
        Logger.__cblogger.info(msg)

    @staticmethod
    def warn(msg: str):
        Logger.__cblogger.warning(msg)

    @staticmethod
    def error(msg: str):
        Logger.__cblogger.error(msg, exc_info=True)
