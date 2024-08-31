import time

from pythonjsonlogger.jsonlogger import JsonFormatter


class UTCJsonFormatter(JsonFormatter):
    converter = time.gmtime
