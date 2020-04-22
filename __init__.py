from controllers import *
from util import *

__version__ = '1.1.0'


def main():
    import os

    Util.clear_console()
    # cwd (current working dir): diretório de trabalho atual
    cwd = os.getcwd()
    # dataset_path: diretório onde se encontra o dataset do codebenh
    dataset_path = f'{cwd}/dataset/'
    csv_output_path = f'{cwd}/csv'
    periodos_csv_file = f'{csv_output_path}/periodos.csv'
    turmas_csv_file = f'{csv_output_path}/turmas.csv'
    atividades_csv_file = f'{csv_output_path}/atividades.csv'
    estudantes_csv_file = f'{csv_output_path}/estudantes.csv'
    execucoes_csv_file = f'{csv_output_path}/execucoes.csv'
    solucoes_csv_file = f'{csv_output_path}/solucoes.csv'

    # diretório dos datasets de saída
    try:
        if not os.path.exists(csv_output_path):
            os.mkdir(csv_output_path)

        with open(periodos_csv_file, 'w') as f:
            f.write(Periodo.get_columns() + os.linesep)

        with open(turmas_csv_file, 'w') as f:
            f.write(Turma.get_columns() + os.linesep)

        with open(atividades_csv_file, 'w') as f:
            f.write(Atividade.get_columns() + os.linesep)

        with open(estudantes_csv_file, 'w') as f:
            f.write(Estudante.get_columns() + os.linesep)

        with open(execucoes_csv_file, 'w') as f:
            f.write(Execucao.get_columns() + os.linesep)

        with open(solucoes_csv_file, 'w') as f:
            f.write(Execucao.get_columns() + os.linesep)

    except OSError:
        pass

    periodos = ControllerPeriodo.get_periodos(dataset_path)
    ControllerPeriodo.save_periodos(periodos, periodos_csv_file)

    for periodo in periodos:
        turmas = ControllerTurma.get_turmas_periodo(periodo)
        ControllerTurma.save_turmas(turmas, turmas_csv_file)
        for turma in turmas:
            atividades = ControllerAtividade.get_atividades(turma)
            ControllerAtividade.save_atividades(atividades, atividades_csv_file)
            del atividades

            estudantes = ControllerEstudante.get_estudantes(turma)
            ControllerEstudante.save_estudantes(estudantes, estudantes_csv_file)
            for estudante in estudantes:
                execucoes = ControllerExecucao.get_execucoes(estudante)
                ControllerExecucao.save_execucoes(execucoes, execucoes_csv_file)
                del execucoes
            del estudantes
        del turmas
    del periodos

    solutions_metrics = ControllerSolucao.get_metricas(f'{cwd}/solutions')
    ControllerSolucao.save_metricas(solutions_metrics, solucoes_csv_file)

    with open(f'{cwd}/csv/erros_comuns.csv', 'w') as f:
        f.write('tipo,n_ocorrencias\n')
        writter = csv.writer(f)
        for name, count in Util.get_unique_errors():
            writter.writerow([name, count])


if __name__ == '__main__':
    main()
