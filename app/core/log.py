import logging
from datetime import datetime
from logging.handlers import SMTPHandler
from threading import Thread

from flask import has_request_context, request

from config import Config


def get_full_class_name(obj):
    module = obj.__class__.__module__
    if module is None or module == str.__class__.__module__:
        return obj.__class__.__name__
    return module + "." + obj.__class__.__name__


def message_struct(
    module, method, error, calling_method=None, calling_module=None, exc_class=None
):
    return {
        "exception_class": exc_class,
        "module": module,
        "method": method,
        "calling module": calling_module,
        "calling method": calling_method,
        "error": error,
    }


class MailHandler(SMTPHandler):
    def emit(self, record):
        """
        Emit a record.
        Format the record and send it to the specified addressees.
        """
        Thread(target=self.send_mail, kwargs={"record": record}).start()

    def send_mail(self, record):
        self.timeout = 30
        super().emit(record)


class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None
        return super().format(record)


def log_config():
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "loggers": {
            "root": {
                "level": "ERROR",
                "handlers": [
                    "console_handler",
                    "error_file_handler",
                    "critical_mail_handler",
                ],
            },
            "gunicorn.error": {
                "handlers": [
                    "console_handler",
                    "error_file_handler",
                    "error_mail_handler",
                ],
                "level": "ERROR",
                "propagate": False,
            },
            "gunicorn.access": {
                "handlers": ["access_file_handler"],
                "level": "INFO",
                "propagate": False,
            },
        },
        "handlers": {
            "console_handler": {
                "level": "ERROR",
                "class": "logging.StreamHandler",
                "formatter": "error_formatter",
                "stream": "ext://sys.stdout",
            },
            "error_mail_handler": {
                "()": "app.core.log.MailHandler",
                "formatter": "error_formatter",
                "level": "ERROR",
                "mailhost": (Config.MAIL_SERVER, Config.MAIL_SERVER_PORT),
                "fromaddr": Config.DEFAULT_MAIL_SENDER_ADDRESS,
                "toaddrs": Config.ADMIN_MAIL_ADDRESSES,
                "subject": f"{Config.LOG_HEADER} {datetime.utcnow().date()}",
                "credentials": (
                    Config.DEFAULT_MAIL_SENDER_ADDRESS,
                    Config.DEFAULT_MAIL_SENDER_PASSWORD,
                ),
                "secure": (),
            },
            "error_file_handler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "error_formatter",
                "level": "ERROR",
                "filename": "gunicorn.error.log",
                "when": "D",
                "interval": 30,
                "backupCount": 2,
            },
            "access_file_handler": {
                "class": "logging.handlers.TimedRotatingFileHandler",
                "formatter": "access_formatter",
                "filename": "gunicorn.access.log",
                "when": "D",
                "interval": 30,
                "backupCount": 2,
            },
            "critical_mail_handler": {
                "()": "app.core.log.MailHandler",
                "formatter": "error_formatter",
                "level": "CRITICAL",
                "mailhost": (Config.MAIL_SERVER, Config.MAIL_SERVER_PORT),
                "fromaddr": Config.DEFAULT_MAIL_SENDER_ADDRESS,
                "toaddrs": Config.ADMIN_MAIL_ADDRESSES,
                "subject": f"{Config.LOG_HEADER} {datetime.utcnow().date()}",
                "credentials": (
                    Config.DEFAULT_MAIL_SENDER_ADDRESS,
                    Config.DEFAULT_MAIL_SENDER_PASSWORD,
                ),
                "secure": (),
            },
        },
        "formatters": {
            "access_formatter": {
                "format": "%(message)s",
            },
            "error_formatter": {
                "()": "app.core.log.RequestFormatter",
                "format": """
                \n--- Logging %(levelname)s at %(asctime)s --- \n%(message)s
                """,
                "datefmt": "%Y-%m-%d %H:%M:%S",
            },
        },
    }
