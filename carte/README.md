# Carte · set di prova

Set di prova delle carte di **Dreamscape**: 12 carte (3 fazioni × 4 rarità) e 3 versioni full art delle Leggendarie, che sono anche i Lord delle fazioni.

> 🚧 **Proposta da discutere.** Nomi e statistiche sono esempi. Gli effetti stampati sulle carte vengono dal primo catalogo: la proposta di regolamento indica con quale effetto della [lista di Nicolas](effetti/Effetti%20Keyword%20Descrizioni.txt) sostituirli.

La presentazione per il team, con le scelte fatte e tutte le carte, è in [presentazione-set-carte.pdf](presentazione-set-carte.pdf).

## Struttura

```
carte/
├── presentazione-set-carte.pdf   # presentazione per il team
├── carte-finali/                 # le carte finite (generate dallo script)
├── illustrazioni/                # illustrazioni usate nel set
│   └── alternative/              # illustrazioni scartate, conservate per confronto
├── cornici/                      # 12 cornici: cornice_<fazione>_<rarita>.png
├── compositore/                  # script che compone le carte + dati delle carte (carte.csv)
├── testi-generazione/            # testi per generare illustrazioni, cornici e full art
└── effetti/                      # lista degli effetti proposta da Nicolas
```

## Come si rigenerano le carte

```bash
cd carte/compositore
python3 -m pip install -r requirements.txt
python3 componi_carte.py --sovrascrivi
```

Dettagli in [compositore/README.md](compositore/README.md).

## Come si aggiunge una carta

1. Aggiungi una riga in `compositore/carte.csv` (codice, nome, fazione, rarità, attacco, difesa, descrizione, effetto, file dell'illustrazione).
2. Genera l'illustrazione con i testi di [testi-generazione/illustrazioni.md](testi-generazione/illustrazioni.md) e salvala in `illustrazioni/` con il nome indicato nel CSV.
3. Lancia lo script: la carta compare in `carte-finali/`.

## Le carte del set

| Codice | Nome | Fazione | Rarità | ATT | DIF |
|--------|------|---------|--------|-----|-----|
| BASE-001 | Il Rifugio Sicuro | Dreams | Comune | 2 | 8 |
| BASE-002 | Il Volo Sopra la Città | Dreams | Rara | 4 | 5 |
| BASE-003 | Il Faro nella Nebbia | Dreams | Epica | 4 | 7 |
| BASE-004 | Il Sogno Lucido | Dreams | Leggendaria (+ full art) | 5 | 7 |
| BASE-005 | Il Dente Che Cade | Nightmares | Comune | 4 | 2 |
| BASE-006 | La Caduta Senza Fine | Nightmares | Rara | 7 | 3 |
| BASE-007 | La Stanza Senza Porte | Nightmares | Epica | 6 | 5 |
| BASE-008 | L'Uomo Senza Volto | Nightmares | Leggendaria (+ full art) | 8 | 5 |
| BASE-009 | Il Ricordo Sbiadito | Memories | Comune | 3 | 5 |
| BASE-010 | Il Déjà-vu | Memories | Rara | 4 | 5 |
| BASE-011 | Il Corridoio Infinito | Memories | Epica | 3 | 7 |
| BASE-012 | La Custode del Tempo Fermo | Memories | Leggendaria (+ full art) | 6 | 6 |
