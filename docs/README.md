# Documentazione del progetto

Linee guida e documentazione dettagliata. Per la panoramica del progetto vedi il [README principale](../README.md).

## Linee guida

| Documento | Contenuto |
|-----------|-----------|
| [Flusso di lavoro su GitHub](workflow-github.md) | Board di GitHub Projects, issue, etichette, branch, commit, pull request |
| [Regole generali per il codice](regole-codice.md) | Lingua, formattazione, motore di gioco, backend, database, frontend, sicurezza, test |
| [Naming](naming.md) | Nomi per Java, database, API REST, frontend, file di documentazione |
| [Formattazione dei commenti](commenti.md) | Quando commentare, Javadoc, etichette `TODO`/`FIXME`, commenti in altri linguaggi |
| [Documentazione](documentazione.md) | Cosa documentare, dove e chi lo aggiorna |
| [Template](template.md) | Issue, bug, pull request, commit, classi Java, test, decisioni, verbali, `.editorconfig` |
| [Checklist PR](checklist-pr.md) | Controlli da fare prima di aprire una pull request |

## Progettazione

| Documento | Contenuto |
|-----------|-----------|
| [Proposta di schema del database](database/schema.md) | **Da verificare.** Tabelle, diagrammi ER, scelte, regole dei service, migration Flyway |
| [schema.sql](database/schema.sql) | SQL completo dello schema, diviso nelle future migration |
| [Guida ai dati per il frontend](api/guida-frontend.md) | Per il team WMD: API, dati in ingresso e in uscita, accesso con JWT, pagina per pagina |

## Proposte da discutere

| Documento | Contenuto |
|-----------|-----------|
| [Proposta di regolamento](proposte/proposta-regolamento-dreamscape.pdf) (PDF) | Regolamento di Dreamscape: modalità Base con effetti, mazzo, rarità, carte iniziali, amici e scambi, rank, punti da valutare |

## Materiale del gioco

| Documento | Contenuto |
|-----------|-----------|
| [Set di carte di prova](../carte/README.md) | 12 carte e 3 full art, cornici, illustrazioni, script che compone le carte |
| [Lista degli effetti](../carte/effetti/Effetti%20Keyword%20Descrizioni.txt) | Proposta di Nicolas: keyword degli effetti, descrizioni e fazione consigliata |
| [Presentazione del set di carte](../carte/presentazione-set-carte.pdf) (PDF) | Scelte visive, come sono fatte le carte, tutte le carte create |

## Altre cartelle

| Cartella | Contenuto |
|----------|-----------|
| `decisioni/` | Decisioni prese dal gruppo, una per file (`NNN-titolo-breve.md`) |
| `verbali/` | Verbali delle riunioni (`AAAA-MM-GG-argomento.md`) |
| `api/` | Elenco degli endpoint REST (la guida per il frontend c'è già) |
| `diagrammi/` | Diagramma ER, architettura, flussi |

Queste cartelle si creano quando serve il primo documento.
