import os

from model.execucao import Execucao

from util.utilidades import Util
from util.logger import Logger


class ControllerExecucao:

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
        arquivo = None
        data = dict()
        try:
            arquivo = open(path, 'r')
            lines = arquivo.readlines()
            lines = [x.strip() for x in lines]
            find_grade = False

            sub = len([x for x in lines if x.startswith('== SU')])
            data['n_submissoes'] = sub

            test = len([x for x in lines if x.startswith('== TE')])
            data['n_testes'] = test

            err = len([x for x in lines if x.startswith('== ER')])
            data['n_erros'] = err

            found_erros = [x.split(':')[0] for x in lines if 'Error' in x]
            Util.register_errors(found_erros)

            for line in lines:
                if find_grade:
                    find_grade = False
                    data['nota_final'] = float(line[:-1])
                elif line.startswith('-- GR'):
                    find_grade = True
                    continue

            lines.clear()
            del lines

        except Exception as e:
            Logger.error(str(e))
            Util.wait_user_input()
        finally:
            if arquivo is not None:
                arquivo.close()

        return data

    @staticmethod
    def get_execucoes(estudante):
        """
            Recupera todas as execuções feitas por um estudante para as atividades na turma que ele participou
            Cada estudante possui um registro de execuções para cada questão.
            As execuções estão localizadas dentro da pasta 'executions', dentro do diretório do estudante.
            As execuções de uma determinada questão corresponde a um arquivo de extensão '.log',
            e cujo nome é formado pela composição do código da atividade e do código da questão, separados por um 'underscore'.

            Args:
                estudante : Estudante
                    O estudante cujas execuções devem ser recuperadas
                    @see model.estudante.Estudante

            Returns:
                execucoes : list
                    Todas as execuções realizadas por um estudante, para as questões selecionadas em atividades que o estudante resolveu.

            Error:
                Em caso de erro retorna uma lista vazia.
        """
        execucoes = []

        try:
            # coleta todas os arquivos/pastas dentro do diretório de execuções do aluno
            with os.scandir(f'{estudante.path}/executions') as entries:
                for entry in entries:
                    # se a 'entrada' for um arquivo de extensão '.log', então corresponde as execuções de uma questão.
                    if entry.is_file() and entry.path.endswith('.log'):
                        Logger.debug(f'Arquivo: {entry.path}')
                        data = ControllerExecucao.__get_file_data(entry.path)

                        data['atividade_id'] = int(entry.name[:-4].split('_')[0])
                        data['exercicio_id'] = int(entry.name[:-4].split('_')[1])
                        acertou = True if data.get('nota_final', 0.0) > 99.99 else False

                        execucao = Execucao(data.get('atividade_id', 0),
                                            data.get('exercicio_id', 0),
                                            data.get('n_submissoes', 0),
                                            data.get('n_testes', 0),
                                            data.get('n_erros', 0),
                                            data.get('nota_final', 0.0),
                                            acertou)
                        # execucao.print_info()
                        Logger.info(f'Execução encontrada!')
                        execucoes.append(execucao)

        except OSError:
            Logger.error(f'Erro ao acessar o caminho informado: {estudante.path}/executions')
            Util.wait_user_input()

        return execucoes
