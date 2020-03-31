# TODO: metrias com >30 resoluções
from util.logger import Logger

from controller.controller_periodo import ControllerPeriodo
from util.utilidades import Util

import os
import pandas as pd


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

    periodos = ControllerPeriodo.carrega_periodos(cwd)

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
