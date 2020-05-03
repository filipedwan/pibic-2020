from extractor import CodebenchExtractor
from util import Util, Logger
from parser import CSVParser

import os

__version__ = '3.1.0'
# cwd (current working dir): diretório de trabalho atual
__cwd__ = os.getcwd()
# dataset_path: diretório onde se encontra o dataset do codebenh
__dataset_dir__ = f'{__cwd__}/cb_dataset_v1.11/'


def main():
    # limpa o console de saída
    Util.clear_console()
    # cria a pasta para os arquivos de saídade (CSV), caso já exista, recria os arquivos
    CSVParser.create_output_dir()
    # configura o módulo de log
    Logger.configure()

    # recupera a lista de 'Periodos' dentro da pasta do dataset Codebench
    periodos = CodebenchExtractor.extract_periodos(__dataset_dir__)
    # os 'Periodos' são então salvos no arquivo '.csv'
    #CSVParser.salvar_periodos(periodos)

    for periodo in periodos:
        # extrai as 'Turmas' para o 'Período'
        CodebenchExtractor.extract_turmas(periodo)
        # salva as 'Turmas' no arquivo .'csv'
        #CSVParser.salvar_turmas(periodo.turmas)
        for turma in periodo.turmas:
            # extrai as 'Atividades' da 'Turma'
            CodebenchExtractor.extract_atividades(turma)
            # salva as 'Atividades' no arquivo '.csv'
            CSVParser.salvar_atividades(turma.atividades)
            # extrai os 'Estudantes' da 'Turma'
            # CodebenchExtractor.extract_estudantes(turma)
            # salva os 'Estudantes' no arquivo '.csv'
            #CSVParser.salvar_estudantes(turma.estudantes)
            #for estudante in turma.estudantes:
                # extrai as 'Execuções' do 'Estudante'
                #CodebenchExtractor.extract_execucoes(estudante)
                # salva as 'Execuções' no arquivo '.csv'
                #CSVParser.salvar_execucoes(estudante.execucoes)

    # extrai as métricas das 'Soluções' propostas pelos professores
    #solucoes = CodebenchExtractor.extract_solucoes(f'{__cwd__}/solutions')
    # salva as 'Soluções'  no arquivo '.csv'
    #CSVParser.salvar_solucoes(solucoes)


if __name__ == '__main__':
    import time
    start_time = time.time()
    main()
    time_elapsed = time.strftime('%H:%M:%S', time.gmtime(time.time() - start_time))
    print(f'Tempo Total de Execução: {time_elapsed}')
