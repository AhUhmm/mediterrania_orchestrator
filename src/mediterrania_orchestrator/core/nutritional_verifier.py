from dataclasses import dataclass
from typing import Dict, List, Optional
import math
from mediterrania_orchestrator.database.database_handler import DatabaseRicette

@dataclass
class RequisitiNutrizionali:
    calorie_min: float
    calorie_max: float
    proteine_min: float
    proteine_max: float
    carboidrati_min: float
    carboidrati_max: float
    grassi_min: float
    grassi_max: float
    fibre_min: float

class VerificatoreNutrizionale:
    def __init__(self, db_ricette: DatabaseRicette):
        self.db = db_ricette

    def calcola_requisiti(self, dati_utente: Dict) -> RequisitiNutrizionali:
        """
        Calcola i requisiti nutrizionali basati sui dati utente
        """
        # Calcolo BMR (Basal Metabolic Rate) usando la formula di Harris-Benedict
        if dati_utente["sesso"] == "M":
            bmr = 88.362 + (13.397 * dati_utente["peso"]) + \
                  (4.799 * dati_utente["altezza"]) - (5.677 * dati_utente["età"])
        else:
            bmr = 447.593 + (9.247 * dati_utente["peso"]) + \
                  (3.098 * dati_utente["altezza"]) - (4.330 * dati_utente["età"])

        # Aggiustamento basato sull'obiettivo
        if dati_utente["obiettivo"] == "Perdere peso":
            calorie_target = bmr * 0.85  # Deficit calorico del 15%
        elif dati_utente["obiettivo"] == "Aumentare massa muscolare":
            calorie_target = bmr * 1.15  # Surplus calorico del 15%
        else:
            calorie_target = bmr

        return RequisitiNutrizionali(
            calorie_min=calorie_target * 0.95,
            calorie_max=calorie_target * 1.05,
            proteine_min=dati_utente["peso"] * 1.6,  # 1.6g/kg peso corporeo
            proteine_max=dati_utente["peso"] * 2.2,  # 2.2g/kg peso corporeo
            carboidrati_min=calorie_target * 0.45 / 4,  # 45-65% delle calorie
            carboidrati_max=calorie_target * 0.65 / 4,
            grassi_min=calorie_target * 0.20 / 9,  # 20-35% delle calorie
            grassi_max=calorie_target * 0.35 / 9,
            fibre_min=25  # Minimo raccomandato giornaliero
        )

    def verifica_bilanciamento(self, piano: Dict, dati_utente: Dict) -> Dict:
        """
        Verifica il bilanciamento nutrizionale del piano con logging dettagliato
        """
        requisiti = self.calcola_requisiti(dati_utente)
        totali_giornalieri = self._calcola_totali_giornalieri(piano)
        
        risultati = {
            "bilanciato": True,
            "problemi": [],
            "valori_attuali": totali_giornalieri,
            "requisiti": requisiti,
            "analisi_dettagliata": {}  # Nuovo campo per l'analisi dettagliata
        }

        # Per ogni nutriente, calcola e logga la deviazione dal target
        for nutriente in ["calorie", "proteine", "carboidrati", "grassi"]:
            valore = totali_giornalieri[nutriente]
            min_val = getattr(requisiti, f"{nutriente}_min")
            max_val = getattr(requisiti, f"{nutriente}_max")
            target = (min_val + max_val) / 2
            
            # Calcola la deviazione percentuale dal target
            deviazione_perc = ((valore - target) / target) * 100
            
            # Prepara l'analisi dettagliata
            analisi = {
                "valore_attuale": valore,
                "target": target,
                "deviazione_percentuale": deviazione_perc,
                "range_min": min_val,
                "range_max": max_val,
                "dentro_range": min_val <= valore <= max_val
            }
            
            risultati["analisi_dettagliata"][nutriente] = analisi
            
            # Logga l'analisi
            self.logger.log_info(
                f"{nutriente.capitalize()}: "
                f"{valore:.1f} ({deviazione_perc:+.1f}% dal target) "
                f"[range: {min_val:.1f}-{max_val:.1f}]"
            )

            # Aggiungi problemi se fuori range
            if not analisi["dentro_range"]:
                risultati["bilanciato"] = False
                risultati["problemi"].append(
                    f"{nutriente.capitalize()} fuori range: "
                    f"{valore:.1f} ({deviazione_perc:+.1f}% dal target) "
                    f"[range: {min_val:.1f}-{max_val:.1f}]"
                )

        # Verifica fibre come prima
        if totali_giornalieri["fibre"] < requisiti.fibre_min:
            risultati["bilanciato"] = False
            risultati["problemi"].append(
                f"Fibre insufficienti: {totali_giornalieri['fibre']:.1f}g "
                f"(minimo: {requisiti.fibre_min:.1f})"
            )

        return risultati

    def _calcola_totali_giornalieri(self, piano: Dict) -> Dict:
        """
        Calcola i totali nutrizionali giornalieri del piano
        """
        totali = {
            "calorie": 0,
            "proteine": 0,
            "carboidrati": 0,
            "grassi": 0,
            "fibre": 0
        }

        # Take the first recipe for each meal type as a sample daily plan
        for tipo_pasto, ricette in piano.items():
            if ricette:  # Check if there are any recipes
                id_ricetta = ricette[0]  # Take just the first recipe
                ricetta = self.db.get_ricetta_by_id(id_ricetta)
                if ricetta:
                    valori = ricetta["valori_nutrizionali"]
                    totali["calorie"] += valori["calorie"]
                    totali["proteine"] += valori["proteine"]
                    totali["carboidrati"] += valori["carboidrati"]
                    totali["grassi"] += valori["grassi"]
                    totali["fibre"] += valori["fibre"]

        return totali