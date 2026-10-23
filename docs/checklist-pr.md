# Checklist prima di aprire una Pull Request

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
