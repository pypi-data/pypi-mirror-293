import traceback
import logging
from .interface import Comm, LogLevel


class LogComm(Comm):
    def __init__(self, logger: logging.Logger, print_traceback: bool = False):
        self.logger = logger
        self.print_traceback = print_traceback

    def send(level: LogLevel, msg: str = "", **kwargs):
        self.logger.log(level.to_logging_level(), msg, exc_info = self.print_traceback)
