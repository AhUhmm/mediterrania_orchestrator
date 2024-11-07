import json
import os
from pathlib import Path
from typing import Dict, List, Optional
from mediterrania_orchestrator.database.database_handler import DatabaseRicette
from mediterrania_orchestrator.utils.logger import LoggerMediterranIA
from mediterrania_orchestrator.core.nutritional_verifier import VerificatoreNutrizionale
from mediterrania_orchestrator.core.substitution_handler import GestoreSostituzioni

class OrchestratoreAlimentare:
    def __init__(self):
        self.logger = LoggerMediterranIA()
        self.db_ricette = DatabaseRicette()
        self.verificatore = VerificatoreNutrizionale(self.db_ricette)
        self.gestore_sostituzioni = GestoreSostituzioni(self.db_ricette)

    def crea_piano_personalizzato(self, dati_utente: Dict) -> Dict:
        """
        Crea un piano alimentare completamente personalizzato
        
        Args:
            dati_utente: dati dal questionario utente
        """
        try:
            # 1. Seleziona piano base
            tipo_piano = self.determina_tipo_piano(
                dati_utente["tipo_dieta"],
                dati_utente["obiettivo"]
            )
            piano_base = self.piani_base[tipo_piano]
            
            self.logger.log_piano_creazione(dati_utente, tipo_piano)
            
            # 2. Applica filtro allergie
            if dati_utente.get("allergie"):
                piano_base = self.filtra_per_allergie(
                    piano_base,
                    dati_utente["allergie"]
                )
                
            # 3. Sostituisci verdure escluse
            if dati_utente.get("verdure_escluse"):
                piano_base, sostituzioni_verdure = self.gestore_sostituzioni.sostituisci_verdure(
                    piano_base,
                    set(dati_utente["verdure_escluse"])
                )
                for sostituzione in sostituzioni_verdure:
                    self.logger.log_sostituzione(
                        sostituzione.ricetta_originale,
                        sostituzione.ricetta_sostitutiva,
                        sostituzione.motivo
                    )
                
            # 4. Gestisci preferenze latte
            if dati_utente.get("preferenza_latte"):
                piano_base, sostituzioni_latte = self.gestore_sostituzioni.sostituisci_latte(
                    piano_base,
                    dati_utente["preferenza_latte"]
                )
                for sostituzione in sostituzioni_latte:
                    self.logger.log_sostituzione(
                        sostituzione.ricetta_originale,
                        sostituzione.ricetta_sostitutiva,
                        sostituzione.motivo
                    )
                
            # 5. Verifica bilanciamento nutrizionale
            risultati_verifica = self.verificatore.verifica_bilanciamento(
                piano_base, 
                dati_utente
            )
            self.logger.log_verifica_nutrizionale(risultati_verifica)
            
            if not risultati_verifica["bilanciato"]:
                raise ValueError(
                    "Piano non bilanciato nutrizionalmente: " + 
                    "; ".join(risultati_verifica["problemi"])
                )
                
            return piano_base
            
        except Exception as e:
            self.logger.log_errore(e, "creazione_piano_personalizzato")
            raise

    def determina_tipo_piano(self, tipo_dieta: str, obiettivo: str) -> str:
        """Determina il codice del piano base da usare"""
        mapping = {
            ("vegano", "Perdere peso"): "VE-WL",
            ("vegano", "Mantenere peso"): "VE-M",
            ("vegano", "Aumentare massa muscolare"): "VE-MG",
            ("vegetariano", "Perdere peso"): "V-WL",
            ("vegetariano", "Mantenere peso"): "V-M",
            ("vegetariano", "Aumentare massa muscolare"): "V-MG",
            ("nessuno", "Perdere peso"): "S-WL",
            ("nessuno", "Mantenere peso"): "S-M",
            ("nessuno", "Aumentare massa muscolare"): "S-MG"
        }
        return mapping[(tipo_dieta, obiettivo)]

    def filtra_per_allergie(self, piano: Dict, allergie: List[str]) -> Dict:
        """
        Filtra il piano rimuovendo ricette con allergeni
        """
        piano_filtrato = {}
        for tipo_pasto, ricette_ids in piano.items():
            ricette_filtrate = []
            for ricetta_id in ricette_ids:
                ricetta = self.db_ricette.get_ricetta_by_id(ricetta_id)
                if not any(allergene in ricetta["ingredienti"] for allergene in allergie):
                    ricette_filtrate.append(ricetta_id)
            piano_filtrato[tipo_pasto] = ricette_filtrate
        return piano_filtrato

    @property
    def piani_base(self) -> Dict:
        """
        Carica i piani base dal file JSON
        """
        if not hasattr(self, '_piani_base'):
            # Get the absolute path to the package directory
            package_dir = Path(__file__).parent.parent.parent
            path = package_dir / "data" / "base_plans.json"
            
            try:
                with open(path, "r", encoding="utf-8") as f:
                    self._piani_base = json.load(f)
            except FileNotFoundError:
                self.logger.log_errore(f"File base_plans.json non trovato in: {path}", "caricamento_piani_base")
                raise
                
        return self._piani_base
