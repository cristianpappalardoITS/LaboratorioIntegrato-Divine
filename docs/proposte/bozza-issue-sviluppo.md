# Bozza delle issue per lo sviluppo

> ✅ **Issue create su GitHub il 28/10/2026**, con etichette, sprint e milestone, e aggiunte alla board. Gli assegnatari li mette Cristian a mano.

Oggi la [board](https://github.com/users/cristianpappalardoITS/projects/2) ha 26 issue, tutte di progettazione e preparazione. Mancano le attività di sviluppo che portano al SAL del 23/11 e alla consegna del 10/12. Questa bozza le propone sprint per sprint, con gli sprint di una settimana già impostati sulla board.

Come leggere le tabelle:

- **Codice:** continua la numerazione di ogni team (SWD-07, WMD-09, DGS-07, COM-06…).
- **Fatto quando:** cosa deve esistere per spostare la issue in Done.
- **Tipo** e **Priorità:** le etichette `tipo:` e `priorità:` di [workflow-github.md](../workflow-github.md). Ogni issue ha anche `team:` e, come quelle già esistenti, `task-individuale` o `task-comune`.
- **Assegnatario:** nessuno; lo mette Cristian a mano.

## Calendario degli sprint

Gli sprint sono quelli del campo iterazione della board «Sprint»: Sprint 1 è chiuso, gli sprint 7 e 8 sono più corti.

| Sprint | Date | Milestone |
|--------|------|-----------|
| Sprint 2 | 26/10 – 01/11 | Primo incontro con il cliente (02/11) |
| Sprint 3 | 02/11 – 08/11 | SAL (23/11) |
| Sprint 4 | 09/11 – 15/11 | SAL (23/11) |
| Sprint 5 | 16/11 – 22/11 | SAL (23/11) |
| Sprint 6 | 23/11 – 29/11 | Presentazione finale (10/12) |
| Sprint 7 | 30/11 – 05/12 | Presentazione finale (10/12) |
| Sprint 8 | 06/12 – 10/12 | Presentazione finale (10/12) |

---

## Sprint 3 · 02/11 – 08/11 · Basi del progetto

| Codice | Titolo | Fatto quando | Tipo | Priorità |
|--------|--------|--------------|------|----------|
| SWD-07 | Creare il progetto Spring Boot 4 con Docker e PostgreSQL 18 | `backend/` si avvia con `docker compose up`; profilo `dev`; Flyway attivo; versione di Flyway compatibile con PostgreSQL 18 verificata | feature | alta |
| SWD-08 | Scrivere le migration V1–V8 e i dati finti di sviluppo | Le 27 tabelle nascono da Flyway; `db/testdata` con circa 30 carte `TEST-`; `ddl-auto=validate` passa | feature | alta |
| SWD-09 | Creare il modulo del motore di gioco con mescolamento e seed | `engine/` in Java puro; mazzo mescolato con un `Random` passato da fuori; primi test JUnit con seed fisso | feature | alta |
| SWD-10 | Implementare registrazione, accesso e refresh token JWT | `/auth/register`, `/auth/login`, `/auth/refresh`, `/auth/logout`, `/me` come nella guida per il frontend; password con BCrypt; test | feature | alta |
| WMD-09 | Impostare il progetto frontend | `frontend/` con struttura delle cartelle, CSS di base, `api.js` della guida, pagina di prova che chiama il backend | feature | alta |
| WMD-10 | Realizzare le pagine di registrazione e accesso | Registrazione con i consensi, accesso, uscita; errori mostrati all'utente | feature | alta |
| DGS-07 | Definire il catalogo della fase 1 | Elenco di circa 30 carte con nome, fazione, rarità, ATT/DIF ed effetto; almeno 7 Comuni e 3 Rare, per il set iniziale. Insieme a Nicolas | docs | alta |
| DGS-08 | Consegnare l'identità visiva definitiva | Logo (SVG e PNG), palette, caratteri, con la proposta scelta dal cliente | docs | alta |
| COM-06 | Registrare le decisioni del colloquio con il cliente | Le note del note-taker diventano una pagina in `docs/decisioni/` e le issue che ne seguono | docs | alta |

## Sprint 4 · 09/11 – 15/11 · Catalogo, pacchetti e motore

| Codice | Titolo | Fatto quando | Tipo | Priorità |
|--------|--------|--------------|------|----------|
| SWD-11 | Implementare le API del catalogo | `GET /cards`, fazioni, rarità, effetti e `GET /rules`; immagini servite con la cache | feature | alta |
| SWD-12 | Implementare crediti, negozio e apertura dei pacchetti | Acquisto con aggiornamento atomico dei crediti, estrazione lato server con i pesi, full art, storico delle aperture; set iniziale e benvenuto alla registrazione | feature | alta |
| SWD-13 | Implementare il round del motore senza effetti | Scontro contemporaneo, vantaggio di fazione, danni ai giocatori, morte, fine partita e pareggio; `round_log` come in schema.md; test | feature | alta |
| SWD-14 | Implementare collezione e mazzi con la validazione | `/me/cards`, CRUD dei mazzi, controlli su 20 carte, copie, limiti per rarità, possesso e `isFullArt` | feature | alta |
| WMD-11 | Realizzare il componente JavaScript della carta | Carta montata da dati e illustrazione (ritaglio, miniatura, full art), uguale alle carte di prova | feature | alta |
| WMD-12 | Realizzare negozio e apertura dei pacchetti | Lista dei pacchetti con le copertine, acquisto, pagina dell'apertura con l'id nell'URL | feature | alta |
| WMD-13 | Realizzare collezione e dettaglio della carta | Griglia con filtri e paginazione, dettaglio con il passaggio alla full art | feature | media |
| DGS-09 | Generare le illustrazioni del catalogo della fase 1 | Un'illustrazione per ogni carta di DGS-07, con i testi di generazione in `carte/testi-generazione/` e i metadati originali | feature | alta |
| DGS-10 | Scrivere i testi delle pagine pubbliche | Home, Il gioco e lore, Regolamento per i giocatori, FAQ, Glossario | docs | media |

## Sprint 5 · 16/11 – 22/11 · Effetti e preparazione del SAL

| Codice | Titolo | Fatto quando | Tipo | Priorità |
|--------|--------|--------------|------|----------|
| SWD-15 | Implementare gli effetti delle carte nel motore | I 23 effetti della lista di Nicolas, con l'ordine dato dalla moneta; un test per effetto | feature | alta |
| SWD-16 | Simulare le partite e proporre punti vita e limite di round | Simulazione di migliaia di partite con il catalogo vero; tabella con i risultati e proposta a Maie e Nicolas | test | media |
| SWD-17 | Scrivere i test di integrazione con Testcontainers | Test di accesso, acquisto dei pacchetti e mazzi su PostgreSQL 18 vero | test | media |
| WMD-14 | Realizzare l'editor dei mazzi | Contatori in diretta con i limiti di `GET /rules`, salvataggio, errori di `problems`, interruttore della full art | feature | alta |
| WMD-15 | Realizzare le pagine statiche | Privacy, Termini, Cookie, Contatti (con il form), 404 | feature | media |
| DGS-11 | Realizzare le copertine dei pacchetti con i Lord | Tre copertine, una per Lord, nel formato del negozio | feature | media |
| COM-07 | Preparare il SAL del 23 novembre | Demo che funziona dalla registrazione al mazzo, documentazione aggiornata, presentazione provata | docs | alta |

## Sprint 6 · 23/11 – 29/11 · Amici, scambi e sfide

| Codice | Titolo | Fatto quando | Tipo | Priorità |
|--------|--------|--------------|------|----------|
| SWD-18 | Implementare amici e scambi | Richieste di amicizia, scambi solo tra amici in transazione con `SELECT … FOR UPDATE`, annullamento automatico degli scambi non più validi | feature | alta |
| SWD-19 | Implementare sfide, partita e storico | Sfida, accettazione con il ricontrollo dei mazzi, partita salvata con le copie dei mazzi e il seed, storico | feature | alta |
| SWD-20 | Implementare le API del backoffice | CRUD di carte e pacchetti, caricamento delle immagini con le copie WebP, messaggi dei contatti | feature | alta |
| WMD-16 | Realizzare le pagine Amici e Scambi | Lista amici, richieste, nuovo scambio dalla lista amici, scambi ricevuti e inviati | feature | alta |
| WMD-17 | Realizzare sfide, replay e storico | Nuova sfida, sfide ricevute, replay round per round, scheda delle partite concluse | feature | alta |
| DGS-12 | Preparare il piano di marketing | Buyer persona, canali, materiali di lancio, a partire da DGS-06 | docs | media |

## Sprint 7 · 30/11 – 05/12 · Rifinitura e test

| Codice | Titolo | Fatto quando | Tipo | Priorità |
|--------|--------|--------------|------|----------|
| SWD-21 | Documentare le API con Swagger e scrivere i README | Swagger completo; README di `engine/` e `backend/` con avvio, test e utenti di prova | docs | alta |
| SWD-22 | Preparare il deploy | Tutto il progetto si avvia con un solo `docker compose up`; proposta AWS aggiornata | feature | media |
| WMD-18 | Realizzare il backoffice | Pagine Carte, Pacchetti, Configurazione e Messaggi per `role: ADMIN` | feature | alta |
| WMD-19 | Rifinire responsive, accessibilità e SEO | Tutte le pagine leggibili da telefono, testi alternativi delle carte, `noindex` nell'area utente, `sitemap.xml` | refactor | media |
| DGS-13 | Bilanciare il catalogo con le simulazioni | Statistiche finali delle carte, decise con SWD-16 | docs | media |
| COM-08 | Fare il test finale del portale e correggere i bug | Percorso completo provato da almeno una persona per team; bug aperti come issue `tipo: bug` | test | alta |

## Sprint 8 · 06/12 – 10/12 · Consegna

| Codice | Titolo | Fatto quando | Tipo | Priorità |
|--------|--------|--------------|------|----------|
| COM-09 | Preparare la presentazione finale del 10 dicembre | Slide, demo dal vivo, ruoli, prova cronometrata | docs | alta |

## Backlog · dopo le funzionalità obbligatorie

| Codice | Titolo | Tipo | Priorità |
|--------|--------|------|----------|
| SWD-23 | Implementare il rank con punteggio Elo e leghe | feature | bassa |
| SWD-24 | Implementare il recupero della password via email | feature | bassa |
| WMD-20 | Realizzare classifica e rank nel profilo | feature | bassa |
| DGS-14 | Progettare l'acquisto di crediti con denaro reale | docs | bassa |

**In tutto 42 issue nuove:** 38 negli sprint (16 SWD, 11 WMD, 7 DGS, 4 comuni) e 4 nel Backlog.

---

## Modifiche alle issue che esistono già

| Issue | Oggi | Proposta |
|-------|------|----------|
| Tutte le 25 issue di progettazione | Nessuno sprint | Sprint 2 e milestone "Primo incontro con il cliente" |
| #42 Presentazione cliente 2 Novembre | Senza etichette | Etichette `team: COM` e `task-comune` |
| #43 SWD-01 Regolamento | In Progress | Review: il regolamento v2 è pubblicato |
| #47 SWD-05 Entità e database | In Progress | Review: lo schema è pronto per lo sviluppo (`docs/documenti-iniziali`) |
| #67 COM-05 Domande per il cliente | Todo | In Progress: domande e risposte in `docs/presentazione/domande-colloquio.md` |
| Issue WMD e DGS | Senza assegnatario | Le assegna Cristian a mano. Di DGS tra i collaboratori c'è solo `decosm`: mancano due account |

Queste modifiche sono ancora proposte: non sono state fatte.

## Decisioni prese il 28/10

1. **Etichette:** si segue `workflow-github.md`. Le etichette di team sono state rinominate in `team: SWD`, `team: WMD`, `team: DGS`, `team: COM`, e sono state create le etichette `tipo:` e `priorità:`. `task-individuale` e `task-comune` restano.
2. **Sprint:** aggiunti gli sprint dal 4 all'8 nel campo Sprint della board.
3. **Roadmap delle slide:** allineata agli sprint settimanali della board.
4. **Issue:** create con `gh`, senza assegnatari. Gli assegnatari li mette Cristian a mano.
