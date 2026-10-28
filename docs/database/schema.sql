-- ============================================================================
-- Schema del database di Dreamscape · PROPOSTA DA VERIFICARE (non ancora approvata)
-- PostgreSQL 18 o successivo (serve uuidv7())
--
-- Il file è diviso nelle future migration Flyway: ogni blocco "V#__nome"
-- diventerà un file in backend/src/main/resources/db/migration/.
-- Spiegazione delle scelte: docs/database/schema.md
-- Regolamento di riferimento: docs/proposte/proposta-regolamento-dreamscape.pdf
--
-- Regole comuni:
-- - Chiavi primarie e chiavi esterne: UUID v7 (ordinati nel tempo). Gli UUID non si
--   indovinano: si possono usare negli URL. In Java il campo è java.util.UUID e lo genera
--   Hibernate (Spring Boot 4) con @UuidGenerator(style = VERSION_7); il DEFAULT uuidv7()
--   serve alle migration con i dati e a chi scrive SQL a mano.
-- - PostgreSQL non indicizza da solo le colonne delle chiavi esterne: gli indici ci sono
--   dove si cerca per quella colonna.
-- - Date e ore: TIMESTAMPTZ, salvate in UTC.
-- - updated_at: lo aggiorna JPA (@UpdateTimestamp); PostgreSQL non ha ON UPDATE.
-- - Testi da cercare senza distinguere maiuscole (username, email): indici UNIQUE su LOWER().
-- ============================================================================


-- ============================================================================
-- V1__create_users_and_auth.sql
-- ============================================================================

-- I Dreamweaver (giocatori) e gli admin.
-- Gli utenti non si cancellano: si disattivano con is_enabled = FALSE.
-- Così storico di sfide e scambi resta sempre completo.
-- rating è il punteggio del rank (tipo Elo, si parte da 1000). Si usa solo quando
-- il rank viene attivato, dopo le funzionalità obbligatorie. Le leghe non si salvano:
-- si calcolano dal punteggio.
-- privacy_accepted_at / terms_accepted_at: quando il giocatore ha accettato Privacy Policy
-- e Termini di servizio alla registrazione. Obbligatori per i giocatori; l'admin, creato
-- all'avvio da variabili d'ambiente, non passa dalla registrazione.
CREATE TABLE users (
    id                  UUID        NOT NULL DEFAULT uuidv7(),
    username            VARCHAR(30)  NOT NULL,
    email               VARCHAR(255) NOT NULL,
    password_hash       VARCHAR(255) NOT NULL,
    role                VARCHAR(20)  NOT NULL DEFAULT 'PLAYER',
    credits             INT          NOT NULL DEFAULT 0,
    rating              INT          NOT NULL DEFAULT 1000,
    is_enabled          BOOLEAN      NOT NULL DEFAULT TRUE,
    privacy_accepted_at TIMESTAMPTZ  NULL,
    terms_accepted_at   TIMESTAMPTZ  NULL,
    last_login_at       TIMESTAMPTZ  NULL,
    created_at          TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at          TIMESTAMPTZ  NOT NULL DEFAULT now(),
    CONSTRAINT pk_users PRIMARY KEY (id),
    CONSTRAINT chk_users_role CHECK (role IN ('PLAYER', 'ADMIN')),
    CONSTRAINT chk_users_credits CHECK (credits >= 0),
    CONSTRAINT chk_users_rating CHECK (rating >= 0),
    CONSTRAINT chk_users_consents CHECK (role = 'ADMIN'
                                         OR (privacy_accepted_at IS NOT NULL AND terms_accepted_at IS NOT NULL))
);

-- Username ed email unici senza distinguere maiuscole e minuscole ("Marco" = "marco").
CREATE UNIQUE INDEX uq_users_username ON users (LOWER(username));
CREATE UNIQUE INDEX uq_users_email ON users (LOWER(email));

-- Accesso con token JWT: il token di accesso dura poco e non si salva;
-- il refresh token serve a ottenerne uno nuovo. Uno per dispositivo/sessione.
-- Si salva l'hash del token, mai il token in chiaro. revoked_at = logout o revoca.
CREATE TABLE refresh_tokens (
    id         UUID        NOT NULL DEFAULT uuidv7(),
    user_id    UUID        NOT NULL,
    token_hash CHAR(64)    NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    revoked_at TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT pk_refresh_tokens PRIMARY KEY (id),
    CONSTRAINT uq_refresh_tokens_token_hash UNIQUE (token_hash),
    CONSTRAINT fk_refresh_tokens_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Per revocare tutti i token di un utente (logout ovunque, cambio password).
CREATE INDEX idx_refresh_tokens_user ON refresh_tokens (user_id);

-- Recupero password: token monouso con scadenza (serve solo se il portale invia email).
CREATE TABLE password_reset_tokens (
    id         UUID        NOT NULL DEFAULT uuidv7(),
    user_id    UUID        NOT NULL,
    token_hash CHAR(64)    NOT NULL,
    expires_at TIMESTAMPTZ NOT NULL,
    used_at    TIMESTAMPTZ NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT pk_password_reset_tokens PRIMARY KEY (id),
    CONSTRAINT uq_password_reset_tokens_token_hash UNIQUE (token_hash),
    CONSTRAINT fk_password_reset_tokens_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);


-- ============================================================================
-- V2__create_card_catalog.sql
-- ============================================================================

-- Le fazioni di Dreamscape: Dreams, Nightmares, Memories.
-- Ogni fazione ha un Lord: una sua carta Leggendaria che la rappresenta
-- (es. "Dreams Lord" = Il Sogno Lucido). È solo titolo e immagine, senza regole
-- di gioco speciali. lord_card_id riceve la chiave esterna dopo la creazione di cards.
CREATE TABLE factions (
    id           UUID        NOT NULL DEFAULT uuidv7(),
    code         VARCHAR(30) NOT NULL,
    name         VARCHAR(50) NOT NULL,
    description  TEXT        NULL,
    lord_title   VARCHAR(50) NULL,
    lord_card_id UUID        NULL,
    CONSTRAINT pk_factions PRIMARY KEY (id),
    CONSTRAINT uq_factions_code UNIQUE (code),
    CONSTRAINT uq_factions_name UNIQUE (name),
    CONSTRAINT uq_factions_lord_card UNIQUE (lord_card_id)
);

-- Una riga = "faction_id è forte contro target_faction_id".
-- I bonus si applicano alla creatura di faction_id quando affronta target_faction_id.
-- Regolamento attuale: ciclo Dreams → Memories → Nightmares → Dreams, +1 attacco.
-- defense_bonus resta disponibile se il bilanciamento lo richiede.
CREATE TABLE faction_advantages (
    id                UUID        NOT NULL DEFAULT uuidv7(),
    faction_id        UUID   NOT NULL,
    target_faction_id UUID   NOT NULL,
    attack_bonus      INT    NOT NULL DEFAULT 0,
    defense_bonus     INT    NOT NULL DEFAULT 0,
    CONSTRAINT pk_faction_advantages PRIMARY KEY (id),
    CONSTRAINT uq_faction_advantages_pair UNIQUE (faction_id, target_faction_id),
    CONSTRAINT fk_faction_advantages_faction FOREIGN KEY (faction_id) REFERENCES factions (id),
    CONSTRAINT fk_faction_advantages_target FOREIGN KEY (target_faction_id) REFERENCES factions (id),
    CONSTRAINT chk_faction_advantages_different CHECK (faction_id <> target_faction_id),
    CONSTRAINT chk_faction_advantages_bonus CHECK (attack_bonus >= 0 AND defense_bonus >= 0
                                                   AND (attack_bonus > 0 OR defense_bonus > 0))
);

-- I TIER di rarità con i vincoli del mazzo.
-- max_per_deck: quante carte di questo TIER al massimo in un mazzo (NULL = nessun limite).
-- max_copies: quante copie della stessa carta di questo TIER al massimo in un mazzo.
-- Regolamento attuale: COMMON NULL/2, RARE 8/2, EPIC 4/2, LEGENDARY 2/1.
CREATE TABLE rarities (
    id           UUID        NOT NULL DEFAULT uuidv7(),
    code         VARCHAR(30) NOT NULL,
    name         VARCHAR(50) NOT NULL,
    sort_order   INT         NOT NULL,
    max_per_deck INT         NULL,
    max_copies   INT         NOT NULL DEFAULT 2,
    CONSTRAINT pk_rarities PRIMARY KEY (id),
    CONSTRAINT uq_rarities_code UNIQUE (code),
    CONSTRAINT uq_rarities_sort_order UNIQUE (sort_order),
    CONSTRAINT chk_rarities_max_per_deck CHECK (max_per_deck IS NULL OR max_per_deck >= 0),
    CONSTRAINT chk_rarities_max_copies CHECK (max_copies > 0)
);

-- Le espansioni (set di carte): set base, espansione 1, ...
-- Servono per i pacchetti che contengono solo le carte di un'espansione.
CREATE TABLE card_sets (
    id          UUID        NOT NULL DEFAULT uuidv7(),
    code        VARCHAR(20) NOT NULL,
    name        VARCHAR(80) NOT NULL,
    description TEXT        NULL,
    released_at DATE        NULL,
    is_active   BOOLEAN     NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT pk_card_sets PRIMARY KEY (id),
    CONSTRAINT uq_card_sets_code UNIQUE (code),
    CONSTRAINT uq_card_sets_name UNIQUE (name)
);

-- Le carte del catalogo (tutte creature). Una carta posseduta da qualcuno
-- non si cancella: si disattiva con is_active = FALSE.
-- code è un identificativo stabile (es. BASE-001): resta uguale anche se il nome
-- cambia, si usa nelle migration con i dati e per il nome dei file immagine.
-- La carta la monta il frontend in JavaScript: illustrazione, cornice della fazione e
-- della rarità, simbolo, nome, testi, ATT e DIF. Qui si salvano solo l'illustrazione
-- e il suo ritaglio; cornici e simboli sono file del frontend.
-- illustration_url: illustrazione orizzontale 3:2 della carta normale.
-- full_art_illustration_url: illustrazione verticale 2:3 della versione full art
-- (solo Leggendarie, controllato dal service). La full art è la stessa carta.
-- *_focus_y: ritaglio verticale dell'illustrazione, da 0 (in alto) a 1 (in basso),
-- come la colonna centro_y del compositore (es. Il Sogno Lucido 0.27).
-- Immagini: il PNG originale resta intatto, con i suoi metadati, e non si serve al
-- browser. Dall'originale si creano due copie WebP: grande (larghezza 1024 px) e
-- miniatura (larghezza 400 px). *_url = copia grande, *_thumb_url = miniatura.
-- Il nome del file ha un numero di versione (es. base-004-v1.webp): una nuova
-- illustrazione ha un nome nuovo, così il browser tiene i file in cache per sempre.
-- attack >= 1: con attacco almeno 1 ogni round toglie difesa e la partita va avanti.
CREATE TABLE cards (
    id                        UUID        NOT NULL DEFAULT uuidv7(),
    code                      VARCHAR(20)  NOT NULL,
    name                      VARCHAR(80)  NOT NULL,
    description               TEXT         NULL,
    attack                    INT          NOT NULL,
    defense                   INT          NOT NULL,
    faction_id                UUID         NOT NULL,
    rarity_id                 UUID         NOT NULL,
    card_set_id               UUID         NOT NULL,
    illustration_url          VARCHAR(500) NULL,
    illustration_thumb_url    VARCHAR(500) NULL,
    illustration_focus_y      NUMERIC(3,2) NOT NULL DEFAULT 0.40,
    full_art_illustration_url VARCHAR(500) NULL,
    full_art_thumb_url        VARCHAR(500) NULL,
    full_art_focus_y          NUMERIC(3,2) NOT NULL DEFAULT 0.40,
    is_active                 BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at                TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at                TIMESTAMPTZ  NOT NULL DEFAULT now(),
    CONSTRAINT pk_cards PRIMARY KEY (id),
    CONSTRAINT uq_cards_code UNIQUE (code),
    CONSTRAINT uq_cards_name UNIQUE (name),
    CONSTRAINT fk_cards_faction FOREIGN KEY (faction_id) REFERENCES factions (id),
    CONSTRAINT fk_cards_rarity FOREIGN KEY (rarity_id) REFERENCES rarities (id),
    CONSTRAINT fk_cards_card_set FOREIGN KEY (card_set_id) REFERENCES card_sets (id),
    CONSTRAINT chk_cards_attack CHECK (attack >= 1),
    CONSTRAINT chk_cards_defense CHECK (defense >= 1),
    CONSTRAINT chk_cards_focus CHECK (illustration_focus_y BETWEEN 0 AND 1 AND full_art_focus_y BETWEEN 0 AND 1),
    -- Copia grande e miniatura ci sono sempre insieme
    CONSTRAINT chk_cards_thumbs CHECK ((illustration_url IS NULL) = (illustration_thumb_url IS NULL)
                                       AND (full_art_illustration_url IS NULL) = (full_art_thumb_url IS NULL))
);

-- Ora che cards esiste, si collega il Lord di ogni fazione alla sua carta.
-- Che sia una Leggendaria della stessa fazione lo controlla il service.
ALTER TABLE factions
    ADD CONSTRAINT fk_factions_lord_card FOREIGN KEY (lord_card_id) REFERENCES cards (id);

-- Catalogo degli effetti (lista proposta da Nicolas). Gli effetti fanno parte della
-- modalità Base: valgono in ogni partita.
-- code collega la riga all'implementazione Java nel motore di gioco.
-- trigger_event dice quando agisce l'effetto:
--   ON_PLAY      quando la carta viene giocata (fase iniziale)
--   WHILE_IN_PLAY finché la carta resta in campo (es. Protezione, Indebolimento)
--   END_OF_ROUND alla fine di ogni round, se la carta è ancora in campo
--   ON_DEATH     quando la carta viene uccisa
--   ON_KILL      quando la carta uccide una creatura avversaria
-- description è il testo per i giocatori; {value} viene sostituito con card_effects.effect_value.
CREATE TABLE effects (
    id            UUID        NOT NULL DEFAULT uuidv7(),
    code          VARCHAR(50)  NOT NULL,
    name          VARCHAR(80)  NOT NULL,
    description   VARCHAR(255) NOT NULL,
    trigger_event VARCHAR(20)  NOT NULL,
    CONSTRAINT pk_effects PRIMARY KEY (id),
    CONSTRAINT uq_effects_code UNIQUE (code),
    CONSTRAINT uq_effects_name UNIQUE (name),
    CONSTRAINT chk_effects_trigger_event CHECK (trigger_event IN ('ON_PLAY', 'WHILE_IN_PLAY', 'END_OF_ROUND',
                                                                  'ON_DEATH', 'ON_KILL'))
);

-- Gli effetti di ogni carta. Lo stesso effetto può avere valori diversi
-- su carte diverse (es. "Protezione {value}": 1 su una carta, 2 su un'altra).
-- effect_value è NULL per gli effetti che non hanno un numero (es. Neutralità).
-- Il regolamento attuale prevede un solo effetto per carta: lo controlla il service,
-- così lo schema resta pronto se in futuro se ne vorranno di più.
CREATE TABLE card_effects (
    id           UUID        NOT NULL DEFAULT uuidv7(),
    card_id      UUID   NOT NULL,
    effect_id    UUID   NOT NULL,
    effect_value INT    NULL,
    CONSTRAINT pk_card_effects PRIMARY KEY (id),
    CONSTRAINT uq_card_effects_card_effect UNIQUE (card_id, effect_id),
    CONSTRAINT fk_card_effects_card FOREIGN KEY (card_id) REFERENCES cards (id) ON DELETE CASCADE,
    CONSTRAINT fk_card_effects_effect FOREIGN KEY (effect_id) REFERENCES effects (id)
);


-- ============================================================================
-- V3__create_collections_and_decks.sql
-- ============================================================================

-- La collezione: una riga per (utente, carta) con il numero di copie.
-- quantity conta TUTTE le copie; full_art_quantity quante di queste sono full art.
-- Quando quantity arriverebbe a 0 la riga si cancella.
CREATE TABLE user_cards (
    id                UUID        NOT NULL DEFAULT uuidv7(),
    user_id           UUID        NOT NULL,
    card_id           UUID        NOT NULL,
    quantity          INT         NOT NULL,
    full_art_quantity INT         NOT NULL DEFAULT 0,
    acquired_at       TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT pk_user_cards PRIMARY KEY (id),
    CONSTRAINT uq_user_cards_user_card UNIQUE (user_id, card_id),
    CONSTRAINT fk_user_cards_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_user_cards_card FOREIGN KEY (card_id) REFERENCES cards (id),
    CONSTRAINT chk_user_cards_quantity CHECK (quantity > 0),
    CONSTRAINT chk_user_cards_full_art CHECK (full_art_quantity >= 0 AND full_art_quantity <= quantity)
);

CREATE TABLE decks (
    id         UUID        NOT NULL DEFAULT uuidv7(),
    user_id    UUID        NOT NULL,
    name       VARCHAR(40) NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT pk_decks PRIMARY KEY (id),
    CONSTRAINT uq_decks_user_name UNIQUE (user_id, name),
    CONSTRAINT fk_decks_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

-- Le carte di un mazzo. I vincoli del regolamento (20 carte, copie massime per rarità,
-- limiti per TIER, possesso delle carte) si verificano nel service, non qui.
-- Full art e copia normale sono la stessa carta: nel mazzo contano insieme.
-- is_full_art: il giocatore sceglie di mostrare la full art nel mazzo e in partita.
-- Vale solo per le carte con full art (Leggendarie, 1 copia per mazzo) e solo se
-- l'utente possiede una copia full art: lo controlla il service.
CREATE TABLE deck_cards (
    id          UUID    NOT NULL DEFAULT uuidv7(),
    deck_id     UUID    NOT NULL,
    card_id     UUID    NOT NULL,
    quantity    INT     NOT NULL,
    is_full_art BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT pk_deck_cards PRIMARY KEY (id),
    CONSTRAINT uq_deck_cards_deck_card UNIQUE (deck_id, card_id),
    CONSTRAINT fk_deck_cards_deck FOREIGN KEY (deck_id) REFERENCES decks (id) ON DELETE CASCADE,
    CONSTRAINT fk_deck_cards_card FOREIGN KEY (card_id) REFERENCES cards (id),
    CONSTRAINT chk_deck_cards_quantity CHECK (quantity > 0),
    CONSTRAINT chk_deck_cards_full_art CHECK (NOT is_full_art OR quantity = 1)
);


-- ============================================================================
-- V4__create_packs.sql
-- ============================================================================

-- I pacchetti (gestiti dal backoffice).
-- pack_type: SHOP = in vendita nel negozio; STARTER = set iniziale regalato alla
-- registrazione; WELCOME = pacchetto di benvenuto regalato alla registrazione.
-- Il set iniziale (slot 14 Comuni + 6 Rare) si estrae a caso ma senza superare le copie
-- massime per carta (rarities.max_copies): così forma sempre un mazzo valido, che il
-- giocatore compone da sé. Il limite lo applica il service solo ai pacchetti STARTER.
-- Solo i pacchetti SHOP hanno un prezzo; gli altri non si possono comprare.
-- card_set_id: se valorizzato, il pacchetto pesca solo le carte di quell'espansione;
-- NULL = pesca da tutte le espansioni attive.
-- full_art_chance: probabilità (in percentuale) che una carta con versione full art
-- esca come full art. Si regola per pacchetto, es. più alta in un pacchetto speciale.
CREATE TABLE packs (
    id              UUID        NOT NULL DEFAULT uuidv7(),
    name            VARCHAR(60)  NOT NULL,
    description     TEXT         NULL,
    pack_type       VARCHAR(20)  NOT NULL DEFAULT 'SHOP',
    price_credits   INT          NOT NULL DEFAULT 0,
    card_set_id     UUID         NULL,
    full_art_chance NUMERIC(5,2) NOT NULL DEFAULT 5.00,
    image_url       VARCHAR(500) NULL,
    is_active       BOOLEAN      NOT NULL DEFAULT TRUE,
    created_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
    updated_at      TIMESTAMPTZ  NOT NULL DEFAULT now(),
    CONSTRAINT pk_packs PRIMARY KEY (id),
    CONSTRAINT uq_packs_name UNIQUE (name),
    CONSTRAINT fk_packs_card_set FOREIGN KEY (card_set_id) REFERENCES card_sets (id),
    CONSTRAINT chk_packs_type CHECK (pack_type IN ('SHOP', 'STARTER', 'WELCOME')),
    CONSTRAINT chk_packs_price CHECK ((pack_type = 'SHOP' AND price_credits > 0)
                                      OR (pack_type <> 'SHOP' AND price_credits = 0)),
    CONSTRAINT chk_packs_full_art_chance CHECK (full_art_chance BETWEEN 0 AND 100)
);

-- Le copertine di un pacchetto: stesso contenuto, immagine diversa.
-- Es. il pacchetto base ha tre copertine, una per ogni Lord di fazione:
-- il giocatore sceglie quella che preferisce quando compra.
-- Un pacchetto senza copertine usa packs.image_url.
-- Le immagini dei pacchetti e delle copertine seguono le regole delle illustrazioni:
-- una copia WebP con la versione nel nome (es. base-dreams-v1.webp), niente miniatura.
CREATE TABLE pack_covers (
    id         UUID        NOT NULL DEFAULT uuidv7(),
    pack_id    UUID         NOT NULL,
    faction_id UUID         NULL,
    name       VARCHAR(60)  NOT NULL,
    image_url  VARCHAR(500) NOT NULL,
    sort_order INT          NOT NULL DEFAULT 0,
    is_active  BOOLEAN      NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_pack_covers PRIMARY KEY (id),
    CONSTRAINT uq_pack_covers_pack_name UNIQUE (pack_id, name),
    CONSTRAINT fk_pack_covers_pack FOREIGN KEY (pack_id) REFERENCES packs (id) ON DELETE CASCADE,
    CONSTRAINT fk_pack_covers_faction FOREIGN KEY (faction_id) REFERENCES factions (id)
);

-- Gli slot del pacchetto: ogni slot dà card_count carte.
-- La rarità di ogni carta dello slot si estrae con i pesi di pack_slot_rarities.
-- Es. pacchetto base: slot 1 = 3 carte COMMON; slot 2 = 1 carta RARE;
--     slot 3 = 1 carta EPIC (peso 90) o LEGENDARY (peso 10).
CREATE TABLE pack_slots (
    id         UUID        NOT NULL DEFAULT uuidv7(),
    pack_id    UUID   NOT NULL,
    sort_order INT    NOT NULL,
    card_count INT    NOT NULL,
    CONSTRAINT pk_pack_slots PRIMARY KEY (id),
    CONSTRAINT uq_pack_slots_pack_order UNIQUE (pack_id, sort_order),
    CONSTRAINT fk_pack_slots_pack FOREIGN KEY (pack_id) REFERENCES packs (id) ON DELETE CASCADE,
    CONSTRAINT chk_pack_slots_card_count CHECK (card_count > 0)
);

-- Le rarità possibili in uno slot, con il loro peso.
-- Probabilità di una rarità = suo peso / somma dei pesi dello slot.
-- Uno slot con una sola riga dà sempre quella rarità (es. Epica garantita).
CREATE TABLE pack_slot_rarities (
    id           UUID        NOT NULL DEFAULT uuidv7(),
    pack_slot_id UUID   NOT NULL,
    rarity_id    UUID   NOT NULL,
    weight       INT    NOT NULL,
    CONSTRAINT pk_pack_slot_rarities PRIMARY KEY (id),
    CONSTRAINT uq_pack_slot_rarities_slot_rarity UNIQUE (pack_slot_id, rarity_id),
    CONSTRAINT fk_pack_slot_rarities_slot FOREIGN KEY (pack_slot_id) REFERENCES pack_slots (id) ON DELETE CASCADE,
    CONSTRAINT fk_pack_slot_rarities_rarity FOREIGN KEY (rarity_id) REFERENCES rarities (id),
    CONSTRAINT chk_pack_slot_rarities_weight CHECK (weight > 0)
);

-- Ogni apertura di un pacchetto (comprato e aperto subito, oppure regalato).
-- source: PURCHASE = comprato nel negozio; SIGNUP = set iniziale e pacchetti di benvenuto.
-- price_paid salva il prezzo del momento, che può cambiare in seguito (0 se regalato).
-- pack_cover_id: la copertina scelta (NULL se il pacchetto non ne ha).
CREATE TABLE pack_openings (
    id            UUID        NOT NULL DEFAULT uuidv7(),
    user_id       UUID        NOT NULL,
    pack_id       UUID        NOT NULL,
    pack_cover_id UUID        NULL,
    source        VARCHAR(20) NOT NULL DEFAULT 'PURCHASE',
    price_paid    INT         NOT NULL,
    opened_at     TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT pk_pack_openings PRIMARY KEY (id),
    CONSTRAINT fk_pack_openings_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_pack_openings_pack FOREIGN KEY (pack_id) REFERENCES packs (id),
    CONSTRAINT fk_pack_openings_cover FOREIGN KEY (pack_cover_id) REFERENCES pack_covers (id) ON DELETE SET NULL,
    CONSTRAINT chk_pack_openings_source CHECK (source IN ('PURCHASE', 'SIGNUP')),
    CONSTRAINT chk_pack_openings_price CHECK ((source = 'PURCHASE' AND price_paid > 0)
                                              OR (source <> 'PURCHASE' AND price_paid = 0))
);

CREATE INDEX idx_pack_openings_user_opened ON pack_openings (user_id, opened_at);

-- Le carte uscite da un'apertura: una riga per carta (i doppioni sono righe diverse).
-- is_full_art = TRUE se la copia è uscita in versione full art.
CREATE TABLE pack_opening_cards (
    id              UUID        NOT NULL DEFAULT uuidv7(),
    pack_opening_id UUID    NOT NULL,
    card_id         UUID    NOT NULL,
    is_full_art     BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT pk_pack_opening_cards PRIMARY KEY (id),
    CONSTRAINT fk_pack_opening_cards_opening FOREIGN KEY (pack_opening_id) REFERENCES pack_openings (id) ON DELETE CASCADE,
    CONSTRAINT fk_pack_opening_cards_card FOREIGN KEY (card_id) REFERENCES cards (id)
);

-- Per mostrare le carte di un'apertura (pagina /negozio/apertura/{id}).
CREATE INDEX idx_pack_opening_cards_opening ON pack_opening_cards (pack_opening_id);


-- ============================================================================
-- V5__create_friendships_and_trades.sql
-- ============================================================================

-- La lista amici. A (requester) manda la richiesta, B (addressee) la accetta.
-- status: PENDING = in attesa di risposta; ACCEPTED = amici.
-- Se B rifiuta, o uno dei due toglie l'amicizia, la riga si cancella.
-- Una sola riga per coppia, in qualunque direzione (indice su LEAST/GREATEST).
CREATE TABLE friendships (
    id           UUID        NOT NULL DEFAULT uuidv7(),
    requester_id UUID        NOT NULL,
    addressee_id UUID        NOT NULL,
    status       VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    created_at   TIMESTAMPTZ NOT NULL DEFAULT now(),
    accepted_at  TIMESTAMPTZ NULL,
    CONSTRAINT pk_friendships PRIMARY KEY (id),
    CONSTRAINT fk_friendships_requester FOREIGN KEY (requester_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_friendships_addressee FOREIGN KEY (addressee_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT chk_friendships_status CHECK (status IN ('PENDING', 'ACCEPTED')),
    CONSTRAINT chk_friendships_different_users CHECK (requester_id <> addressee_id),
    CONSTRAINT chk_friendships_accepted CHECK ((status = 'ACCEPTED') = (accepted_at IS NOT NULL))
);

CREATE UNIQUE INDEX uq_friendships_pair ON friendships (LEAST(requester_id, addressee_id),
                                                        GREATEST(requester_id, addressee_id));
CREATE INDEX idx_friendships_addressee_status ON friendships (addressee_id, status);
CREATE INDEX idx_friendships_requester_status ON friendships (requester_id, status);

-- Gli scambi: solo tra amici (lo controlla il service, alla proposta e all'accettazione).
-- Quantità e rarità libere: si può dare 1 Epica per 5 Comuni. Lo scambio avviene
-- solo se il destinatario accetta.
-- Niente ON DELETE CASCADE verso users: gli utenti non si cancellano e lo storico resta.
CREATE TABLE trades (
    id           UUID        NOT NULL DEFAULT uuidv7(),
    proposer_id  UUID         NOT NULL,
    recipient_id UUID         NOT NULL,
    status       VARCHAR(20)  NOT NULL DEFAULT 'PENDING',
    message      VARCHAR(255) NULL,
    created_at   TIMESTAMPTZ  NOT NULL DEFAULT now(),
    resolved_at  TIMESTAMPTZ  NULL,
    CONSTRAINT pk_trades PRIMARY KEY (id),
    CONSTRAINT fk_trades_proposer FOREIGN KEY (proposer_id) REFERENCES users (id),
    CONSTRAINT fk_trades_recipient FOREIGN KEY (recipient_id) REFERENCES users (id),
    CONSTRAINT chk_trades_status CHECK (status IN ('PENDING', 'ACCEPTED', 'REJECTED', 'CANCELLED')),
    CONSTRAINT chk_trades_different_users CHECK (proposer_id <> recipient_id)
);

CREATE INDEX idx_trades_recipient_status ON trades (recipient_id, status);
CREATE INDEX idx_trades_proposer_status ON trades (proposer_id, status);

-- Le carte dello scambio. side = OFFERED (le dà chi propone)
-- oppure REQUESTED (le dà chi riceve). Permette scambi 3 contro 1, 1 contro 5...
-- is_full_art distingue le copie full art da quelle normali della stessa carta.
CREATE TABLE trade_items (
    id          UUID        NOT NULL DEFAULT uuidv7(),
    trade_id    UUID        NOT NULL,
    card_id     UUID        NOT NULL,
    side        VARCHAR(10) NOT NULL,
    is_full_art BOOLEAN     NOT NULL DEFAULT FALSE,
    quantity    INT         NOT NULL,
    CONSTRAINT pk_trade_items PRIMARY KEY (id),
    CONSTRAINT uq_trade_items_trade_card_side UNIQUE (trade_id, card_id, side, is_full_art),
    CONSTRAINT fk_trade_items_trade FOREIGN KEY (trade_id) REFERENCES trades (id) ON DELETE CASCADE,
    CONSTRAINT fk_trade_items_card FOREIGN KEY (card_id) REFERENCES cards (id),
    CONSTRAINT chk_trade_items_side CHECK (side IN ('OFFERED', 'REQUESTED')),
    CONSTRAINT chk_trade_items_quantity CHECK (quantity > 0)
);


-- ============================================================================
-- V6__create_game_modes_challenges_and_matches.sql
-- ============================================================================

-- Le modalità di gioco. Oggi ce n'è una sola, BASE, con gli effetti delle carte
-- (il brief aggiornato permette di modificare la modalità Base).
-- starting_life_points e round_limit sono i valori del regolamento: un formato futuro
-- che cambia solo i numeri è una riga nuova. is_active lo accende e spegne dal backoffice.
-- Carte per mazzo e copie restano uguali per tutte le modalità (configurazione e rarities),
-- così un mazzo valido si può usare in ogni modalità.
CREATE TABLE game_modes (
    id                   UUID        NOT NULL DEFAULT uuidv7(),
    code                 VARCHAR(30)  NOT NULL,
    name                 VARCHAR(60)  NOT NULL,
    description          VARCHAR(255) NULL,
    starting_life_points INT          NOT NULL DEFAULT 20,
    round_limit          INT          NOT NULL DEFAULT 60,
    is_active            BOOLEAN      NOT NULL DEFAULT TRUE,
    CONSTRAINT pk_game_modes PRIMARY KEY (id),
    CONSTRAINT uq_game_modes_code UNIQUE (code),
    CONSTRAINT chk_game_modes_life_points CHECK (starting_life_points > 0),
    CONSTRAINT chk_game_modes_round_limit CHECK (round_limit > 0)
);

-- La modalità BASE serve sempre: il service la cerca per code e la usa per ogni sfida.
INSERT INTO game_modes (code, name, description, starting_life_points, round_limit, is_active)
VALUES ('BASE', 'Base', 'Regolamento di Dreamscape, con gli effetti delle carte.', 20, 60, TRUE);

-- La sfida: A sceglie il mazzo e sfida B (qualunque Dreamweaver, non solo gli amici);
-- B accetta scegliendo il suo mazzo.
-- Se un mazzo viene cancellato la colonna diventa NULL: lo storico resta
-- comunque completo grazie alle copie dei mazzi salvate in matches.
CREATE TABLE challenges (
    id                 UUID        NOT NULL DEFAULT uuidv7(),
    challenger_id      UUID        NOT NULL,
    opponent_id        UUID        NOT NULL,
    challenger_deck_id UUID        NULL,
    opponent_deck_id   UUID        NULL,
    game_mode_id       UUID        NOT NULL,
    status             VARCHAR(20) NOT NULL DEFAULT 'PENDING',
    created_at         TIMESTAMPTZ NOT NULL DEFAULT now(),
    resolved_at        TIMESTAMPTZ NULL,
    CONSTRAINT pk_challenges PRIMARY KEY (id),
    CONSTRAINT fk_challenges_challenger FOREIGN KEY (challenger_id) REFERENCES users (id),
    CONSTRAINT fk_challenges_opponent FOREIGN KEY (opponent_id) REFERENCES users (id),
    CONSTRAINT fk_challenges_challenger_deck FOREIGN KEY (challenger_deck_id) REFERENCES decks (id) ON DELETE SET NULL,
    CONSTRAINT fk_challenges_opponent_deck FOREIGN KEY (opponent_deck_id) REFERENCES decks (id) ON DELETE SET NULL,
    CONSTRAINT fk_challenges_game_mode FOREIGN KEY (game_mode_id) REFERENCES game_modes (id),
    CONSTRAINT chk_challenges_status CHECK (status IN ('PENDING', 'REJECTED', 'CANCELLED', 'COMPLETED')),
    CONSTRAINT chk_challenges_different_users CHECK (challenger_id <> opponent_id)
);

CREATE INDEX idx_challenges_opponent_status ON challenges (opponent_id, status);
CREATE INDEX idx_challenges_challenger_status ON challenges (challenger_id, status);

-- Il risultato della partita simulata dal motore. Una sola partita per sfida.
-- winner_id NULL = pareggio.
-- starting_life_points e round_limit: copia dei valori della modalità usati in questa
-- partita, così lo storico resta corretto anche se la modalità cambia.
-- *_deck_snapshot: copia dei mazzi al momento della partita (carte con ATT, DIF, fazione,
-- effetti e se mostrare la full art).
-- round_log: lo svolgimento round per round, così come lo restituisce il motore.
-- random_seed: permette di rigiocare la stessa partita per verifiche e test
-- (decide anche il lancio della moneta per l'ordine degli effetti).
-- *_rating_change: variazione del punteggio di rank; NULL se la partita non conta
-- per il rank (rank non ancora attivo, o oltre le prime partite del giorno contro lo
-- stesso avversario).
CREATE TABLE matches (
    id                       UUID        NOT NULL DEFAULT uuidv7(),
    challenge_id             UUID        NOT NULL,
    winner_id                UUID        NULL,
    end_reason               VARCHAR(30) NOT NULL,
    total_rounds             INT         NOT NULL,
    starting_life_points     INT         NOT NULL,
    round_limit              INT         NOT NULL,
    challenger_life_points   INT         NOT NULL,
    opponent_life_points     INT         NOT NULL,
    challenger_rating_change INT         NULL,
    opponent_rating_change   INT         NULL,
    random_seed              BIGINT      NOT NULL,
    challenger_deck_snapshot JSONB       NOT NULL,
    opponent_deck_snapshot   JSONB       NOT NULL,
    round_log                JSONB       NOT NULL,
    played_at                TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT pk_matches PRIMARY KEY (id),
    CONSTRAINT uq_matches_challenge UNIQUE (challenge_id),
    CONSTRAINT fk_matches_challenge FOREIGN KEY (challenge_id) REFERENCES challenges (id) ON DELETE CASCADE,
    -- Niente ON DELETE SET NULL: una vittoria non deve mai diventare un pareggio.
    CONSTRAINT fk_matches_winner FOREIGN KEY (winner_id) REFERENCES users (id),
    CONSTRAINT chk_matches_end_reason CHECK (end_reason IN ('LIFE_POINTS', 'DECK_EXHAUSTED', 'ROUND_LIMIT')),
    CONSTRAINT chk_matches_total_rounds CHECK (total_rounds >= 1 AND total_rounds <= round_limit)
);


-- ============================================================================
-- V7__create_credit_transactions.sql
-- ============================================================================

-- Registro di ogni movimento di crediti. users.credits è il saldo attuale;
-- questa tabella spiega come ci si è arrivati.
-- I pacchetti regalati (set iniziale e benvenuto) non muovono crediti.
-- I tipi dipendono da come si ottengono i crediti in fase 1 (decisione DGS).
CREATE TABLE credit_transactions (
    id              UUID        NOT NULL DEFAULT uuidv7(),
    user_id         UUID        NOT NULL,
    type            VARCHAR(30) NOT NULL,
    amount          INT         NOT NULL,
    balance_after   INT         NOT NULL,
    pack_opening_id UUID        NULL,
    match_id        UUID        NULL,
    created_at      TIMESTAMPTZ NOT NULL DEFAULT now(),
    CONSTRAINT pk_credit_transactions PRIMARY KEY (id),
    CONSTRAINT fk_credit_transactions_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_credit_transactions_pack_opening FOREIGN KEY (pack_opening_id) REFERENCES pack_openings (id) ON DELETE SET NULL,
    CONSTRAINT fk_credit_transactions_match FOREIGN KEY (match_id) REFERENCES matches (id) ON DELETE SET NULL,
    CONSTRAINT chk_credit_transactions_type CHECK (type IN ('SIGNUP_BONUS', 'DAILY_REWARD', 'PACK_PURCHASE',
                                                            'MATCH_REWARD', 'ADMIN_ADJUSTMENT')),
    CONSTRAINT chk_credit_transactions_amount CHECK (amount <> 0),
    CONSTRAINT chk_credit_transactions_balance CHECK (balance_after >= 0)
);

CREATE INDEX idx_credit_transactions_user_created ON credit_transactions (user_id, created_at);


-- ============================================================================
-- V8__create_contact_messages.sql
-- ============================================================================

-- I messaggi inviati dal form della pagina Contatti. L'admin li legge nella pagina
-- Messaggi del backoffice: nessun invio di email da configurare.
-- user_id è valorizzato se chi scrive ha fatto l'accesso, NULL per i visitatori.
-- status: NEW = da leggere, READ = letto, ARCHIVED = archiviato.
CREATE TABLE contact_messages (
    id         UUID        NOT NULL DEFAULT uuidv7(),
    user_id    UUID         NULL,
    name       VARCHAR(80)  NOT NULL,
    email      VARCHAR(255) NOT NULL,
    message    TEXT         NOT NULL,
    status     VARCHAR(20)  NOT NULL DEFAULT 'NEW',
    created_at TIMESTAMPTZ  NOT NULL DEFAULT now(),
    read_at    TIMESTAMPTZ  NULL,
    CONSTRAINT pk_contact_messages PRIMARY KEY (id),
    CONSTRAINT fk_contact_messages_user FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE SET NULL,
    CONSTRAINT chk_contact_messages_status CHECK (status IN ('NEW', 'READ', 'ARCHIVED'))
);

CREATE INDEX idx_contact_messages_status_created ON contact_messages (status, created_at);
