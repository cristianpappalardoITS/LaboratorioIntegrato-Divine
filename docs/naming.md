# Naming

## Java

| Elemento | Convenzione | ✅ Esempio | ❌ Da evitare |
|----------|-------------|-----------|---------------|
| Package | minuscolo, una parola | `it.gruppo5.tcg.deck` | `it.Gruppo5.TCG.Deck_Manager` |
| Classe | `PascalCase`, sostantivo | `DeckService`, `BattleEngine` | `deckservice`, `GestisciMazzi` |
| Interfaccia | `PascalCase`, senza prefisso `I` | `CardRepository` | `ICardRepository` |
| Metodo | `camelCase`, verbo | `calculateDamage()`, `openPack()` | `damage()`, `Calcola()` |
| Metodo booleano | `is` / `has` / `can` | `isValid()`, `hasFactionAdvantage()` | `valid()`, `checkAdvantage()` |
| Variabile | `camelCase`, descrittiva | `remainingLifePoints` | `rlp`, `x`, `temp2` |
| Costante | `UPPER_SNAKE_CASE` | `MAX_COPIES_PER_CARD` | `maxCopies`, `MAXCOPIES` |
| Enum e valori | `PascalCase` / `UPPER_SNAKE_CASE` | `Rarity.COMMON` | `rarity.common` |
| Eccezione | finisce con `Exception` | `DeckNotFoundException` | `DeckError` |
| Test | classe + `Test` | `DamageCalculatorTest` | `TestDanno`, `Prova` |

Suffissi per ruolo:

| Ruolo | Suffisso | Esempio |
|-------|----------|---------|
| Controller REST | `Controller` | `TradeController` |
| Service | `Service` | `TradeService` |
| Repository | `Repository` | `TradeRepository` |
| DTO in ingresso | `Request` | `TradeOfferRequest` |
| DTO in uscita | `Response` | `TradeOfferResponse` |
| Entità JPA | nessuno | `Trade`, `Card`, `User` |

**Nomi dei test:** `metodo_condizione_risultatoAtteso`

```java
@Test
void calculateDamage_attackerHasFactionAdvantage_addsBonus() { ... }

@Test
void addCard_thirdCopyOfSameCard_throwsException() { ... }
```

## Database (PostgreSQL)

| Elemento | Convenzione | ✅ Esempio | ❌ Da evitare |
|----------|-------------|-----------|---------------|
| Tabella | `snake_case`, plurale | `cards`, `user_cards`, `trade_offers` | `Card`, `tblCarte`, `userCard` |
| Colonna | `snake_case` | `attack_points`, `created_at` | `AttackPoints`, `att` |
| Chiave primaria | `id` | `id` | `card_id` nella tabella `cards` |
| Chiave esterna | `tabella_singolare_id` | `user_id`, `deck_id` | `utente`, `fk1` |
| Booleano | `is_` / `has_` | `is_active` | `active_flag` |
| Data/ora | `_at` | `created_at`, `played_at` | `data`, `timestamp1` |
| Indice | `idx_tabella_colonna` | `idx_cards_rarity` | `index1` |

```java
@Entity
@Table(name = "user_cards")
public class UserCard {

    // Chiave UUID v7 generata da Hibernate (Spring Boot 4) prima del salvataggio
    @Id
    @UuidGenerator(style = UuidGenerator.Style.VERSION_7)
    private UUID id;

    @ManyToOne(optional = false)
    @JoinColumn(name = "user_id")
    private User user;

    @Column(name = "quantity", nullable = false)
    private int quantity;
}
```

## API REST

- Prefisso `/api/v1/`.
- Risorse al **plurale**, in **kebab-case**, senza verbi nell'URL: il verbo è il metodo HTTP.
- Parametri JSON in `camelCase`.

| Azione | ✅ Corretto | ❌ Da evitare |
|--------|------------|---------------|
| Lista mazzi dell'utente | `GET /api/v1/decks` | `GET /api/v1/getDecks` |
| Dettaglio mazzo | `GET /api/v1/decks/{deckId}` | `GET /api/v1/deck?id=5` |
| Crea mazzo | `POST /api/v1/decks` | `POST /api/v1/createDeck` |
| Modifica mazzo | `PUT /api/v1/decks/{deckId}` | `POST /api/v1/updateDeck` |
| Elimina mazzo | `DELETE /api/v1/decks/{deckId}` | `GET /api/v1/deleteDeck/5` |
| Apri un pacchetto | `POST /api/v1/packs/{packId}/open` | `GET /api/v1/apriPacchetto` |
| Offerte di scambio | `GET /api/v1/trade-offers` | `GET /api/v1/tradeOffers` |

```json
{
  "deckId": 12,
  "name": "Mazzo offensivo",
  "cardIds": [3, 3, 7, 15]
}
```

## Frontend

Tecnologie: HTML, CSS e JavaScript.

> 🚧 **Da completare a cura del team WMD.**
>
> Da indicare, con esempi ✅/❌ come nelle altre sezioni:
> - Nomi di file e cartelle
> - Nomi delle pagine HTML e dei file JavaScript
> - Nomi di classi CSS (es. BEM o altra convenzione)
> - Nomi di variabili, funzioni e costanti

## File di documentazione

| Tipo | Formato | Esempio |
|------|---------|---------|
| Decisione | `NNN-titolo-breve.md` | `docs/decisioni/003-fazioni-e-bonus.md` |
| Verbale | `AAAA-MM-GG-argomento.md` | `docs/verbali/2026-10-26-scelta-concept.md` |
| Diagramma | `kebab-case` + formato | `docs/diagrammi/er-database.png` |
