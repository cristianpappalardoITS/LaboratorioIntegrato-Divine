# Dreamscape

Progetto Laboratorio Integrato · Gruppo 5 · **Somnia**

**Dreamscape** è un gioco di carte collezionabili digitale (TCG) a tema sogni. I giocatori sono i **Dreamweaver**: si registrano, ricevono crediti virtuali e un set di carte iniziale, comprano pacchetti di carte casuali, gestiscono la collezione e i mazzi, scambiano carte con i propri amici e si sfidano in partite simulate dal server, con risultato round per round e storico delle partite.

- **Repository:** [cristianpappalardoITS/gruppo-05-dreamscape](https://github.com/cristianpappalardoITS/gruppo-05-dreamscape)
- **Tema:** i sogni. Tre fazioni: **Dreams**, **Nightmares** e **Memories**, ognuna con il suo Lord.

## Team

| Team | Membri | Ambito |
|------|--------|--------|
| **SWD** · Software Developer | Cristian (TL), Marco (Vice TL), Nicolas | Motore di gioco, backend, database, API |
| **WMD** · Web Developer | Gaia (TL), Alessandro, Daniele, Yuri | Sitemap, UX/UI, wireframe, frontend |
| **DGS** · Digital Strategist | Sara (TL), Valerio, Maie | Concept, lore, economia di gioco, marketing |

> 🚧 Il brief chiede lo username GitHub di ogni studente (`@username`): va aggiunto qui per tutti i membri.

Le decisioni finali dei task comuni (COM-xx) vanno comunicate a **Marco** o **Cristian**, che le registrano in `docs/decisioni/`.

## Il gioco in breve

- **Una sola modalità**, la Base, che comprende gli effetti delle carte (il brief aggiornato permette di modificare la modalità Base).
- Mazzi da 20 carte, al massimo 2 copie per carta (1 per le Leggendarie), limiti per rarità.
- Fazioni con vantaggi reciproci, scontro contemporaneo, partita simulata dal server.
- **Lista amici**: si scambia solo con i propri amici, in quantità e rarità libere (es. 1 Epica per 5 Comuni), sempre solo se l'altro accetta.

I dettagli sono nella [proposta di regolamento](docs/proposte/proposta-regolamento-dreamscape.pdf).

## Stack

| Livello | Tecnologia |
|---------|------------|
| Motore di gioco | Java, modulo isolato, test **JUnit** |
| Backend / portale | Java + **Spring Boot**, Spring Data **JPA**, accesso con token **JWT** |
| Database | **PostgreSQL**, migration con **Flyway** |
| Frontend | **HTML, CSS e JavaScript** |
| Gestione progetto | **GitHub Projects** |

Il pagamento con denaro reale non fa parte della fase 1: i crediti sono solo virtuali.

## Scadenze

| Data | Milestone |
|------|-----------|
| 19/10 | Kick-off |
| 26/10 | Presentazione delle prime bozze |
| 02/11 | Primo incontro con il cliente |
| 23/11 | SAL (stato avanzamento lavori) |
| 10/12 | Presentazione finale |

## Struttura del repository

```
gruppo-05-dreamscape/
├── engine/      # Motore di gioco Java + test JUnit
├── backend/     # Applicazione Spring Boot (portale + API REST)
├── frontend/    # Frontend in HTML, CSS e JavaScript
├── database/    # Script SQL, migrazioni, dati di prova
├── carte/       # Set di carte di prova: cornici, illustrazioni, carte finite, script, effetti
├── docs/        # Documentazione e linee guida
└── .github/     # Template di issue e pull request
```

## Documentazione

Le linee guida del progetto sono in [`docs/`](docs/README.md):

- [Flusso di lavoro su GitHub](docs/workflow-github.md): board, issue, branch, commit, pull request
- [Regole generali per il codice](docs/regole-codice.md)
- [Naming](docs/naming.md)
- [Formattazione dei commenti](docs/commenti.md)
- [Documentazione](docs/documentazione.md): cosa documentare e dove
- [Template](docs/template.md)
- [Checklist prima di aprire una pull request](docs/checklist-pr.md)
- [Proposta di schema del database](docs/database/schema.md) (da verificare)
- [Proposta di regolamento](docs/proposte/proposta-regolamento-dreamscape.pdf) (da discutere)
- [Guida ai dati per il frontend](docs/api/guida-frontend.md): quali dati arrivano dal backend, pagina per pagina

Set di carte di prova: [carte/](carte/README.md), con la [presentazione per il team](carte/presentazione-set-carte.pdf) e la [lista degli effetti proposta da Nicolas](carte/effetti/Effetti%20Keyword%20Descrizioni.txt).
