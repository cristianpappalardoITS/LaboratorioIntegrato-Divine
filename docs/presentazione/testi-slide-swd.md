# Colloquio con il cliente · Testi delle slide

Primo incontro con il cliente: **lunedì 2 novembre 2026**. 10 minuti di presentazione, poi circa 5 minuti di domande.

Presentano **Cristian** e **Marco**. Le slide di Digital (DGS) e WebDev (WMD) arrivano dai team e si montano nei blocchi B e D. Per ogni slide c'è cosa scrivere (poche parole) e cosa dire a voce.

> Regola per tutte le slide: poche parole e immagini grandi. Quello che serve spiegare si dice a voce, non si legge.

## Scaletta

| Blocco | Tempo | Durata | Contenuto | Chi presenta | Slide |
|--------|-------|--------|-----------|--------------|-------|
| A | 0:00–1:30 | 1:30 | Chi siamo e richieste del cliente | Cristian | 1–3 |
| B | 1:30–4:00 | 2:30 | Concept, target, mercato e competitor, visual | Cristian (slide DGS) | 4–8 |
| C | 4:00–6:00 | 2:00 | Lore, mini set di carte, regolamento | Marco | 9–12 |
| D | 6:00–8:00 | 2:00 | Proposta tecnica: funzionalità, backend, frontend | Marco (+ slide WMD) | 13–16 |
| E | 8:00–9:30 | 1:30 | Metodo di lavoro, board, roadmap | Cristian | 17–19 |
| F | 9:30–10:00 | 0:30 | Cosa chiediamo al cliente, chiusura | Marco | 20 |
| | 10:00–15:00 | 5:00 | Domande del cliente | Entrambi | Slide di riserva |

Cambi di voce: tre (A-B Cristian → C-D Marco → E Cristian → F Marco). Chi passa la parola lo dice con una frase, es. "Ora Marco vi mostra come si gioca".

---

## Blocco A · Chi siamo e richieste (Cristian, 1:30)

### Slide 1 · Titolo (10 s)

**Sulla slide:** logo e nome del gioco **Dreamscape**, "una proposta di **Somnia**", data.

**A voce:** "Buongiorno, siamo Somnia e oggi vi presentiamo Dreamscape, il gioco di carte collezionabili che vorremmo costruire per voi."

### Slide 2 · Chi siamo (40 s)

**Sulla slide:** Somnia, startup di 10 persone in tre team, con foto o iniziali e ruolo:

| Team | Persone | Cosa fa |
|------|---------|---------|
| Software Development | Cristian (TL), Marco (Vice TL), Nicolas | Motore di gioco, backend, database |
| Web Development | Gaia (TL), Alessandro, Daniele, Yuri | Portale, interfaccia, frontend |
| Digital Strategy | Sara (TL), Valerio, Maie | Concept, lore, identità visiva, economia di gioco |

**A voce:** il nome Somnia (dal latino "sogni") e perché tre competenze diverse lavorano allo stesso prodotto. Un team leader per team, un'unica board di lavoro.

### Slide 3 · Cosa ci avete chiesto (40 s)

**Sulla slide:** le richieste del brief in 6 icone:

1. Registrazione, crediti virtuali e pacchetti di carte casuali
2. Collezione e più mazzi, con regole di composizione
3. Scambi di carte, solo se l'altro accetta
4. Sfide tra giocatori, simulate dal server, con risultato round per round e storico
5. Creature con attacco, difesa e fazione; fazioni con vantaggi reciproci
6. Backoffice per gestire carte e pacchetti

In piccolo: "Fuori dalla fase 1: acquisto di crediti con denaro reale".

**A voce:** "Abbiamo coperto tutte le richieste obbligatorie e ne aggiungiamo alcune: le vedrete nella proposta tecnica."

---

## Blocco B · Concept e visual (Cristian, 2:30)

Slide preparate da **DGS** (3–4 slide più il visual). Ordine suggerito:

| Slide | Contenuto |
|-------|-----------|
| 4 | Il concept: perché i sogni, l'idea in una frase |
| 5 | Target: chi gioca, età, abitudini, dispositivi |
| 6 | Mercato e competitor: 3–4 giochi a confronto e cosa ci distingue |
| 7 | Identità visiva, proposta 1: logo, naming, palette, caratteri |
| 8 | Identità visiva, proposta 2 (se c'è) |

Il brief chiede **una o più proposte** di visual: con due proposte il cliente può scegliere, ed è un feedback in più.

Entro mercoledì 28/10 alle 20, insieme alle slide, DGS manda a Cristian cosa dire su ogni slide (note del relatore). La prova è giovedì 29/10.

---

## Blocco C · Il gioco (Marco, 2:00)

### Slide 9 · Il mondo di Dreamscape (30 s)

**Sulla slide:** le tre fazioni con simbolo e Lord, e il ciclo dei vantaggi:

| Fazione | Identità | Simbolo | Lord |
|---------|----------|---------|------|
| Dreams | Speranza, desiderio, protezione | Luna | Il Sogno Lucido |
| Nightmares | Paura, oscurità, perdita di controllo | Occhio | L'Uomo Senza Volto |
| Memories | Ricordi, nostalgia, déjà-vu | Clessidra | La Custode del Tempo Fermo |

Ciclo: Dreams → Memories → Nightmares → Dreams.

**A voce:** "Desideri, ricordi e paure lasciano tracce nell'inconscio, e nel sonno diventano creature. Il giocatore è un Dreamweaver: le colleziona e le porta in battaglia. Ogni fazione ha un Lord, la sua carta più iconica, che è anche la copertina dei pacchetti."

### Slide 10 · Il mini set di carte (30 s)

**Sulla slide:** le 12 carte di prova in griglia (4 rarità × 3 fazioni) e una full art in grande (da `carte/carte-finali/`).

**A voce:** quattro rarità riconoscibili dalla cornice; le Leggendarie hanno una versione full art rara. Illustrazioni generate con l'AI, come chiede il brief, con i loro metadati originali.

### Slide 11 · Le regole in breve (35 s)

**Sulla slide:**

- Mazzo di 20 carte, massimo 2 copie (1 per le Leggendarie)
- Limiti per rarità: Leggendarie 2, Epiche 4, Rare 8
- 20 punti vita, +1 attacco contro la fazione debole
- 23 effetti (Protezione, Castigo, Miasma...)
- Fine: punti vita a 0, mazzo esaurito o 60 round (pareggio)

**A voce:** "La strategia sta nella costruzione del mazzo: la partita la simula il server in un istante e il giocatore la rivede round per round."

### Slide 12 · Un round d'esempio (25 s)

**Sulla slide:** il round 3 dell'esempio del regolamento: il Faro nella Nebbia (4/7) contro l'Uomo Senza Volto (8/5). Indebolimento porta il Faro a 2 di attacco, l'Uomo attacca con 9 grazie al vantaggio di fazione, il Faro muore e il giocatore A perde 9 − 7 = 2 punti vita.

**A voce:** segui le frecce sulla slide, senza leggere i numeri uno per uno.

---

## Blocco D · Proposta tecnica (Marco, 2:00)

### Slide 13 · Funzionalità (35 s)

**Sulla slide:** due colonne.

| Richieste dal brief | In più, proposte da Somnia |
|---------------------|----------------------------|
| Registrazione e accesso | Lista amici: si scambia solo con gli amici, in quantità libere |
| Crediti e pacchetti casuali | Effetti delle carte già nella modalità Base |
| Collezione e mazzi | Lord di fazione e copertine dei pacchetti a scelta |
| Scambi | Full art come copia rara da collezionare |
| Sfide, risultato round per round, storico | Set iniziale e pacchetti di benvenuto |
| Backoffice | Rank con leghe a tema (dopo le funzionalità obbligatorie) |

**A voce:** "Prima le funzionalità obbligatorie; il rank arriva solo quando tutto il resto funziona."

### Slide 14 · Architettura (40 s)

**Sulla slide:** schema a blocchi: Browser (HTML, CSS, JS) → API REST con JWT → Spring Boot 4 → PostgreSQL 18, con il **motore di gioco** come modulo Java separato. Tutto in Docker.

**A voce, i perché in una frase ciascuno:**

- **Motore separato e ripetibile:** con lo stesso seed rigioca la stessa partita. Lo usiamo per i test e per simulare migliaia di partite e bilanciare le regole (così abbiamo scelto i 60 round).
- **Tutto lato server:** estrazione dei pacchetti, partite e scambi. Il giocatore non può barare dal browser.
- **PostgreSQL con transazioni:** in uno scambio o in un acquisto nessuna carta e nessun credito si perde o si duplica.
- **Sicurezza:** password cifrate, accesso con token JWT, nessun pagamento reale in fase 1.

### Slides 15–16 · Frontend (45 s)

Slide preparate da **WMD**: tecnologie scelte (HTML, CSS, JavaScript, responsive, SEO) e due wireframe, es. collezione e negozio. Marco le presenta con le note di WMD.

Frase di collegamento: "Il backend manda solo i dati: la carta la monta il browser, quindi se cambiamo una statistica tutte le carte si aggiornano da sole."

---

## Blocco E · Come lavoriamo (Cristian, 1:30)

### Slide 17 · Metodo di lavoro (30 s)

**Sulla slide:**

- Metodo agile con board Kanban su GitHub Projects: Backlog → To Do → In Progress → Review → Done
- Ogni attività è una issue con responsabile, team e priorità
- Un branch per issue, pull request con revisione di un'altra persona
- Linee guida comuni nel repository (naming, commenti, commit)
- Punto di controllo settimanale tra i team leader

### Slide 18 · La board (30 s)

**Sulla slide:** screenshot della board di GitHub Projects con le colonne piene e i filtri per team. In un angolo: numero di issue per team.

**A voce:** "Ogni persona sa cosa deve fare e per quando; il cliente può seguire l'avanzamento."

> Prima della presentazione: controllare che la board sia **popolata e completa** (lo chiede il brief) e fare lo screenshot il giorno prima.

### Slide 19 · Roadmap (30 s)

**Sulla slide:** gli sprint di una settimana, gli stessi della board.

| Sprint | Date | Obiettivo |
|--------|------|-----------|
| 1–2 | 19/10 – 01/11 | Fondamenta: concept, regolamento, carte di prova, linee guida, database, sitemap |
| 3 | 02/11 – 08/11 | Basi: progetti backend e frontend, migration, accesso, motore di gioco, catalogo e identità visiva definitivi |
| 4 | 09/11 – 15/11 | Catalogo, pacchetti, collezione, mazzi, componente della carta |
| 5 | 16/11 – 22/11 | Effetti, simulazioni, test, editor dei mazzi; **SAL il 23/11** |
| 6 | 23/11 – 29/11 | Amici e scambi, sfide e storico, API del backoffice |
| 7 | 30/11 – 05/12 | Backoffice, Swagger, deploy, rifinitura, test finale |
| 8 | 06/12 – 08/12 | Prove e demo; **presentazione finale il 10/12** |
| Backlog | dopo | Rank, recupero password via email, acquisto di crediti |

**A voce:** "Lavoriamo a sprint di una settimana, gli stessi della board. Le funzionalità obbligatorie prima di tutto il resto: se siamo in ritardo, si sposta il rank, non i requisiti."

> Le issue di ogni sprint sono sulla board (#68–#109), con le etichette e le milestone del SAL e della presentazione finale.

---

## Blocco F · Chiusura (Marco, 0:30)

### Slide 20 · Cosa vi chiediamo oggi

**Sulla slide:** tre domande al cliente, scelte da [domande-colloquio.md](domande-colloquio.md), es.:

1. Quale proposta di visual preferite?
2. Partite più lunghe e tattiche (20 punti vita) o più rapide (10 punti vita)?
3. Il rank vi interessa già alla consegna, o va bene dopo?

**A voce:** "Le vostre risposte ci servono per partire con lo sviluppo. Grazie: ora siamo a disposizione per le vostre domande."

---

## Slide di riserva (dopo la 20, solo per le domande)

- Regolamento completo: le 3 fasi del round e la tabella degli effetti
- Database: diagramma delle tabelle
- Simulazione dei punti vita (tabella della sezione 10 del regolamento)
- Pagine del portale (sitemap di WMD)
- Costi di hosting (proposta AWS, se è pronta)

Il driver le tiene pronte e le apre solo se arriva la domanda giusta.
