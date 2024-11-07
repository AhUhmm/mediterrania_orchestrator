from typing import Dict, List, Set
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SostituzionePasto:
    ricetta_originale: str
    ricetta_sostitutiva: str
    motivo: str
    valore_nutrizionale_delta: float

class GestoreSostituzioni:
    def __init__(self, db_ricette: DatabaseRicette):
        self.db = db_ricette
        self.stagione_corrente = self._determina_stagione()
        
    def _determina_stagione(self) -> str:
        """Determina la stagione corrente"""
        mese = datetime.now().month
        if mese in [12, 1, 2]:
            return "inverno"
        elif mese in [3, 4, 5]:
            return "primavera"
        elif mese in [6, 7, 8]:
            return "estate"
        else:
            return "autunno"
            
    def sostituisci_verdure(self, piano: Dict, verdure_escluse: Set[str]) -> Dict:
        """
        Sostituisce le ricette che contengono verdure escluse
        
        Args:
            piano: piano alimentare corrente
            verdure_escluse: set di verdure da escludere
        """
        piano_modificato = {}
        sostituzioni = []
        
        for tipo_pasto, ricette in piano.items():
            ricette_sostituite = []
            for id_ricetta in ricette:
                ricetta = self.db.get_ricetta_by_id(id_ricetta)
                
                # Controlla se la ricetta contiene verdure escluse
                if any(verdura in ricetta["ingredienti"] for verdura in verdure_escluse):
                    # Trova una ricetta sostitutiva
                    sostituzione = self._trova_sostituzione_ricetta(
                        ricetta,
                        verdure_escluse,
                        tipo_pasto
                    )
                    if sostituzione:
                        ricette_sostituite.append(sostituzione.ricetta_sostitutiva)
                        sostituzioni.append(sostituzione)
                else:
                    ricette_sostituite.append(id_ricetta)
                    
            piano_modificato[tipo_pasto] = ricette_sostituite
            
        return piano_modificato, sostituzioni
        
    def sostituisci_latte(self, piano: Dict, preferenza_latte: str) -> Dict:
        """
        Sostituisce le ricette che contengono latte con alternative vegetali
        
        Args:
            piano: piano alimentare corrente
            preferenza_latte: tipo di latte vegetale preferito
        """
        piano_modificato = {}
        sostituzioni = []
        
        for tipo_pasto, ricette in piano.items():
            ricette_sostituite = []
            for id_ricetta in ricette:
                ricetta = self.db.get_ricetta_by_id(id_ricetta)
                
                # Controlla se la ricetta contiene latte
                if "latte" in [ing["nome"] for ing in ricetta["ingredienti"]]:
                    # Trova una ricetta sostitutiva
                    sostituzione = self._trova_sostituzione_latte(
                        ricetta,
                        preferenza_latte,
                        tipo_pasto
                    )
                    if sostituzione:
                        ricette_sostituite.append(sostituzione.ricetta_sostitutiva)
                        sostituzioni.append(sostituzione)
                else:
                    ricette_sostituite.append(id_ricetta)
                    
            piano_modificato[tipo_pasto] = ricette_sostituite
            
        return piano_modificato, sostituzioni
        
    def _trova_sostituzione_ricetta(self, ricetta: Dict, verdure_escluse: Set[str], tipo_pasto: str) -> Optional[SostituzionePasto]:
        """Trova una ricetta sostitutiva compatibile"""
        ricette_compatibili = []
        
        for id_ricetta, candidato in self.db.ricette_per_id.items():
            if (candidato["id_pasto"].startswith(tipo_pasto) and
                not any(verdura in candidato["ingredienti"] for verdura in verdure_escluse) and
                self._valori_nutrizionali_simili(ricetta, candidato)):
                ricette_compatibili.append(candidato)
                
        if ricette_compatibili:
            # Sceglie la ricetta più simile nutrizionalmente
            sostituto = min(ricette_compatibili, 
                          key=lambda x: abs(x["valori_nutrizionali"]["calorie"] - 
                                          ricetta["valori_nutrizionali"]["calorie"]))
                                          
            return SostituzionePasto(
                ricetta_originale=ricetta["id_pasto"],
                ricetta_sostitutiva=sostituto["id_pasto"],
                motivo="Sostituzione per verdure escluse",
                valore_nutrizionale_delta=abs(sostituto["valori_nutrizionali"]["calorie"] - 
                                            ricetta["valori_nutrizionali"]["calorie"])
            )
        
        return None
        
    def _valori_nutrizionali_simili(self, ricetta1: Dict, ricetta2: Dict, threshold: float = 0.2) -> bool:
        """Verifica se i valori nutrizionali di due ricette sono simili"""
        v1 = ricetta1["valori_nutrizionali"]
        v2 = ricetta2["valori_nutrizionali"]
        
        return (abs(v1["calorie"] - v2["calorie"]) / v1["calorie"] <= threshold and
                abs(v1["proteine"] - v2["proteine"]) / v1["proteine"] <= threshold and
                abs(v1["carboidrati"] - v2["carboidrati"]) / v1["carboidrati"] <= threshold and
                abs(v1["grassi"] - v2["grassi"]) / v1["grassi"] <= threshold)