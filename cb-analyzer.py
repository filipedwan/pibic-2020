import os
import csv

from controller.atividade import ControllerAtividade
from controller.estudante import ControllerEstudante
from controller.execucao import ControllerExecucao
from controller.periodo import ControllerPeriodo
from controller.turma import ControllerTurma
from util.logger import Logger
from util.utilidades import Util


def save_execucoes(lista_execucoes, file_name):
    Logger.info(f'Salvando execuções no arquivo: {file_name}')
    with open(file_name, 'w') as file:
        file.write('periodo,turma_id,estudante_id,atividade_id,exercicio_id,data_inicio,data_termino,n_submissoes,n_testes,n_erros,nota_final,acertou\n')
        writter = csv.writer(file)
        for e in lista_execucoes:
            writter.writerow(e)


def save_estudantes(lista_estudantes, file_name):
    Logger.info(f'Salvando estudantes no arquivo: {file_name}')
    with open(file_name, 'w') as file:
        file.write('periodo,turma_id,estudante_id,curso_id,curso_nome,instituicao_id,instituicao_nome,escola_nome,escola_tipo,escola_turno,escola_ano_grad,sexo,ano_nascimento,estado_civil,tem_filhos\n')
        writter = csv.writer(file)
        for e in lista_estudantes:
            writter.writerow(e)


def save_atividades(lista_atividades, file_name):
    Logger.info(f'Salvando atividades no arquivo: {file_name}')
    with open(file_name, 'w') as file:
        file.write('turma_id,atividade_id,titulo,tipo,linguagem,peso,data_inicio,data_termino,n_exercicios,blocos_exercicios\n')
        writter = csv.writer(file)
        for a in lista_atividades:
            writter.writerow(a)


def save_turmas(lista_turmas, file_name):
    Logger.info(f'Salvando turmas no arquivo: {file_name}')
    with open(file_name, 'w') as file:
        file.write('periodo,turma_id,turma_descricao\n')
        writter = csv.writer(file)
        for t in lista_turmas:
            writter.writerow(t)


def save_periodos(lista_periodos, file_name):
    Logger.info(f'Salvando períodos no arquivo: {file_name}')
    with open(file_name, 'w') as file:
        file.write('periodo\n')
        writter = csv.writer(file)
        for p in lista_periodos:
            writter.writerow(p)


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
                        execucao.data_inicio,
                        execucao.data_termino,
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

    with open(f'{csv_path}/error_report.csv', 'w') as f:
        f.write('erro_name,error_count\n')
        writter = csv.writer(f)
        for name, count in Util.get_unique_errors():
            writter.writerow([name, count])


if __name__ == '__main__':
    main()
