# Regole generali per il codice

Regole valide per tutto il codice del progetto. Per i nomi vedi [naming.md](naming.md), per i commenti [commenti.md](commenti.md).

## Organizzazione dei package del backend

Il package base è `it.gruppo5.tcg`. Il nome è neutro (come `Card`, `Faction`, `Deck`) e non va cambiato se cambia il tema del gioco.

I package del backend sono divisi **per funzionalità** (`deck/`, `trade/`...), non per tipo (`controllers/`, `services/`...). Dentro ogni package ci sono controller, service, repository, entità e DTO di quella funzionalità.

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

## Lingua

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

## Formattazione

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

Il file `.editorconfig` (vedi [template.md](template.md#editorconfig)) applica queste regole in automatico in IntelliJ, Eclipse e VS Code.

## Motore di gioco (`engine/`)

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

## Backend (`backend/`)

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

## Database

- Le modifiche allo schema si fanno con **script SQL versionati** in `database/` (o con lo strumento di migrazione scelto), mai a mano solo sul proprio PC.
- Ogni tabella ha una chiave primaria `id` (`BIGINT AUTO_INCREMENT`).
- Le relazioni hanno sempre la foreign key dichiarata.
- I dati di prova stanno in uno script separato (`database/seed/`).

## Frontend

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

## Sicurezza e file da non caricare

- **Mai** caricare password, chiavi o credenziali del database. Si usa `application-local.properties` (in `.gitignore`) o variabili d'ambiente.
- Le password degli utenti si salvano solo con hash (es. BCrypt).
- Non si caricano: cartelle `target/`, `build/`, `node_modules/`, `.idea/`, `.vscode/`, file `.DS_Store`.

## Test

- Il motore ha test JUnit per ogni regola; il backend almeno per i service.
- Un test controlla **un solo comportamento**.
- Struttura **Given / When / Then** (prepara, esegui, verifica).
- Prima di aprire una PR, tutti i test devono passare.
