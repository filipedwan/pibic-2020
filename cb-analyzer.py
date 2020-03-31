# TODO: metrias com >30 resoluções
import os
from model.periodo import Periodo
from util.Util import Util
import pandas as pd


def get_all_semesters(path):
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

    try:
        with os.scandir(
                path) as entries:  # coleta todas as 'entradas' (arquivos ou pastas) no caminho informado (path).
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
        print(f'Erro ao acessar o caminho informado: {path}')
        print(f'Mensagem: {str(e)}')
        Util.count_error()
        Util.wait_user_input()

    return periodos


def main():
    Util.clear_console()

    # cwd (current working dir): caminho onde está o Dataset do Codebench
    cwd = os.getcwd() + '/dataset/'

    periodos = get_all_semesters(cwd)

    data_turmas_periodo = []
    data_periodos = []
    for periodo in periodos:
        data_periodos.append([periodo.descricao, periodo.n_turmas])
        for turma in periodo.get_turmas_periodo():
            data_turmas_periodo.append([periodo.descricao, turma.codigo, turma.descricao])

    df_periodos = pd.DataFrame(data=data_periodos, columns=['periodo', 'n_turmas'])
    df_periodos.name = 'Periodos Letivos'

    df_turmas_periodo = pd.DataFrame(data=data_turmas_periodo, columns=['periodo', 'turma_codigo', 'turma_descricao'])
    df_turmas_periodo.name = 'Turmas por Periodo'

    try:
        if not os.path.isdir('csv'):
            os.mkdir('csv')

        df_periodos.to_csv('csv/periodos.csv')
        df_turmas_periodo.to_csv('csv/turmas_periodo.csv')

    except OSError:
        print("Creation of the directory 'csv' failed")
        Util.count_error()
        Util.wait_user_input()
    else:
        print("Successfully created the directory 'csv' and outputfiles")

    print('Erros encontrados: {}'.format(Util.get_total_errors()))


if __name__ == '__main__':
    main()
