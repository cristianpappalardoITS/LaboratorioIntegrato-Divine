# LaboratorioIntegrato-Divine

Progetto Laboratorio Integrato · Gruppo 5

Gioco di carte collezionabili digitale (TCG). Gli utenti si registrano, ricevono crediti virtuali, comprano pacchetti di carte casuali, gestiscono la collezione e i mazzi, scambiano carte con altri utenti e si sfidano in battaglie simulate dal server, con risultato turno per turno e storico delle partite.

> **Stato del concept:** il tema non è ancora definitivo. Le proposte sono **Divine** (mitologia) e **Dreams & Nightmares** (sogni, incubi, ricordi).

## Team

| Team | Membri | Ambito |
|------|--------|--------|
| **SWD** · Software Developer | Cristian (TL), Marco (Vice TL), Nicolas | Motore di gioco, backend, database, API |
| **WMD** · Web Developer | Gaia (TL), Alessandro, Daniele, Yuri | Sitemap, UX/UI, wireframe, frontend |
| **DGS** · Digital Strategist | Sara (TL), Valerio, Maie | Concept, lore, economia di gioco, marketing |

Le decisioni finali dei task comuni (COM-xx) vanno comunicate a **Marco** o **Cristian**, che le registrano in `docs/decisioni/`.

## Stack

| Livello | Tecnologia |
|---------|------------|
| Motore di gioco | Java, modulo isolato, test **JUnit** |
| Backend / portale | Java + **Spring Boot**, Spring Data **JPA** |
| Database | **MySQL** |
| Frontend | 🚧 **Da definire** (scelta del team WMD) |
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
LaboratorioIntegrato-Divine/
├── engine/      # Motore di gioco Java + test JUnit
├── backend/     # Applicazione Spring Boot (portale + API REST)
├── frontend/    # Frontend (tecnologie da definire)
├── database/    # Script SQL, migrazioni, dati di prova
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
