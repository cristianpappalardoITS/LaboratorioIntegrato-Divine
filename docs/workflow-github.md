# Flusso di lavoro su GitHub

## Board di GitHub Projects

| Colonna | Significato |
|---------|-------------|
| **Backlog** | Idee e lavoro futuro, non ancora pianificato |
| **To Do** | Pianificato e assegnato, si può iniziare |
| **In Progress** | Qualcuno ci sta lavorando (massimo 2 issue a testa) |
| **Review** | Pull request aperta, in attesa di revisione |
| **Done** | PR approvata e unita in `develop` |

## Issue

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

## Branch

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

## Commit

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

## Pull Request

- Si apre una PR da `feature/...` verso `develop`.
- Serve **almeno 1 approvazione** di un altro membro del team prima del merge.
- Il titolo segue lo stesso formato dei commit.
- La descrizione usa il [template PR](template.md#template-pull-request) e collega la issue con `Closes #12` (la issue si chiude da sola al merge).
- Chi apre la PR non la approva da solo. Chi la revisiona commenta in modo concreto ("qui manca il controllo sul null") e non generico ("non mi piace").
- Dopo il merge, il branch si cancella.
