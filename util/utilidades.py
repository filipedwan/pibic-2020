import os
from collections import Counter


class Util:
    __error_names = []
    __error_count = []

    # função que pausa o console aguardando o usuário teclar [ENTER]
    @staticmethod
    def wait_user_input():
        input('{:^15s}'.format('Tecle [ENTER]...'))

    # função que limpa a tela do console
    @staticmethod
    def clear_console():
        os.system('clear')

    @staticmethod
    def register_errors(error_list):
        error_names = Counter(error_list).keys()
        error_count = Counter(error_list).values()

        for name, count in zip(error_names, error_count):
            if name in Util.__error_names:
                Util.__error_count[Util.__error_names.index(name)] += count
            else:
                Util.__error_names.append(name)
                Util.__error_count.append(count)

    @staticmethod
    def get_unique_errors():
        return zip(Util.__error_names, Util.__error_count)
