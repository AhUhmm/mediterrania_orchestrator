import sys
sys.path.insert(0, "../../src")
print(sys.path)  # Verify that 'src' is in the path

from mediterrania_orchestrator.core.orchestrator import OrchestratoreAlimentare

def main():
    # Inizializza l'orchestratore
    orchestratore = OrchestratoreAlimentare()
    
    # Esempio dati utente
    dati_utente = {
        "sesso": "F",
        "età": 30,
        "peso": 65,
        "altezza": 165,
        "obiettivo": "Perdere peso",
        "tipo_dieta": "vegetariano",
        "allergie": [],
        "verdure_escluse": ["cavolfiori"],
        "preferenza_latte": "soia"
    }
    
    # BMI check
    bmi = dati_utente["peso"] / ((dati_utente["altezza"] / 100) ** 2)
    print(f"DEBUG - BMI calcolato: {bmi:.1f}")

    try:
        # Genera piano personalizzato
        piano = orchestratore.crea_piano_personalizzato(dati_utente)
        
        # Stampa risultato
        print("\nPiano Alimentare Generato:")
        for tipo_pasto, ricette in piano.items():
            print(f"\n{tipo_pasto.capitalize()}:")
            for id_ricetta in ricette:
                ricetta = orchestratore.db_ricette.get_ricetta_by_id(id_ricetta)
                print(f"- {ricetta['nome']}")
                
    except Exception as e:
        print(f"Errore nella generazione del piano: {str(e)}")

if __name__ == "__main__":
    main()