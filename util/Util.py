import os


class Util:
    __errors = 0

    # função que pausa o console aguardando o usuário teclar [ENTER]
    @staticmethod
    def wait_user_input():
        # input('{:^15s}'.format('Tecle [ENTER]...'))
        None

    # função que limpa a tela do console
    @staticmethod
    def clear_console():
        os.system('clear')

    @staticmethod
    def count_error():
        Util.__errors += 1

    @staticmethod
    def get_total_errors():
        return Util.__errors
