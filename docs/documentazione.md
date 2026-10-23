# Documentazione

## Cosa documentare e dove

| Cosa | Dove | Chi lo aggiorna |
|------|------|-----------------|
| Panoramica del progetto | `README.md` nella radice | Marco / Cristian |
| Linee guida (workflow, codice, naming, commenti, template) | `docs/*.md` | Marco / Cristian |
| Come avviare e usare un modulo | `README.md` dentro `engine/`, `backend/`, `frontend/` | Chi lavora sul modulo |
| Classi e metodi | Javadoc nel codice | Chi scrive il codice |
| Endpoint REST | `docs/api/endpoints.md` | Chi crea o modifica l'endpoint |
| Decisioni del gruppo (concept, fazioni, valori di gioco...) | `docs/decisioni/` | Marco / Cristian, su comunicazione dei referenti |
| Riunioni | `docs/verbali/` | Chi fa da verbalizzante |
| Diagrammi ER, architettura, flussi | `docs/diagrammi/` | SWD (ER, architettura), WMD (flussi) |

## Regole

- **La documentazione si aggiorna nella stessa PR del codice.** Se cambi un endpoint, aggiorni `docs/api/endpoints.md` nella stessa PR.
- Si scrive in **Markdown** (`.md`), in italiano.
- Frasi brevi, tabelle ed esempi concreti al posto di paragrafi lunghi.
- Ogni decisione ha un file suo: chi arriva dopo deve capire **cosa** si è deciso e **perché**, senza dover chiedere.
- I valori ancora in discussione si segnano come tali ("ipotesi", "da verificare"), mai come definitivi.

## Esempio: documentazione di un endpoint

````markdown
### Crea un mazzo

`POST /api/v1/decks`

Crea un nuovo mazzo per l'utente autenticato. Le carte devono essere nella sua collezione.

**Body**

| Campo | Tipo | Obbligatorio | Note |
|-------|------|--------------|------|
| `name` | string | sì | 1–40 caratteri |
| `cardIds` | number[] | sì | Esattamente 20 carte, max 2 copie per carta |

**Esempio di richiesta**

```json
{ "name": "Mazzo offensivo", "cardIds": [3, 3, 7, 15, ...] }
```

**Risposte**

| Codice | Quando |
|--------|--------|
| `201 Created` | Mazzo creato, restituisce il `DeckResponse` |
| `400 Bad Request` | Numero di carte errato o più di 2 copie della stessa carta |
| `404 Not Found` | Una carta non è nella collezione dell'utente |
````
