import os

cwd = os.getcwd()
solutions_path = f'{cwd}/solutions/solucoes.csv'
output_path = f'{cwd}/solutions'

try:
    os.mkdir(output_path)
except OSError:
    pass

output = None
with open(solutions_path, 'r') as f:
    for line in f:
        if line.strip().endswith(' == SOLUCAO DO PROFESSOR ==>'):
            codigo = line.split(' == ')[0]
            if output:
                output.close()
            output = open(f'{output_path}/{codigo}.code', 'w')
        else:
            output.write(line)

    if output:
        output.close()
