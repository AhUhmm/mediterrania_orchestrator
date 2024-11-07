# Approcci Alternativi alla Verifica del Piano Alimentare

## 1. Metodo Template-Based

### Descrizione
Questo approccio si basa sulla definizione di template di porzioni per ogni tipo di pasto, specificati per ciascun obiettivo nutrizionale.

### Struttura
```python
MEAL_TEMPLATES = {
    "Perdere peso": {
        "colazione": {
            "proteine": "1 porzione",    # es: 2 uova, 150g yogurt greco, 100g tofu
            "carboidrati": "0.5 porzione",# es: 1 fetta pane, 30g avena
            "grassi": "1 porzione",       # es: 30g frutta secca, 1/4 avocado
            "fibre": "1 porzione"         # es: 1 frutto, 100g verdura
        },
        "pranzo": {
            "proteine": "1 porzione",     # es: 120g legumi, 150g pesce
            "carboidrati": "1 porzione",  # es: 70g pasta, 70g riso
            "verdure": "2 porzioni",      # es: 200g verdure miste
            "grassi": "0.5 porzione"      # es: 1 cucchiaio olio
        },
        "cena": {
            "proteine": "1 porzione",
            "carboidrati": "0.5 porzione",
            "verdure": "2 porzioni",
            "grassi": "0.5 porzione"
        },
        "spuntini": {
            "proteine": "0.5 porzione",
            "carboidrati": "0.5 porzione",
            "grassi": "0.5 porzione"
        }
    },
    "Mantenere peso": {
        // Template simile con porzioni bilanciate
    },
    "Aumentare massa muscolare": {
        // Template con porzioni aumentate di proteine e carboidrati
    }
}
```

### Vantaggi
- Più intuitivo e facile da seguire per gli utenti
- Facile da adattare a diverse esigenze dietetiche
- Permette variazioni naturali mantenendo l'equilibrio
- Più pratico da implementare nella vita quotidiana

### Svantaggi
- Meno preciso dei calcoli matematici
- Richiede una buona comprensione delle porzioni
- Può essere meno adatto per esigenze molto specifiche

## 2. Metodo del Piatto (Harvard Plate Method)

### Descrizione
Questo approccio si basa sulla suddivisione visiva del piatto in proporzioni, seguendo il modello promosso dalla Harvard School of Public Health.

### Struttura
```python
PLATE_PROPORTIONS = {
    "Perdere peso": {
        "pranzo_cena": {
            "verdure": 0.5,      # metà del piatto verdure
            "proteine": 0.25,    # un quarto proteine
            "carboidrati": 0.25  # un quarto carboidrati
        },
        "colazione": {
            "proteine": 0.33,    # un terzo proteine
            "carboidrati": 0.33, # un terzo carboidrati integrali
            "frutta": 0.33       # un terzo frutta
        }
    },
    "Mantenere peso": {
        // Proporzioni simili con più flessibilità
    },
    "Aumentare massa muscolare": {
        // Proporzioni modificate per aumentare proteine
    }
}
```

### Vantaggi
- Estremamente intuitivo e visuale
- Facile da implementare senza pesare gli alimenti
- Promuove naturalmente una dieta bilanciata
- Validato scientificamente

### Svantaggi
- Meno preciso per il tracking calorico
- Può essere troppo semplificato per alcuni obiettivi
- Richiede adattamenti per pasti complessi

## Implementazione Pratica

Per implementare questi approcci, si suggerisce:

1. Creare una classe enum per il metodo di verifica:
```python
class MetodoVerifica(Enum):
    MATEMATICO = "matematico"
    TEMPLATE = "template"
    PIATTO = "piatto"
```

2. Permettere la selezione del metodo in base al profilo utente:
```python
def seleziona_metodo_verifica(profilo_utente: Dict) -> MetodoVerifica:
    if profilo_utente.get("preferenza_tracking") == "preciso":
        return MetodoVerifica.MATEMATICO
    elif profilo_utente.get("esperienza_cucina") == "principiante":
        return MetodoVerifica.PIATTO
    else:
        return MetodoVerifica.TEMPLATE
```

3. Implementare verifiche specifiche per ciascun metodo:
```python
def verifica_bilanciamento(self, piano: Dict, dati_utente: Dict) -> Dict:
    metodo = seleziona_metodo_verifica(dati_utente)
    if metodo == MetodoVerifica.MATEMATICO:
        return self._verifica_matematica(piano, dati_utente)
    elif metodo == MetodoVerifica.TEMPLATE:
        return self._verifica_template(piano, dati_utente)
    else:
        return self._verifica_piatto(piano, dati_utente)
```

## Conclusioni

L'utilizzo di questi approcci alternativi può rendere il piano alimentare più accessibile e sostenibile nel lungo termine. La scelta del metodo dovrebbe basarsi sulle caratteristiche e preferenze dell'utente, considerando:
- Livello di esperienza con la nutrizione
- Obiettivi specifici
- Preferenze di tracking
- Stile di vita

Si consiglia di implementare tutti e tre i metodi e permettere all'utente di scegliere quello più adatto alle proprie esigenze.
