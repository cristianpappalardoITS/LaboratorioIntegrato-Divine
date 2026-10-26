"""Compone le carte di Dreamscape.

Per ogni riga del file dati prende la cornice della rarità, l'illustrazione
della carta e scrive nome, simbolo di fazione, descrizione, effetto, attacco
e difesa. Le carte finite vanno in ../carte-finali/.

Uso:
    python3 componi_carte.py
    python3 componi_carte.py --solo BASE-001
    python3 componi_carte.py --sovrascrivi

Le carte già presenti nella cartella di uscita non vengono mai sovrascritte,
a meno di usare --sovrascrivi.
"""
import argparse
import csv
import os
import re
import sys
import unicodedata

try:
    from PIL import Image, ImageChops, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps
except ImportError:
    sys.exit("Manca la libreria Pillow. Installala con: python3 -m pip install pillow")

CARTELLA = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Zone delle cornici (in pixel, cornici da 1024 x 1536).
# Rettangoli: (sinistra, alto, destra, basso). Numeri: centro (x, y).
# "fazione": centro del cerchio della cornice e raggio del medaglione che lo copre.
# Se una cornice cambia, basta correggere i numeri qui.
# ---------------------------------------------------------------------------
LAYOUT = {
    "comune": {
        "arte": (58, 186, 968, 934), "raggio_arte": 46,
        "nome": (120, 52, 800, 160),
        "fazione": (919, 112, 72),
        "descrizione": (100, 990, 925, 1112),
        "effetto": (100, 1158, 925, 1322),
        "att": (197, 1412), "dif": (934, 1412),
    },
    "rara": {
        "arte": (58, 192, 966, 922), "raggio_arte": 46,
        "nome": (170, 62, 810, 166),
        "fazione": (903, 119, 72),
        "descrizione": (100, 985, 925, 1110),
        "effetto": (100, 1158, 925, 1318),
        "att": (198, 1408), "dif": (918, 1408),
    },
    "epica": {
        "arte": (78, 238, 948, 892), "raggio_arte": 46,
        "nome": (215, 104, 815, 212),
        "fazione": (911, 164, 72),
        "descrizione": (110, 955, 915, 1066),
        "effetto": (110, 1112, 915, 1282),
        "att": (206, 1392), "dif": (906, 1392),
    },
    "leggendaria": {
        # La cornice originale è più stretta delle altre: la allarghiamo in orizzontale.
        # Le coordinate qui sotto sono quelle della cornice originale, non allargata.
        "allarga_x": 1.18,
        # full art: l'illustrazione copre tutta la carta e passa dietro ai cristalli
        "full_art": True, "oscura_esterno": 0.55,
        # Cosa si vede dietro ai cristalli, fuori dalla finestra:
        #   "sfocato"       = alone sfocato ricavato dall'illustrazione (sicuro con qualsiasi immagine)
        #   "illustrazione" = l'illustrazione intera e nitida (solo con illustrazioni pulite, senza cornice né testi)
        "esterno": "sfocato",
        # Solo per "illustrazione": punto della carta su cui cade il centro dell'immagine.
        "centro_illustrazione_y": 690,
        "protetti": [("cerchio", (822, 184, 76)), ("rettangolo", (168, 1300, 318, 1432)),
                     ("rettangolo", (708, 1300, 862, 1432))],
        "arte": (190, 262, 838, 898), "raggio_arte": 30,
        "nome": (250, 136, 750, 242),
        "fazione": (822, 184, 76),
        "descrizione": (222, 925, 800, 1058),
        "effetto": (222, 1102, 800, 1272),
        "att": (279, 1366), "dif": (823, 1366),
    },
}

FILE_CORNICE = "dreams_nightmares_cornice_{}.png"            # cornice generica per rarità
FILE_CORNICE_FAZIONE = "cornice_{fazione}_{rarita}.png"       # cornice già nei colori della fazione

# Posizione e grandezza dei numeri di attacco e difesa: UGUALI per tutte le cornici per fazione,
# così in ogni carta i numeri stanno esattamente nello stesso punto.
NUMERI_FISSI = {"att": (250, 1400), "dif": (772, 1400), "dimensione": 74}
# Eccezioni temporanee: in queste cornici lo scudo è disegnato più a destra e il numero lo coprirebbe.
# Da togliere quando le cornici verranno rigenerate con i riquadri nella posizione standard.
NUMERI_ECCEZIONI = {
    "cornice_dreams_comune.png": {"dif": (835, 1396)},
    "cornice_dreams_rara.png": {"dif": (835, 1396)},
}

# Le cornici per fazione (con la finestra verde) vengono misurate in automatico dallo script:
# finestra, targhetta del nome, riquadro del testo, cerchio e riquadri di attacco e difesa.
FAZIONI = ("dreams", "nightmares", "memories")

# Colori per fazione: tinta del metallo della cornice e medaglione del simbolo.
# "nero" / "medio" / "chiaro" ricolorano le zone scure, intermedie e chiare della cornice.
COLORI_FAZIONE = {
    "dreams": {  # argento-azzurro
        "nero": (8, 12, 30), "medio": (92, 124, 196), "chiaro": (236, 243, 255),
        "anello_chiaro": (214, 226, 250), "anello_scuro": (96, 122, 186), "disco": (14, 18, 40),
    },
    "nightmares": {  # ferro scuro e cremisi
        "nero": (5, 3, 6), "medio": (92, 20, 32), "chiaro": (214, 196, 200),
        "anello_chiaro": (196, 176, 180), "anello_scuro": (104, 26, 38), "disco": (12, 6, 9),
    },
    "memories": {  # bronzo-ambra
        "nero": (18, 11, 5), "medio": (158, 110, 50), "chiaro": (248, 238, 220),
        "anello_chiaro": (240, 214, 160), "anello_scuro": (146, 100, 42), "disco": (24, 15, 8),
    },
}
FORZA_TINTA = {"comune": 0.85, "rara": 0.85, "epica": 0.85, "leggendaria": 0.78}
FORZA_TINTA_TESTO = 0.22  # sul riquadro del testo e sulla targhetta del nome la tinta è leggera
COLORE_TESTO = (38, 32, 58)
COLORE_NUMERI = (245, 243, 250)

# Font: prima quelli nella cartella "font" accanto allo script, poi quelli di sistema.
FONT = {
    "normale": [("font/serif-regular.ttf", 0), ("/System/Library/Fonts/Palatino.ttc", 0),
                ("C:/Windows/Fonts/pala.ttf", 0), ("/System/Library/Fonts/Supplemental/Times New Roman.ttf", 0),
                ("DejaVuSerif.ttf", 0)],
    "corsivo": [("font/serif-italic.ttf", 0), ("/System/Library/Fonts/Palatino.ttc", 1),
                ("C:/Windows/Fonts/palai.ttf", 0), ("/System/Library/Fonts/Supplemental/Times New Roman Italic.ttf", 0),
                ("DejaVuSerif-Italic.ttf", 0)],
    "grassetto": [("font/serif-bold.ttf", 0), ("/System/Library/Fonts/Palatino.ttc", 2),
                  ("C:/Windows/Fonts/palab.ttf", 0), ("/System/Library/Fonts/Supplemental/Times New Roman Bold.ttf", 0),
                  ("DejaVuSerif-Bold.ttf", 0)],
}
_cache_font = {}


def font(stile, dimensione):
    chiave = (stile, dimensione)
    if chiave not in _cache_font:
        for percorso, indice in FONT[stile]:
            if not os.path.isabs(percorso) and os.path.exists(os.path.join(CARTELLA, percorso)):
                percorso = os.path.join(CARTELLA, percorso)
            try:
                _cache_font[chiave] = ImageFont.truetype(percorso, dimensione, index=indice)
                break
            except OSError:
                continue
        else:
            sys.exit(f"Nessun font trovato per lo stile '{stile}'. Metti un file .ttf nella cartella 'font'.")
    return _cache_font[chiave]


# ---------------------------------------------------------------------------
# Testo
# ---------------------------------------------------------------------------
def a_capo(parti, larghezza_max, dimensione):
    """Divide in righe una lista di (testo, stile) senza superare la larghezza."""
    parole = []
    for testo, stile in parti:
        for parola in testo.split():
            parole.append((parola, stile))
    righe, riga, larghezza = [], [], 0
    spazio = font("normale", dimensione).getlength(" ")
    for parola, stile in parole:
        lunghezza = font(stile, dimensione).getlength(parola)
        aggiunta = lunghezza + (spazio if riga else 0)
        if riga and larghezza + aggiunta > larghezza_max:
            righe.append((riga, larghezza))
            riga, larghezza = [(parola, stile)], lunghezza
        else:
            riga.append((parola, stile))
            larghezza += aggiunta
    if riga:
        righe.append((riga, larghezza))
    return righe


def scrivi_blocco(disegno, zona, parti, dimensione_max, dimensione_min=20, interlinea=1.22, colore=None, ombra=None):
    """Scrive il testo centrato nella zona, rimpicciolendolo finché ci sta."""
    sinistra, alto, destra, basso = zona
    larghezza, altezza = destra - sinistra, basso - alto
    for dimensione in range(dimensione_max, dimensione_min - 1, -1):
        righe = a_capo(parti, larghezza, dimensione)
        passo = dimensione * interlinea
        if len(righe) * passo <= altezza:
            break
    y = alto + (altezza - len(righe) * passo) / 2
    spazio = font("normale", dimensione).getlength(" ")
    for riga, larghezza_riga in righe:
        x = sinistra + (larghezza - larghezza_riga) / 2
        for parola, stile in riga:
            if ombra:
                disegno.text((x + 2, y + passo / 2 + 2), parola, font=font(stile, dimensione), fill=ombra, anchor="lm")
            disegno.text((x, y + passo / 2), parola, font=font(stile, dimensione), fill=colore or COLORE_TESTO, anchor="lm")
            x += font(stile, dimensione).getlength(parola) + spazio
        y += passo


def parti_effetto(effetto):
    """'Guscio 1: subisce...' -> nome in grassetto, resto normale."""
    if ":" in effetto:
        nome, resto = effetto.split(":", 1)
        return [(nome + ":", "grassetto"), (resto.strip(), "normale")]
    return [(effetto, "normale")]


# ---------------------------------------------------------------------------
# Icone di fazione (disegnate, così restano nitide a qualsiasi dimensione)
# ---------------------------------------------------------------------------
def simbolo_fazione(fazione, lato):
    """Maschera del simbolo (luna, occhio, clessidra) su un quadrato di lato 'lato'."""
    livello = Image.new("L", (lato, lato), 0)
    d = ImageDraw.Draw(livello)
    c, r = lato / 2, lato * 0.36
    if fazione == "dreams":  # luna crescente
        d.ellipse((c - r, c - r, c + r, c + r), fill=255)
        spostamento = r * 0.45
        d.ellipse((c - r + spostamento, c - r - spostamento * 0.6, c + r + spostamento, c + r - spostamento * 0.6), fill=0)
    elif fazione == "nightmares":  # occhio aperto
        punti_alto, punti_basso = [], []
        for i in range(41):
            t = -1 + i / 20
            x = c + t * r * 1.15
            y = r * 0.62 * (1 - t * t)
            punti_alto.append((x, c - y))
            punti_basso.append((x, c + y))
        d.polygon(punti_alto + punti_basso[::-1], fill=255)
        d.ellipse((c - r * 0.42, c - r * 0.42, c + r * 0.42, c + r * 0.42), fill=0)
        d.ellipse((c - r * 0.17, c - r * 0.17, c + r * 0.17, c + r * 0.17), fill=255)
    elif fazione == "memories":  # clessidra
        w, h = r * 0.7, r * 0.95
        spessore = r * 0.14
        d.rectangle((c - w * 1.1, c - h - spessore, c + w * 1.1, c - h), fill=255)
        d.rectangle((c - w * 1.1, c + h, c + w * 1.1, c + h + spessore), fill=255)
        d.polygon([(c - w, c - h), (c + w, c - h), (c + r * 0.08, c), (c - r * 0.08, c)], fill=255)
        d.polygon([(c - r * 0.08, c), (c + r * 0.08, c), (c + w, c + h), (c - w, c + h)], fill=255)
        d.polygon([(c - w * 0.55, c - h * 0.55), (c + w * 0.55, c - h * 0.55), (c, c - h * 0.05)], fill=0)
    # Centro il simbolo sulla sua forma visibile (la luna, per esempio, ha il peso spostato a sinistra)
    sx, sy, dx, dy = livello.getbbox()
    centrato = Image.new("L", (lato, lato), 0)
    centrato.paste(livello.crop((sx, sy, dx, dy)), (round(c - (dx - sx) / 2), round(c - (dy - sy) / 2)))
    return centrato


def medaglione(fazione, raggio):
    """Medaglione rotondo e nitido: anello metallico nel colore della fazione, disco scuro, simbolo centrato."""
    colori = COLORI_FAZIONE[fazione]
    scala = 4  # disegno in grande e riduco: bordi morbidi e nitidi
    lato = raggio * 2 * scala
    img = Image.new("RGBA", (lato, lato), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    c = lato / 2
    R = raggio * scala
    # Ombra leggera, anello esterno chiaro, filetto scuro, anello interno, disco
    d.ellipse((c - R, c - R, c + R, c + R), fill=(0, 0, 0, 110))
    r1 = R * 0.95
    d.ellipse((c - r1, c - r1, c + r1, c + r1), fill=colori["anello_chiaro"] + (255,))
    r2 = R * 0.86
    d.ellipse((c - r2, c - r2, c + r2, c + r2), fill=colori["anello_scuro"] + (255,))
    r3 = R * 0.80
    d.ellipse((c - r3, c - r3, c + r3, c + r3), fill=colori["anello_chiaro"] + (255,))
    r4 = R * 0.74
    d.ellipse((c - r4, c - r4, c + r4, c + r4), fill=colori["disco"] + (255,))
    # Riflesso sull'anello in alto a sinistra
    riflesso = Image.new("L", (lato, lato), 0)
    ImageDraw.Draw(riflesso).arc((c - r1 * 0.97, c - r1 * 0.97, c + r1 * 0.97, c + r1 * 0.97), 200, 290,
                                 fill=170, width=round(R * 0.05))
    img.paste((255, 255, 255, 255), (0, 0), riflesso.filter(ImageFilter.GaussianBlur(R * 0.02)))
    # Simbolo
    lato_simbolo = round(r4 * 2 * 0.78)
    simbolo = simbolo_fazione(fazione, lato_simbolo)
    colore_simbolo = Image.new("RGBA", simbolo.size, colori["chiaro"] + (255,))
    img.paste(colore_simbolo, (round(c - lato_simbolo / 2), round(c - lato_simbolo / 2)), simbolo)
    return img.resize((raggio * 2, raggio * 2), Image.LANCZOS)


def tinta_cornice(cornice, fazione, rarita, zone):
    """Ricolora il metallo della cornice nei colori della fazione e la rende più nitida."""
    colori = COLORI_FAZIONE[fazione]
    grigio = cornice.convert("L")
    tinta = ImageOps.colorize(grigio, black=colori["nero"], white=colori["chiaro"], mid=colori["medio"])
    # Forza della tinta: piena sul metallo, leggera sulla targhetta del nome e sul riquadro del testo
    forza = Image.new("L", cornice.size, round(255 * FORZA_TINTA[rarita]))
    d = ImageDraw.Draw(forza)
    leggera = round(255 * FORZA_TINTA_TESTO)
    sx, sy, dx, dy = zone["nome"]
    d.rounded_rectangle((sx - 40, sy - 20, dx + 40, dy + 20), radius=30, fill=leggera)
    sx, sy = zone["descrizione"][:2]
    dx, dy = zone["effetto"][2:]
    d.rounded_rectangle((sx - 60, sy - 50, dx + 60, dy + 50), radius=40, fill=leggera)
    forza = forza.filter(ImageFilter.GaussianBlur(12))
    tinta = Image.composite(tinta, cornice, forza)
    return tinta.filter(ImageFilter.UnsharpMask(radius=2.2, percent=110, threshold=2))


# ---------------------------------------------------------------------------
# Composizione
# ---------------------------------------------------------------------------
def adatta(illustrazione, dimensioni, zoom=1.0, centro_y=0.4):
    """Adatta l'illustrazione alla finestra.

    zoom = 1 riempie tutta la finestra; sotto 1 mostra più illustrazione e riempie
    i lati con un alone sfocato della stessa immagine. centro_y sposta il ritaglio
    in verticale: 0 = parte alta, 1 = parte bassa.
    """
    larghezza, altezza = dimensioni
    riempita = ImageOps.fit(illustrazione, dimensioni, Image.LANCZOS, centering=(0.5, centro_y))
    if zoom >= 1:
        return riempita
    scala = max(larghezza / illustrazione.width, altezza / illustrazione.height) * zoom
    nuova = illustrazione.resize((round(illustrazione.width * scala), round(illustrazione.height * scala)), Image.LANCZOS)
    # Ritaglio solo dove l'immagine è ancora più grande della finestra
    taglio_w = min(nuova.width, larghezza)
    taglio_h = min(nuova.height, altezza)
    sx = (nuova.width - taglio_w) // 2
    sy = round((nuova.height - taglio_h) * centro_y)
    nuova = nuova.crop((sx, sy, sx + taglio_w, sy + taglio_h))
    # Sfondo: la stessa illustrazione sfocata e un po' scurita
    sfondo = riempita.resize((larghezza // 10, altezza // 10), Image.LANCZOS).filter(ImageFilter.GaussianBlur(3))
    sfondo = ImageEnhance.Brightness(sfondo.resize(dimensioni, Image.LANCZOS)).enhance(0.88)
    # Bordi sfumati per fondere l'illustrazione con lo sfondo
    maschera = Image.new("L", nuova.size, 0)
    sfumatura = max(8, round(min(nuova.size) * 0.04))
    ImageDraw.Draw(maschera).rectangle((sfumatura, sfumatura, nuova.width - sfumatura, nuova.height - sfumatura), fill=255)
    if taglio_w == larghezza:
        ImageDraw.Draw(maschera).rectangle((0, sfumatura, nuova.width, nuova.height - sfumatura), fill=255)
    if taglio_h == altezza:
        ImageDraw.Draw(maschera).rectangle((sfumatura, 0, nuova.width - sfumatura, nuova.height), fill=255)
    maschera = maschera.filter(ImageFilter.GaussianBlur(sfumatura / 2))
    sfondo.paste(nuova, ((larghezza - taglio_w) // 2, (altezza - taglio_h) // 2), maschera)
    return sfondo


def regolazioni(carta):
    """Legge zoom e centro_y dal CSV (colonne facoltative)."""
    def numero(chiave, predefinito):
        valore = (carta.get(chiave) or "").strip().replace(",", ".")
        try:
            return float(valore) if valore else predefinito
        except ValueError:
            return predefinito
    return min(1.0, max(0.3, numero("zoom", 1.0))), min(1.0, max(0.0, numero("centro_y", 0.4)))


def _o(a, b):
    return ImageChops.lighter(a, b)


def _e(a, b):
    return ImageChops.multiply(a, b)


def _allarga(maschera, pixel):
    return maschera.filter(ImageFilter.MaxFilter(pixel * 2 + 1))


def maschera_verde(cornice):
    """Zona in cui va l'illustrazione: il verde della finestra fino al bordo della cornice.

    Comprende anche i pixel di passaggio ancora verdastri e il filetto scuro tra il verde
    e il metallo, così tra illustrazione e cornice non resta nessuno spazio vuoto.
    """
    r, g, b = cornice.split()
    verde_puro = _e(_e(r.point(lambda v: 255 if v < 110 else 0), g.point(lambda v: 255 if v > 150 else 0)),
                    b.point(lambda v: 255 if v < 110 else 0))
    if not verde_puro.getbbox():
        return verde_puro
    # Pixel in cui il verde domina ancora (bordo sfumato), solo vicino alla finestra
    dominante = ImageChops.subtract(g, ImageChops.lighter(r, b)).point(lambda v: 255 if v > 35 else 0)
    base = _o(verde_puro, _e(dominante, _allarga(verde_puro, 6)))
    # Filetto scuro attaccato al verde
    scuro = cornice.convert("L").point(lambda v: 255 if v < 70 else 0)
    base = _o(base, _e(scuro, _allarga(base, 5)))
    return _allarga(base, 1)


def togli_riflesso_verde(cornice, maschera):
    """Sul metallo appena fuori dalla finestra toglie il riflesso verde lasciato dallo sfondo."""
    fascia = ImageChops.subtract(_allarga(maschera, 6), maschera)
    r, g, b = cornice.split()
    g_pulito = ImageChops.darker(g, ImageChops.lighter(r, b).point(lambda v: min(255, v + 8)))
    return Image.composite(Image.merge("RGB", (r, g_pulito, b)), cornice, fascia)


def componi_su_verde(cornice, illustrazione, verde, zoom, centro_y):
    """L'illustrazione va sotto la cornice: si vede solo nella finestra verde (bordo compreso)."""
    sx, sy, dx, dy = verde.getbbox()
    livello = Image.new("RGB", cornice.size)
    livello.paste(adatta(illustrazione, (dx - sx, dy - sy), zoom, centro_y), (sx, sy))
    cornice = togli_riflesso_verde(cornice, verde)
    return Image.composite(livello, cornice, verde.filter(ImageFilter.GaussianBlur(0.7)))


def _regione(maschera, seme):
    """Area connessa al punto 'seme' in una maschera bianco/nero: restituisce il riquadro (bbox)."""
    copia = maschera.copy()
    if copia.getpixel(seme) != 255:
        return None
    ImageDraw.floodfill(copia, seme, 128)
    return copia.point(lambda v: 255 if v == 128 else 0).getbbox()


def misura_zone(cornice, verde):
    """Ricava le zone di una cornice con la finestra verde."""
    larghezza, altezza = cornice.size
    finestra = verde.getbbox()
    r, g, b = cornice.split()
    # Pergamena: chiara e calda (il rosso supera il blu); l'argento della cornice è freddo e resta fuori
    pergamena = ImageChops.multiply(r.point(lambda v: 255 if v > 175 else 0), b.point(lambda v: 255 if v > 120 else 0))
    pergamena = ImageChops.multiply(pergamena, g.point(lambda v: 255 if v > 160 else 0))
    pergamena = ImageChops.multiply(pergamena, ImageChops.subtract(r, b).point(lambda v: 255 if v > 12 else 0))
    scuro = cornice.convert("L").point(lambda v: 255 if v < 75 else 0)
    nerissimo = cornice.convert("L").point(lambda v: 255 if v < 22 else 0)

    def cerca(maschera, x, y, passo=12):
        """Prova il seme e i punti vicini finché trova la zona."""
        for dx in (0, passo, -passo, 2 * passo, -2 * passo):
            for dy in (0, passo, -passo, 2 * passo, -2 * passo):
                punto = (int(x + dx), int(y + dy))
                if 0 <= punto[0] < larghezza and 0 <= punto[1] < altezza:
                    riquadro = _regione(maschera, punto)
                    if riquadro:
                        return riquadro
        raise ValueError(f"zona non trovata vicino a ({int(x)}, {int(y)})")

    def riquadro_rettangolare(x, y, salto=16, raggio=200):
        """Parte rettangolare di un riquadro di pergamena: si ferma dove diventa più stretto.
        'salto' = larghezza massima delle interruzioni da superare (riflessi di luce sulla pergamena)."""
        def ampiezza(riga):
            if not pergamena.getpixel((x, riga)):
                return None

            def estendi(partenza, verso):
                ultimo = partenza
                pos = partenza
                buco = 0
                while 0 < pos < larghezza - 1:
                    pos += verso
                    if pergamena.getpixel((pos, riga)):
                        ultimo, buco = pos, 0
                    else:
                        buco += 1
                        if buco > salto:
                            break
                return ultimo
            return estendi(x, -1), estendi(x, 1)
        # Misuro le righe intorno al seme e tengo quelle con la larghezza più comune:
        # così riflessi o decorazioni attaccate alla pergamena non falsano la misura.
        righe = {}
        for riga in range(max(0, int(y) - raggio), min(altezza, int(y) + raggio)):
            a = ampiezza(riga)
            if a:
                righe[riga] = a
        if not righe:
            raise ValueError(f"riquadro non trovato vicino a ({int(x)}, {int(y)})")
        larghezze = sorted(d - s for s, d in righe.values())
        riferimento = larghezze[len(larghezze) * 3 // 4]  # tra le righe più larghe
        simili = sorted(r for r, (s, d) in righe.items() if (d - s) >= riferimento * 0.8)
        # Blocco continuo di righe simili più vicino al seme
        blocchi, blocco = [], [simili[0]]
        for r in simili[1:]:
            if r - blocco[-1] <= 3:
                blocco.append(r)
            else:
                blocchi.append(blocco)
                blocco = [r]
        blocchi.append(blocco)
        blocco = max(blocchi, key=len)
        alto, basso = blocco[0], blocco[-1]
        sinistre = sorted(righe[r][0] for r in blocco if r in righe)
        destre = sorted(righe[r][1] for r in blocco if r in righe)
        # Bordi laterali "interni": scarto gli estremi dovuti agli angoli arrotondati
        return (sinistre[len(sinistre) * 9 // 10], alto, destre[len(destre) // 10], basso)

    nome = riquadro_rettangolare(int(larghezza * 0.37), int(finestra[1] * 0.5), salto=70, raggio=90)
    testo = riquadro_rettangolare(larghezza // 2, int(finestra[3] + (altezza - finestra[3]) * 0.30), raggio=330)

    # Cerchio: la zona nerissima più grande in alto a destra
    area = nerissimo.crop((int(larghezza * 0.62), 15, larghezza - 30, max(40, finestra[1] - 5)))
    sx, sy, dx, dy = area.getbbox()
    centro = (int(larghezza * 0.62) + (sx + dx) // 2, 15 + (sy + dy) // 2)
    cerchio = cerca(nerissimo, *centro, passo=8)
    cx, cy = (cerchio[0] + cerchio[2]) // 2, (cerchio[1] + cerchio[3]) // 2
    raggio = min(cerchio[2] - cerchio[0], cerchio[3] - cerchio[1]) // 2

    grigio = cornice.convert("L")

    def numero(x, y):
        """Centro del numero: tra l'icona (spada o scudo) e il bordo destro del riquadro scuro."""
        x, y = int(x), int(y)
        for dx, dy in ((0, 0), (0, 20), (0, -20), (30, 0), (-30, 0), (0, 40), (0, -40), (30, 20), (-30, 20), (60, 0)):
            if grigio.getpixel((x + dx, y + dy)) < 75:
                x, y = x + dx, y + dy
                break
        else:
            raise ValueError(f"riquadro di attacco/difesa non trovato in ({x}, {y})")
        destra = x
        while destra < larghezza - 1 and grigio.getpixel((destra + 1, y)) < 75:
            destra += 1
        sinistra = x
        while sinistra > 0 and grigio.getpixel((sinistra - 1, y)) < 75:
            sinistra -= 1  # si ferma sull'icona o sul bordo sinistro
        centro_x = (sinistra + destra) // 2
        alto = basso = y
        while alto > 0 and grigio.getpixel((centro_x, alto - 1)) < 75:
            alto -= 1
        while basso < altezza - 1 and grigio.getpixel((centro_x, basso + 1)) < 75:
            basso += 1
        return centro_x, (alto + basso) // 2, round((basso - alto) * 0.62)

    att = numero(larghezza * 0.27, altezza * 0.875)
    dif = numero(larghezza * 0.80, altezza * 0.875)

    tl, tt, tr, tb = testo
    th, tw = tb - tt, tr - tl
    divisore_y = tt + round(th * 0.46)
    nl, nt, nr, nb = nome
    zone = {
        "nome": (nl + round((nr - nl) * 0.06), nt + 6, nr - round((nr - nl) * 0.06), nb - 6),
        "fazione": (cx, cy, raggio),
        "descrizione": (tl + round(tw * 0.07), tt + round(th * 0.05), tr - round(tw * 0.07), divisore_y - round(th * 0.035)),
        "effetto": (tl + round(tw * 0.07), divisore_y + round(th * 0.05), tr - round(tw * 0.07), tb - round(th * 0.06)),
        "divisore": (tl + round(tw * 0.18), tr - round(tw * 0.18), divisore_y),
        "att": NUMERI_FISSI["att"], "dif": NUMERI_FISSI["dif"],
        "dimensione_numeri": NUMERI_FISSI["dimensione"],
        "solo_simbolo": True,
    }
    return zone


def maschera_finestra(cornice, zona, raggio):
    """Area scura della finestra dell'illustrazione, con angoli arrotondati."""
    forma = Image.new("L", cornice.size, 0)
    ImageDraw.Draw(forma).rounded_rectangle(zona, radius=raggio, fill=255)
    scuro = cornice.convert("L").point(lambda v: 255 if v < 80 else 0)
    maschera = Image.composite(scuro, Image.new("L", cornice.size, 0), forma)
    return maschera.filter(ImageFilter.GaussianBlur(1.2))


def componi_full_art(cornice, illustrazione, zone, zoom=1.0, centro_y=0.4):
    """L'illustrazione passa dietro ai cristalli; la cornice resta sopra con le parti scure trasparenti."""
    larghezza, altezza = cornice.size
    sx, sy, dx, dy = zone["arte"]

    # Finestra: l'illustrazione ritagliata come nelle altre rarità
    nella_finestra = adatta(illustrazione, (dx - sx, dy - sy), zoom, centro_y)

    if zone.get("esterno", "sfocato") == "illustrazione":
        # Illustrazione intera e nitida su tutta la carta
        cx = (sx + dx) // 2
        cy = zone.get("centro_illustrazione_y", (sy + dy) // 2)
        meta_w, meta_h = max(cx, larghezza - cx), max(cy, altezza - cy)
        grande = ImageOps.fit(illustrazione, (meta_w * 2, meta_h * 2), Image.LANCZOS, centering=(0.5, 0.5))
        esterno = Image.new("RGB", cornice.size)
        esterno.paste(grande, (cx - meta_w, cy - meta_h))
    else:
        # Alone: la parte della finestra, ingrandita su tutta la carta e molto sfocata.
        # Usa solo la zona centrale dell'illustrazione, quindi non può mostrare scritte o cornici.
        esterno = ImageOps.fit(nella_finestra, cornice.size, Image.LANCZOS)
        esterno = esterno.resize((larghezza // 8, altezza // 8), Image.LANCZOS).filter(ImageFilter.GaussianBlur(6))
        esterno = esterno.resize(cornice.size, Image.LANCZOS)
    esterno = ImageEnhance.Brightness(esterno).enhance(zone.get("oscura_esterno", 0.75))

    sfondo = esterno.copy()
    finestra = Image.new("L", cornice.size, 0)
    ImageDraw.Draw(finestra).rounded_rectangle(zone["arte"], radius=zone["raggio_arte"], fill=255)
    livello_finestra = Image.new("RGB", cornice.size)
    livello_finestra.paste(nella_finestra, (sx, sy))
    sfondo = Image.composite(livello_finestra, sfondo, finestra.filter(ImageFilter.GaussianBlur(2)))

    # Opacità della cornice: le zone scure lasciano vedere lo sfondo, i cristalli restano
    # La cornice resta sopra all'illustrazione ovunque non sia scura, anche dentro la finestra
    alfa = cornice.convert("L").point(lambda v: 0 if v < 38 else 255 if v > 100 else int((v - 38) * 255 / 62))
    d = ImageDraw.Draw(alfa)
    for forma, valori in zone.get("protetti", []):
        if forma == "cerchio":
            x, y, r = valori
            d.ellipse((x - r, y - r, x + r, y + r), fill=255)
        else:
            d.rounded_rectangle(valori, radius=30, fill=255)
    alfa = alfa.filter(ImageFilter.GaussianBlur(1.5))
    return Image.composite(cornice, sfondo, alfa)


def allarga_cornice(cornice, zone):
    """Allarga la cornice in orizzontale e ricalcola le zone."""
    k = zone["allarga_x"]
    larghezza, altezza = cornice.size
    centro = larghezza / 2
    nuova_larghezza = round(larghezza * k)
    allargata = cornice.resize((nuova_larghezza, altezza), Image.LANCZOS)
    margine = (nuova_larghezza - larghezza) // 2
    allargata = allargata.crop((margine, 0, margine + larghezza, altezza))

    def x(valore):
        return round(centro + (valore - centro) * k)

    nuove = dict(zone)
    for chiave in ("arte", "nome", "descrizione", "effetto"):
        s, a, d, b = zone[chiave]
        nuove[chiave] = (x(s), a, x(d), b)
    for chiave in ("att", "dif"):
        nuove[chiave] = (x(zone[chiave][0]), zone[chiave][1])
    fx, fy, fr = zone["fazione"]
    nuove["fazione"] = (x(fx), fy, fr)
    protetti = []
    for forma, valori in zone.get("protetti", []):
        if forma == "cerchio":
            protetti.append((forma, (x(valori[0]), valori[1], valori[2])))
        else:
            s, a, d, b = valori
            protetti.append((forma, (x(s), a, x(d), b)))
    nuove["protetti"] = protetti

    return allargata, nuove


def componi(carta, cartella_cornici, percorso_illustrazione):
    rarita = carta["rarita"].strip().lower()
    fazione = carta["fazione"].strip().lower()
    if rarita not in LAYOUT:
        raise ValueError(f"rarità '{carta['rarita']}' sconosciuta (ammesse: {', '.join(LAYOUT)})")
    if fazione not in FAZIONI:
        raise ValueError(f"fazione '{carta['fazione']}' sconosciuta (ammesse: {', '.join(FAZIONI)})")
    illustrazione = Image.open(percorso_illustrazione).convert("RGB")
    zoom, centro_y = regolazioni(carta)

    file_fazione = os.path.join(cartella_cornici, FILE_CORNICE_FAZIONE.format(fazione=fazione, rarita=rarita))
    if os.path.exists(file_fazione):
        # Cornice già nei colori della fazione: niente tinta, niente allargamento
        cornice = Image.open(file_fazione).convert("RGB")
        if cornice.size != (1024, 1536):
            cornice = cornice.resize((1024, 1536), Image.LANCZOS)
        zone = None  # misurate sotto, dalla finestra verde
    else:
        cornice = Image.open(os.path.join(cartella_cornici, FILE_CORNICE.format(rarita))).convert("RGB")
        zone = LAYOUT[rarita]
        if zone.get("allarga_x"):
            cornice, zone = allarga_cornice(cornice, zone)
        cornice = tinta_cornice(cornice, fazione, rarita, zone)

    verde = maschera_verde(cornice)
    finestra_verde = verde.getbbox()
    if zone is None and not (finestra_verde and (finestra_verde[2] - finestra_verde[0]) * (finestra_verde[3] - finestra_verde[1]) > 100000):
        raise ValueError(f"la cornice {os.path.basename(file_fazione)} non ha la finestra verde")
    if finestra_verde and (finestra_verde[2] - finestra_verde[0]) * (finestra_verde[3] - finestra_verde[1]) > 100000:
        if zone is None:
            zone = misura_zone(cornice, verde)
            zone.update(NUMERI_ECCEZIONI.get(os.path.basename(file_fazione), {}))
        carta_img = componi_su_verde(cornice, illustrazione, verde, zoom, centro_y)
        return scrivi_testi(carta_img, carta, fazione, zone)

    if zone.get("full_art"):
        carta_img = componi_full_art(cornice, illustrazione, zone, zoom, centro_y)
    else:
        # Illustrazione: riempie la finestra (o meno, se zoom < 1)
        sx, sy, dx, dy = zone["arte"]
        adattata = adatta(illustrazione, (dx - sx, dy - sy), zoom, centro_y)
        livello_arte = Image.new("RGB", cornice.size)
        livello_arte.paste(adattata, (sx, sy))
        carta_img = Image.composite(livello_arte, cornice, maschera_finestra(cornice, zone["arte"], zone["raggio_arte"]))

    return scrivi_testi(carta_img, carta, fazione, zone)


def scrivi_testi(carta_img, carta, fazione, zone):
    """Nome, medaglione di fazione, descrizione, effetto, attacco e difesa."""
    disegno = ImageDraw.Draw(carta_img)

    # Nome
    scrivi_blocco(disegno, zone["nome"], [(carta["nome"].strip(), "grassetto")], 54, 26)

    cx, cy, raggio = zone["fazione"]
    if zone.get("solo_simbolo"):
        # La cornice ha già un cerchio nitido: metto solo il simbolo, centrato
        lato = round(raggio * 1.25)
        scala = 4
        maschera = simbolo_fazione(fazione, lato * scala).resize((lato, lato), Image.LANCZOS)
        colore = Image.new("RGB", (lato, lato), COLORI_FAZIONE[fazione]["chiaro"])
        carta_img.paste(colore, (cx - lato // 2, cy - lato // 2), maschera)
    else:
        # Medaglione con il simbolo della fazione, sopra il cerchio della cornice
        simbolo = medaglione(fazione, raggio)
        carta_img.paste(simbolo, (cx - raggio, cy - raggio), simbolo)

    # Riga decorativa tra descrizione ed effetto, se la cornice non ce l'ha
    if zone.get("divisore"):
        x1, x2, y = zone["divisore"]
        colore = COLORI_FAZIONE[fazione]["anello_scuro"]
        disegno.line((x1, y, x2, y), fill=colore, width=3)
        lato = 11
        disegno.polygon([(x1 + (x2 - x1) // 2, y - lato), (x1 + (x2 - x1) // 2 + lato, y),
                         (x1 + (x2 - x1) // 2, y + lato), (x1 + (x2 - x1) // 2 - lato, y)], fill=colore)

    # Descrizione (corsivo) ed effetto
    descrizione = carta["descrizione"].strip().strip('"«»')
    scrivi_blocco(disegno, zone["descrizione"], [(descrizione, "corsivo")], 46, 24)
    if carta.get("effetto", "").strip():
        scrivi_blocco(disegno, zone["effetto"], parti_effetto(carta["effetto"].strip()), 44, 24)

    # Attacco e difesa
    for chiave in ("att", "dif"):
        valore = carta["attacco" if chiave == "att" else "difesa"].strip()
        disegno.text(zone[chiave], valore, font=font("grassetto", zone.get("dimensione_numeri", 70)), fill=COLORE_NUMERI, anchor="mm")
    return carta_img


# ---------------------------------------------------------------------------
# Full art: illustrazione su tutta la carta, testi su pannelli scuri semitrasparenti
# ---------------------------------------------------------------------------
FULL_ART = {
    "bordo": 14,                      # spessore del bordo nel colore della fazione
    "raggio_carta": 42,               # angoli arrotondati della carta
    "nome": (48, 48, 828, 158),
    "fazione": (918, 103, 58),        # centro e raggio del disco del simbolo
    "testo": (48, 1030, 976, 1352),
    "att": (48, 1378, 318, 1490),
    "dif": (706, 1378, 976, 1490),
    "opacita": 150,                   # 0 = pannelli trasparenti, 255 = neri pieni
    "sfocatura": 10,                  # quanto è sfocato lo sfondo dietro ai pannelli
}
COLORE_TESTO_CHIARO = (246, 241, 230)


def pannello(carta_img, riquadro, raggio, colore_bordo):
    """Pannello scuro semitrasparente con lo sfondo sfocato dietro (effetto vetro)."""
    maschera = Image.new("L", carta_img.size, 0)
    ImageDraw.Draw(maschera).rounded_rectangle(riquadro, radius=raggio, fill=255)
    sfocata = carta_img.filter(ImageFilter.GaussianBlur(FULL_ART["sfocatura"]))
    carta_img.paste(sfocata, (0, 0), maschera)
    velo = Image.new("RGBA", carta_img.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(velo)
    d.rounded_rectangle(riquadro, radius=raggio, fill=(8, 8, 16, FULL_ART["opacita"]))
    d.rounded_rectangle(riquadro, radius=raggio, outline=colore_bordo + (170,), width=2)
    carta_img.paste(velo, (0, 0), velo)


def icona_statistica(tipo, lato, colore):
    """Spada o scudo disegnati, nitidi."""
    scala = 4
    L = lato * scala
    img = Image.new("L", (L, L), 0)
    d = ImageDraw.Draw(img)
    if tipo == "spada":
        lama = [(L * 0.78, L * 0.08), (L * 0.92, L * 0.22), (L * 0.40, L * 0.74), (L * 0.26, L * 0.60)]
        d.polygon(lama, fill=255)
        d.polygon([(L * 0.16, L * 0.58), (L * 0.42, L * 0.84), (L * 0.36, L * 0.90), (L * 0.10, L * 0.64)], fill=255)  # guardia
        d.polygon([(L * 0.24, L * 0.70), (L * 0.30, L * 0.76), (L * 0.14, L * 0.92), (L * 0.08, L * 0.86)], fill=255)  # impugnatura
        d.ellipse((L * 0.02, L * 0.88, L * 0.12, L * 0.98), fill=255)  # pomo
    else:
        forma = [(L * 0.5, L * 0.06), (L * 0.88, L * 0.18), (L * 0.84, L * 0.56), (L * 0.5, L * 0.94),
                 (L * 0.16, L * 0.56), (L * 0.12, L * 0.18)]
        d.polygon(forma, fill=255)
        interno = [(L * 0.5, L * 0.16), (L * 0.78, L * 0.25), (L * 0.75, L * 0.54), (L * 0.5, L * 0.83),
                   (L * 0.25, L * 0.54), (L * 0.22, L * 0.25)]
        d.polygon(interno, fill=0)
        d.polygon([(L * 0.5, L * 0.16), (L * 0.78, L * 0.25), (L * 0.75, L * 0.54), (L * 0.5, L * 0.83)], fill=150)
    img = img.resize((lato, lato), Image.LANCZOS)
    icona = Image.new("RGBA", (lato, lato), colore + (0,))
    icona.putalpha(img)
    return icona


def componi_full_art_alt(carta, percorso_illustrazione):
    """Versione full art: illustrazione su tutta la carta e pannelli semitrasparenti."""
    fazione = carta["fazione"].strip().lower()
    colori = COLORI_FAZIONE[fazione]
    larghezza, altezza = 1024, 1536
    zoom, centro_y = regolazioni(carta)
    illustrazione = Image.open(percorso_illustrazione).convert("RGB")
    carta_img = ImageOps.fit(illustrazione, (larghezza, altezza), Image.LANCZOS, centering=(0.5, centro_y))

    # Pannelli
    pannello(carta_img, FULL_ART["nome"], 30, colori["anello_chiaro"])
    pannello(carta_img, FULL_ART["testo"], 34, colori["anello_chiaro"])
    pannello(carta_img, FULL_ART["att"], 30, colori["anello_chiaro"])
    pannello(carta_img, FULL_ART["dif"], 30, colori["anello_chiaro"])
    cx, cy, r = FULL_ART["fazione"]
    pannello(carta_img, (cx - r, cy - r, cx + r, cy + r), r, colori["anello_chiaro"])

    disegno = ImageDraw.Draw(carta_img)
    ombra = (0, 0, 0)
    sx, sy, dx, dy = FULL_ART["nome"]
    scrivi_blocco(disegno, (sx + 30, sy + 8, dx - 30, dy - 8), [(carta["nome"].strip(), "grassetto")], 56, 28,
                  colore=COLORE_TESTO_CHIARO, ombra=ombra)

    # Simbolo di fazione
    lato = round(r * 1.25)
    maschera = simbolo_fazione(fazione, lato * 4).resize((lato, lato), Image.LANCZOS)
    carta_img.paste(Image.new("RGB", (lato, lato), colori["chiaro"]), (cx - lato // 2, cy - lato // 2), maschera)

    # Descrizione, riga, effetto
    tl, tt, tr, tb = FULL_ART["testo"]
    th = tb - tt
    divisore_y = tt + round(th * 0.45)
    descrizione = carta["descrizione"].strip().strip('"«»')
    scrivi_blocco(disegno, (tl + 50, tt + 22, tr - 50, divisore_y - 14), [(descrizione, "corsivo")], 44, 24,
                  colore=COLORE_TESTO_CHIARO, ombra=ombra)
    lato_riga = 10
    mezzo = (tl + tr) // 2
    disegno.line((tl + 170, divisore_y, tr - 170, divisore_y), fill=colori["anello_chiaro"], width=2)
    disegno.polygon([(mezzo, divisore_y - lato_riga), (mezzo + lato_riga, divisore_y), (mezzo, divisore_y + lato_riga),
                     (mezzo - lato_riga, divisore_y)], fill=colori["anello_chiaro"])
    if carta.get("effetto", "").strip():
        scrivi_blocco(disegno, (tl + 50, divisore_y + 18, tr - 50, tb - 22), parti_effetto(carta["effetto"].strip()),
                      42, 24, colore=COLORE_TESTO_CHIARO, ombra=ombra)

    # Attacco e difesa
    for chiave, tipo, campo in (("att", "spada", "attacco"), ("dif", "scudo", "difesa")):
        sx, sy, dx, dy = FULL_ART[chiave]
        lato = round((dy - sy) * 0.62)
        icona = icona_statistica(tipo, lato, colori["anello_chiaro"])
        carta_img.paste(icona, (sx + 28, (sy + dy) // 2 - lato // 2), icona)
        disegno.text(((sx + 28 + lato + dx) // 2, (sy + dy) // 2), carta[campo].strip(),
                     font=font("grassetto", round((dy - sy) * 0.62)), fill=COLORE_NUMERI, anchor="mm")

    # Bordo nel colore della fazione e angoli arrotondati (niente cornice: decisione del gruppo)
    raggio = FULL_ART["raggio_carta"]
    b = FULL_ART["bordo"]
    d = ImageDraw.Draw(carta_img)
    d.rounded_rectangle((b // 2, b // 2, larghezza - 1 - b // 2, altezza - 1 - b // 2), radius=raggio,
                        outline=colori["medio"], width=b)
    d.rounded_rectangle((2, 2, larghezza - 3, altezza - 3), radius=raggio, outline=colori["anello_chiaro"], width=2)
    d.rounded_rectangle((b - 1, b - 1, larghezza - b, altezza - b), radius=raggio - b, outline=colori["anello_chiaro"], width=2)
    angoli = Image.new("L", carta_img.size, 0)
    ImageDraw.Draw(angoli).rounded_rectangle((0, 0, larghezza - 1, altezza - 1), radius=raggio, fill=255)
    sfondo = Image.new("RGB", carta_img.size, (0, 0, 0))
    return Image.composite(carta_img, sfondo, angoli)


def nome_file(carta, variante=""):
    nome = unicodedata.normalize("NFKD", carta["nome"]).encode("ascii", "ignore").decode()
    nome = re.sub(r"[^a-zA-Z0-9]+", "-", nome).strip("-").lower()
    suffisso = f"_{variante}" if variante else ""
    return f"{carta['codice'].strip()}_{nome}{suffisso}.png"


ESTENSIONI = (".png", ".jpg", ".jpeg", ".webp")


def trova_illustrazioni(cartella, nome_indicato):
    """Restituisce [(variante, percorso)]: il file indicato nel CSV oppure le sue varianti -A, -B, -C..."""
    radice = os.path.splitext(nome_indicato.strip())[0].lower()
    if not radice or not os.path.isdir(cartella):
        return []
    trovate = []
    for file in sorted(os.listdir(cartella)):
        nome, estensione = os.path.splitext(file)
        if estensione.lower() not in ESTENSIONI:
            continue
        nome = nome.lower()
        if nome == radice:
            trovate.append(("", os.path.join(cartella, file)))
        elif re.fullmatch(re.escape(radice) + r"[-_ ]([a-z0-9]+)", nome):
            variante = re.fullmatch(re.escape(radice) + r"[-_ ]([a-z0-9]+)", nome).group(1).upper()
            trovate.append((variante, os.path.join(cartella, file)))
    return trovate


def leggi_dati(percorso):
    with open(percorso, encoding="utf-8-sig", newline="") as f:
        campione = f.read(4096)
        f.seek(0)
        separatore = ";" if campione.count(";") >= campione.count(",") else ","
        return [riga for riga in csv.DictReader(f, delimiter=separatore) if riga.get("codice", "").strip()]


def main():
    parser = argparse.ArgumentParser(description="Compone le carte di Dreamscape.")
    parser.add_argument("--dati", default=os.path.join(CARTELLA, "carte.csv"), help="file CSV con i dati delle carte")
    parser.add_argument("--cornici", default=os.path.join(CARTELLA, "..", "cornici"), help="cartella delle cornici")
    parser.add_argument("--illustrazioni", default=os.path.join(CARTELLA, "..", "illustrazioni"), help="cartella delle illustrazioni")
    parser.add_argument("--uscita", default=os.path.join(CARTELLA, "..", "carte-finali"), help="cartella delle carte finite")
    parser.add_argument("--solo", help="compone solo la carta con questo codice (es. BASE-001)")
    parser.add_argument("--sovrascrivi", action="store_true", help="rigenera anche le carte già presenti")
    args = parser.parse_args()

    os.makedirs(args.uscita, exist_ok=True)
    fatte = saltate = errori = 0
    for carta in leggi_dati(args.dati):
        if args.solo and carta["codice"].strip() != args.solo:
            continue
        illustrazioni = trova_illustrazioni(args.illustrazioni, carta.get("illustrazione", ""))
        if not illustrazioni:
            print(f"manca l'illustrazione per {carta['codice']} ({carta.get('illustrazione', '')}): la salto")
            saltate += 1
            continue
        for variante, percorso in illustrazioni:
            destinazione = os.path.join(args.uscita, nome_file(carta, variante))
            if os.path.exists(destinazione) and not args.sovrascrivi:
                print(f"già presente, la lascio così: {os.path.basename(destinazione)}")
                saltate += 1
                continue
            try:
                if variante.startswith("FULL"):
                    componi_full_art_alt(carta, percorso).save(destinazione)
                else:
                    componi(carta, args.cornici, percorso).save(destinazione)
                print(f"creata: {os.path.basename(destinazione)}")
                fatte += 1
            except (OSError, ValueError, KeyError) as errore:
                print(f"errore su {carta.get('codice', '?')} {variante}: {errore}")
                errori += 1
    print(f"\nCarte create: {fatte} · saltate: {saltate} · errori: {errori}")


if __name__ == "__main__":
    main()
