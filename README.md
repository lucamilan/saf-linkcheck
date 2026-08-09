# linkcheck

Uno strumento a riga di comando che valida i link di un manoscritto Markdown, e il
laboratorio in cui il metodo SAF è stato messo alla prova a partire da una cognizione vuota.
Il codice è vero e funziona; il progetto no: è nato per il libro
**[«Il Senior amplificato»](https://leanpub.com/il-senior-amplificato)**, come materiale
visionabile a corredo della Parte 2.

Chi arriva qui per lo strumento trova un file di Python senza dipendenze. Chi arriva qui per
il metodo trova un repository abbastanza piccolo da leggerlo tutto, in cui la cognizione di un
progetto — decisioni, iterazioni, lezioni, fonti, lavoro rinviato — è nata da zero sotto
osservazione e si è depositata in `.saf/` e nella storia Git.

## Lo strumento

`linkcheck` percorre i file `.md` di una cartella, ne estrae i link e verifica che i bersagli
esistano.

```bash
python linkcheck.py <cartella> [--esterni]
```

- **Link interni.** I percorsi relativi devono risolvere a un file esistente.
- **Ancore.** Se il link porta un frammento (`altro-file.md#sezione`), il frammento viene
  confrontato con le ancore ricavate dai titoli del file bersaglio, con lo slug in stile
  GitHub: minuscole, punteggiatura rimossa, spazi in trattini, accenti conservati, duplicati
  con suffisso `-1`, `-2`. Le ancore HTML esplicite (`<a id=...>`) restano fuori perimetro.
- **Link esterni.** Fuori perimetro per impostazione predefinita: senza `--esterni` il
  controllo è deterministico e non tocca la rete. Con `--esterni`, `http` e `https` vengono
  verificati con una richiesta `HEAD`, e l'esito resta in cache per un giorno in
  `.linkcheck-cache.json`, dentro la cartella controllata.
- **Uscita.** Un elenco `file:riga: motivo -> bersaglio`, poi il conteggio. Codice di uscita
  `1` se almeno un link è rotto, `0` altrimenti: usabile in CI così com'è.

Serve Python 3 e nient'altro. L'esclusione delle dipendenze non è una svista: è registrata
con il suo prezzo in `.saf/.decisions/002_nessuna-dipendenza.md`.

Due fixture fanno da oracolo:

```bash
python linkcheck.py fixture       # un link rotto e un'ancora mancante, uscita 1
python linkcheck.py fixture-sana  # nessun rilievo, uscita 0
```

La fixture sana contiene di proposito un link esterno: un'esclusione di perimetro va
validata, non soltanto dichiarata.

## Il laboratorio

Il 9 agosto 2026 ho installato in questa cartella un'istanza SAF vuota (kit v49) e ci ho
costruito linkcheck in dieci atti, uno per ciascuna prova che i capitoli del libro devono
mostrare. La cognizione che leggi in `.saf/` non è stata scritta a tavolino: è il residuo di
quelle sessioni.

| Atto | Che cosa mette alla prova | Dove si vede |
|---|---|---|
| 1 | Apertura e chiusura di un'iterazione a grafo vuoto | `iteration:001`, `decision:001`, `decision:002` |
| 2 | Il recupero del giudizio: una domanda pesca due decisioni | `.saf/.decisions/001`, `002` |
| 3 | La supersessione, come ripensamento che lascia traccia | `decision:003` supera la `001` |
| 4 | Il lavoro rinviato, registrato invece che dimenticato | `.saf/.roadmap/` |
| 5 | Una fonte esterna catturata e distillata | `source:001` → `knowledge:001` |
| 6 | Loop con contratto d'arresto, parcheggio e ripresa | `decision:004`, `iteration:004` |
| 7 | Il co-recupero fra cognizione e codice | il gettone `.linkcheck-cache.json` |
| 8 | Il banco di manutenzione: invarianti e segnali di merito | il grafo completo, letto da `saf-ops` |
| 9 | La replica con le disposizioni reali dell'autore | `decision:005`, che estende la `002` |
| 10 | Sei agenti freschi interrogano lo stesso grafo | la storia Git |

La domanda a cui il laboratorio risponde è quella del punto di pareggio: quanto costa formare
una cognizione, e dopo quanto poco comincia a restituire. Qui il pareggio è arrivato alla
terza sessione, quando una domanda qualunque — «aggiungiamo `requests` e controlliamo anche i
link esterni?» — ha riportato sul tavolo due giudizi che senza archivio sarebbero stati
sovrascritti in silenzio.

## Come si legge il repository

Tutto si legge come Markdown, senza strumenti.

- **`linkcheck.py`** — lo strumento, in un file solo.
- **`.saf/`** — la cognizione: `.decisions/`, `.iterations/`, `.knowledge/`, `.sources/`,
  `.roadmap/`. Ogni record dichiara in fondo la propria correntezza: una decisione superata lo
  dice, e dice da chi.
- **`saf-prompt.md`** e **`CLAUDE.md`** — il metodo nella forma vincolante in cui arriva a un
  progetto che installa l'harness.
- **`.githooks/`** — gli hook di Git che rifiutano un commit fuori contratto. Durante il
  laboratorio hanno colpito due volte, e nessuna delle due era in programma.
- **`.claude/skills/`** — le skill `saf` e `saf-ops`.
- **La storia Git** — dal secondo commit in poi, ognuno porta esattamente un trailer di specie
  (`Chore:`, `Iteration:`, `Roadmap:`, `Source:`). Il grafo ne deriva le relazioni senza
  che nessuno le abbia scritte a mano, quindi `git log` si legge come un indice:

```bash
git log --format='%h %s%n%(trailers:only=true)'
```

## Che cosa questo repository non è

Un caso dimostrativo, costruito apposta per il libro. Le esecuzioni, gli output, i record e i
commit sono reali; il progetto no: nessun committente, nessuna produzione, nessun utente oltre
l'autore. Negli atti 1–6 le disposizioni del Senior sono state simulate dall'agente per
collaudare i binari; nell'atto 9 sono reali, con l'autore alla tastiera.

Non è nemmeno un'introduzione a SAF: qui trovi un progetto già girato, non il metodo
documentato. Del metodo il libro dà la trattazione; questo repository ne mostra un residuo.

Un rilievo autentico è rimasto agli atti: la `decision:004` scrive che la cache vive «accanto»
alla cartella controllata, mentre l'attuazione la mette «dentro». La discrepanza è emersa dal
controllo incrociato dell'atto 10 e non è stata sanata in silenzio.

## Licenza

Tre materiali, tre condizioni; il dettaglio sta in [`LICENSE`](LICENSE).

- **Il codice dimostrativo** — `linkcheck.py` e le fixture — è sotto licenza MIT: prendilo,
  se ti serve.
- **Il kit SAF** — `saf-prompt.md`, `CLAUDE.md`, gli hook, le skill — è pubblicato in sola
  lettura, con tutti i diritti riservati. Serve a rendere leggibile il laboratorio, non a
  essere ridistribuito. Per usarlo in un tuo progetto, scrivimi.
- **La cognizione del laboratorio** — i record di `.saf/`, i messaggi di commit, questo
  README — segue le condizioni del libro: CC BY-NC-ND 4.0.
