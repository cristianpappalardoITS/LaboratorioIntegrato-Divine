# Guida ai dati per il frontend · Dreamscape

Per il team **WMD**. Spiega quali dati arrivano dal backend, come chiederli e come mandarli, pagina per pagina, così la sitemap e le pagine restano coerenti con il database.

> 🚧 **Proposta di SWD da confermare insieme.** I dati vengono dalla [proposta di database](../database/schema.md). I nomi delle API seguono [naming.md](../naming.md) e sono una proposta: quelli definitivi saranno in **Swagger** quando il backend esiste. Se qualcosa non torna con quello che vi serve, ditelo a Marco o Cristian.

## Indice

1. [Come funziona in breve](#1-come-funziona-in-breve)
2. [Regole comuni delle API](#2-regole-comuni-delle-api)
3. [Accesso con JWT](#3-accesso-con-jwt)
4. [Il file api.js](#4-il-file-apijs)
5. [Gli oggetti che ricevete](#5-gli-oggetti-che-ricevete)
6. [Pagine e chiamate](#6-pagine-e-chiamate)
7. [Come si monta una carta](#7-come-si-monta-una-carta)
8. [Elenco delle pagine per la sitemap](#8-elenco-delle-pagine-per-la-sitemap)
9. [Regole da ricordare](#9-regole-da-ricordare)
10. [Cose ancora da decidere](#10-cose-ancora-da-decidere)

---

## 1. Come funziona in breve

- Il frontend è fatto di **pagine HTML** con **CSS** e **JavaScript**, senza framework.
- Il JavaScript chiede i dati al backend con `fetch()` e riceve **JSON**. Poi riempie la pagina.
- Il backend fa tutti i conti e tutti i controlli: estrazione dei pacchetti, validità dei mazzi, partite, scambi. Il frontend **mostra** quello che riceve e **manda** quello che l'utente sceglie.
- Il giocatore si chiama **Dreamweaver**. Le fazioni sono **Dreams**, **Nightmares** e **Memories**.

```
 Pagina HTML  ──fetch()──▶  Backend (Spring Boot)  ──▶  Database (PostgreSQL)
      ▲                            │
      └────────── JSON ────────────┘
```

---

## 2. Regole comuni delle API

| Cosa | Regola | Esempio |
|------|--------|---------|
| Indirizzo base | Tutte le API partono da `/api/v1` | `http://localhost:8080/api/v1` in sviluppo |
| Id | Ogni id è un **UUID**: un testo di 36 caratteri. Si usa così come arriva, anche negli URL; non si calcola e non si confronta come un numero | `"019a1f2e-7c41-7d3a-9b2e-5f6a7b8c9d01"`, `/sfide/019a1f2e-…` |
| Formato | JSON in entrata e in uscita, nomi in `camelCase` | `{ "totalCards": 20, "isFullArt": false }` |
| Risorse | In inglese, al plurale, il verbo è il metodo HTTP | `GET /decks`, `POST /decks`, `DELETE /decks/{deckId}` |
| Date | Testo ISO 8601 in UTC: va convertito nell'ora locale per mostrarlo | `"2026-10-26T14:30:00Z"` |
| Immagini | URL relativi al backend, in WebP: si mettono così come sono in `src` o si usano nel disegno della carta. Il browser le tiene in cache (vedi [capitolo 7](#7-come-si-monta-una-carta)) | `"/images/cards/base-004-v1.webp"` |
| Liste lunghe | Con paginazione: `page` (da 0) e `size` | `GET /me/cards?page=0&size=24` |

Una lista paginata arriva così:

```json
{
  "items": [ ],
  "page": 0,
  "size": 24,
  "totalItems": 57,
  "totalPages": 3
}
```

### Errori

Ogni errore ha lo stesso formato, così si mostra il messaggio senza logica speciale:

```json
{
  "status": 409,
  "code": "USERNAME_TAKEN",
  "message": "Questo username è già usato.",
  "fieldErrors": [ { "field": "username", "message": "Questo username è già usato." } ]
}
```

| Codice HTTP | Quando | Cosa fa il frontend |
|-------------|--------|---------------------|
| `200` / `201` | Tutto bene (`201` = creato) | Mostra il risultato |
| `204` | Tutto bene, nessun dato in risposta | Mostra una conferma |
| `400` | Dati sbagliati (campo vuoto, password troppo corta, mazzo non valido) | Mostra `fieldErrors` accanto ai campi, oppure `message` |
| `401` | Token mancante o scaduto | Prova `/auth/refresh`; se fallisce, porta alla pagina di accesso |
| `403` | Accesso non permesso (es. un giocatore nel backoffice) | Mostra "non hai i permessi" |
| `404` | Non esiste (carta, mazzo, scambio...) | Pagina o messaggio "non trovato" |
| `409` | Conflitto (username già usato, crediti insufficienti, carte non più possedute) | Mostra `message` |

---

## 3. Accesso con JWT

Il backend usa i **token JWT**. Ci sono due token:

| Token | A cosa serve | Quanto dura | Dove sta |
|-------|--------------|-------------|----------|
| **Token di accesso** (`accessToken`) | Va in **ogni** richiesta che richiede l'accesso | Poco (proposta: 15 minuti) | In una variabile JavaScript, **non** in `localStorage` |
| **Refresh token** | Serve a ottenere un nuovo token di accesso | Più a lungo (proposta: 7 giorni) | In un **cookie `HttpOnly`** che il browser gestisce da solo: il JavaScript non lo vede e non lo tocca |

Perché non `localStorage`: se una pagina avesse un bug di sicurezza (XSS), uno script estraneo potrebbe leggere il token. Il cookie `HttpOnly` non è leggibile dal JavaScript.

Il sito è fatto di più pagine HTML, quindi la variabile si perde a ogni cambio pagina. Non è un problema: all'apertura di ogni pagina `api.js` chiama `/auth/refresh` e ottiene un token nuovo dal cookie (vedi il [capitolo 4](#4-il-file-apijs)).

### Le chiamate dell'accesso

| Azione | Chiamata | Cosa mandate | Cosa ricevete |
|--------|----------|--------------|---------------|
| Registrazione | `POST /auth/register` | `username`, `email`, `password`, `privacyAccepted`, `termsAccepted` | `201` + i dati dell'utente. Poi si fa l'accesso |
| Accesso | `POST /auth/login` | `login` (username **o** email), `password` | `accessToken` + dati dell'utente; il refresh token arriva nel cookie |
| Nuovo token di accesso | `POST /auth/refresh` | Niente: il cookie parte da solo | Un nuovo `accessToken` |
| Uscita | `POST /auth/logout` | Niente | `204`; il backend revoca il refresh token e cancella il cookie |
| Chi sono | `GET /me` | — | I dati dell'utente collegato |
| Modifica profilo | `PUT /me` | `email` | L'utente aggiornato |
| Cambio password | `PUT /me/password` | `currentPassword`, `newPassword` | `204`; per sicurezza gli altri dispositivi vengono scollegati |
| Password dimenticata (facoltativa) | `POST /auth/password-reset-requests` | `email` | Sempre `202`, anche se l'email non esiste (per non rivelare chi è registrato) |
| Nuova password (facoltativa) | `POST /auth/password-resets` | `token` (dal link dell'email), `newPassword` | `204` |

Esempio di registrazione:

```json
POST /api/v1/auth/register
{
  "username": "lucida",
  "email": "lucida@example.com",
  "password": "una-password-lunga",
  "privacyAccepted": true,
  "termsAccepted": true
}
```

Esempio di risposta all'accesso:

```json
{
  "accessToken": "eyJhbGciOi...",
  "expiresIn": 900,
  "user": { "id": "019a1f2e-7c41-7d3a-9b2e-5f6a7b8c9d01", "username": "lucida", "role": "PLAYER", "credits": 0 }
}
```

- `role` è `PLAYER` oppure `ADMIN`: con `ADMIN` si mostra il backoffice. Un solo login per tutti: l'admin entra dalla stessa pagina.
- **Regole dei campi** (il backend le ricontrolla sempre): username da 3 a 30 caratteri, lettere, numeri e trattino basso; email valida; password di almeno 8 caratteri; Privacy e Termini obbligatori.
- Username ed email sono unici **senza distinguere le maiuscole**: "Lucida" e "lucida" sono lo stesso utente.

---

## 4. Il file api.js

Tutte le chiamate passano da un solo file, `api.js`, che aggiunge il token, rinnova quello scaduto e trasforma gli errori. Le pagine non usano mai `fetch()` direttamente.

```js
// api.js: unico punto da cui passano le chiamate al backend
const API_BASE = "http://localhost:8080/api/v1";

// Token di accesso solo in memoria; il refresh token sta nel cookie HttpOnly.
let accessToken = null;

async function send(path, method, body) {
  const headers = { "Content-Type": "application/json" };
  if (accessToken) headers.Authorization = `Bearer ${accessToken}`;
  return fetch(API_BASE + path, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
    credentials: "include" // fa partire il cookie del refresh token
  });
}

export async function refresh() {
  const response = await fetch(API_BASE + "/auth/refresh", { method: "POST", credentials: "include" });
  if (!response.ok) return false;
  accessToken = (await response.json()).accessToken;
  return true;
}

export async function api(path, { method = "GET", body } = {}) {
  let response = await send(path, method, body);
  if (response.status === 401 && (await refresh())) {
    response = await send(path, method, body); // riprova una volta con il token nuovo
  }
  if (response.status === 401) {
    window.location.href = "/accesso.html";
    return null;
  }
  if (response.status === 204) return null;
  const data = await response.json();
  if (!response.ok) throw data; // { status, code, message, fieldErrors }
  return data;
}

export async function login(loginName, password) {
  const data = await api("/auth/login", { method: "POST", body: { login: loginName, password } });
  accessToken = data.accessToken;
  return data.user;
}
```

Uso in una pagina:

```js
import { api, refresh } from "./api.js";

await refresh(); // all'apertura della pagina: recupera il token dal cookie
const summary = await api("/me/summary");
document.querySelector("#credits").textContent = summary.credits;
```

---

## 5. Gli oggetti che ricevete

Questi oggetti tornano in più pagine: conviene scrivere una sola funzione JavaScript per mostrarli.

### Carta

```json
{
  "id": "019a1f30-0000-7000-8000-000000000004",
  "code": "BASE-004",
  "name": "Il Sogno Lucido",
  "faction": { "code": "DREAMS", "name": "Dreams" },
  "rarity": { "code": "LEGENDARY", "name": "Leggendaria" },
  "attack": 5,
  "defense": 7,
  "description": "Sai di sognare, e il sogno ti obbedisce.",
  "effect": {
    "code": "NEUTRALITY",
    "name": "Neutralità",
    "value": null,
    "text": "Questa carta non subisce il vantaggio di fazione dell'avversario."
  },
  "illustrationUrl": "/images/cards/base-004-v1.webp",
  "illustrationThumbUrl": "/images/cards/base-004-v1-thumb.webp",
  "illustrationFocusY": 0.27,
  "fullArtIllustrationUrl": "/images/cards/base-004-fullart-v1.webp",
  "fullArtThumbUrl": "/images/cards/base-004-fullart-v1-thumb.webp",
  "fullArtFocusY": 0.40,
  "lordTitle": "Dreams Lord"
}
```

- `effect` è `null` se la carta non ha effetti; `value` è il numero X dell'effetto (es. `Protezione 1`), `null` se l'effetto non ha numero.
- `illustrationUrl` è la copia **grande** (larghezza 1024 px), `illustrationThumbUrl` la **miniatura** (larghezza 400 px): quale usare è spiegato nel [capitolo 7](#7-come-si-monta-una-carta).
- `illustrationFocusY` e `fullArtFocusY` dicono quale fascia dell'immagine resta visibile nel ritaglio: 0 = in alto, 1 = in basso (quasi sempre 0,40).
- `fullArtIllustrationUrl` e `fullArtThumbUrl` ci sono solo per le Leggendarie.
- `lordTitle` c'è solo per le tre carte Lord.
- Codici delle rarità: `COMMON`, `RARE`, `EPIC`, `LEGENDARY`. Codici delle fazioni: `DREAMS`, `NIGHTMARES`, `MEMORIES`.

### Carta della collezione

```json
{ "card": { "id": "019a1f30-0000-7000-8000-000000000004", "name": "Il Sogno Lucido", "...": "..." }, "quantity": 2, "fullArtQuantity": 1 }
```

`quantity` conta tutte le copie, `fullArtQuantity` quante di queste sono full art.

### Utente (in liste, amici, sfide)

```json
{ "id": "019a1f2e-8d52-7e4b-8c3f-6a7b8c9d0e12", "username": "incubo_99" }
```

Degli altri giocatori si vede solo lo username: mai email o crediti.

---

## 6. Pagine e chiamate

Per ogni pagina: le chiamate da fare e cosa mostrare. 🔓 = pagina pubblica, 🔑 = serve l'accesso, 🛠️ = solo admin.

### Pagine pubbliche 🔓

| Pagina | Chiamate | Cosa mostra |
|--------|----------|-------------|
| Home | `GET /cards?featured=true` | Alcune carte del catalogo come anteprima |
| Il gioco / Lore | `GET /factions` | Le tre fazioni con forze, debolezze e il loro Lord |
| Regolamento | `GET /rules` | I numeri del regolamento, sempre aggiornati |
| Contatti | `POST /contact-messages` | Form: `name`, `email`, `message` → `201` e messaggio di conferma |
| Chi siamo, FAQ, Glossario, Privacy, Cookie, Termini, 404 | Nessuna | Pagine statiche |

Risposta di `GET /rules`:

```json
{
  "deckSize": 20,
  "startingLifePoints": 20,
  "roundLimit": 60,
  "rarities": [
    { "code": "COMMON", "name": "Comune", "maxPerDeck": null, "maxCopies": 2 },
    { "code": "RARE", "name": "Rara", "maxPerDeck": 8, "maxCopies": 2 },
    { "code": "EPIC", "name": "Epica", "maxPerDeck": 4, "maxCopies": 2 },
    { "code": "LEGENDARY", "name": "Leggendaria", "maxPerDeck": 2, "maxCopies": 1 }
  ],
  "factionAdvantages": [
    { "faction": "DREAMS", "strongAgainst": "MEMORIES", "attackBonus": 1 },
    { "faction": "MEMORIES", "strongAgainst": "NIGHTMARES", "attackBonus": 1 },
    { "faction": "NIGHTMARES", "strongAgainst": "DREAMS", "attackBonus": 1 }
  ]
}
```

`maxPerDeck: null` vuol dire "nessun limite".

### Accesso 🔓

| Pagina | Chiamate |
|--------|----------|
| Registrazione | `POST /auth/register`, poi `POST /auth/login` e passaggio a **Benvenuto** |
| Accesso | `POST /auth/login` → Dashboard (o Backoffice se `role` è `ADMIN`) |
| Password dimenticata (facoltativa) | `POST /auth/password-reset-requests` |
| Nuova password (facoltativa, dal link dell'email) | `POST /auth/password-resets` |
| Esci (nel menu) | `POST /auth/logout` → Home |

### Area del Dreamweaver 🔑

#### Benvenuto (dopo la registrazione)

`GET /me/welcome` → il set iniziale e i due pacchetti di benvenuto, già aperti dal backend alla registrazione.

```json
{
  "starterCards": [ { "card": { "...": "..." }, "isFullArt": false } ],
  "welcomeOpenings": [
    { "openingId": "019a2b40-0000-7000-8000-000000000101", "packName": "Benvenuto", "cards": [ { "card": { "...": "..." }, "isFullArt": false } ] },
    { "openingId": "019a2b40-0000-7000-8000-000000000102", "packName": "Benvenuto con Epica", "cards": [ { "card": { "...": "..." }, "isFullArt": false } ] }
  ]
}
```

Il set iniziale ha 20 carte (14 Comuni e 6 Rare), estratte senza mai superare le copie massime: con queste 20 carte si compone sempre un mazzo valido. Il mazzo **non** viene creato in automatico: dalla pagina Benvenuto conviene un pulsante "Componi il tuo primo mazzo" che apre l'editor. Le carte si possono rivelare una alla volta come in un'apertura.

#### Dashboard

`GET /me/summary`

```json
{
  "username": "lucida",
  "credits": 250,
  "pendingFriendRequests": 1,
  "pendingTrades": 2,
  "pendingChallenges": 0,
  "latestCards": [ { "card": { "...": "..." }, "isFullArt": false } ]
}
```

#### Profilo

| Azione | Chiamata |
|--------|----------|
| Vedere i dati | `GET /me` → `username`, `email`, `createdAt` |
| Cambiare email | `PUT /me` |
| Cambiare password | `PUT /me/password` |

Lo username non si cambia (è il nome visibile agli amici).

#### Crediti

`GET /me/credit-transactions?page=0&size=20`

```json
{
  "items": [
    { "type": "PACK_PURCHASE", "amount": -100, "balanceAfter": 150, "createdAt": "2026-10-26T15:02:00Z" },
    { "type": "DAILY_REWARD", "amount": 50, "balanceAfter": 250, "createdAt": "2026-10-26T09:00:00Z" }
  ],
  "page": 0, "size": 20, "totalItems": 2, "totalPages": 1
}
```

Tipi possibili: `SIGNUP_BONUS`, `DAILY_REWARD`, `PACK_PURCHASE`, `MATCH_REWARD`, `ADMIN_ADJUSTMENT` (il frontend li traduce in italiano). Il riquadro "Acquista crediti" con denaro vero va mostrato solo come "in arrivo": in fase 1 non c'è.

#### Negozio e apertura dei pacchetti

`GET /packs` → i pacchetti in vendita:

```json
[
  {
    "id": "019a1f31-0000-7000-8000-000000000001",
    "name": "Pacchetto base",
    "description": "5 carte dal set base.",
    "priceCredits": 100,
    "fullArtChance": 5.0,
    "covers": [
      { "id": "019a1f31-0000-7000-8000-0000000000c1", "name": "Dreams Lord", "factionCode": "DREAMS", "imageUrl": "/images/packs/base-dreams-v1.webp" },
      { "id": "019a1f31-0000-7000-8000-0000000000c2", "name": "Nightmares Lord", "factionCode": "NIGHTMARES", "imageUrl": "/images/packs/base-nightmares-v1.webp" },
      { "id": "019a1f31-0000-7000-8000-0000000000c3", "name": "Memories Lord", "factionCode": "MEMORIES", "imageUrl": "/images/packs/base-memories-v1.webp" }
    ],
    "slots": [
      { "cardCount": 3, "rarities": [ { "code": "COMMON", "chance": 100.0 } ] },
      { "cardCount": 1, "rarities": [ { "code": "RARE", "chance": 100.0 } ] },
      { "cardCount": 1, "rarities": [ { "code": "EPIC", "chance": 90.0 }, { "code": "LEGENDARY", "chance": 10.0 } ] }
    ]
  }
]
```

- Il giocatore sceglie una delle tre copertine: il contenuto è lo stesso.
- `slots` serve a mostrare "3 Comuni, 1 Rara, 1 Epica (10% Leggendaria)".

Acquisto: `POST /packs/{packId}/open` con `{ "coverId": "019a1f31-0000-7000-8000-0000000000c2" }`:

```json
{
  "openingId": "019a2b44-5c6d-7e8f-9a0b-1c2d3e4f5a6b",
  "creditsAfter": 150,
  "cards": [
    { "card": { "...": "..." }, "isFullArt": false },
    { "card": { "...": "..." }, "isFullArt": true }
  ]
}
```

Poi si va su `/negozio/apertura/{openingId}`, che legge `GET /pack-openings/{openingId}`. Con l'**id dell'apertura** nell'URL, ricaricare la pagina non compra un altro pacchetto. Se i crediti non bastano arriva un `409` con `code: "NOT_ENOUGH_CREDITS"`.

#### Collezione e dettaglio carta

| Azione | Chiamata |
|--------|----------|
| Collezione con filtri | `GET /me/cards?faction=DREAMS&rarity=RARE&search=sogno&fullArt=true&page=0&size=24` |
| Dettaglio di una carta | `GET /cards/{cardId}` (dati della carta) + la riga della collezione (copie possedute) |

Il dettaglio mostra anche contro chi la fazione è forte o debole (da `GET /rules`) e, se l'utente ha una copia full art, il passaggio alla versione full art.

#### Mazzi

| Azione | Chiamata |
|--------|----------|
| I miei mazzi | `GET /decks` |
| Un mazzo | `GET /decks/{deckId}` |
| Nuovo mazzo | `POST /decks` |
| Modifica | `PUT /decks/{deckId}` |
| Elimina | `DELETE /decks/{deckId}` |

Cosa si manda al salvataggio:

```json
{ "name": "Incubi veloci", "cards": [ { "cardId": "019a1f30-0000-7000-8000-000000000005", "quantity": 2, "isFullArt": false }, { "cardId": "019a1f30-0000-7000-8000-000000000008", "quantity": 1, "isFullArt": true } ] }
```

Cosa si riceve:

```json
{
  "id": "019a2a10-1b2c-7d3e-8f40-a1b2c3d4e5f6",
  "name": "Incubi veloci",
  "totalCards": 20,
  "isValid": true,
  "problems": [],
  "cards": [ { "card": { "...": "..." }, "quantity": 2, "isFullArt": false } ]
}
```

- **Full art nel mazzo:** per una Leggendaria di cui l'utente possiede una copia full art (`fullArtQuantity` ≥ 1 nella collezione), l'editor mostra un interruttore "Usa la full art". Con `isFullArt: true` la carta si monta con `fullArtIllustrationUrl` nell'editor, nella lista dei mazzi e nel replay della partita. Non cambia le statistiche. Se l'utente non ha la full art, il backend risponde `400`.

- Se il mazzo non rispetta le regole il salvataggio risponde `400`, e `problems` dice cosa non va, es. `"Le Rare sono 9: il massimo è 8."`.
- L'editor mostra i contatori in diretta (carte totali, copie, limiti per rarità) con i numeri di `GET /rules`, così l'utente vede l'errore prima di salvare. Il backend controlla comunque.
- Un mazzo salvato può diventare non valido dopo uno scambio: `isValid: false` e `problems` lo dicono nella lista dei mazzi.

#### Amici (pagina nuova)

| Azione | Chiamata |
|--------|----------|
| I miei amici | `GET /friends` |
| Cerca un Dreamweaver | `GET /users?search=luc` (solo username) |
| Manda una richiesta | `POST /friend-requests` con `{ "username": "lucida" }` |
| Richieste ricevute / inviate | `GET /friend-requests?direction=received` / `?direction=sent` |
| Accetta | `POST /friend-requests/{requestId}/accept` |
| Rifiuta (ricevuta) o annulla (inviata) | `DELETE /friend-requests/{requestId}` |
| Togli un amico | `DELETE /friends/{userId}` |

```json
GET /api/v1/friends
[ { "user": { "id": "019a1f2e-8d52-7e4b-8c3f-6a7b8c9d0e12", "username": "incubo_99" }, "since": "2026-10-20T18:11:00Z" } ]
```

#### Scambi

Si scambia **solo con gli amici**. Quantità e rarità sono libere (es. 1 Epica per 5 Comuni): decide l'amico accettando o rifiutando.

| Azione | Chiamata |
|--------|----------|
| Ricevuti / Inviati / Storico | `GET /trades?box=received`, `?box=sent`, `?box=history` |
| Dettaglio | `GET /trades/{tradeId}` |
| Proponi | `POST /trades` |
| Accetta / Rifiuta (destinatario) | `POST /trades/{tradeId}/accept`, `POST /trades/{tradeId}/reject` |
| Annulla (chi propone) | `POST /trades/{tradeId}/cancel` |

Proposta di scambio:

```json
{
  "recipientId": "019a1f2e-8d52-7e4b-8c3f-6a7b8c9d0e12",
  "message": "Ti va?",
  "offered":   [ { "cardId": "019a1f30-0000-7000-8000-000000000007", "quantity": 1, "isFullArt": false } ],
  "requested": [ { "cardId": "019a1f30-0000-7000-8000-000000000001", "quantity": 5, "isFullArt": false } ]
}
```

- `offered` = carte che do io; `requested` = carte che chiedo all'amico. Almeno una carta per lato.
- Nella pagina "Nuovo scambio" il destinatario si sceglie **dalla lista amici** e le carte dalla propria collezione e da quella dell'amico (`GET /users/{userId}/cards`, visibile solo agli amici).
- Stati di uno scambio: `PENDING` (in attesa), `ACCEPTED`, `REJECTED`, `CANCELLED`.
- Se all'accettazione qualcuno non ha più le carte, arriva un `409` e nessuna carta si muove.

#### Sfide, risultato e storico

Le sfide sono **aperte a tutti i Dreamweaver**, non solo agli amici.

| Azione | Chiamata |
|--------|----------|
| Ricevute / Inviate / Concluse | `GET /challenges?box=received`, `?box=sent`, `?box=completed` |
| Lancia una sfida | `POST /challenges` con `{ "opponentId": "…", "deckId": "…" }` (solo mazzi validi) |
| Accetta e gioca | `POST /challenges/{challengeId}/accept` con `{ "deckId": "…" }` → `{ "matchId": "…" }` |
| Rifiuta / Annulla | `POST /challenges/{challengeId}/reject`, `POST /challenges/{challengeId}/cancel` |
| Risultato | `GET /matches/{matchId}` |

La partita la gioca il server appena la sfida è accettata: non c'è niente da aspettare. Il risultato:

```json
{
  "id": "019a2c55-6d7e-7f80-9a1b-2c3d4e5f6a7b",
  "challenger": { "id": "019a1f2e-7c41-7d3a-9b2e-5f6a7b8c9d01", "username": "lucida" },
  "opponent": { "id": "019a1f2e-8d52-7e4b-8c3f-6a7b8c9d0e12", "username": "incubo_99" },
  "winnerId": "019a1f2e-8d52-7e4b-8c3f-6a7b8c9d0e12",
  "endReason": "LIFE_POINTS",
  "totalRounds": 24,
  "startingLifePoints": 20,
  "finalLifePoints": { "challenger": 0, "opponent": 6 },
  "coinTossWinner": "OPPONENT",
  "playedAt": "2026-10-26T16:40:00Z",
  "rounds": [
    {
      "round": 3,
      "clash": 2,
      "challengerCard": { "cardId": "019a1f30-0000-7000-8000-000000000003", "attack": 4, "attackModifier": -2, "factionBonus": 0, "defenseBefore": 7, "defenseAfter": -2 },
      "opponentCard":   { "cardId": "019a1f30-0000-7000-8000-000000000008", "attack": 8, "attackModifier": 0, "factionBonus": 1, "defenseBefore": 5, "defenseAfter": 3 },
      "outcome": "CHALLENGER_CARD_DIED",
      "triggeredEffects": [ { "cardId": "019a1f30-0000-7000-8000-000000000008", "code": "WEAKENING", "text": "Indebolimento 2: l'attacco del Faro nella Nebbia scende da 4 a 2" } ],
      "damageToPlayer": { "challenger": 2, "opponent": 0 },
      "lifePointsAfter": { "challenger": 18, "opponent": 20 }
    }
  ],
  "decks": { "challenger": { "...": "..." }, "opponent": { "...": "..." } }
}
```

- `winnerId: null` = pareggio.
- `endReason`: `LIFE_POINTS` (punti vita a 0), `DECK_EXHAUSTED` (mazzo finito), `ROUND_LIMIT` (60 round, pareggio).
- `outcome`: `NONE_DIED`, `CHALLENGER_CARD_DIED`, `OPPONENT_CARD_DIED`, `BOTH_DIED`.
- Un **round** è un singolo scambio di colpi; uno **scontro** (`clash`) è la serie di round tra le stesse due creature. Nella cronaca si usa "round", non "turno".
- `decks` contiene la copia dei due mazzi com'erano al momento della partita: serve per mostrare le carte anche se poi i mazzi sono cambiati.
- **Storico:** è la scheda "Concluse" di `/sfide`. Basta una pagina sola.

### Backoffice 🛠️ (solo `role: ADMIN`)

| Pagina | Chiamate | Note |
|--------|----------|------|
| Dashboard admin | `GET /admin/stats` | Numeri di utenti, carte, pacchetti, partite |
| Carte | `GET/POST /admin/cards`, `PUT /admin/cards/{cardId}` | Campi: codice, nome, descrizione, ATT, DIF, fazione, rarità, espansione, effetto e valore, illustrazione 3:2 e ritaglio, full art 2:3 e ritaglio (solo Leggendarie), attiva |
| Caricamento illustrazioni | `POST /admin/images` (form `multipart/form-data` con il file, il codice della carta e il tipo: illustrazione, full art o copertina) → `{ "url": "/images/cards/base-013-v1.webp", "thumbUrl": "/images/cards/base-013-v1-thumb.webp" }` | Si carica il PNG originale: il backend lo conserva intatto e crea da solo le copie WebP. Una nuova immagine per la stessa carta diventa `-v2`. Le copertine hanno solo `url` |
| Pacchetti | `GET/POST /admin/packs`, `PUT /admin/packs/{packId}` | Tipo (negozio, set iniziale, benvenuto), prezzo, slot con rarità e probabilità (per ogni slot sommano a 100), copertine, probabilità full art, attivo |
| Configurazione | `GET/PUT /admin/factions`, `/admin/rarities`, `/admin/game-modes` | Vantaggi e Lord delle fazioni, limiti delle rarità, punti vita e limite di round. Le carte per mazzo (20) sono in sola lettura |
| Messaggi | `GET /admin/contact-messages`, `PUT /admin/contact-messages/{messageId}` | Messaggi del form Contatti: letto, archiviato |

Le carte e i pacchetti non si cancellano: si disattivano (`isActive: false`).

---

## 7. Come si monta una carta

La carta la **monta il frontend in JavaScript**: il backend manda i dati e l'illustrazione, non l'immagine finita. Così, se cambia una statistica, la carta si aggiorna da sola.

Ingredienti:

| Ingrediente | Da dove arriva |
|-------------|----------------|
| Illustrazione (`illustrationUrl` o `illustrationThumbUrl`) e ritaglio verticale (`illustrationFocusY`, da 0 = in alto a 1 = in basso) | Backend, per ogni carta |
| Cornice della fazione e della rarità, con la finestra trasparente | File del frontend: 12 cornici (3 fazioni × 4 rarità), anche queste in WebP grande e miniatura |
| Simbolo della fazione: luna (Dreams), occhio (Nightmares), clessidra (Memories) | File del frontend |
| Coordinate di nome, simbolo, testi, ATT e DIF sulla cornice | File del frontend (es. `zone.json`) |
| Nome, descrizione, effetto, ATT, DIF | Backend, per ogni carta |

Ordine di disegno (es. su un `<canvas>` di 1024 × 1536 con le copie grandi, o di 400 × 600 con le miniature, poi adattato con il CSS):

1. Illustrazione, ritagliata in verticale con `illustrationFocusY`, senza zoom.
2. Cornice sopra (la finestra trasparente lascia vedere l'illustrazione).
3. Simbolo della fazione, nome, descrizione ed effetto, ATT e DIF nelle loro coordinate.
4. Full art: l'illustrazione copre tutta la carta e i testi stanno su pannelli scuri semitrasparenti.

Il riferimento visivo sono le 15 carte del set di prova in `carte/carte-finali/`. Come preparare cornici trasparenti e coordinate (compositore Python o tutto in JavaScript) è ancora da decidere con SWD. Per l'accessibilità, ogni carta ha un testo alternativo con nome, fazione, rarità, attacco e difesa.

### Il ritaglio

L'immagine si adatta alla finestra della cornice senza deformarsi e senza zoom; quello che avanza si taglia. `illustrationFocusY` dice quanto tagliare sopra e quanto sotto. Esempio: avanzano 400 px in altezza e il focus è 0,40, quindi si tagliano 160 px sopra e 240 px sotto.

Con livelli HTML/CSS:

```js
img.style.objectFit = "cover";
img.style.objectPosition = `50% ${carta.illustrationFocusY * 100}%`;
```

Con il canvas: `sy = (altezzaScalata - altezzaFinestra) * illustrationFocusY`.

### Grande o miniatura

| Dove | Copia | Peso indicativo |
|------|-------|-----------------|
| Griglie e liste: collezione, editor del mazzo, scambi, dashboard, campo di partita | **Miniatura** (`illustrationThumbUrl`, cornice piccola) | 25–80 KB l'illustrazione, 20–35 KB la cornice |
| Carta da sola in grande: dettaglio carta, apertura del pacchetto, Lord nella pagina della fazione | **Grande** (`illustrationUrl`, cornice grande) | 120–350 KB l'illustrazione, 75–140 KB la cornice |

Con le miniature la prima visita alla collezione pesa meno di 1 MB. Con i PNG originali sarebbero circa 55 MB.

Le coordinate delle zone (es. `zone.json`) si scrivono una volta per la carta grande (1024 × 1536). Per la miniatura si moltiplicano per 400 / 1024.

### Cache: cosa resta nel browser

| Cosa | Resta in cache? | Perché |
|------|-----------------|--------|
| Illustrazioni e copertine (`/images/...`) | **Sì, per sempre** | Il backend le manda con `Cache-Control: public, max-age=31536000, immutable`. Se un'immagine cambia, il nome cambia (`-v1` → `-v2`), quindi non si vede mai una versione vecchia |
| Cornici, simboli e font del frontend | **Sì**, se anche voi mettete la versione nel nome (es. `cornice-dreams-comune-v1.webp`) e configurate lo stesso `Cache-Control` | Stesso motivo |
| Pagine HTML, `api.js`, CSS | Per poco, o con controllo a ogni visita | Così un aggiornamento del sito arriva subito |
| Risposte delle API (JSON) | **No** | Contengono dati personali e cambiano spesso. Spring Security manda già `no-store` |
| Carta montata | **No, non serve** | Montarla costa pochi millisecondi. A ogni pagina si rimonta con le immagini già in cache, ed è sempre aggiornata se cambiano statistiche o testi |

In una prima sessione di un nuovo utente si montano circa 150–200 carte: benvenuto ~30, collezione ~30, editor del mazzo ~50, un pacchetto 5, una partita fino a 40. In tutto meno di un secondo. Ogni immagine si scarica solo la prima volta.

Un consiglio: se nella stessa pagina la stessa carta compare più volte (es. due copie nel mazzo), si può montarla una volta e copiarla (`cloneNode(true)` con i livelli HTML, `drawImage` da un canvas già pronto).

---

## 8. Elenco delle pagine per la sitemap

Le pagine che il database permette, già con le decisioni di questi giorni.

| Area | Pagine |
|------|--------|
| 🔓 Pubblica | Home · Il gioco / Lore · Regolamento · Chi siamo · Contatti · FAQ · Glossario · Privacy Policy · Cookie · Termini di servizio · 404 |
| 🔓 Accesso | Registrazione · Accesso · Password dimenticata (facoltativa) · Nuova password (facoltativa) |
| 🔑 Dreamweaver | Benvenuto · Dashboard · Profilo (con cambio email e password) · Crediti · Negozio · Apertura pacchetto · Collezione · Dettaglio carta · Mazzi · Editor mazzo · **Amici** · Scambi · Nuovo scambio · Dettaglio scambio · Sfide (con la scheda Concluse = storico) · Nuova sfida · Accetta sfida · Risultato partita |
| 🛠️ Backoffice | Dashboard admin · Carte · Pacchetti · Configurazione · Messaggi |

Rispetto alla prima sitemap: nuove **Benvenuto**, **Amici**, **Nuova password** e **Messaggi**; tolto l'accesso admin separato (si entra dalla stessa pagina); Storico unito a Sfide; nessuna scelta della modalità nella Nuova sfida (c'è solo la Base).

---

## 9. Regole da ricordare

- **Il server decide**: estrazione dei pacchetti, esito delle partite, validità dei mazzi, scambi. Il frontend non calcola niente di tutto questo.
- **I controlli si fanno due volte**: nel frontend per aiutare l'utente, nel backend per sicurezza.
- **Mai token in `localStorage`**: solo in memoria, come in `api.js`.
- **Miniature nelle griglie, copia grande solo per la carta da sola**: le immagini restano leggere anche da telefono.
- **Mai dati personali negli URL** (es. email nella barra degli indirizzi).
- **Pagine dell'area utente e del backoffice in `noindex`**; `robots.txt` e `sitemap.xml` solo con le pagine pubbliche.
- **Responsive**: ATT, DIF, fazione e rarità leggibili anche su mobile.
- **Acquisto crediti con denaro reale**: solo "in arrivo", non si sviluppa in fase 1.

---

## 10. Cose ancora da decidere

| Decisione | Proposta | Chi |
|-----------|----------|-----|
| Durata dei token | Accesso 15 minuti, refresh 7 giorni | SWD |
| Recupero password in fase 1 | Solo se c'è tempo: richiede l'invio di email | SWD + WMD |
| Come si ottengono i crediti (giornaliero, vittorie...) | Ricompensa giornaliera + premio vittoria | DGS |
| Canvas o livelli HTML/CSS per la carta | Canvas: stesso risultato delle carte di prova | WMD |
| Cornici trasparenti e coordinate: compositore Python o JavaScript | Da scegliere | SWD + WMD |
| Collezione con le carte mancanti in ombra (album) | Sì: invoglia a completare la collezione | WMD + DGS |
| Cancellazione dell'account dal profilo | Pulsante che rende anonimo l'account | SWD + WMD |
| Classifica e rank | Dopo le funzioni obbligatorie; lasciare spazio nel menu | Tutti |
