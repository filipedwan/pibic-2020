# TODO: metrias com >30 resoluções
from util.logger import Logger

from controller.periodo import ControllerPeriodo
from controller.turma import ControllerTurma
from controller.atividade import ControllerAtividade
from controller.estudante import ControllerEstudante
from controller.execucao import ControllerExecucao

from util.utilidades import Util

import os


def save_execucoes(lista_execucoes, file_name):
    Logger.info(f'Salvando execuções no arquivo: {file_name}')
    with open(file_name, 'w') as file:
        file.write('periodo,turma_id,estudante_id,atividade_id,exercicio_id,n_submissoes,n_testes,n_erros,nota_final,acertou\n')
        for e in lista_execucoes:
            file.write(f'{e[0]},{e[1]},{e[2]},{e[3]},{e[4]},{e[5]},{e[6]},{e[7]},{e[8]},{e[9]}\n')


def save_estudantes(lista_estudantes, file_name):
    Logger.info(f'Salvando estudantes no arquivo: {file_name}')
    with open(file_name, 'w') as file:
        file.write('periodo,turma_id,estudante_id,curso_id,curso_nome,instituicao_id,instituicao_nome,escola_nome,escola_tipo,escola_turno,escola_ano_grad,sexo,ano_nascimento,estado_civil,tem_filhos\n')
        for e in lista_estudantes:
            file.write(f'{e[0]},{e[1]},{e[2]},{e[3]},{e[4]},{e[5]},{e[6]},{e[7]},{e[8]},{e[9]},{e[10]},{e[11]},{e[12]},{e[13]},{e[14]}\n')


def save_atividades(lista_atividades, file_name):
    Logger.info(f'Salvando atividades no arquivo: {file_name}')
    with open(file_name, 'w') as file:
        file.write('turma_id,atividade_id,titulo,tipo,linguagem,peso,data_inicio,data_termino,n_exercicios,blocos_exercicios\n')
        for a in lista_atividades:
            file.write(f'{a[0]},{a[1]},{a[2]},{a[3]},{a[4]},{a[5]},{a[6]},{a[7]},{a[8]},{a[9]}\n')


def save_turmas(lista_turmas, file_name):
    Logger.info(f'Salvando turmas no arquivo: {file_name}')
    with open(file_name, 'w') as file:
        file.write('periodo,turma_id,turma_descricao\n')
        for t in lista_turmas:
            file.write(f'{t[0]},{t[1]},{t[2]}\n')


def save_periodos(lista_periodos, file_name):
    Logger.info(f'Salvando períodos no arquivo: {file_name}')
    with open(file_name, 'w') as file:
        file.write('periodo\n')
        for p in lista_periodos:
            file.write(f'{p[0]}\n')


def main():
    Util.clear_console()

    # cwd (current working dir): diretório de trabalho atual
    cwd = os.getcwd()
    # dataset_path: diretório onde se encontra o dataset do codebenh
    dataset_path = f'{cwd}/dataset/'
    # csv_path: diretório dos arquivos de saída
    csv_path = f'{cwd}/csv'

    lista_turmas = []
    lista_estudantes = []
    lista_periodos = []
    lista_atividades = []
    lista_execucoes = []

    for periodo in ControllerPeriodo.get_periodos(dataset_path):
        lista_periodos.append([periodo.descricao])

        for turma in ControllerTurma.get_turmas_periodo(periodo):
            lista_turmas.append([periodo.descricao,
                                 turma.id,
                                 turma.descricao])

            for atividade in ControllerAtividade.get_atividades(turma):
                lista_atividades.append([
                    atividade.turma_id,
                    atividade.id,
                    atividade.titulo,
                    atividade.tipo,
                    atividade.linguagem,
                    atividade.peso,
                    atividade.data_inicio,
                    atividade.data_termino,
                    atividade.n_questoes,
                    atividade.blocos_ex
                ])

            for estudante in ControllerEstudante.get_estudantes(turma):
                lista_estudantes.append([
                    periodo.descricao,
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
                    estudante.tem_filhos
                ])

                for execucao in ControllerExecucao.get_execucoes(estudante):
                    lista_execucoes.append([
                        periodo.descricao,
                        turma.id,
                        estudante.id,
                        execucao.atividade_id,
                        execucao.exercicio_id,
                        execucao.n_submissoes,
                        execucao.n_testes,
                        execucao.n_erros,
                        execucao.nota_final,
                        execucao.acertou
                    ])

    try:
        os.mkdir(csv_path)
    except OSError:
        pass

    save_periodos(lista_periodos, f'{csv_path}/periodos.csv')
    lista_periodos.clear()
    del lista_periodos

    save_turmas(lista_turmas, f'{csv_path}/turmas.csv')
    lista_turmas.clear()
    del lista_turmas

    save_atividades(lista_atividades, f'{csv_path}/atividades.csv')
    lista_atividades.clear()
    del lista_atividades

    save_estudantes(lista_estudantes, f'{csv_path}/estudantes.csv')
    lista_estudantes.clear()
    del lista_estudantes

    save_execucoes(lista_execucoes, f'{csv_path}/execucoes.csv')
    lista_execucoes.clear()
    del lista_execucoes

    with open('error_report.csv', 'w') as f:
        f.write('erro_name,error_count\n')
        for name, count in Util.get_unique_errors():
            f.write(f'{name}({count})\n')


if __name__ == '__main__':
    main()
