# Revisione delle task e divisione tra i membri

> 🚧 **Proposta per Cristian, 28/10/2026.** Gli assegnatari li mette Cristian a mano: su GitHub non è stato assegnato nessuno. Fonte: le 73 issue della [board](https://github.com/users/cristianpappalardoITS/projects/2).

## In breve

- **73 issue:** 26 di progettazione (#42–#67), 42 di sviluppo (#68–#109) e 5 aggiunte dopo questa revisione (#111–#115).
- **Sprint:** ogni issue ha il suo sprint sulla board.
  - Sprint 1: la #45 e la #47, cioè il lavoro della prima settimana già finito.
  - Sprint 2: le altre 24 di progettazione.
  - Sprint 3–8: le 38 di sviluppo.
  - Le 4 del Backlog non hanno uno sprint.
- **Le issue di progettazione sono da riordinare:**
  - 6 sono già fatte o superate dalle decisioni degli ultimi giorni;
  - 4 si sovrappongono ad altre;
  - non hanno milestone, tranne la #42, né etichette `tipo:` e `priorità:`;
  - quelle di WMD e DGS sono tutte in Todo.
- **Mancavano 5 issue**, ora create (#111–#115): pagine Benvenuto, Dashboard, Profilo e Crediti, lato frontend e lato backend; layout comune del frontend; wireframe delle pagine nuove; username GitHub nel README.
- **SWD:** Cristian e Marco seguono backend e motore di gioco; Nicolas segue regolamento, valori di gioco, catalogo e bilanciamento.
- **Divisione:** dallo Sprint 3 al massimo 2 issue a testa per sprint, come chiede `workflow-github.md` (massimo 2 issue In Progress a testa). Lo Sprint 2 ne ha di più, perché raccoglie tutta la progettazione già in corso: molte si chiudono il 2/11.

---

## 1. Revisione delle issue di progettazione (#42–#67)

### Già fatte o superate

| Issue | Perché | Proposta |
|-------|--------|----------|
| #45 SWD-03 Organizzazione GitHub | Board, colonne, etichette e regole sono pronte | Chiudere (Done) |
| #57 DGS-01 Concept e identità | Il concept è scelto (#63 COM-01: Dreamscape, tema sogni) | Tenere solo per il materiale del 2/11 (concept e logo), poi chiudere |
| #60 DGS-04 Carte e illustrazioni IA di prova | Esiste già il set di prova: 12 carte, 3 full art, cornici e testi di generazione in `carte/` | Cambiare in "Dare il feedback sullo stile del set di prova", da chiudere entro il 2/11 |
| #64 COM-02 Mondi, fazioni e vantaggi | Il regolamento v2 definisce le 3 fazioni, i Lord e il ciclo con +1 attacco | Confermare con DGS e chiudere |
| #67 COM-05 Domande per il cliente | Domande pronte in `docs/presentazione/domande-colloquio.md` | In Progress, poi Done dopo il 2/11 |
| #49 WMD-01 Sitemap | WMD ha già mandato la prima sitemap e ha ricevuto il feedback (`docs/riunioni/feedback-sitemap-portale.pdf`) | In Progress, non Todo: resta da applicare il feedback |

### Sovrapposizioni

| Issue | Si sovrappone a | Proposta |
|-------|-----------------|----------|
| #66 COM-04 Bilanciamento delle carte | #48 SWD-06 Statistiche delle carte | COM-04 diventa solo la riunione in cui si decide; il lavoro resta nella SWD-06. Poi il catalogo va nella #74 DGS-07 e il bilanciamento finale nella #103 DGS-13 |
| #59 DGS-03 Lore e mondi | #64 COM-02 | DGS-03 resta per il racconto e i testi della lore; fazioni e vantaggi sono già decisi |
| #65 COM-03 Nome, logo e identità | #75 DGS-08 Identità definitiva, #50 WMD-02 Direzione grafica | Sono tre passi in fila: COM-03 è la proposta per il 2/11, DGS-08 la versione definitiva dopo la scelta del cliente, WMD-02 come usarla nell'interfaccia |
| #61 DGS-05 Rarità, pacchetti e crediti | Regolamento v2 e `schema.md`, dove rarità e slot dei pacchetti sono già fatti | Resta solo l'economia: come si guadagnano i crediti e i prezzi. È il punto aperto di `schema.md` |

### Da aggiornare

- ✅ **Milestone:** "Primo incontro con il cliente" sulle issue dello Sprint 2, "Presentazione delle prime bozze" sulla #45 e sulla #47.
- ✅ **Etichette:** `tipo: docs` e `priorità:` su tutte e 26; la #42 ha anche `team: COM` e `task-comune`.
- **Titoli con il verbo all'infinito** (`workflow-github.md`), es. `[SWD-02] Progettare il motore di gioco`. Facoltativo, ma rende la board uniforme.
- **#56 WMD-08:** nella descrizione "turni" diventa "round", come nel regolamento.

---

## 2. Issue che mancano

| Issue | Titolo | Sprint | Perché |
|-------|--------|--------|--------|
| #111 COM-10 | Aggiungere gli username GitHub nel README e invitare chi manca | 2 | Lo chiede il brief. Di DGS tra i collaboratori c'è solo `decosm`: mancano due account |
| #112 WMD-21 | Disegnare i wireframe di Amici, Benvenuto, Profilo e backoffice | 3 | Sono pagine nuove della sitemap, senza wireframe |
| #113 WMD-22 | Realizzare il layout comune del frontend | 3 | Menu, intestazione, piè di pagina e stili di base servono a tutte le pagine |
| #114 WMD-23 | Realizzare Benvenuto, Dashboard, Profilo e Crediti | 5 | Pagine obbligatorie dell'area utente, non coperte da nessuna issue |
| #115 SWD-25 | Implementare profilo, cambio password, riepilogo e ricompensa giornaliera | 5 | `/me/welcome`, `/me/summary`, cambio di email e password, movimenti dei crediti. La ricompensa dipende dalla #61 |

---

## 3. Nuova divisione

Criteri:

- **SWD:** Cristian su basi, motore di gioco e integrazione; Marco su dati, accesso, pacchetti, scambi e test. Nicolas su regolamento, valori di gioco, catalogo e bilanciamento, insieme a DGS.
- **WMD:** Gaia (TL) su struttura, layout e qualità; Alessandro, Daniele e Yuri si dividono le aree, e chi ha disegnato il wireframe di una pagina poi la sviluppa.
- **DGS:** Sara (TL) su concept, identità e marketing, Valerio su lore, testi e illustrazioni, Maie su economia e bilanciamento.

Gli sprint sono quelli della board: dallo Sprint 3 in poi le date sono quelle impostate da Cristian.

### Sprint 1 · 19/10 – 25/10 · finito

| Issue | Chi |
|-------|-----|
| #45 SWD-03 Organizzazione GitHub | Cristian (in Review, da chiudere) |
| #47 SWD-05 Entità e database | Marco, Cristian (Done) |

### Sprint 2 · 26/10 – 01/11 · Primo incontro con il cliente

| Issue | Chi |
|-------|-----|
| #42 Presentazione del 2 novembre | Cristian, Marco |
| #43 SWD-01 Regolamento e valori | Nicolas, Marco |
| #44 SWD-02 Progettazione del motore | Cristian |
| #46 SWD-04 Architettura e API | Marco |
| #48 SWD-06 Statistiche delle carte | Nicolas, Marco |
| #49 WMD-01 Sitemap e user journey | Gaia |
| #50 WMD-02 Direzione grafica | Gaia |
| #51 WMD-03 Wireframe home, login, registrazione | Alessandro |
| #52 WMD-04 Wireframe negozio | Daniele (serve per la slide del 2/11) |
| #53 WMD-05 Wireframe collezione | Yuri (serve per la slide del 2/11) |
| #54 WMD-06 Wireframe mazzi | Alessandro |
| #55 WMD-07 Wireframe scambi | Daniele |
| #56 WMD-08 Wireframe sfide e storico | Yuri |
| #57 DGS-01 Concept | Sara |
| #58 DGS-02 Competitor | Valerio |
| #59 DGS-03 Lore | Valerio |
| #60 DGS-04 Feedback sullo stile delle carte | Sara |
| #61 DGS-05 Economia dei crediti | Maie |
| #62 DGS-06 Buyer persona | Sara |
| #63 COM-01 Scelta del concept | Cristian, Marco (Done) |
| #64 COM-02 Fazioni e vantaggi | Valerio, Nicolas (da confermare e chiudere) |
| #65 COM-03 Nome, logo e identità | Sara, Gaia |
| #66 COM-04 Riunione sul bilanciamento | Nicolas, Maie |
| #67 COM-05 Domande per il cliente | Cristian, Marco |
| #111 COM-10 Username GitHub nel README | Cristian |

### Sprint 3 · 02/11 – 08/11

| Issue | Chi |
|-------|-----|
| #68 SWD-07 Progetto Spring Boot con Docker | Cristian |
| #70 SWD-09 Modulo del motore | Cristian |
| #69 SWD-08 Migration e dati finti | Marco |
| #71 SWD-10 Registrazione e accesso JWT | Marco |
| #76 COM-06 Decisioni del colloquio | Nicolas |
| #72 WMD-09 Progetto frontend | Gaia |
| #113 WMD-22 Layout comune | Gaia, Yuri |
| #73 WMD-10 Pagine di registrazione e accesso | Alessandro |
| #112 WMD-21 Wireframe Amici, Benvenuto, Profilo, backoffice | Daniele |
| #74 DGS-07 Catalogo della fase 1 | Maie (con Nicolas) |
| #75 DGS-08 Identità visiva definitiva | Sara |

### Sprint 4 · 09/11 – 15/11

| Issue | Chi |
|-------|-----|
| #77 SWD-11 API del catalogo | Cristian |
| #80 SWD-14 Collezione e mazzi | Cristian |
| #78 SWD-12 Crediti e pacchetti | Marco |
| #79 SWD-13 Round del motore | Marco |
| #81 WMD-11 Componente della carta | Yuri, con il supporto di Gaia |
| #82 WMD-12 Negozio e apertura pacchetti | Daniele |
| #83 WMD-13 Collezione e dettaglio | Alessandro |
| #84 DGS-09 Illustrazioni del catalogo | Valerio, Sara |
| #85 DGS-10 Testi delle pagine pubbliche | Valerio |

### Sprint 5 · 16/11 – 22/11 · SAL il 23/11

| Issue | Chi |
|-------|-----|
| #92 COM-07 Preparazione del SAL | Cristian |
| #87 SWD-16 Simulazioni di punti vita e round | Marco (con Maie) |
| #115 SWD-25 Profilo, password, riepilogo, ricompensa | Marco |
| #86 SWD-15 Effetti nel motore | Cristian |
| #89 WMD-14 Editor dei mazzi | Alessandro |
| #90 WMD-15 Pagine statiche | Daniele |
| #114 WMD-23 Benvenuto, Dashboard, Profilo, Crediti | Yuri |
| #91 DGS-11 Copertine dei pacchetti con i Lord | Valerio |

### Sprint 6 · 23/11 – 29/11

| Issue | Chi |
|-------|-----|
| #94 SWD-19 Sfide, partita e storico | Cristian |
| #93 SWD-18 Amici e scambi | Marco |
| #88 SWD-17 Test di integrazione | Marco (sulla board è nello Sprint 5: conviene spostarla nel 6) |
| #95 SWD-20 API del backoffice | Cristian |
| #96 WMD-16 Amici e Scambi | Daniele |
| #97 WMD-17 Sfide, replay e storico | Yuri |
| #101 WMD-18 Backoffice | Alessandro (sulla board è nello Sprint 7: conviene anticiparla, così parte nel 6 e finisce nel 7) |
| #98 DGS-12 Piano di marketing | Sara |

### Sprint 7 · 30/11 – 05/12

| Issue | Chi |
|-------|-----|
| #99 SWD-21 Swagger e README | Cristian |
| #100 SWD-22 Deploy | Marco |
| #102 WMD-19 Responsive, accessibilità, SEO | Gaia |
| #103 DGS-13 Bilanciamento finale | Maie, Nicolas |
| #104 COM-08 Test finale e correzione dei bug | Un tester per team: Nicolas, Daniele, Yuri, Valerio |

### Sprint 8 · 06/12 – 10/12 · Presentazione finale

| Issue | Chi |
|-------|-----|
| #105 COM-09 Presentazione finale | Cristian, Marco, con Gaia e Sara |

### Backlog · nessuno sprint

| Issue | Chi |
|-------|-----|
| #106 SWD-23 Rank con Elo | Cristian |
| #107 SWD-24 Recupero password via email | Marco |
| #108 WMD-20 Classifica e rank | Yuri |
| #109 DGS-14 Acquisto di crediti | Maie |

---

## 4. Carico per persona

Conta le issue ancora da fare dallo Sprint 2 allo Sprint 8: senza lo Sprint 1, la #63 già chiusa e il Backlog. Una issue condivisa conta per ognuno.

| Persona | Team | Sprint 2 | Sprint 3–8 | Totale | Sprint con più di 2 issue |
|---------|------|----------|------------|--------|---------------------------|
| Cristian | SWD (TL) | 4 | 10 | 14 | 2 |
| Marco | SWD | 5 | 10 | 15 | 2 |
| Nicolas | SWD | 4 | 4 | 8 | 2 |
| Gaia | WMD (TL) | 3 | 5 | 8 | 2 |
| Alessandro | WMD | 2 | 4 | 6 | – |
| Daniele | WMD | 2 | 5 | 7 | – |
| Yuri | WMD | 2 | 5 | 7 | – |
| Sara | DGS (TL) | 4 | 4 | 8 | 2 |
| Valerio | DGS | 3 | 4 | 7 | 2 |
| Maie | DGS | 2 | 3 | 5 | – |

Dallo Sprint 3 nessuno ha più di 2 issue nello stesso sprint. Backend e motore stanno su Cristian e Marco: 10 issue a testa in sei sprint, cioè 2 a sprint quasi sempre. Per stare in questo limite la #88 passa dallo Sprint 5 al 6. Se il carico non regge, la prima da spostare è la #99 (Swagger e README), che si può dividere tra chi ha scritto ogni parte.

## 5. Da chiarire

1. **Account GitHub di DGS:** tra i collaboratori del repository DGS ha un solo account, `decosm` (De Cosmo). `V1n5Fr4n` è un docente, come Shadi Lahham (`shadi-lahham-its`) e Michele Leone (`mLeoneITS`). Gli altri due membri di DGS vanno invitati, altrimenti non si possono assegnare le loro issue.
2. **Modifiche sulla board:** stati, milestone, etichette e le 5 issue nuove sono applicati con `gh` (vedi la sezione 6). Gli assegnatari restano a Cristian.

## 6. Modifiche applicate sulla board il 28/10

| Cosa | Issue |
|------|-------|
| Sprint 1 | #45, #47 |
| Sprint 2 | le altre 24 di progettazione e la #111 |
| Stato Done e issue chiusa | #45 |
| Stato Review | #43 |
| Stato In Progress | #49, #67 |
| Milestone ed etichette `tipo:` e `priorità:` | tutte le 26 di progettazione |
| Issue nuove, in Todo, con sprint e milestone | #111 (Sprint 2), #112 e #113 (Sprint 3), #114 e #115 (Sprint 5) |

Non sono stati cambiati: assegnatari, titoli, descrizioni, e lo sprint della #88 e della #101 (proposti nello Sprint 6).

