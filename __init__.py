from extractors import *
from util import *

__version__ = '2.0.0'
# cwd (current working dir): diretório de trabalho atual
__cwd__ = os.getcwd()
# dataset_path: diretório onde se encontra o dataset do codebenh
__dataset_dir__ = f'{__cwd__}/cb_dataset_v1.11/'
# diretório dos arquivos de saída (datasets)
__output_dir__ = f'{__cwd__}/csv'


def main():
    # limpa o console de saída
    Util.clear_console()

    # cria a pasta para os arquivos de saídade (CSV), caso já exista, recria os arquivos
    Util.create_output_dir(__output_dir__)

    # configura o módulo de log
    Logger.configure()

    periodos = PeriodoExtractor.get_periodos(__dataset_dir__)
    PeriodoExtractor.save_periodos(periodos, f'{__output_dir__}/periodos.csv')

    for periodo in periodos:
        TurmaExtractor.get_turmas_periodo(periodo)
        TurmaExtractor.save_turmas(periodo.turmas, f'{__output_dir__}/turmas.csv')
        for turma in periodo.turmas:
            AtividadeExtractor.get_atividades(turma)
            AtividadeExtractor.save_atividades(turma.atividades, f'{__output_dir__}/atividades.csv')

            EstudanteExtractor.get_estudantes(turma)
            EstudanteExtractor.save_estudantes(turma.estudantes, f'{__output_dir__}/estudantes.csv')
            for estudante in turma.estudantes:
                ExecucaoExtractor.get_execucoes(estudante)
                ExecucaoExtractor.save_execucoes(estudante.execucoes, f'{__output_dir__}/execucoes.csv')

    solutions_metrics = SolucaoExtractor.get_metricas(f'{__cwd__}/solutions')
    SolucaoExtractor.save_metricas(solutions_metrics, f'{__output_dir__}/solucoes.csv')


if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    time_elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))
    print(f'Tempo Total de Execução: {time_elapsed}')
