import os

from model.atividade import Atividade

from util.utilidades import Util
from util.logger import Logger


class ControllerAtividade:

    @staticmethod
    def __get_file_data(path):
        """
            Retorna uma Atividade com as propriedades obtidas de um arquivo de atividade (extensão '.data')

            Args:
                path (string): caminho absoluto do arquivo com as informações da atividade.

            Returns:
                atividade (string): A atividade realizada.

            Error:
                Em caso de erro retorna None.
        """
        data = dict()
        arquivo = None
        try:
            # print('\t\tObtendo dados da atividade do arquivo: ', path)
            data['codigo'] = int(path.split('/')[-1][:-5])  # código da atividade

            arquivo = open(path, 'r')
            lines = arquivo.readlines()
            blocos = []

            for line in lines:
                line = line.lower().strip()
                if line.startswith('---- as'):
                    data['titulo'] = line.split(':')[-1].strip()
                elif line.startswith('---- class nu'):
                    data['codigo_turma'] = int(line.split(':')[-1].strip())
                elif line.startswith('---- st'):
                    data['data_inicio'] = line.split(':')[-1].strip()
                elif line.startswith('---- en'):
                    data['data_termino'] = line.split(':')[-1].strip()
                elif line.startswith('---- la'):
                    data['linguagem'] = line.split(':')[-1].strip()
                elif line.startswith('---- la'):
                    data['linguagem'] = line.split(':')[-1].strip()
                elif line.startswith('---- ty'):
                    data['tipo'] = line.split(':')[-1].strip()
                elif line.startswith('---- ty'):
                    data['tipo'] = line.split(':')[-1].strip()
                elif line.startswith('---- we'):
                    data['peso'] = float(line.split(':')[-1].strip())
                elif line.startswith('---- to'):
                    data['n_questoes'] = int(line.split(':')[-1].strip())
                elif line.startswith('---- ex'):
                    bloco = line.split(':')[-1].strip()
                    if len(bloco) > 0:  # verifica se exite alguma questão, pois no dataset alguns dados estão faltando
                        # testa se realmente corresponde a um bloco de exercícios, blocos são separados por 'or'
                        if ' or ' in bloco:
                            # separa os códigos dos exercícios do bloco
                            bloco = bloco.split(' or ')
                            bloco = [int(x) for x in bloco]  # converte os códigos dos exercícios em inteiro
                            bloco.sort()
                        else:
                            bloco = int(bloco)

                        blocos.append(bloco)

            data['blocos_ex'] = blocos

        except Exception as e:
            Logger.error(f'Erro ao acessar o arquivo da atividade: {path}')
            Util.count_error()
            Util.wait_user_input()
        finally:
            # finally é sempre executado, então fechamos o arquivo se ele existir
            if arquivo is not None:
                arquivo.close()

        return data

    # noinspection PyBroadException
    @staticmethod
    def get_atividades(turma):
        """
            Recupera todas as atividades realizadas naquela turma.
            Cada turma possui informações sobre os alunos e atividades.
            As atividades estão localizadas dentro da pasta 'assessments', dentro do diretório da turma.
            Cada atividade corresponde a um arquivo de extensão '.data'.

            Args:
                turma : Turma
                    A turma da qual deve-se recupera as atividades
                    @see model.turma.Turma

            Returns:
                atividades : list
                    Todas as atividades realizadas na turma.

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        atividades = []
        assessments_path = f'{turma.path}/assessments'

        try:
            files = []
            # coleta todas os arquivos/pastas dentro do diretório de atividades da turma
            with os.scandir(assessments_path) as entries:
                for entry in entries:
                    # se a 'entrada' for um arquivo de extensão '.data', então corresponde a uma atividade.
                    if entry.is_file() and entry.path.endswith('.data'):
                        # remove a extensão do nome dos arquivos para que se possa ordenar as atividades por código
                        files.append(entry.name[:-5])

            # ordena as atividades por código
            try:
                files = [int(x) for x in files]
                files.sort()
                files = [str(x) for x in files]
            except Exception as e:
                Logger.error(f'Erro ao tentar ordenar lista de avalições: {assessments_path}')
                Util.count_error()
                Util.wait_user_input()

            # cria as 'atividades' com base nas informações de cada arquivo
            for file_name in files:
                data = ControllerAtividade.__get_file_data(f'{assessments_path}/{file_name}.data')

                atividade = Atividade(data.get('codigo', 0),
                                      data.get('titulo', ''),
                                      data.get('codigo_turma', 0),
                                      data.get('data_inicio', ''),
                                      data.get('data_termino', ''),
                                      data.get('linguagem', ''),
                                      data.get('tipo', ''),
                                      data.get('peso', 0.0),
                                      data.get('n_questoes', 0),
                                      data.get('blocos_ex', []))
                # atividade.print_info()
                atividades.append(atividade)

                # Util.wait_user_input()

        except Exception as e:
            Logger.error(f'Erro ao acessar o caminho informado: {assessments_path}')
            Util.count_error()
            Util.wait_user_input()

        return atividades

