from util.Util import Util
from model.atividade import Atividade
from model.estudante import Estudante

import os


class Turma:

    def __init__(self, codigo, path):
        self.codigo = codigo
        self.path = path
        self.descricao = Turma.__get_descricao(f'{path}/assessments')

    @staticmethod
    def __get_descricao(path):
        """
            Retorna uma string com a descrição, de uma turma, obtida de um dos arquivo de atividades (assessments) da turma.

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
            assessment_path = ''
            with os.scandir(path) as entries:  # coleta todas os arquivos ou pastas no diretório informado
                for entry in entries:
                    # se a 'entrada' for um arquivo de extensão '.data' então corresponde avaliação
                    if entry.is_file() and entry.path.endswith('.data'):
                        assessment_path = entry.path
                        break

            arquivo = open(assessment_path, 'r')
            arquivo.readline()  # primeira linha é o cabeçalho do arquivo de avaliação
            arquivo.readline()  # segunda linha é o título da avaliação

            # terceira linha é enfim a descrição da turma
            # exemplo:
            # ---- class name: Introdução à Programação de Computadores
            descricao = arquivo.readline()[17:-1]

        except Exception as e:
            print(f'Erro ao acessar o caminho informado: {path}')
            print(f'Mensagem: {str(e)}')
            Util.count_error()
        finally:
            if arquivo is not None:
                arquivo.close()
        return descricao

    def get_atividades(self):
        """
            Recupera todas as atividades realizadas naquela turma.
            Cada turma possui informações sobre os alunos e atividades.
            As atividades estão localizadas dentro da pasta 'assessments', no diretório da turma.
            Cada atividade corresponde a um arquivo de extensão '.data'.

            Returns:
                atividades (lista): Todas as atividades realizadas na turma.

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        atividades = []
        assessments_path = f'{self.path}/assessments'

        try:
            files = []
            # coleta todas as 'entradas' (arquivos ou pastas) no diretório informado
            with os.scandir(assessments_path) as entries:
                for entry in entries:
                    # se a 'entrada' for um arquivo de extensão '.data', então corresponde a uma atividade.
                    if entry.is_file() and entry.path.endswith('.data'):
                        # remove a extensão do nome dos arquivos para que se possa ordenar as atividades por código
                        files.append(entry.name[:-5])

            try:
                files = [int(x) for x in files]
                files.sort()
                files = [str(x) for x in files]
            except Exception as e_cast:
                print(f'Erro ao tentar ordenar lista de avalições: {assessments_path}')
                print(f'Mensagem: {str(e_cast)}')
                Util.count_error()
                Util.wait_user_input()

            # percorre a lista de avaliações (arquivos) obtendo as informações de cada uma
            for file_name in files:
                atividade = Atividade(f'{assessments_path}/{file_name}.data')
                atividade.print_info()
                atividades.append(atividade)

                # Util.wait_user_input()

        except Exception as e:
            print(f'Erro ao acessar o caminho informado: {assessments_path}')
            print(f'Mensagem: {str(e)}')
            Util.count_error()
            Util.wait_user_input()

        return atividades

    def get_estudantes(self):
        """
            Recupera todas os estudantes (usuários) matriculados naquela turma.
            Cada turma possui informações sobre os alunos e atividades.
            Os alunos estão localizadas dentro da pasta 'users', no diretório da turma.
            Cada aluno possui suas informações dentre de uma pasta nomeada com seu 'id'.

            Returns:
                estudantes (lista): Todos os estudantes matriculados na turma.

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        estudantes = []
        students_path = f'{self.path}/users'

        try:
            folders = []
            # coleta todas as 'entradas' (arquivos ou pastas) no diretório informado
            with os.scandir(students_path) as entries:
                for entry in entries:
                    # se a 'entrada' for um diretório, então corresponde a um estudante.
                    if entry.is_dir():
                        folders.append(entry.name)

            try:
                folders = [int(x) for x in folders]
                folders.sort()
                folders = [str(x) for x in folders]
            except Exception as e_cast:
                print(f'Erro ao tentar ordenar lista de estudantes: {students_path}')
                print(f'Mensagem: {str(e_cast)}')
                Util.count_error()
                Util.wait_user_input()

            # percorre a lista de usuários (diretórios) obtendo as informações de cada um
            for folder in folders:
                estudante = Estudante(f'{students_path}/{folder}')
                estudante.print_info()
                estudantes.append(estudante)
                # Util.wait_user_input()

        except Exception as e:
            print(f'Erro ao acessar o caminho informado: {students_path}')
            print(f'Mensagem: {str(e)}')
            Util.count_error()
            Util.wait_user_input()

        return estudantes

    def print_info(self):
        """
             Imprime no console as informações de uma turma.
        """
        print(f'\t> Turma [{self.codigo}]: {self.descricao}')
        print(f'\t> Pasta: {self.path}\n')
