class Estudante:

    def __init__(self,
                 codigo,
                 path,
                 curso_id,
                 curso_nome,
                 instituicao_id,
                 instituicao_nome,
                 escola_nome,
                 escola_tipo,
                 escola_turno,
                 escola_ano_grad,
                 sexo,
                 ano_nascimento,
                 estado_civil,
                 tem_filhos):
        self.id = codigo
        self.path = path
        self.curso_id = curso_id
        self.curso_nome = curso_nome
        self.instituicao_id = instituicao_id
        self.instituicao_nome = instituicao_nome
        self.escola_nome = escola_nome
        self.escola_tipo = escola_tipo
        self.escola_turno = escola_turno
        self.escola_ano_grad = escola_ano_grad
        self.sexo = sexo
        self.ano_nascimento = ano_nascimento
        self.estado_civil = estado_civil
        self.tem_filhos = tem_filhos

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


