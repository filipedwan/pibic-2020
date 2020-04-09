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

    # diretório dos datasets de saída
    try:
        os.mkdir(f'{cwd}/csv')
    except OSError:
        pass

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

    ControllerPeriodo.save_periodos(lista_periodos)
    lista_periodos.clear()
    del lista_periodos

    ControllerTurma.save_turmas(lista_turmas)
    lista_turmas.clear()
    del lista_turmas

    ControllerAtividade.save_atividades(lista_atividades)
    lista_atividades.clear()
    del lista_atividades

    ControllerEstudante.save_estudantes(lista_estudantes)
    lista_estudantes.clear()
    del lista_estudantes

    ControllerExecucao.save_execucoes(lista_execucoes)
    lista_execucoes.clear()
    del lista_execucoes

    with open(f'{cwd}/csv/erros_comuns.csv', 'w') as f:
        f.write('tipo,n_ocorrencias\n')
        writter = csv.writer(f)
        for name, count in Util.get_unique_errors():
            writter.writerow([name, count])


if __name__ == '__main__':
    main()
