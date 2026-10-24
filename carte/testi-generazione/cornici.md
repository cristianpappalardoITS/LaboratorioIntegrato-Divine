# Testi per rigenerare le cornici

Servono **12 cornici vuote**: 3 fazioni × 4 rarità, già nei colori della fazione, nitide e con la stessa disposizione delle zone. Nome, simbolo di fazione, testi, attacco e difesa li aggiunge lo script.

## Come si usa

1. Apri una **chat nuova** nel generatore di immagini.
2. Allega una cornice esistente come riferimento per la disposizione (per esempio `carte/cornici/cornice_nightmares_comune.png`) e incolla il **messaggio iniziale**.
3. Chiedi le cornici **una alla volta**, nell'ordine della tabella in fondo. Parti dalla **Comune** di ogni fazione: quando ti piace, usala come base per Rara, Epica e Leggendaria della stessa fazione, così le zone restano nella stessa posizione.
4. Salva ogni cornice con il nome indicato nella cartella `carte/cornici/`.

### Se qualcosa non va

| Problema | Cosa scrivere |
|----------|---------------|
| La finestra non è verde pieno | *"Riempi la finestra dell'illustrazione di verde puro #00FF00 uniforme, senza sfumature né riflessi."* |
| Il cerchio è ovale | *"Il cerchio in alto a destra deve essere perfettamente rotondo, non ovale."* |
| Ci sono scritte o numeri | *"Rigenera senza nessuna scritta, lettera o numero."* |
| Le zone sono in posizioni diverse dalla Comune | *"Usa la cornice Comune che ti ho mandato come base: stessa posizione e dimensione di tutte le zone, cambia solo le decorazioni."* |
| La Leggendaria è più stretta | *"La cornice deve essere larga quanto la Comune: finestra e riquadro del testo della stessa larghezza. I cristalli vanno sopra il bordo, non lo restringono."* |
| L'immagine è sfocata | *"Rigenera con linee più nitide e definite, senza sfocature."* |

---

## Messaggio iniziale

```
Devi disegnare le cornici vuote di "Dreams & Nightmares", un gioco di carte collezionabili digitale. Ti allego una cornice di riferimento: usala SOLO per la disposizione delle zone (posizioni e proporzioni), non per colori e decorazioni.

Mi servono 12 cornici: 3 fazioni × 4 rarità. Le genereremo una alla volta.

REGOLE VALIDE PER TUTTE LE CORNICI

Formato e qualità
- Verticale, proporzioni 2:3, alla massima risoluzione possibile.
- Linee nitide e pulite: niente sfocature, niente rumore, niente effetto pittorico sfumato sulla cornice.
- Perfettamente simmetrica tra sinistra e destra.
- Vista frontale e piatta: niente prospettiva, niente ombre esterne, niente mani o oggetti intorno.
- La cornice occupa tutta la carta fino ai bordi, con angoli arrotondati; fuori dagli angoli, sfondo nero uniforme.
- Nessun testo, nessuna lettera, nessun numero, nessun logo.

Disposizione (identica in tutte le 12 cornici, come nel riferimento)
1. In alto a sinistra e al centro: targhetta orizzontale per il nome, color pergamena chiara, vuota.
2. In alto a destra: un cerchio PERFETTAMENTE ROTONDO (non ovale), con l'interno nero uniforme e vuoto, senza simboli.
3. Al centro, nella parte alta: grande finestra per l'illustrazione, rettangolare con angoli arrotondati, riempita di VERDE PURO UNIFORME (#00FF00), senza sfumature, texture, riflessi o bagliori sopra. Le decorazioni della cornice possono sporgere leggermente sopra il bordo della finestra.
4. Sotto la finestra: riquadro del testo color pergamena chiara, uniforme e vuoto, senza righe o decorazioni all'interno.
5. In basso a sinistra: riquadro scuro per l'attacco, con una piccola spada sul lato sinistro e lo spazio a destra vuoto per il numero.
6. In basso a destra: riquadro scuro per la difesa, con un piccolo scudo sul lato sinistro e lo spazio a destra vuoto per il numero.
Le zone devono avere esattamente la stessa posizione e la stessa dimensione in tutte le cornici: cambiano solo materiali, colori e decorazioni.

COLORI PER FAZIONE (metallo della cornice)
- DREAMS: argento lucido con riflessi azzurri e blu notte; gemme di zaffiro azzurro.
- NIGHTMARES: ferro brunito quasi nero con accenti rosso cremisi spento; decorazioni gotiche appuntite; gemme di rubino scuro.
- MEMORIES: bronzo antico e oro ambrato con una leggera patina; gemme di topazio color ambra.

RARITÀ (quantità di decorazioni, a parità di forma)
- COMUNE: cornice semplice e pulita, profili lisci.
- RARA: incisioni ornamentali e piccoli fregi agli angoli.
- EPICA: fregi più ricchi e tre gemme nel colore della fazione (una in alto al centro e una per lato all'altezza della finestra), con un leggero bagliore.
- LEGGENDARIA: cristalli e schegge iridescenti nei colori della fazione lungo i bordi, una gemma grande in alto e una in basso, aura luminosa. ATTENZIONE: deve restare larga quanto le altre, con finestra e riquadro del testo della stessa larghezza; i cristalli si aggiungono sopra il bordo, non lo restringono.

Quando ti chiedo una cornice, generane una sola.

A questo messaggio rispondi solo "Pronto".
```

---

## Le 12 cornici

Per la prima cornice di ogni fazione:

```
Genera la cornice: [FAZIONE] · Comune.
```

Per le altre rarità della stessa fazione:

```
Genera la cornice: [FAZIONE] · [RARITÀ]. Usa come base la cornice Comune di questa fazione appena generata: stessa identica posizione e dimensione di targhetta, cerchio, finestra verde, riquadro del testo e riquadri di attacco e difesa. Aggiungi solo le decorazioni della rarità.
```

| Ordine | Fazione | Rarità | Salva come |
|--------|---------|--------|------------|
| 1 | Dreams | Comune | `cornice_dreams_comune.png` |
| 2 | Dreams | Rara | `cornice_dreams_rara.png` |
| 3 | Dreams | Epica | `cornice_dreams_epica.png` |
| 4 | Dreams | Leggendaria | `cornice_dreams_leggendaria.png` |
| 5 | Nightmares | Comune | `cornice_nightmares_comune.png` |
| 6 | Nightmares | Rara | `cornice_nightmares_rara.png` |
| 7 | Nightmares | Epica | `cornice_nightmares_epica.png` |
| 8 | Nightmares | Leggendaria | `cornice_nightmares_leggendaria.png` |
| 9 | Memories | Comune | `cornice_memories_comune.png` |
| 10 | Memories | Rara | `cornice_memories_rara.png` |
| 11 | Memories | Epica | `cornice_memories_epica.png` |
| 12 | Memories | Leggendaria | `cornice_memories_leggendaria.png` |
