import csv
import os
import shutil

from model import *
from util import Logger


class CSVParser:
    """Class Responsável por manipular os arquivos de saída '.csv'"""

    # diretório dos arquivos de saída '.csv' (datasets)
    __output_dir = os.getcwd() + '/csv'
    __periodos_csv = f'{__output_dir}/periodos.csv'
    __turmas_csv = f'{__output_dir}/turmas.csv'
    __atividades_csv = f'{__output_dir}/atividades.csv'
    __estudantes_csv = f'{__output_dir}/estudantes.csv'
    __execucoes_csv = f'{__output_dir}/execucoes.csv'
    __solucoes_csv = f'{__output_dir}/solucoes.csv'
    __erros_csv = f'{__output_dir}/erros.csv'

    @staticmethod
    def __create_csv_file(filename: str, header: List[str]):
        with open(filename, 'w') as f:
            header = ','.join(header) + os.linesep
            f.write(header)

    @staticmethod
    def create_output_dir():
        """Cria a pasta e os arquivos de saídas '.csv' (datasets)."""
        try:
            # se o diretório de saída existir, apaga seu conteúdo
            # if os.path.exists(CSVParser.__output_dir):
            #    shutil.rmtree(CSVParser.__output_dir)
            # cria o diretório de saída
            # os.mkdir(CSVParser.__output_dir)
            # cria todos os arquivos de saída '.csv' (datasets)
            # CSVParser.__create_csv_file(CSVParser.__periodos_csv, Periodo.get_csv_header())
            # CSVParser.__create_csv_file(CSVParser.__turmas_csv, Turma.get_csv_header())
            # CSVParser.__create_csv_file(CSVParser.__atividades_csv, Atividade.get_csv_header())
            # CSVParser.__create_csv_file(CSVParser.__estudantes_csv, Estudante.get_csv_header())
            CSVParser.__create_csv_file(CSVParser.__execucoes_csv, Execucao.get_csv_header())
            # CSVParser.__create_csv_file(CSVParser.__solucoes_csv, Solucao.get_csv_header())
            # CSVParser.__create_csv_file(CSVParser.__erros_csv, Erro.get_csv_header())
        except OSError:
            Logger.error('Erro ao criar diretório de saída!')

    @staticmethod
    def __write_to_csv(entidades: List[CSVEntity], path: str, mode: str):
        """
        Salva uma lista de :class:`CsvEntity` num arquivo no formato CSV.

        :param entidades: Lista de Entidades a serem salvas.
        :type entidades: List[CSVEntity]
        :param path: Caminho absoluto do arquivo '.csv' onde as Entidades devam ser salvas.
        :type path: str
        :param mode: Modo de abertura do arquivo.
        :type mode: str
        """
        Logger.info(f'Salvando entidades no arquivo: {path}')
        rows = []
        for entidade in entidades:
            rows.append(entidade.as_row())

        with open(path, mode) as file:
            writter = csv.writer(file)
            writter.writerows(rows)

    @staticmethod
    def salvar_periodos(periodos: List[Periodo]):
        """
        Salva uma lista de :class:`Periodo` no arquivo '.csv' (dataset).

        :param periodos: Lista de Períodos a serem salvos.
        """
        CSVParser.__write_to_csv(periodos, CSVParser.__periodos_csv, 'a')

    @staticmethod
    def salvar_turmas(turmas: List[Turma]):
        """
        Salva uma lista de :class:`Turma` no arquivo '.csv' (dataset).

        :param turmas: Lista de Turmas a serem salvos.
        """
        CSVParser.__write_to_csv(turmas, CSVParser.__turmas_csv, 'a')

    @staticmethod
    def salvar_atividades(atividades: List[Atividade]):
        """
        Salva uma lista de :class:`Atividade` no arquivo '.csv' (dataset).

        :param atividades: Lista de Atividades a serem salvas.
        """
        CSVParser.__write_to_csv(atividades, CSVParser.__atividades_csv, 'a')

    @staticmethod
    def salvar_estudantes(estudantes: List[Estudante]):
        """
         Salva uma lista de :class:`Estudante` no arquivo '.csv' (dataset).

         :param estudantes: Lista de Estudantes a serem salvos.
         """
        CSVParser.__write_to_csv(estudantes, CSVParser.__estudantes_csv, 'a')

    @staticmethod
    def salvar_execucoes(execucoes: List[Execucao]):
        """
         Salva uma lista de :class:`Execucao` no arquivo '.csv' (dataset).

         :param execucoes: Lista de Execucões a serem salvas.
        """
        CSVParser.__write_to_csv(execucoes, CSVParser.__execucoes_csv, 'a')

    @staticmethod
    def salvar_solucoes(solucoes: List[Solucao]):
        """
         Salva uma lista de :class:`Solucao` no arquivo '.csv' (dataset).

         :param solucoes: Lista de Solucões a serem salvas.
        """
        CSVParser.__write_to_csv(solucoes, CSVParser.__solucoes_csv, 'a')

    @staticmethod
    def salvar_erros(erros: List[Erro]):
        """
         Salva uma lista de :class:`Erro` no arquivo '.csv' (dataset).

         :param erros: Lista de Erros a serem salvos.
        """
        CSVParser.__write_to_csv(erros, CSVParser.__erros_csv, 'a')

