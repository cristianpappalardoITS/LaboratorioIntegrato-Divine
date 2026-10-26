# Testi per le illustrazioni full art (solo Leggendarie)

Versione alternativa delle tre Leggendarie: **stesso personaggio, scena diversa**, illustrazione su tutta la carta. Nome, simbolo, testi, attacco e difesa vanno su pannelli scuri semitrasparenti che aggiunge lo script.

## Come si usa

1. Apri una **chat nuova** nel generatore di immagini e incolla il **messaggio iniziale**.
2. Per ogni carta **allega l'illustrazione base** del personaggio (indicata sotto) e incolla il testo della carta.
3. Salva l'immagine con il nome indicato in `carte/illustrazioni/`.
4. Lo script la riconosce dal nome (`-fullart`) e crea la carta `..._FULLART.png`, senza toccare la versione normale.

Se l'immagine non è verticale o ha scritte: *"Rigenera in verticale 2:3, solo illustrazione, senza testi né cornici."*
Se il personaggio è diverso dall'originale: *"Il personaggio deve essere identico a quello dell'immagine allegata: stesso aspetto, colori e dettagli. Cambia solo la scena."*

---

## Messaggio iniziale

```
Sei l'illustratore di "Dreamscape", un gioco di carte collezionabili digitale. Sogni, paure e ricordi diventano creature che vivono nel Dreamscape, un mondo onirico e instabile.

Devi creare le versioni FULL ART delle carte leggendarie. Per ogni carta ti allego l'illustrazione originale del personaggio e ti descrivo una scena nuova.

REGOLE
- Il personaggio deve essere IDENTICO a quello dell'immagine allegata: stesso aspetto, stessi colori, stessi dettagli. Cambia solo cosa sta facendo e la scena intorno.
- Genera SOLO l'illustrazione: niente cornice, niente testi, niente lettere, niente numeri, niente simboli o icone.
- Formato VERTICALE 2:3. L'illustrazione occuperà tutta la carta.
- Il personaggio deve stare nella fascia centrale dell'immagine, tra il 10% e il 65% dell'altezza, intero e ben visibile.
- La fascia in alto (circa il 10%) e la parte bassa (circa il 35%) verranno coperte da riquadri di testo semitrasparenti: lì metti solo sfondo, cielo, nebbia, luce o paesaggio, senza dettagli importanti.
- Scena monumentale ed epica, molto dettagliata, luce cinematografica, con un'aura luminosa intorno al personaggio.
- Mantieni lo stile e la palette della fazione:
  - DREAMS: luminosa ed eterea, blu notte, azzurro e argento, luce lunare.
  - NIGHTMARES: gotica e spaventosa, sfondi quasi neri, viola scurissimo, rosso cremisi spento, luce fredda. Senza sangue né violenza esplicita.
  - MEMORIES: nostalgica, seppia e ambra con riflessi viola, polvere sospesa nella luce, orologi e fotografie.

Genera una sola immagine per messaggio. A questo messaggio rispondi solo "Pronto".
```

---

## Le carte

```
FULL ART · Il Sogno Lucido
Fazione: Dreams · Rarità: Leggendaria
Descrizione: "Sai di sognare, e il sogno ti obbedisce."
Scena: il personaggio, sospeso nel vuoto cosmico, crea con le mani una galassia a spirale che nasce tra i suoi palmi; intorno a lui stelle, pianeti e isole fluttuanti prendono forma dal nulla seguendo i suoi gesti.
```
Allega: `carte/illustrazioni/base-004.png` · Salva come: `base-004-fullart.png`

```
FULL ART · L'Uomo Senza Volto
Fazione: Nightmares · Rarità: Leggendaria
Descrizione: "La paura dell'ignoto ha un corpo, ma non un viso."
Scena: il personaggio, altissimo, si erge sulla cima di una cattedrale gotica in rovina sotto una luna pallida enorme; dalle sue braccia allungate si diramano ombre che avvolgono la città addormentata sottostante, mentre stormi di corvi gli girano intorno. Il cilindro è interamente visibile.
```
Allega: `carte/illustrazioni/base-008.png` · Salva come: `base-008-fullart.png`

```
FULL ART · La Custode del Tempo Fermo
Fazione: Memories · Rarità: Leggendaria
Descrizione: "Custodisce l'attimo che non vuoi lasciare andare."
Scena: il personaggio, al centro di una gigantesca clessidra di vetro, ferma con le mani la sabbia dorata che cade; dentro i granelli sospesi si vedono frammenti di ricordi, mentre ingranaggi e lancette enormi ruotano lentamente sullo sfondo.
```
Allega: `carte/illustrazioni/base-012.png` · Salva come: `base-012-fullart.png`
