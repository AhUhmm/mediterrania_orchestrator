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
├── docs/                             # Documentation
│   ├── __init__.py
│   ├── alternative-meal-planning.md
│   └── mediterrania-extended-docs.md
├── logs/                            # Logging directory
│   ├── __init__.py
│   └── mediterrania.log
├── src/                             # Source code
│   ├── data/                        # Data files
│   │   ├── __init__.py
│   │   ├── base_plans.json
│   │   └── ricette.json
│   └── mediterrania_orchestrator/    # Main package
│       ├── core/                    # Core functionality
│       │   ├── __init__.py
│       │   ├── nutritional_verifier.py
│       │   ├── orchestrator.py
│       │   └── substitution_handler.py
│       ├── database/                # Database handling
│       │   ├── __init__.py
│       │   └── database_handler.py
│       ├── utils/                   # Utilities
│       │   ├── __init__.py
│       │   └── logger.py
│       └── __init__.py
├── tests/                           # Test suite
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_nutritional_verifier.py
│   ├── test_orchestrator.py
│   ├── test_substitution_handler.py
│   └── README.md
├── tools/                           # Utility scripts
│   ├── example/
│   │   ├── example_usage.py
│   │   └── README.md
│   ├── init-project.py
│   └── README.md
├── check_structure.py
├── README.md
├── requirements.txt
├── setup.py
└── test_imports.py
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
4. Esegui lo script di verifica degli import

```bash
python test_imports.py
```

5. Esegui lo script di test

```bash
python example_usage
```

## 📝 Roadmap

1. **Ottimizzazioni delle prestazioni**

   - Implementare sistema di caching multi-livello
   - Ottimizzare gli algoritmi di sostituzione
   - Aggiungere indici per ricerche veloci nel database delle ricette
   - Sistema di monitoraggio delle performance

2. **Espansione della documentazione**

   - Implementazione documentazione Sphinx
   - Esempi di utilizzo dettagliati
   - Diagrammi di flusso dei processi
   - Guide di integrazione

3. **Integrazioni esterne**

   - Integrazione con Vtiger CRM
   - Generatore PDF per piani alimentari
   - Sistema di notifiche
   - API RESTful

4. **Test avanzati**
   - Test con vari profili utente
   - Test di integrazione end-to-end
   - Test di carico
   - Validazione nutrizionale avanzata

Per maggiori dettagli sulle implementazioni pianificate e le guide di integrazione, consultare [docs/mediterrania-extended-docs.md](docs/mediterrania-extended-docs.md).
