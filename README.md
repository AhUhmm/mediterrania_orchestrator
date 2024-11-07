# MediterranIA Orchestrator

Un orchestratore per la creazione di piani alimentari personalizzati basati sulla dieta mediterranea. Il sistema analizza le preferenze dell'utente, requisiti nutrizionali e restrizioni alimentari per generare piani alimentari personalizzati.

## 🚀 Funzionalità

- Generazione di piani alimentari personalizzati
- Gestione di allergie e intolleranze
- Sostituzione intelligente degli ingredienti
- Verifica del bilanciamento nutrizionale
- Supporto per diete speciali (vegana, vegetariana)
- Adattamento stagionale delle ricette

## 💻 Utilizzo

```python
from mediterrania_orchestrator.core.orchestrator import OrchestratoreAlimentare

# Inizializza l'orchestratore
orchestratore = OrchestratoreAlimentare()

# Configura i dati utente
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

# Genera piano personalizzato
piano = orchestratore.crea_piano_personalizzato(dati_utente)
```

## 🌳 Struttura del Progetto

```
mediterrania_orchestrator/
├── src/                               # Codice sorgente
│   ├── __init__.py
│   ├── database/                      # Gestione database ricette
│   │   ├── __init__.py
│   │   └── database_handler.py
│   ├── core/                          # Logica principale
│   │   ├── __init__.py
│   │   ├── orchestrator.py
│   │   ├── nutritional_verifier.py
│   │   └── substitution_handler.py
│   ├── utils/                         # Utilità e helper
│   │   ├── __init__.py
│   │   └── logger.py
│   └── data/                          # Dati e configurazioni
│       ├── base_plans.json
│       └── ricette.json
├── tests/                             # Test unitari e di integrazione
│   ├── __init__.py
│   ├── test_nutritional_verifier.py
│   ├── test_orchestrator.py
│   └── test_substitution_handler.py
├── logs/                              # File di log
│   └── .gitkeep
├── docs/                              # Documentazione
│   ├── README.md
│   └── API.md
├── tools/                             # Script di utilità
├── requirements.txt
├── setup.py
└── README.md
```

## 🔩 File principali e loro contenuto

1. `src/database/database_handler.py` - Gestione dell'accesso al database delle ricette
2. `src/core/orchestrator.py` - Orchestratore principale del sistema
3. `src/core/nutritional_verifier.py` - Verifica del bilanciamento nutrizionale
4. `src/core/substitution_handler.py` - Gestione delle sostituzioni di ingredienti
5. `src/utils/logger.py` - Sistema di logging
6. `src/data/base_plans.json` - Piani alimentari base
7. `tests/*` - Suite di test unitari e di integrazione

## 📋 Prerequisiti

- Python 3.7 o superiore
- pip (gestore pacchetti Python)
- Git

## 🦴 Requirements

```
numpy>=1.21.0
pandas>=1.3.0
pytest>=6.2.5
logging>=0.5.1.2
typing>=3.7.4.3
```

## 🔧 Installazione

```bash
git clone https://github.com/yourusername/mediterrania_orchestrator.git
cd mediterrania_orchestrator
pip install -r requirements.txt
```

## 🛠 Sviluppo

### Setup Ambiente di Sviluppo

1. Clona il repository
2. Crea un ambiente virtuale
3. Installa le dipendenze di sviluppo
4. Esegui lo script di inizializzazione:

```bash
python tools/init_project.py
```

## 📝 Roadmap

1. **Ottimizzazioni delle prestazioni**

   - Implementare caching per i dati frequentemente acceduti
   - Ottimizzare gli algoritmi di sostituzione
   - Aggiungere indici per ricerche veloci nel database delle ricette

2. **Documentazione API completa**

   - Documentare tutte le funzioni pubbliche
   - Aggiungere esempi di utilizzo
   - Creare diagrammi di flusso per i processi principali

3. **Test di integrazione**

   - Creare scenari di test end-to-end
   - Testare diversi profili utente
   - Validare il bilanciamento nutrizionale

4. **Caching**
   - Implementare Redis per il caching dei piani base
   - Caching delle ricette più utilizzate
   - Sistema di invalidazione cache
