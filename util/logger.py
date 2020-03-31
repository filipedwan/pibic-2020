import logging
import os


class Logger:
    __path = os.getcwd() + '/logs/'
    __debug = None
    __info = None
    __warn = None
    __error = None

    @staticmethod
    def configure():
        logging.basicConfig(level=logging.ERROR)

        try:
            if not os.path.isdir('logs'):
                os.mkdir('logs')
        except Exception as e:
            print(str(e))

        Logger.configure_debugger()
        Logger.configure_info()
        Logger.configure_warn()
        Logger.configure_error()

        Logger.info('Logging configurado')

    @staticmethod
    def debug(msg):
        Logger.__debug.debug(msg)

    @staticmethod
    def info(msg):
        Logger.__info.info(msg)

    @staticmethod
    def warn(msg):
        Logger.__warn.warning(msg)

    @staticmethod
    def error(msg):
        Logger.__error.error(msg, exc_info=True)

    @staticmethod
    def configure_debugger():
        if not Logger.__debug:
            Logger.__debug = logging.getLogger('debug')
            formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')

            file_handler = logging.FileHandler(f'{Logger.__path}/debug.log')
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)

            Logger.__debug.addHandler(file_handler)
            Logger.__debug.addHandler(console_handler)

    @staticmethod
    def configure_info():
        if not Logger.__info:
            Logger.__info = logging.getLogger('info')
            formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)

            Logger.__info.addHandler(console_handler)

    @staticmethod
    def configure_warn():
        if not Logger.__warn:
            Logger.__warn = logging.getLogger('warn')
            formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')

            file_handler = logging.FileHandler(f'{Logger.__path}/warn.log')
            file_handler.setLevel(logging.WARNING)
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.WARNING)
            console_handler.setFormatter(formatter)

            Logger.__warn.addHandler(file_handler)
            Logger.__warn.addHandler(console_handler)

    @staticmethod
    def configure_error():
        if not Logger.__error:
            Logger.__error = logging.getLogger('error')

            formatter = logging.Formatter('%(asctime)s %(name)s [%(levelname)s]: %(message)s')

            file_handler = logging.FileHandler(f'{Logger.__path}/error.log')
            file_handler.setLevel(logging.ERROR)
            file_handler.setFormatter(formatter)

            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.ERROR)
            console_handler.setFormatter(formatter)

            Logger.__error.addHandler(file_handler)
            Logger.__error.addHandler(console_handler)


Logger.configure()
