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

        RUTA_LOG_FILE = os.path.join("logs", "banco.log")
        
        file_handler = logging.FileHandler(RUTA_LOG_FILE, encoding="utf-8")

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)

        self.logging.addHandler(file_handler)
        self.logging.addHandler(console_handler)

        return self.logging