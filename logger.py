import logging
import os
import sys


class Logger:

    def __init__(self):
        self.logging = logging.getLogger("BankSystem")

    def configurar_logging(self):

        if self.logging.hasHandlers():
            self.logging.handlers.clear()

        self.logging.setLevel(logging.INFO)

        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s"
        )

        os.makedirs("logs", exist_ok=True)
        ruta_log_file = os.path.join("logs", "banco.log")

        file_handler = logging.FileHandler(ruta_log_file, encoding="utf-8")
        file_handler.setFormatter(formatter)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        self.logging.addHandler(file_handler)
        self.logging.addHandler(console_handler)

        return self.logging