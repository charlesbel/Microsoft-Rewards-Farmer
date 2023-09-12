import logging


class ColoredFormatter(logging.Formatter):
    verbose_notifs = False
    notifier = str()

    grey = "\x1b[38;21m"
    blue = "\x1b[38;5;39m"
    yellow = "\x1b[38;5;226m"
    red = "\x1b[38;5;196m"
    boldRed = "\x1b[31;1m"
    reset = "\x1b[0m"

    def __init__(self, fmt):
        super().__init__()
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.yellow + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.boldRed + self.fmt + self.reset,
        }

    def format(self, record):
        logFmt = self.FORMATS.get(record.levelno)

        if self.verbose_notifs and self.notifier is not None:
            log_msg = f"[{self.formatTime(record, self.datefmt)}] [{logging.getLevelName(record.levelno)}] {record.msg}"
            self.notifier.send(log_msg)

        formatter = logging.Formatter(logFmt)
        return formatter.format(record)
