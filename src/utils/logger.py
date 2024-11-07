import logging
import logging.handlers
from datetime import datetime
import os

class LoggerMediterranIA:
    def __init__(self):
        # Crea directory per i log se non esiste
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Configura il logger principale
        self.logger = logging.getLogger('MediterranIA')
        self.logger.setLevel(logging.DEBUG)

        # Handler per file
        file_handler = logging.handlers.RotatingFileHandler(
            filename=f"{log_dir}/mediterrania.log",
            maxBytes=5*1024*1024,  # 5MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)

        # Handler per console
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # Formattazione
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Aggiungi handlers
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def log_piano_creazione(self, dati_utente: Dict, piano_id: str):
        """Log della creazione di un nuovo piano"""
        self.logger.info(
            f"Nuovo piano creato - ID: {piano_id} - "
            f"Utente: {dati_utente['sesso']}, {dati_utente['età']} anni, "
            f"Obiettivo: {dati_utente['obiettivo']}"
        )

    def log_sostituzione(self, ricetta_originale: str, ricetta_nuova: str, motivo: str):
        """Log di una sostituzione di ricetta"""
        self.logger.debug(
            f"Sostituzione ricetta - "
            f"Originale: {ricetta_originale} -> Nuova: {ricetta_nuova} - "
            f"Motivo: {motivo}"
        )

    def log_errore(self, errore: Exception, contesto: str):
        """Log di un errore"""
        self.logger.error(
            f"Errore in {contesto}: {str(errore)}",
            exc_info=True
        )

    def log_verifica_nutrizionale(self, risultati: Dict):
        """Log dei risultati della verifica nutrizionale"""
        if risultati["bilanciato"]:
            self.logger.info("Verifica nutrizionale: Piano bilanciato")
        else:
            self.logger.warning(
                "Verifica nutrizionale: Piano non bilanciato\n" +
                "\n".join(risultati["problemi"])
            )