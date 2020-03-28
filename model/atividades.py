from util.Util import Util
import os


class Atividade:

    def __init__(self, codigo, titulo, codigo_turma):
        self.codigo = codigo
        self.titulo = titulo
        self.codigo_turma = codigo_turma
        self.data_inicio = ''
        self.data_termino = ''
        self.linguagem = ''
        self.tipo = ''
        self.peso = 0.0
        self.n_questoes = 0
        self.exercicios = []

    @staticmethod
    def get_atividade_from_file(path):
        """
            Retorna uma Atividade com as propriedades obtidas de um arquivo de atividade (extensão '.data')

            Args:
                path (string): caminho absoluto do arquivo com as informações da atividade.

            Returns:
                atividade (string): A atividade realizada.

            Error:
                Em caso de erro retorna None.
        """
        atividade = None
        arquivo = None
        try:
            print('\t\tObtendo atividade do arquivo: ', path)
            arquivo = open(path, 'r')

            arquivo.readline()                               # primeira linha é apenas cabeçalho
            codigo = int(path.split('/')[-1][:-5])          # título da atividade
            titulo = arquivo.readline()[23:-1]              # título da atividade
            arquivo.readline()                              # descricao da turma
            codigo_turma = int(arquivo.readline()[19:-1])   # data de início da atividade

            atividade = Atividade(codigo, titulo, codigo_turma)

            atividade.data_inicio = arquivo.readline()[12:-1]       # data de início da atividade
            atividade.data_termino = arquivo.readline()[10:-1]      # data de encerramento da avaliação
            atividade.linguagem = arquivo.readline()[15:-1]         # linguagem de programação
            arquivo.readline()                                      # linha do codemirror é irrelevante
            atividade.tipo = arquivo.readline()[11:-1]              # tipo da atividade
            atividade.peso = float(arquivo.readline()[13:-1])       # peso da atividade
            atividade.n_questoes = int(arquivo.readline()[22:-1])   # número de execicios selecionados na atividade
            arquivo.readline()                                      # cabeçalho da listagem de exercícios

            line = arquivo.readline()
            while line:
                ex = line[18:-1]
                ex = ex.strip()
                if len(ex) > 0:  # verifica se exite alguma questão, pois no dataset alguns dados estão faltando
                    # os blocos consistem de códigos de exercícios, separados por 'or'
                    if ' or ' in ex:
                        # separa os códigos dos exercícios do bloco
                        ex = ex.split(' or ')
                        ex = [int(x) for x in ex]  # converte os códigos dos exercícios em inteiro
                        ex.sort()
                    else:
                        ex = int(ex)

                    atividade.exercicios.append(ex)
                line = arquivo.readline()

        except Exception as e:
            print(f'Erro ao acessar o arquivo informado: {path}')
            print(f'Mensagem: {str(e)}')
            Util.count_error()
            Util.wait_user_input()
        finally:
            # finally é sempre executado, então fechamos o arquivo se ele existir
            if arquivo is not None:
                arquivo.close()

        return atividade

    def print_info(self):
        print('\t\t- Avaliação [{}]: {}'.format(self.codigo, self.titulo))
        print('\t\t- De {} até {}'.format(self.data_inicio, self.data_termino))
        print('\t\t- Linguagem: {}'.format(self.linguagem))
        print('\t\t- Tipo: {}'.format(self.tipo))
        print('\t\t- Peso: {:.2f}'.format(self.peso))
        print('\t\t- Nº Questões: {}'.format(self.n_questoes))
        print('\t\t- Questões: {}'.format(self.exercicios))
