# Template

> I template di issue e PR conviene salvarli anche in `.github/ISSUE_TEMPLATE/` e `.github/pull_request_template.md`, così GitHub li propone in automatico.

## Template: Issue (task)

```markdown
## Descrizione
Cosa va fatto, in 2–3 frasi.

## Obiettivo / risultato atteso
- [ ] Primo risultato verificabile
- [ ] Secondo risultato verificabile

## Riferimenti
- Task del piano: SWD-02
- Decisione collegata: docs/decisioni/003-fazioni-e-bonus.md
- Dipende da: #numero

## Note
Dubbi, vincoli, cose da chiedere.
```

**Esempio compilato**

```markdown
Titolo: [SWD] Implementare il calcolo del bonus di fazione

## Descrizione
Il motore deve aggiungere il bonus di attacco quando la fazione dell'attaccante
è avvantaggiata su quella del difensore.

## Obiettivo / risultato atteso
- [ ] Metodo `hasAdvantageOver(Faction other)` in `Faction`
- [ ] `DamageCalculator` applica `factionBonusAttack` da `GameRules`
- [ ] Test JUnit per caso avvantaggiato, svantaggiato e stessa fazione

## Riferimenti
- Task del piano: SWD-02
- Decisione collegata: docs/decisioni/003-fazioni-e-bonus.md

## Note
Il valore del bonus (+1) è un'ipotesi: deve restare configurabile.
```

## Template: Bug

```markdown
## Cosa succede
Descrizione del problema.

## Come riprodurlo
1. Vai su ...
2. Clicca su ...
3. Vedi l'errore ...

## Cosa dovrebbe succedere
Comportamento atteso.

## Contesto
- Branch / commit:
- Browser o ambiente:
- Screenshot o log:
```

## Template: Pull Request

```markdown
## Cosa cambia
Breve descrizione delle modifiche.

## Issue collegata
Closes #numero

## Come verificare
1. Avvia ...
2. Esegui ...
3. Controlla che ...

## Checklist
- [ ] Il codice segue le linee guida in `docs/` (naming, commenti, formattazione)
- [ ] I test passano e ho aggiunto test per le parti nuove
- [ ] Ho aggiornato la documentazione (Javadoc, docs/api, docs/decisioni)
- [ ] Nessuna credenziale o file generato nel commit

## Screenshot (se ci sono modifiche grafiche)
```

## Template: Messaggio di commit

```
tipo(ambito): descrizione breve al presente (#numero-issue)

Spiegazione facoltativa: perché questa modifica serve
e cosa cambia, se non è evidente dal titolo.
```

```
feat(engine): aggiunge bonus di fazione al calcolo del danno (#12)

Il bonus si legge da GameRules così si può cambiare dopo il bilanciamento
di COM-04 senza toccare il motore.
```

## Template: Classe del motore di gioco

```java
package it.gruppo5.tcg.engine;

import java.util.Objects;

/**
 * Calcola il danno inflitto tra due carte durante uno scontro.
 *
 * <p>Non ha stato interno: tutti i valori arrivano da {@link GameRules}.
 */
public class DamageCalculator {

    private final GameRules rules;

    public DamageCalculator(GameRules rules) {
        this.rules = Objects.requireNonNull(rules, "rules");
    }

    /**
     * Calcola il danno che l'attaccante infligge al difensore.
     *
     * @param attacker la carta che attacca, non {@code null}
     * @param defender la carta che difende, non {@code null}
     * @return il danno inflitto, sempre maggiore o uguale a zero
     */
    public int calculateDamage(BattleCard attacker, BattleCard defender) {
        Objects.requireNonNull(attacker, "attacker");
        Objects.requireNonNull(defender, "defender");

        int attack = attacker.attack();
        if (attacker.faction().hasAdvantageOver(defender.faction())) {
            attack += rules.factionBonusAttack();
        }
        return Math.max(0, attack);
    }
}
```

## Template: Service Spring

```java
package it.gruppo5.tcg.deck;

import it.gruppo5.tcg.deck.dto.DeckRequest;
import it.gruppo5.tcg.deck.dto.DeckResponse;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

/**
 * Gestisce creazione, modifica e validazione dei mazzi degli utenti.
 */
@Service
public class DeckService {

    private final DeckRepository deckRepository;

    public DeckService(DeckRepository deckRepository) {
        this.deckRepository = deckRepository;
    }

    /**
     * Crea un nuovo mazzo dopo averne verificato la validità.
     *
     * @param request i dati del mazzo da creare
     * @return il mazzo salvato
     * @throws InvalidDeckException se il mazzo non rispetta le regole
     */
    @Transactional
    public DeckResponse createDeck(DeckRequest request) {
        // ...
    }
}
```

## Template: Test JUnit

```java
package it.gruppo5.tcg.engine;

import static org.junit.jupiter.api.Assertions.assertEquals;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

class DamageCalculatorTest {

    private DamageCalculator calculator;

    @BeforeEach
    void setUp() {
        GameRules rules = new GameRules(20, 20, 2, 1);
        calculator = new DamageCalculator(rules);
    }

    @Test
    void calculateDamage_attackerHasFactionAdvantage_addsBonus() {
        // Given
        BattleCard attacker = new BattleCard("A", 4, 3, Faction.DREAMS);
        BattleCard defender = new BattleCard("B", 2, 5, Faction.MEMORIES);

        // When
        int damage = calculator.calculateDamage(attacker, defender);

        // Then
        assertEquals(5, damage);
    }

    @Test
    void calculateDamage_sameFaction_noBonus() {
        // Given
        BattleCard attacker = new BattleCard("A", 4, 3, Faction.DREAMS);
        BattleCard defender = new BattleCard("B", 2, 5, Faction.DREAMS);

        // When
        int damage = calculator.calculateDamage(attacker, defender);

        // Then
        assertEquals(4, damage);
    }
}
```

> Le fazioni nell'esempio sono quelle di Dreamscape: Dreams, Nightmares e Memories.

## Template: Decisione (`docs/decisioni/NNN-titolo.md`)

```markdown
# 003 · Fazioni e bonus

- **Data:** 2026-10-26
- **Stato:** proposta | approvata | sostituita da NNN
- **Referenti:** Nicolas, Valerio
- **Task:** COM-02

## Contesto
Perché serviva decidere e quali erano i vincoli.

## Opzioni valutate
1. Opzione A: pro / contro
2. Opzione B: pro / contro

## Decisione
Cosa si è scelto.

## Motivazione
Perché si è scelto questo.

## Conseguenze
Cosa cambia per SWD, WMD, DGS. Cosa resta aperto.
```

## Template: Verbale (`docs/verbali/AAAA-MM-GG-argomento.md`)

```markdown
# Verbale · 26/10/2026 · Scelta del concept

- **Presenti:**
- **Assenti:**
- **Verbalizzante:**

## Ordine del giorno
1. ...
2. ...

## Decisioni prese
- ... (→ docs/decisioni/NNN-...)

## Azioni
| Cosa | Chi | Entro |
|------|-----|-------|
| ... | ... | ... |

## Punti aperti / domande per il cliente
- ...
```

## Template: README di modulo (`engine/README.md`, `backend/README.md`...)

````markdown
# Nome modulo

Cosa fa il modulo, in una o due frasi.

## Requisiti
- Java 17+
- Maven 3.9+

## Avvio
```bash
mvn spring-boot:run
```

## Test
```bash
mvn test
```

## Configurazione
| Variabile | Descrizione | Esempio |
|-----------|-------------|---------|
| `DB_URL` | URL del database PostgreSQL | `jdbc:postgresql://localhost:5432/dreamscape` |

## Struttura
Breve descrizione dei package principali.
````

## `.editorconfig`

Da salvare nella radice del repository.

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 4
max_line_length = 120

[*.{html,css,js,json,yml,yaml}]
indent_size = 2

[*.md]
trim_trailing_whitespace = false
```
