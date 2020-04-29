import os
import shutil
import logging
import csv

from model import *

from collections import Counter


class Util:
    __error_names = []
    __error_count = []

    # função que pausa o console aguardando o usuário teclar [ENTER]
    @staticmethod
    def wait_user_input():
        input('{:^15s}'.format('Tecle [ENTER]...'))

    # função que limpa a tela do console
    @staticmethod
    def clear_console():
        os.system('clear')

    @staticmethod
    def register_errors(error_list, execucao: Execucao):
        error_names = Counter(error_list).keys()
        error_count = Counter(error_list).values()

        with open(f'{os.getcwd()}/csv/erros.csv', 'a') as f:
            writter = csv.writer(f)
            for name, count in zip(error_names, error_count):
                writter.writerow([
                    execucao.periodo,
                    execucao.turma,
                    execucao.atividade,
                    execucao.estudante,
                    execucao.exercicio,
                    name,
                    count
                ])

    @staticmethod
    def create_output_dir(output_path):
        # diretório dos datasets de saída
        try:
            if os.path.exists(output_path):
                shutil.rmtree(output_path)

            os.mkdir(output_path)

            with open(f'{output_path}/periodos.csv', 'w') as f:
                header = ','.join(Periodo.get_attr_names()) + os.linesep
                f.write(header)

            with open(f'{output_path}/turmas.csv', 'w') as f:
                header = ','.join(Turma.get_attr_names()) + os.linesep
                f.write(header)

            with open(f'{output_path}/atividades.csv', 'w') as f:
                header = ','.join(Atividade.get_attr_names()) + os.linesep
                f.write(header)

            with open(f'{output_path}/estudantes.csv', 'w') as f:
                header = ','.join(Estudante.get_attr_names()) + os.linesep
                f.write(header)

            with open(f'{output_path}/execucoes.csv', 'w') as f:
                header = ','.join(Execucao.get_attr_names()) + os.linesep
                f.write(header)

            with open(f'{output_path}/solucoes.csv', 'w') as f:
                header = ','.join(Solucao.get_attr_names()) + os.linesep
                f.write(header)

            with open(f'{output_path}/erros.csv', 'w') as f:
                f.write(','.join(Erro.get_attr_names()) + os.linesep)

        except OSError:
            Logger.error('Erro ao criar diretório de saída!')


class Logger:
    __path = os.getcwd() + '/logs'
    __debug = None
    __info = None
    __warn = None
    __error = None

    @staticmethod
    def configure():
        logging.basicConfig(level=logging.DEBUG)

        if not os.path.exists(Logger.__path):
            os.mkdir(Logger.__path)

        Logger.configure_debugger()
        Logger.configure_info()
        Logger.configure_warn()
        Logger.configure_error()

    @staticmethod
    def debug(msg: str):
        Logger.__debug.debug(msg)

    @staticmethod
    def info(msg: str):
        Logger.__info.info(msg)

    @staticmethod
    def warn(msg: str):
        Logger.__warn.warning(msg)

    @staticmethod
    def error(msg: str):
        Logger.__error.error(msg, exc_info=True)

    @staticmethod
    def configure_debugger():
        if not Logger.__debug:
            Logger.__debug = logging.getLogger('debug')
            formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')

            file_handler = logging.FileHandler(f'{Logger.__path}/debug.log')
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            Logger.__debug.addHandler(file_handler)
            Logger.__debug.addHandler(console_handler)

    @staticmethod
    def configure_info():
        if not Logger.__info:
            Logger.__info = logging.getLogger('info')
            formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')

            file_handler = logging.FileHandler(f'{Logger.__path}/info.log')
            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)

            Logger.__info.addHandler(file_handler)

    @staticmethod
    def configure_warn():
        if not Logger.__warn:
            Logger.__warn = logging.getLogger('warn')
            formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')

            file_handler = logging.FileHandler(f'{Logger.__path}/warn.log')
            file_handler.setLevel(logging.WARNING)
            file_handler.setFormatter(formatter)

            Logger.__warn.addHandler(file_handler)

    @staticmethod
    def configure_error():
        if not Logger.__error:
            Logger.__error = logging.getLogger('error')

            formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')

            file_handler = logging.FileHandler(f'{Logger.__path}/error.log')
            file_handler.setLevel(logging.ERROR)
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.ERROR)
            console_handler.setFormatter(formatter)

            Logger.__error.addHandler(file_handler)
            Logger.__error.addHandler(console_handler)
