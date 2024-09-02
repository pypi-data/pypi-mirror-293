import logging

# Crea un logger specifico per Alfred
logger = logging.getLogger("alfred")

# Imposta il livello di logging desiderato
logger.setLevel(logging.INFO)

# Crea un handler per la console
console_handler = logging.StreamHandler()

# Crea un formatter personalizzato
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# Assegna il formatter all'handler
console_handler.setFormatter(formatter)

# Aggiungi l'handler al logger
logger.addHandler(console_handler)


# Funzione per ottenere il logger
def get_logger():
    return logger
