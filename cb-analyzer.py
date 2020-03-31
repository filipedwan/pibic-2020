# TODO: metrias com >30 resoluções
import os
from util.logger import Logger

from model.periodo import Periodo
from util.utilidades import Util

import pandas as pd


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


def cria_dataframe_estudante(data_estudantes):
    df_estudantes = pd.DataFrame(data=data_estudantes, columns=['periodo',
                                                                'turma_id',
                                                                'estudante_id',
                                                                'curso_id',
                                                                'curso_nome',
                                                                'instituicao_id',
                                                                'instituicao_nome',
                                                                'escola_nome',
                                                                'escola_tipo',
                                                                'escola_turno',
                                                                'escola_ano_grad',
                                                                'sexo',
                                                                'ano_nascimento',
                                                                'estado_civil',
                                                                'tem_filhos'])
    df_estudantes.name = 'Estudantes'
    return df_estudantes


def cria_dataframe_turmas(data_turmas):
    df_turmas = pd.DataFrame(data=data_turmas, columns=['periodo',
                                                        'turma_id',
                                                        'turma_descricao'])
    df_turmas.name = 'Turmas'
    return df_turmas


def cria_dataframe_periodos(data_periodos):
    df_periodos = pd.DataFrame(data=data_periodos, columns=['periodo'])
    return df_periodos


def cria_dataframe_atividades(lista_atividades):
    df_atividades = pd.DataFrame(data=lista_atividades, columns=['atividde_id',
                                                                 'titulo',
                                                                 'turma_id',
                                                                 'tipo',
                                                                 'linguagem',
                                                                 'peso',
                                                                 'data_inicio',
                                                                 'data_termino',
                                                                 'n_questoes',
                                                                 'blocos_ex'])
    return df_atividades


def main():
    Util.clear_console()

    # cwd (current working dir): caminho onde está o Dataset do Codebench
    cwd = os.getcwd() + '/dataset/'

    periodos = carrega_periodos(cwd)

    lista_turmas = []
    lista_estudantes = []
    lista_periodos = []
    lista_atividades = []

    for periodo in periodos:
        lista_periodos.append([periodo.descricao])

        for turma in periodo.get_turmas_periodo():
            lista_turmas.append([periodo.descricao,
                                 turma.id,
                                 turma.descricao])

            for atividade in turma.get_atividades():
                lista_atividades.append([atividade.id,
                                         atividade.titulo,
                                         atividade.turma_id,
                                         atividade.tipo,
                                         atividade.linguagem,
                                         atividade.peso,
                                         atividade.data_inicio,
                                         atividade.data_termino,
                                         atividade.n_questoes,
                                         atividade.blocos_ex])

            for estudante in turma.get_estudantes():
                lista_estudantes.append([periodo.descricao,
                                         turma.id,
                                         estudante.id,
                                         estudante.curso_id,
                                         estudante.curso_nome,
                                         estudante.instituicao_id,
                                         estudante.instituicao_nome,
                                         estudante.escola_nome,
                                         estudante.escola_tipo,
                                         estudante.escola_turno,
                                         estudante.escola_ano_grad,
                                         estudante.sexo,
                                         estudante.ano_nascimento,
                                         estudante.estado_civil,
                                         estudante.tem_filhos])

    try:
        if not os.path.isdir('csv'):
            os.mkdir('csv')

        df_periodos = cria_dataframe_periodos(lista_periodos)
        df_periodos.to_csv('csv/periodos.csv')
        lista_periodos.clear()
        del lista_periodos

        df_turmas = cria_dataframe_turmas(lista_turmas)
        df_turmas.to_csv('csv/turmas.csv')
        lista_turmas.clear()
        del lista_turmas

        df_atividades = cria_dataframe_atividades(lista_atividades)
        df_atividades.to_csv('csv/atividades.csv')
        lista_atividades.clear()
        del lista_atividades

        df_estudantes = cria_dataframe_estudante(lista_estudantes)
        df_estudantes.to_csv('csv/estudantes.csv')
        lista_estudantes.clear()
        del lista_estudantes

    except OSError:
        Logger.error("Não foi possível criar a pasta 'csv'!")
        Util.count_error()
        Util.wait_user_input()
    else:
        print("Pasta 'csv' criada com sucesso!")

    print('Erros encontrados: {}'.format(Util.get_total_errors()))


if __name__ == '__main__':
    # main()
    Logger.debug('debug')
    Logger.info('info')
    Logger.warn('wanning')
    try:
        x = 0/0
    except ZeroDivisionError as e:
        Logger.error('erro')
