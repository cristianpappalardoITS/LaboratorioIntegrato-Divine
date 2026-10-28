# Testi per generare le illustrazioni

Una sola illustrazione per carta. Cornice, nome, testi, simbolo di fazione, attacco e difesa li aggiunge lo script di composizione.

Carte già fatte, da non rigenerare:
Tutte le 12 illustrazioni del set sono già in `carte/illustrazioni/`. Questi testi servono per rigenerarne una o per crearne di nuove con lo stesso stile. Le versioni scartate sono in `carte/illustrazioni/alternative/`.

## Come si usa

1. Apri una **chat nuova** nel generatore di immagini e incolla il **messaggio iniziale**. Deve rispondere "Pronto".
2. Incolla **una carta alla volta**: per ogni carta arriva una sola immagine.
3. Scarica l'immagine e **rinominala** come indicato ("Salva come").
4. Mettila nella cartella `carte/illustrazioni/`.

Se l'immagine ha scritte, cornici o non è orizzontale, rispondi: *"Rigenera rispettando il formato: solo illustrazione, orizzontale 3:2, senza testi né cornici."*

Se dopo molte carte lo stile cambia, apri una chat nuova e incolla di nuovo il messaggio iniziale.

---

## Messaggio iniziale

```
Sei l'illustratore di "Dreamscape", un gioco di carte collezionabili digitale. Sogni, paure e ricordi diventano creature che vivono nel Dreamscape, un mondo onirico e instabile. Payoff del gioco: "Every dream has a dark side".

Ti chiederò di generare le illustrazioni delle carte: UNA SOLA IMMAGINE per ogni messaggio. Rispetta sempre queste regole.

FORMATO
- Genera SOLO l'illustrazione: niente cornice, niente testi, niente lettere, niente numeri, niente simboli o icone.
- Formato ORIZZONTALE 3:2.
- Soggetto principale al centro e intero (testa compresa), con un po' di spazio sopra e sotto.
- Tieni le parti importanti lontane dai bordi destro e sinistro: verranno tagliati leggermente.
- Lo sfondo riempie tutta l'immagine, senza bordi, cornici o vignettature.

STILE GENERALE
Surrealismo onirico: architetture impossibili, nebbie, dimensioni sospese, creature simboliche. Illustrazione digitale dipinta, molto dettagliata, luce cinematografica. Il soggetto è sempre una creatura o una figura surreale, non una persona realistica.

FAZIONI
- DREAMS (speranza, desiderio, creatività, protezione): luminosa ed eterea. Blu notte, azzurro e argento, luce lunare, nuvole, bagliori morbidi. Creature rassicuranti e protettive.
- NIGHTMARES (paura, oscurità, perdita di controllo): gotica e spaventosa. Sfondi quasi neri, viola scurissimo, accenti rosso cremisi spento, luce fredda e pallida. Niente lilla o lavanda chiari. Figure allungate e distorte, texture graffiate, architetture gotiche in rovina, nebbia fredda. Deve inquietare come un vero incubo, ma senza sangue, ferite o violenza esplicita.
- MEMORIES (ricordi, nostalgia, déjà-vu, illusioni): nostalgica e malinconica. Seppia e ambra con riflessi viola, grana da vecchia pellicola, fotografie sbiadite, orologi, polvere sospesa nella luce, illusioni ottiche e prospettive impossibili.

RARITÀ (quanto è spettacolare la scena)
- Comune: scena semplice, un solo soggetto, atmosfera tranquilla.
- Rara: più dettagli e profondità.
- Epica: scena drammatica, luce magica intensa.
- Leggendaria: scena monumentale ed epica, soggetto imponente circondato da un'aura luminosa.

Per ogni carta ti darò nome, fazione, rarità, descrizione, effetto (solo come ispirazione: non va scritto) e la composizione da disegnare.

A questo messaggio rispondi solo "Pronto".
```

---

## Le carte

### Dreams

```
CARTA 2 · Il Volo Sopra la Città
Fazione: Dreams · Rarità: Rara
Descrizione: "Per una notte, la gravità smette di contare."
Effetto: "Slancio onirico 1: +1 attacco finché resta in campo."
Composizione: una balena celeste trasparente, piena di stelle, che nuota nel cielo notturno sopra i tetti di una città addormentata, con le luci delle finestre riflesse sulla sua pelle.
```
Salva come: `base-002.png`

```
CARTA 3 · Il Faro nella Nebbia
Fazione: Dreams · Rarità: Epica
Descrizione: "Una luce lontana che indica sempre la strada di casa."
Effetto: "Riposo 1: a fine round recupera 1 difesa."
Composizione: un faro di cristallo sospeso nel vuoto su un'isola fluttuante, il cui fascio di luce taglia la nebbia, circondato da lucciole che guidano piccole barche di carta su un mare di nuvole.
```
Salva come: `base-003.png`

```
CARTA 4 · Il Sogno Lucido
Fazione: Dreams · Rarità: Leggendaria
Descrizione: "Sai di sognare, e il sogno ti obbedisce."
Effetto: "Mente lucida: il vantaggio di fazione avversario non si applica contro di lei."
Composizione: un essere fatto di costellazioni, seduto a gambe incrociate sopra una luna crescente, con un terzo occhio d'argento aperto sulla fronte e il paesaggio onirico che si piega intorno a lui.
```
Salva come: `base-004.png`

### Nightmares

```
CARTA 5 · Il Dente Che Cade
Fazione: Nightmares · Rarità: Comune
Descrizione: "Un incubo piccolo, ma che ritorna sempre."
Effetto: "Ultimo grido 1: quando muore, 1 danno al giocatore avversario."
Composizione: una creaturina gotica magra e scheletrica, con occhi bianchi luminosi e un sorriso sdentato, che trascina un enorme dente incrinato lungo un corridoio buio.
```
Salva come: `base-005.png`

```
CARTA 6 · La Caduta Senza Fine
Fazione: Nightmares · Rarità: Rara
Descrizione: "La sensazione di perdere il controllo, senza mai toccare terra."
Effetto: "Disperazione 2: +2 attacco quando la sua difesa è scesa alla metà o meno."
Composizione: una creatura fatta d'ombra che precipita in un pozzo infinito di scale gotiche a spirale, mentre mani nere si allungano dalle pareti verso di lei.
```
Salva come: `base-006.png`

```
CARTA 7 · La Stanza Senza Porte
Fazione: Nightmares · Rarità: Epica
Descrizione: "Quattro muri, nessuna uscita, e il respiro che accelera."
Effetto: "Insonnia 1: a fine round il giocatore avversario perde 1 punto vita."
Composizione: una creatura fatta di mattoni e carta da parati strappata, con una porta murata al posto della bocca, in una stanza vittoriana senza uscite illuminata da candele spente.
```
Salva come: `base-007.png`

```
CARTA 8 · L'Uomo Senza Volto
Fazione: Nightmares · Rarità: Leggendaria
Descrizione: "La paura dell'ignoto ha un corpo, ma non un viso."
Effetto: "Paralisi notturna 2: quando entra, la creatura avversaria perde 2 attacco."
Composizione: una figura altissima senza volto, in abito vittoriano nero e cilindro, che emerge da uno specchio gotico incrinato allungando una mano scheletrica, circondata da corvi e nebbia fredda. Il volto è completamente liscio e vuoto. Il cilindro deve essere interamente visibile.
```
Salva come: `base-008.png`

### Memories

```
CARTA 9 · Il Ricordo Sbiadito
Fazione: Memories · Rarità: Comune
Descrizione: "Il timore di dimenticare ciò che contava."
Effetto: "Ricordo dolce 2: quando muore, il proprio giocatore recupera 2 punti vita."
Composizione: una creatura semitrasparente fatta di vecchie fotografie che stanno sbiadendo, seduta su una panchina in un parco color seppia, mentre alcune foto si staccano dal suo corpo e volano via.
```
Salva come: `base-009.png`

```
CARTA 11 · Il Corridoio Infinito
Fazione: Memories · Rarità: Epica
Descrizione: "Smarrimento e incertezza, porta dopo porta."
Effetto: "Sogno ricorrente: quando muore torna in fondo al mazzo (una volta per partita)."
Composizione: una figura eterea con una lanterna che cammina in un corridoio senza fine, le cui pareti sono fatte di cornici dorate con vecchie foto in bianco e nero; alcune foto volano sul pavimento a scacchi.
```
Salva come: `base-011.png`

```
CARTA 12 · La Custode del Tempo Fermo
Fazione: Memories · Rarità: Leggendaria
Descrizione: "Custodisce l'attimo che non vuoi lasciare andare."
Effetto: "Eredità 2: quando muore, la prossima creatura pescata ha +2 difesa."
Composizione: una figura maestosa e surreale vestita di lancette e ingranaggi, con centinaia di orologi fermi che fluttuano intorno a lei in una luce dorata.
```
Salva come: `base-012.png`
