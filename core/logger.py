# -*- coding: utf-8 -*-
"""
Log
"""
from datetime import datetime


def log(termo, file="log_init.txt"):
    """Log."""
    print("Log init ok")
    now = datetime.utcnow()
    current_time = now.strftime("%H:%M:%S - %d/%m/%Y")
    msg = "Termo: " + str(termo) + "-Inicio: " + current_time + " - UTC "+"\n"
    with (open(file, "a+")) as arquivo:
        arquivo.write(msg)


def log_erro(termo, file="log_error.txt"):
    """Log error."""
    now = datetime.utcnow()
    current_time = now.strftime("%H:%M:%S - %d/%m/%Y")
    with (open(file, "a+")) as arquivo:
        arquivo.write(f"termo: {termo} Erro ocorrido em: {current_time} \n")
