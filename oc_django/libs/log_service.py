import datetime
import logging
import os

from django.conf import settings

log_dir = settings.BASE_DIR / 'logs'


class LogService:
    logger = None

    @staticmethod
    def __getLogger():
        if not LogService.logger:
            LogService.logger = logging.getLogger()
        return LogService.logger

    @staticmethod
    def write_to_log(dir_name: str, file_name: str, content: str, new_instance=False, output=False) -> str:
        """
        写入日志
        :param dir_name:
        :param file_name:
        :param content:
        :return:
        """
        logger = LogService.__getLogger()
        logger.setLevel(logging.INFO)
        file = "%s/%s" % (log_dir, dir_name)

        if not os.path.isdir(file):
            os.makedirs(file)

        file += file_name + '_' + datetime.datetime.now().strftime('%Y%m%d') + '.log'
        file_handler = logging.FileHandler(filename=file)
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter("%(asctime)s - %(levelname)s: \n%(message)s")
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)

        logger.info(content)

        logger.removeHandler(file_handler)
        # file_handler.close()

        if output:
            print(content)

        return file