# LaboratorioIntegrato-Divine

Progetto Laboratorio Integrato · Gruppo 5

Gioco di carte collezionabili digitale (TCG): gli utenti si registrano, ricevono crediti virtuali, comprano pacchetti di carte, gestiscono collezione e mazzi, scambiano carte e si sfidano in battaglie simulate dal server.

> **Stato del concept:** il tema non è ancora definitivo. Le proposte sono **Divine** (mitologia) e **Dreams & Nightmares** (sogni, incubi, ricordi). Per questo nel codice usiamo nomi neutri (`Card`, `Faction`, `Deck`...) e il package base `it.gruppo5.tcg`, che non va cambiato se cambia il tema.

---

## Indice

1. [Il progetto in breve](#1-il-progetto-in-breve)
2. [Struttura del repository](#2-struttura-del-repository)
3. [Flusso di lavoro su GitHub](#3-flusso-di-lavoro-su-github)
4. [Regole generali per il codice](#4-regole-generali-per-il-codice)
5. [Naming](#5-naming)
6. [Formattazione dei commenti](#6-formattazione-dei-commenti)
7. [Documentazione](#7-documentazione)
8. [Template](#8-template)
9. [Checklist prima di aprire una Pull Request](#9-checklist-prima-di-aprire-una-pull-request)

---

## 1. Il progetto in breve

### Team

| Team | Membri | Ambito |
|------|--------|--------|
| **SWD** · Software Developer | Cristian (TL), Marco (Vice TL), Nicolas | Motore di gioco, backend, database, API |
| **WMD** · Web Developer | Gaia (TL), Alessandro, Daniele, Yuri | Sitemap, UX/UI, wireframe, frontend |
| **DGS** · Digital Strategist | Sara (TL), Valerio, Maie | Concept, lore, economia di gioco, marketing |

Le decisioni finali dei task comuni (COM-xx) vanno comunicate a **Marco** o **Cristian**, che le registrano in `docs/decisioni/`.

### Stack

| Livello | Tecnologia |
|---------|------------|
| Motore di gioco | Java, modulo **isolato** (nessuna dipendenza da Spring o dal database), test **JUnit** |
| Backend / portale | Java + **Spring Boot**, Spring Data **JPA** |
| Database | **MySQL** |
| Frontend | 🚧 **Da definire** (scelta del team WMD, vedi [Frontend](#frontend)) |
| Gestione progetto | **GitHub Projects** |

> Il pagamento con denaro reale **non** si sviluppa nella fase 1: i crediti sono solo virtuali.

### Scadenze

| Data | Milestone |
|------|-----------|
| 19/10 | Kick-off |
| 26/10 | Presentazione delle prime bozze |
| 02/11 | Primo incontro con il cliente |
| 23/11 | SAL (stato avanzamento lavori) |
| 10/12 | Presentazione finale |

---

## 2. Struttura del repository

```
LaboratorioIntegrato-Divine/
├── engine/                  # Motore di gioco Java puro + test JUnit
│   └── src/
│       ├── main/java/it/gruppo5/tcg/engine/
│       └── test/java/it/gruppo5/tcg/engine/
├── backend/                 # Applicazione Spring Boot (portale + API REST)
│   └── src/main/java/it/gruppo5/tcg/
│       ├── user/            # un package per modulo funzionale
│       ├── card/
│       ├── pack/
│       ├── deck/
│       ├── trade/
│       ├── challenge/
│       └── common/          # eccezioni, configurazione, utility condivise
├── frontend/                # Frontend (struttura da definire con le tecnologie scelte)
├── database/                # Script SQL, migrazioni, dati di prova
├── docs/
│   ├── decisioni/           # Decisioni prese dal gruppo (una per file)
│   ├── verbali/             # Verbali delle riunioni
│   ├── api/                 # Elenco endpoint REST
│   └── diagrammi/           # ER, architettura, flussi
└── .github/                 # Template di issue e pull request
```

**Regola:** i package del backend sono divisi **per funzionalità** (`deck/`, `trade/`...), non per tipo (`controllers/`, `services/`...). Dentro ogni package ci sono controller, service, repository, entità e DTO di quella funzionalità.

```
deck/
├── DeckController.java
├── DeckService.java
├── DeckRepository.java
├── Deck.java                # entità JPA
├── DeckCard.java            # entità JPA (tabella di relazione)
└── dto/
    ├── DeckRequest.java
    └── DeckResponse.java
```

---

## 3. Flusso di lavoro su GitHub

### Board di GitHub Projects

| Colonna | Significato |
|---------|-------------|
| **Backlog** | Idee e lavoro futuro, non ancora pianificato |
| **To Do** | Pianificato e assegnato, si può iniziare |
| **In Progress** | Qualcuno ci sta lavorando (massimo 2 issue a testa) |
| **Review** | Pull request aperta, in attesa di revisione |
| **Done** | PR approvata e unita in `develop` |

### Issue

- Ogni attività ha una issue **prima** di iniziare a scrivere codice.
- Il titolo inizia con il codice del team e un verbo all'infinito.
- Ogni issue ha: un assegnatario, almeno un'etichetta di team, una priorità.

| Etichetta | Valori |
|-----------|--------|
| Team | `team: SWD`, `team: WMD`, `team: DGS`, `team: COM` |
| Tipo | `tipo: feature`, `tipo: bug`, `tipo: docs`, `tipo: refactor`, `tipo: test` |
| Priorità | `priorità: alta`, `priorità: media`, `priorità: bassa` |

✅ `[SWD] Implementare il calcolo del bonus di fazione`
✅ `[WMD] Disegnare il wireframe della pagina collezione`
❌ `bonus` · ❌ `fix vari` · ❌ `Lavoro di Marco`

### Branch

| Branch | Uso |
|--------|-----|
| `main` | Versione stabile, consegnabile. **Protetto:** si aggiorna solo da `develop` tramite PR. |
| `develop` | Integrazione del lavoro di tutti. **Protetto:** si aggiorna solo tramite PR. |
| `tipo/numero-issue-descrizione` | Un branch per ogni issue, creato da `develop`. |

Tipi ammessi: `feature`, `fix`, `docs`, `refactor`, `test`, `chore`.

✅ `feature/12-bonus-fazione`
✅ `fix/31-mazzo-salvato-senza-carte`
✅ `docs/8-diagramma-er`
❌ `marco` · ❌ `prova2` · ❌ `Feature/BonusFazione` · ❌ `nuovo_branch`

```bash
git switch develop
git pull
git switch -c feature/12-bonus-fazione
```

### Commit

Usiamo il formato [Conventional Commits](https://www.conventionalcommits.org/it/): il **tipo** in inglese, la **descrizione** in italiano, al presente, senza punto finale, massimo ~70 caratteri.

```
tipo(ambito): descrizione breve (#numero-issue)
```

| Tipo | Quando |
|------|--------|
| `feat` | Nuova funzionalità |
| `fix` | Correzione di un bug |
| `docs` | Solo documentazione |
| `test` | Aggiunta o modifica di test |
| `refactor` | Modifica del codice che non cambia il comportamento |
| `style` | Formattazione, spazi, nessuna modifica di logica |
| `chore` | Configurazione, dipendenze, build |

Ambiti consigliati: `engine`, `user`, `card`, `pack`, `deck`, `trade`, `challenge`, `db`, `frontend`, `docs`.

✅ `feat(engine): aggiunge bonus di fazione al calcolo del danno (#12)`
✅ `fix(deck): impedisce di salvare un mazzo con più di 2 copie (#31)`
✅ `docs(db): aggiorna il diagramma ER con la tabella trades (#8)`
❌ `modifiche` · ❌ `fix` · ❌ `ho sistemato un po' di cose nel deck e anche il login`

Un commit = una modifica logica. Se nella descrizione serve una "e", probabilmente sono due commit.

### Pull Request

- Si apre una PR da `feature/...` verso `develop`.
- Serve **almeno 1 approvazione** di un altro membro del team prima del merge.
- Il titolo segue lo stesso formato dei commit.
- La descrizione usa il [template PR](#template-pull-request) e collega la issue con `Closes #12` (la issue si chiude da sola al merge).
- Chi apre la PR non la approva da solo. Chi la revisiona commenta in modo concreto ("qui manca il controllo sul null") e non generico ("non mi piace").
- Dopo il merge, il branch si cancella.

---

## 4. Regole generali per il codice

### Lingua

| Cosa | Lingua |
|------|--------|
| Nomi di classi, metodi, variabili, tabelle, endpoint | **Inglese** |
| Commenti, Javadoc, documentazione, issue, PR | **Italiano** |
| Tipo del commit (`feat`, `fix`...) | Inglese |
| Descrizione del commit | Italiano |

```java
// ✅ Nome in inglese, commento in italiano
// Il danno non può essere negativo anche con modificatori futuri
int damage = Math.max(0, attack - shield);

// ❌ Nomi misti
int dannoTotale = calcolaDamage(cartaAttacker);
```

### Formattazione

- Codifica **UTF-8**, fine riga **LF**.
- Indentazione: **4 spazi** per Java e SQL, **2 spazi** per HTML, CSS, JS, JSON, YAML. Mai tab.
- Lunghezza massima della riga: **120 caratteri**.
- Parentesi graffe sempre, anche per `if` di una riga.
- Una classe pubblica per file.
- Niente import con `*`; niente import inutilizzati.

```java
// ✅
if (deck.isEmpty()) {
    return BattleResult.draw();
}

// ❌
if (deck.isEmpty()) return BattleResult.draw();
```

Il file [`.editorconfig`](#editorconfig) (vedi Template) applica queste regole in automatico in IntelliJ, Eclipse e VS Code.

### Motore di gioco (`engine/`)

- È **Java puro**: nessuna dipendenza da Spring, JPA, MySQL o HTTP. Il backend lo usa, non il contrario.
- Riceve dati in ingresso (mazzi, carte, configurazione) e restituisce un risultato (vincitore, turni). Non legge né scrive sul database.
- **Deterministico e testabile:** il mescolamento usa un `Random` passato dall'esterno, così nei test si usa un seed fisso e il risultato è sempre lo stesso.
- I valori di gioco (punti vita, carte per mazzo, copie massime, bonus di fazione) stanno in **una sola classe di configurazione**, non sparsi nel codice. Sono ancora in discussione e cambieranno.
- Ogni regola del regolamento ha almeno un test JUnit.

```java
// ✅ Il Random arriva da fuori: nei test si passa new Random(42)
public BattleResult simulate(DeckSnapshot first, DeckSnapshot second, Random random) { ... }

// ❌ Random nascosto dentro: impossibile riprodurre una partita nei test
public BattleResult simulate(DeckSnapshot first, DeckSnapshot second) {
    Collections.shuffle(cards); // usa un Random interno
}
```

```java
// ✅ Valori in un unico punto
public record GameRules(
        int playerLifePoints,     // ipotesi attuale: 20
        int deckSize,             // ipotesi attuale: 20
        int maxCopiesPerCard,     // ipotesi attuale: 2
        int factionBonusAttack    // ipotesi attuale: +1
) { }

// ❌ Numeri magici sparsi
if (deck.size() != 20) { ... }
life -= damage + 1;
```

### Backend (`backend/`)

- Struttura a livelli: **Controller → Service → Repository**.
  - Il **controller** riceve la richiesta, valida l'input, chiama il service, restituisce la risposta. Niente logica di business.
  - Il **service** contiene la logica e le transazioni (`@Transactional`).
  - Il **repository** accede al database e basta.
- Le **entità JPA non escono mai dalle API**: si usano DTO (`DeckRequest`, `DeckResponse`).
- Dependency injection **tramite costruttore**, mai `@Autowired` sui campi.
- Validazione dell'input con `@Valid` e annotazioni (`@NotBlank`, `@Size`...).
- Gli errori si lanciano come eccezioni specifiche (`DeckNotFoundException`) e si gestiscono in un unico `@RestControllerAdvice`.
- Il **mescolamento dei mazzi e la simulazione avvengono solo lato server**. Il client non decide mai l'esito di una partita né il contenuto di un pacchetto.
- I crediti sono numeri **interi** (`int`/`long`), mai `double` o `float`.

```java
// ✅ Iniezione via costruttore, logica nel service
@RestController
@RequestMapping("/api/v1/decks")
public class DeckController {

    private final DeckService deckService;

    public DeckController(DeckService deckService) {
        this.deckService = deckService;
    }

    @PostMapping
    public ResponseEntity<DeckResponse> createDeck(@Valid @RequestBody DeckRequest request) {
        DeckResponse created = deckService.createDeck(request);
        return ResponseEntity.status(HttpStatus.CREATED).body(created);
    }
}

// ❌ Campo @Autowired, logica e accesso al DB nel controller, entità restituita
@RestController
public class DeckController {
    @Autowired
    private DeckRepository repo;

    @PostMapping("/createDeck")
    public Deck create(@RequestBody Deck deck) {
        if (deck.getCards().size() != 20) { ... }
        return repo.save(deck);
    }
}
```

### Database

- Le modifiche allo schema si fanno con **script SQL versionati** in `database/` (o con lo strumento di migrazione scelto), mai a mano solo sul proprio PC.
- Ogni tabella ha una chiave primaria `id` (`BIGINT AUTO_INCREMENT`).
- Le relazioni hanno sempre la foreign key dichiarata.
- I dati di prova stanno in uno script separato (`database/seed/`).

### Frontend

> 🚧 **Sezione da completare a cura del team WMD** quando verranno scelte le tecnologie.
>
> Da indicare:
> - Tecnologie scelte (framework/librerie, linguaggio, gestione degli stili) e motivazione
> - Struttura delle cartelle in `frontend/`
> - Come avviare il frontend in locale e come si collega al backend
> - Regole di codice specifiche (componenti, stili, gestione delle chiamate alle API)
> - Strumenti di formattazione e lint, se usati
>
> Riferimento: il brief del Laboratorio Integrato. La scelta va registrata anche in `docs/decisioni/`.

Regole che valgono comunque, qualunque tecnologia si scelga:

- Le statistiche delle carte (ATT, DIF, fazione, rarità) devono essere **leggibili anche su mobile**.
- Le chiamate alle API passano da un unico punto, non sparse nelle pagine.
- Il frontend non decide mai l'esito di una partita né il contenuto di un pacchetto: mostra solo quello che restituisce il server.

### Sicurezza e file da non caricare

- **Mai** caricare password, chiavi o credenziali del database. Si usa `application-local.properties` (in `.gitignore`) o variabili d'ambiente.
- Le password degli utenti si salvano solo con hash (es. BCrypt).
- Non si caricano: cartelle `target/`, `build/`, `node_modules/`, `.idea/`, `.vscode/`, file `.DS_Store`.

### Test

- Il motore ha test JUnit per ogni regola; il backend almeno per i service.
- Un test controlla **un solo comportamento**.
- Struttura **Given / When / Then** (prepara, esegui, verifica).
- Prima di aprire una PR, tutti i test devono passare.

---

## 5. Naming

### Java

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

### Database (MySQL)

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

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(optional = false)
    @JoinColumn(name = "user_id")
    private User user;

    @Column(name = "quantity", nullable = false)
    private int quantity;
}
```

### API REST

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

### Frontend

> 🚧 **Da completare a cura del team WMD** dopo la scelta delle tecnologie.
>
> Da indicare, con esempi ✅/❌ come nelle altre sezioni:
> - Nomi di file e cartelle
> - Nomi di componenti/pagine (se si usa un framework)
> - Nomi di classi CSS (es. BEM o altra convenzione)
> - Nomi di variabili, funzioni e costanti

### File di documentazione

| Tipo | Formato | Esempio |
|------|---------|---------|
| Decisione | `NNN-titolo-breve.md` | `docs/decisioni/003-fazioni-e-bonus.md` |
| Verbale | `AAAA-MM-GG-argomento.md` | `docs/verbali/2026-10-26-scelta-concept.md` |
| Diagramma | `kebab-case` + formato | `docs/diagrammi/er-database.png` |

---

## 6. Formattazione dei commenti

### Principio

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

### Javadoc

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

### Commenti su una riga

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

### Etichette

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

### Commenti in altri linguaggi

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

---

## 7. Documentazione

### Cosa documentare e dove

| Cosa | Dove | Chi lo aggiorna |
|------|------|-----------------|
| Panoramica e regole del progetto | Questo `README.md` | Marco / Cristian |
| Come avviare e usare un modulo | `README.md` dentro `engine/`, `backend/`, `frontend/` | Chi lavora sul modulo |
| Classi e metodi | Javadoc nel codice | Chi scrive il codice |
| Endpoint REST | `docs/api/endpoints.md` | Chi crea o modifica l'endpoint |
| Decisioni del gruppo (concept, fazioni, valori di gioco...) | `docs/decisioni/` | Marco / Cristian, su comunicazione dei referenti |
| Riunioni | `docs/verbali/` | Chi fa da verbalizzante |
| Diagrammi ER, architettura, flussi | `docs/diagrammi/` | SWD (ER, architettura), WMD (flussi) |

### Regole

- **La documentazione si aggiorna nella stessa PR del codice.** Se cambi un endpoint, aggiorni `docs/api/endpoints.md` nella stessa PR.
- Si scrive in **Markdown** (`.md`), in italiano.
- Frasi brevi, tabelle ed esempi concreti al posto di paragrafi lunghi.
- Ogni decisione ha un file suo: chi arriva dopo deve capire **cosa** si è deciso e **perché**, senza dover chiedere.
- I valori ancora in discussione si segnano come tali ("ipotesi", "da verificare"), mai come definitivi.

### Esempio: documentazione di un endpoint

````markdown
### Crea un mazzo

`POST /api/v1/decks`

Crea un nuovo mazzo per l'utente autenticato. Le carte devono essere nella sua collezione.

**Body**

| Campo | Tipo | Obbligatorio | Note |
|-------|------|--------------|------|
| `name` | string | sì | 1–40 caratteri |
| `cardIds` | number[] | sì | Esattamente 20 carte, max 2 copie per carta |

**Esempio di richiesta**

```json
{ "name": "Mazzo offensivo", "cardIds": [3, 3, 7, 15, ...] }
```

**Risposte**

| Codice | Quando |
|--------|--------|
| `201 Created` | Mazzo creato, restituisce il `DeckResponse` |
| `400 Bad Request` | Numero di carte errato o più di 2 copie della stessa carta |
| `404 Not Found` | Una carta non è nella collezione dell'utente |
````

---

## 8. Template

> I template di issue e PR conviene salvarli anche in `.github/ISSUE_TEMPLATE/` e `.github/pull_request_template.md`, così GitHub li propone in automatico.

### Template: Issue (task)

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

### Template: Bug

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

### Template: Pull Request

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
- [ ] Il codice segue le regole del README (naming, commenti, formattazione)
- [ ] I test passano e ho aggiunto test per le parti nuove
- [ ] Ho aggiornato la documentazione (Javadoc, docs/api, docs/decisioni)
- [ ] Nessuna credenziale o file generato nel commit

## Screenshot (se ci sono modifiche grafiche)
```

### Template: Messaggio di commit

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

### Template: Classe del motore di gioco

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

### Template: Service Spring

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

### Template: Test JUnit

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

> Le fazioni nell'esempio sono quelle della proposta Dreams & Nightmares: vanno sostituite con quelle scelte in COM-02.

### Template: Decisione (`docs/decisioni/NNN-titolo.md`)

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

### Template: Verbale (`docs/verbali/AAAA-MM-GG-argomento.md`)

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

### Template: README di modulo (`engine/README.md`, `backend/README.md`...)

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
| `DB_URL` | URL del database MySQL | `jdbc:mysql://localhost:3306/tcg` |

## Struttura
Breve descrizione dei package principali.
````

### `.editorconfig`

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

---

## 9. Checklist prima di aprire una Pull Request

- [ ] Il branch parte da `develop` aggiornato e ha un nome tipo `feature/12-descrizione`
- [ ] I commit seguono il formato `tipo(ambito): descrizione (#issue)`
- [ ] Nomi in inglese, commenti e documentazione in italiano
- [ ] Javadoc su classi pubbliche e metodi pubblici non ovvi
- [ ] Niente codice commentato, niente `TODO` senza nome
- [ ] Niente numeri magici: i valori di gioco stanno in `GameRules`
- [ ] Il motore non dipende da Spring o dal database
- [ ] I test passano e le parti nuove hanno i loro test
- [ ] Documentazione aggiornata (`docs/api`, `docs/decisioni`, README di modulo)
- [ ] Nessuna password, chiave o file generato (`target/`, `node_modules/`...)
- [ ] La PR collega la issue con `Closes #numero`
