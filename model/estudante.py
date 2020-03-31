from util.Util import Util


class Estudante:

    def __init__(self, file_path):
        self.id = Estudante.get_id(file_path)

        data = Estudante.get_file_data(f'{file_path}/user.data')

        self.curso_id = data.get('curso_id', 0)
        self.curso_nome = data.get('curso_nome', '')
        self.instituicao_id = data.get('instituicao_id', 0)
        self.instituicao_nome = data.get('instituicao_nome', '')
        self.escola_nome = data.get('escola_nome', '')
        self.escola_tipo = data.get('escola_tipo', '')
        self.escola_turno = data.get('escola_turno', '')
        self.escola_ano_grad = data.get('escola_ano_grad', 0)
        self.sexo = data.get('sexo', '')
        self.ano_nascimento = data.get('ano_nascimento', 0)
        self.estado_civil = data.get('estado_civil', '')
        self.tem_filhos = data.get('tem_filhos', False)

        data.clear()
        del data

    @staticmethod
    def get_file_data(path):
        # TODO: doc
        arquivo = None
        data = dict()

        try:
            print('\t\tObtendo estudante do arquivo: ', path)
            arquivo = open(path, 'r')
            lines = arquivo.readlines()

            # if len(lines) < 31:
            #    print(f'Arquivo incompleto: {path}')
            #    Util.wait_user_input()

            for index, line in enumerate(lines, start=1):
                line = line.lower().strip()
                if index == 2 and line.startswith('---- course id:'):
                    data['curso_id'] = int(Estudante.get_value(line))
                elif index == 3 and line.startswith('---- course name:'):
                    data['curso_nome'] = Estudante.get_value(line)
                elif index == 4 and line.startswith('---- institution id:'):
                    data['instituicao_id'] = int(Estudante.get_value(line))
                elif index == 5 and line.startswith('---- institution name:'):
                    data['instituicao_nome'] = Estudante.get_value(line)
                elif index == 7 and line.startswith('---- high school name:'):
                    data['escola_nome'] = Estudante.get_value(line)
                elif index == 8 and line.startswith('---- school type:'):
                    data['escola_tipo'] = Estudante.get_value(line)
                elif index == 9 and line.startswith('---- shift:'):
                    data['escola_turno'] = Estudante.get_value(line)
                elif index == 10 and line.startswith('---- graduation year:'):
                    data['escola_ano_grad'] = int(Estudante.get_value(line))
                elif index == 28 and line.startswith('---- sex:'):
                    data['sexo'] = Estudante.get_value(line)
                elif index == 29 and line.startswith('---- year of birth:'):
                    data['ano_nascimento'] = int(Estudante.get_value(line))
                elif index == 30 and line.startswith('---- civil status:'):
                    data['estado_civil'] = Estudante.get_value(line)
                elif index == 31 and line.startswith('---- have kids:'):
                    data['tem_filhos'] = True if Estudante.get_value(line) == 'yes' else False

        except Exception as e:
            print(f'Erro ao acessar o arquivo de estudante: {path}')
            print(f'Mensagem: {str(e)}')
            Util.count_error()
            Util.wait_user_input()
        finally:
            # finally é sempre executado, então fechamos o arquivo se ele existir
            if arquivo is not None:
                arquivo.close()

        return data

    @staticmethod
    def get_id(text):
        # TODO: doc
        value = 0
        try:
            value = int(text.split('/')[-1])
        except Exception as e:
            print(f'Erro ao tentar obter id do estudante: {text}')
            print(f'Mensagem: {str(e)}')
            Util.count_error()
            Util.wait_user_input()

        return value

    @staticmethod
    def get_value(text):
        # TODO: doc
        value = ''
        try:
            value = str(text).split(':')[-1].strip()
        except Exception as e:
            print(f'Erro ao tentar obter valor da linha: {text}')
            print(f'Mensagem: {str(e)}')
            Util.count_error()
            Util.wait_user_input()

        return value

    def print_info(self):
        # TODO: doc
        print(f'\t\t- Aluno [{self.id}]')
        print(f'\t\t- Curso [{self.curso_id}]: {self.curso_nome}')
        print(f'\t\t- Instituição [{self.instituicao_id}]: {self.instituicao_nome}')
        print(f'\t\t- Escola: {self.escola_nome}, {self.escola_tipo}, {self.escola_turno}, {self.escola_ano_grad}')
        print(f'\t\t- Nascimento: {self.ano_nascimento}')
        print(f'\t\t- Sexo: {self.sexo}')
        print(f'\t\t- Estado civil: {self.estado_civil}')
        print(f'\t\t- Tem Filhos: {self.tem_filhos}\n')


