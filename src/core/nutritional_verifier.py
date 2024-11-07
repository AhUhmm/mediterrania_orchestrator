from dataclasses import dataclass
from typing import Dict, List, Optional
import math
from ..database.database_handler import DatabaseRicette

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
        Verifica il bilanciamento nutrizionale del piano
        Restituisce un dizionario con i risultati della verifica
        """
        requisiti = self.calcola_requisiti(dati_utente)
        totali_giornalieri = self._calcola_totali_giornalieri(piano)
        
        risultati = {
            "bilanciato": True,
            "problemi": [],
            "valori_attuali": totali_giornalieri,
            "requisiti": requisiti
        }

        # Verifica calorie
        if not (requisiti.calorie_min <= totali_giornalieri["calorie"] <= requisiti.calorie_max):
            risultati["bilanciato"] = False
            risultati["problemi"].append(
                f"Calorie fuori range: {totali_giornalieri['calorie']:.1f} kcal " +
                f"(range: {requisiti.calorie_min:.1f}-{requisiti.calorie_max:.1f})"
            )

        # Verifica proteine
        if not (requisiti.proteine_min <= totali_giornalieri["proteine"] <= requisiti.proteine_max):
            risultati["bilanciato"] = False
            risultati["problemi"].append(
                f"Proteine fuori range: {totali_giornalieri['proteine']:.1f}g " +
                f"(range: {requisiti.proteine_min:.1f}-{requisiti.proteine_max:.1f})"
            )

        # Verifica carboidrati
        if not (requisiti.carboidrati_min <= totali_giornalieri["carboidrati"] <= requisiti.carboidrati_max):
            risultati["bilanciato"] = False
            risultati["problemi"].append(
                f"Carboidrati fuori range: {totali_giornalieri['carboidrati']:.1f}g " +
                f"(range: {requisiti.carboidrati_min:.1f}-{requisiti.carboidrati_max:.1f})"
            )

        # Verifica grassi
        if not (requisiti.grassi_min <= totali_giornalieri["grassi"] <= requisiti.grassi_max):
            risultati["bilanciato"] = False
            risultati["problemi"].append(
                f"Grassi fuori range: {totali_giornalieri['grassi']:.1f}g " +
                f"(range: {requisiti.grassi_min:.1f}-{requisiti.grassi_max:.1f})"
            )

        # Verifica fibre
        if totali_giornalieri["fibre"] < requisiti.fibre_min:
            risultati["bilanciato"] = False
            risultati["problemi"].append(
                f"Fibre insufficienti: {totali_giornalieri['fibre']:.1f}g " +
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

        for tipo_pasto, ricette in piano.items():
            for id_ricetta in ricette:
                ricetta = self.db.get_ricetta_by_id(id_ricetta)
                if ricetta:
                    valori = ricetta["valori_nutrizionali"]
                    totali["calorie"] += valori["calorie"]
                    totali["proteine"] += valori["proteine"]
                    totali["carboidrati"] += valori["carboidrati"]
                    totali["grassi"] += valori["grassi"]
                    totali["fibre"] += valori["fibre"]

        return totali