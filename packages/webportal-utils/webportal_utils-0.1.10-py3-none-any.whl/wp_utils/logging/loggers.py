import logging
from copy import deepcopy
from logging import LogRecord

from wp_utils.settings import utils_settings


class CropLogger(logging.Logger):
    def makeRecord(
        self,
        name: str,
        level: int,
        fn: str,
        lno: int,
        msg: object,
        args,
        exc_info,
        func=None,
        extra=None,
        sinfo=None,
    ) -> LogRecord:
        if utils_settings.CROP_LOG:
            args = self._crop_args(list(args))
            extra = self.__crop_item(extra) if extra else None
        return super().makeRecord(name, level, fn, lno, msg, args, exc_info, func, extra, sinfo)

    def _crop_args(self, args: list) -> tuple:
        for index, arg in enumerate(args):
            args[index] = self.__crop_item(arg)
        return tuple(args)

    def __crop_item(self, value):
        if isinstance(value, dict):
            value = self.__crop_dict(value)
        elif isinstance(value, str):
            value = value[: utils_settings.MAX_LOG_ARG_LENGTH]
        elif not isinstance(value, (int, float)):
            value = str(value)[: utils_settings.MAX_LOG_ARG_LENGTH]
        return value

    def __crop_dict(self, message) -> dict:
        updated_message = deepcopy(message)
        for key, value in message.items():
            updated_message[key] = self.__crop_item(value)
        return updated_message
