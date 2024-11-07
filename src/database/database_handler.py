import json
from typing import Dict, List, Optional

class DatabaseRicette:
    def __init__(self, path_ricette: str = "ricette.json"):
        """
        Inizializza il database delle ricette
        
        Args:
            path_ricette: percorso del file JSON delle ricette
        """
        self.ricette = self._carica_ricette(path_ricette)
        self.ricette_per_id = self._indicizza_ricette()
        
    def _carica_ricette(self, path: str) -> Dict:
        """Carica il database delle ricette dal file JSON"""
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
            
    def _indicizza_ricette(self) -> Dict:
        """Crea un dizionario di ricette indicizzato per ID"""
        ricette_indicizzate = {}
        
        # Indicizza colazioni
        for ricetta in self.ricette["colazioni"]:
            ricette_indicizzate[ricetta["id_pasto"]] = ricetta
            
        # Indicizza pranzi
        for ricetta in self.ricette["pranzi"]:
            ricette_indicizzate[ricetta["id_pasto"]] = ricetta
            
        # Indicizza cene
        for ricetta in self.ricette["cene"]:
            ricette_indicizzate[ricetta["id_pasto"]] = ricetta
            
        # Indicizza spuntini
        for ricetta in self.ricette["spuntini"]:
            ricette_indicizzate[ricetta["id_pasto"]] = ricetta
            
        return ricette_indicizzate
        
    def get_ricetta_by_id(self, ricetta_id: str) -> Optional[Dict]:
        """Recupera una ricetta dal suo ID"""
        return self.ricette_per_id.get(ricetta_id)
        
    def get_ricette_stagione(self, stagione: str) -> List[Dict]:
        """Recupera tutte le ricette disponibili per una stagione"""
        ricette_stagionali = []
        for ricetta in self.ricette_per_id.values():
            if "stagione" in ricetta["proprieta"]:
                if stagione in ricetta["proprieta"]["stagione"] or "tutte" in ricetta["proprieta"]["stagione"]:
                    ricette_stagionali.append(ricetta)
        return ricette_stagionali