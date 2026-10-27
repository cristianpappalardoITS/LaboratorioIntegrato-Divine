# Colloquio con il cliente · Domande

Due elenchi:

1. **Domande per il cliente:** quello che non abbiamo potuto trasformare in una proposta lo chiediamo. Tre vanno sulla slide 20, le altre si tengono pronte.
2. **Domande dei finti clienti:** per la prova di giovedì 29/10. Chi fa il cliente le usa per mettere in difficoltà chi presenta; sotto ogni domanda c'è una traccia di risposta.

---

## 1. Domande per il cliente

Per ognuna portiamo la nostra proposta, così il cliente sceglie e non deve inventare.

| # | Domanda | La nostra proposta | Dove serve |
|---|---------|--------------------|------------|
| 1 | Quale proposta di visual preferite (logo, palette)? | Le proposte di DGS | Identità visiva |
| 2 | Partite più tattiche e lunghe (20 punti vita) o più rapide (10 punti vita)? Con 20 quasi tutte finiscono a mazzo esaurito | Decidere dopo le simulazioni del motore; oggi 20 | Regolamento |
| 3 | Il rank deve esserci alla consegna del 10/12, o può arrivare dopo? | Dopo le funzionalità obbligatorie | Roadmap |
| 4 | Quante carte deve avere il catalogo alla consegna? | Circa 30 (oggi 12 di prova) | DGS, catalogo |
| 5 | Come guadagna crediti il giocatore? | Ricompensa giornaliera + premio per le vittorie | Economia di gioco |
| 6 | Il portale deve inviare email (recupero password, conferma dell'account)? | Solo il recupero password, se c'è tempo | Backend |
| 7 | Serve un'età minima per registrarsi? | Nessuna domanda in più alla registrazione, solo i consensi a Privacy e Termini | Privacy |
| 8 | Il gioco deve essere anche in inglese? | Solo italiano in fase 1, testi pronti per la traduzione | Frontend |
| 9 | Dove verrà pubblicato il portale? Avete un hosting preferito? | Docker, pronto per un cloud (es. AWS) | Deploy |
| 10 | Vi interessa una seconda modalità di gioco in futuro (es. partita con scelte del giocatore)? | Non in fase 1: lo schema è già pronto ad aggiungerla | Roadmap |
| 11 | Le carte non creatura (incantesimi, potenziamenti) del brief vi interessano? | Non in fase 1 | Regolamento |

---

## 2. Domande dei finti clienti (per la prova)

Le domande più probabili, con una traccia di risposta. Le risposte durano al massimo 30 secondi: si risponde, si fa un esempio, ci si ferma.

### Il prodotto

**"Perché qualcuno dovrebbe giocare a Dreamscape invece che a Hearthstone o Marvel Snap?"**
Partite di pochi secondi e un tema che nessuno usa: i sogni, con tre fazioni che tutti capiscono (sogni, incubi, ricordi). Il collezionismo è sociale: si scambia con gli amici. I dati li porta l'analisi di mercato di DGS.

**"Se in partita il giocatore non decide niente, dov'è il divertimento?"**
È la domanda più probabile. La strategia sta prima della partita: quali carte tenere, quali scambiare, come costruire il mazzo con i limiti di rarità e i vantaggi di fazione. La partita è il momento in cui vedi se la tua strategia funziona, round per round, come guardare la tua squadra giocare. Una modalità con scelte durante la partita si può aggiungere in futuro.

**"Come ci guadagno?"**
In fase 1 i crediti sono solo virtuali, come chiede il brief. Il sistema è già pronto per l'acquisto di crediti, i pacchetti a tema e le espansioni: si attivano dopo, senza rifare il database.

**"A chi è rivolto?"**
Risponde con i dati del target di DGS.

### Il gioco

**"Come sapete che il gioco è bilanciato e che una fazione non vince sempre?"**
Il motore è ripetibile: simuliamo migliaia di partite e contiamo come finiscono. L'abbiamo già fatto per scegliere il limite di 60 round. I valori di fazioni e rarità stanno nel database e si correggono senza toccare il codice.

**"Le carte rare sono solo più forti? Chi paga vince?"**
Ci sono limiti per rarità nel mazzo (2 Leggendarie, 4 Epiche, 8 Rare), quindi un mazzo pieno di carte rare non esiste. La full art cambia solo l'immagine, non le statistiche.

**"Le partite non durano troppo?"**
Per il giocatore la partita è istantanea: la simula il server. Il replay si guarda round per round o si salta al risultato.

### La tecnica

**"Come impedite a un giocatore di barare?"**
Tutto quello che conta succede sul server: estrazione dei pacchetti, partite, scambi, crediti. Il browser mostra solo i risultati e ogni richiesta viene ricontrollata.

**"Se il server cade a metà di uno scambio, chi perde le carte?"**
Nessuno: scambi e acquisti sono transazioni del database. O avviene tutto, o non avviene niente.

**"Perché Java e non qualcosa di più moderno?"**
Spring Boot è lo standard per i backend aziendali: sicurezza, database e test sono già pronti, e il team lo conosce. Il motore di gioco in Java puro si testa da solo, senza database.

**"Perché non React per il frontend?"**
Lo spiega WMD. Traccia: HTML, CSS e JavaScript bastano per un portale di questo tipo, caricano veloci e si imparano in fretta. La carta la monta un componente JavaScript.

**"Funziona sul telefono?"**
Il portale è responsive. Le immagini hanno una miniatura leggera, quindi la collezione si carica in fretta anche da telefono.

**"Dove vanno i dati personali? E il GDPR?"**
Chiediamo solo username, email e password, cifrata. Privacy Policy e Termini si accettano alla registrazione e salviamo la data. Si può chiedere la cancellazione dell'account, che viene reso anonimo.

**"Quanto costa tenerlo online?"**
Con un'architettura piccola su cloud (un server per il backend, un database gestito, file statici per il frontend) la spesa è contenuta. Se la proposta AWS è pronta si mostrano i numeri, altrimenti si risponde "ve lo portiamo al SAL" e il note-taker lo segna.

### Le illustrazioni

**"Le immagini sono fatte con l'AI: di chi sono i diritti?"**
Il brief chiede di generarle con l'AI. Teniamo i metadati originali di ogni immagine, così si vede sempre come è stata creata. Prima di una pubblicazione commerciale si verificano le condizioni d'uso dello strumento di generazione.

**"Le carte sono tutte uguali come stile?"**
Abbiamo regole comuni per illustrazioni e cornici (testi di generazione in `carte/testi-generazione/`). DGS sta rivedendo palette e bordi, per esempio il rosso rubino delle Leggendarie Nightmares.

### I tempi

**"Riuscite a consegnare tutto entro il 10 dicembre?"**
Mostra la roadmap. Le funzionalità obbligatorie vengono prima di tutto. Se serve tagliare, si sposta il rank, non i requisiti.

**"Cosa ci mostrerete al SAL del 23 novembre?"**
Registrazione e accesso, catalogo, pacchetti, collezione e mazzi funzionanti, più il motore di gioco con i test.

**"Chi è il responsabile se qualcosa va storto?"**
Ogni attività ha una persona assegnata sulla board, e ogni team ha un team leader. Cristian coordina tutto il progetto.

---

## Consigli per chi fa il cliente alla prova

- Interrompi almeno una volta durante la presentazione: chi presenta deve rispondere in breve e riprendere.
- Fai una domanda a cui non si può rispondere subito: chi presenta deve dire "ve lo facciamo sapere", e il note-taker la deve segnare.
- Chiedi di tornare a una slide già passata: il driver deve trovarla in fretta.
- Alla fine, di' cosa non hai capito: se non lo capisci tu, non lo capirà il cliente.
