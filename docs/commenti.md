# Formattazione dei commenti

## Principio

Il codice dice **cosa** fa; il commento dice **perché**. Se un commento ripete il codice, va tolto. Se il codice ha bisogno di un commento per essere capito, prima prova a rinominare variabili e metodi.

```java
// ❌ Ripete il codice
// incrementa il turno di 1
turn++;

// ❌ Compensa un nome poco chiaro
// x è il danno totale
int x = a + b;

// ✅ Spiega il perché, che dal codice non si vede
// La difesa danneggiata resta tale nei turni successivi (regola del brief)
defender.reduceDefense(damage);
```

## Javadoc

Obbligatorio per:
- tutte le classi pubbliche;
- i metodi pubblici di service e motore di gioco;
- i metodi la cui logica non è evidente.

Non serve per getter, setter e metodi ovvi.

Formato:
1. Prima frase: cosa fa, al presente indicativo, terza persona ("Calcola...", "Restituisce...").
2. Eventuale paragrafo `<p>` con regole o dettagli.
3. `@param` per ogni parametro, `@return` se non è `void`, `@throws` per ogni eccezione prevista.

```java
/**
 * Calcola il danno che una carta attaccante infligge a una carta in difesa.
 *
 * <p>Il danno base è l'attacco dell'attaccante. Se la sua fazione è avvantaggiata
 * su quella del difensore, si aggiunge il bonus di fazione definito in {@link GameRules}.
 *
 * @param attacker la carta che attacca, non {@code null}
 * @param defender la carta che difende, non {@code null}
 * @return il danno inflitto, sempre maggiore o uguale a zero
 * @throws IllegalArgumentException se una delle due carte è {@code null}
 */
public int calculateDamage(BattleCard attacker, BattleCard defender) {
    // ...
}
```

Javadoc di classe:

```java
/**
 * Simula una partita completa tra due mazzi e ne restituisce l'esito turno per turno.
 *
 * <p>La classe non accede al database: riceve i mazzi già caricati e un
 * {@link java.util.Random} esterno, così la stessa partita è riproducibile nei test.
 *
 * @see GameRules
 * @see BattleResult
 */
public class BattleEngine {
    // ...
}
```

## Commenti su una riga

- `//` seguito da **uno spazio**, iniziale maiuscola, niente punto finale se è una frase sola.
- Sopra la riga a cui si riferiscono, non in fondo (tranne note brevissime su campi o record).

```java
// ✅
// Pareggio se entrambi i giocatori arrivano a zero nello stesso turno
if (first.isDefeated() && second.isDefeated()) {
    return BattleResult.draw(turns);
}

// ❌
if (first.isDefeated() && second.isDefeated()) { //pareggio
```

## Etichette

Ogni etichetta ha il nome di chi la scrive e, se c'è, il numero della issue.

| Etichetta | Uso |
|-----------|-----|
| `TODO(nome)` | Lavoro da fare, il codice funziona ma è incompleto |
| `FIXME(nome)` | Bug noto o soluzione provvisoria da correggere |
| `NOTE` | Informazione importante per chi leggerà il codice |

```java
// TODO(nicolas): sostituire con il valore definitivo dopo COM-04 (#18)
private static final int DECK_SIZE = 20;

// FIXME(marco): se entrambi i mazzi finiscono la partita non termina (#23)

// NOTE: l'ordine Dreams → Memories → Nightmares → Dreams è un'ipotesi da testare
```

❌ `// TODO sistemare` · ❌ `// ??? non so perché funziona` · ❌ codice vecchio commentato

> **Niente codice commentato.** Se un pezzo di codice non serve più si cancella: resta comunque nella cronologia di Git.

## Commenti in altri linguaggi

> Gli esempi HTML, CSS e JavaScript sono indicativi: il team WMD li adatterà alle tecnologie scelte per il frontend.

```html
<!-- Sezione: griglia della collezione (WMD-05) -->
```

```css
/* ==========================================================
   Card · stile base comune a tutte le rarità
   ========================================================== */
.card { ... }

/* Rarità rara: bordo distintivo, vedi moodboard WMD-02 */
.card--rare { ... }
```

```javascript
/**
 * Carica la collezione dell'utente e la mostra nella griglia.
 * @param {string} rarity - filtro per rarità, oppure "all"
 * @returns {Promise<void>}
 */
async function loadCollection(rarity) { ... }
```

```sql
-- Una riga per ogni copia posseduta: quantity indica quante copie ha l'utente
CREATE TABLE user_cards (
    id       BIGINT AUTO_INCREMENT PRIMARY KEY,
    user_id  BIGINT NOT NULL,
    card_id  BIGINT NOT NULL,
    quantity INT    NOT NULL DEFAULT 1,
    CONSTRAINT fk_user_cards_user FOREIGN KEY (user_id) REFERENCES users (id),
    CONSTRAINT fk_user_cards_card FOREIGN KEY (card_id) REFERENCES cards (id)
);
```
