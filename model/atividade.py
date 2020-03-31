from util.Util import Util


class Atividade:

    def __init__(self, file_path):
        data = Atividade.get_atividade_from_file(file_path)
        self.codigo = data.get('codigo', 0)
        self.titulo = data.get('titulo', '')
        self.codigo_turma = data.get('codigo_turma', 0)
        self.data_inicio = data.get('data_inicio', '')
        self.data_termino = data.get('data_termino', '')
        self.linguagem = data.get('linguagem', '')
        self.tipo = data.get('tipo', '')
        self.peso = data.get('peso', 0.0)
        self.n_questoes = data.get('n_questoes', 0)
        self.blocos_ex = data.get('blocos_ex', [])

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
        data = dict()
        arquivo = None
        try:
            print('\t\tObtendo dados da atividade do arquivo: ', path)
            data['codigo'] = int(path.split('/')[-1][:-5])  # código da atividade

            arquivo = open(path, 'r')
            lines = arquivo.readlines()
            blocos = []

            for line in lines:
                line = line.lower().strip()
                if line.startswith('---- as'):
                    data['titulo'] = line.split(':')[-1].strip()
                elif line.startswith('---- class nu'):
                    data['codigo_turma'] = int(line.split(':')[-1].strip())
                elif line.startswith('---- st'):
                    data['data_inicio'] = line.split(':')[-1].strip()
                elif line.startswith('---- en'):
                    data['data_termino'] = line.split(':')[-1].strip()
                elif line.startswith('---- la'):
                    data['linguagem'] = line.split(':')[-1].strip()
                elif line.startswith('---- la'):
                    data['linguagem'] = line.split(':')[-1].strip()
                elif line.startswith('---- ty'):
                    data['tipo'] = line.split(':')[-1].strip()
                elif line.startswith('---- ty'):
                    data['tipo'] = line.split(':')[-1].strip()
                elif line.startswith('---- we'):
                    data['peso'] = float(line.split(':')[-1].strip())
                elif line.startswith('---- to'):
                    data['n_questoes'] = int(line.split(':')[-1].strip())
                elif line.startswith('---- ex'):
                    bloco = line.split(':')[-1].strip()
                    if len(bloco) > 0:  # verifica se exite alguma questão, pois no dataset alguns dados estão faltando
                        # testa se realmente corresponde a um bloco de exercícios, blocos são separados por 'or'
                        if ' or ' in bloco:
                            # separa os códigos dos exercícios do bloco
                            bloco = bloco.split(' or ')
                            bloco = [int(x) for x in bloco]  # converte os códigos dos exercícios em inteiro
                            bloco.sort()
                        else:
                            bloco = int(bloco)

                        blocos.append(bloco)

            data['blocos_ex'] = blocos

        except Exception as e:
            print(f'Erro ao acessar o arquivo da atividade: {path}')
            print(f'Mensagem: {str(e)}')
            Util.count_error()
            Util.wait_user_input()
        finally:
            # finally é sempre executado, então fechamos o arquivo se ele existir
            if arquivo is not None:
                arquivo.close()

        return data

    def print_info(self):
        """
           Imprime as informações da ativida no console
        """
        print('\t\t- Atividade [{}]: {}'.format(self.codigo, self.titulo))
        print('\t\t- De {} até {}'.format(self.data_inicio, self.data_termino))
        print('\t\t- Linguagem: {}'.format(self.linguagem))
        print('\t\t- Tipo: {}'.format(self.tipo))
        print('\t\t- Peso: {:.2f}'.format(self.peso))
        print('\t\t- Nº Questões: {}'.format(self.n_questoes))
        print('\t\t- Questões: {}\n'.format(self.blocos_ex))
