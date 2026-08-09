# 004 · Esecuzione del piano: cache degli esiti dei controlli esterni

- **Status:** closed
- **Lane:** fast
- **Area:** scanner, report
- **Nature:** new-feature
- **Date:** 2026-08-09
- **Lesson:** Il tempo e' un input nascosto: un oracolo con cache si valida osservando cio' che non accade — la rete non toccata — e il segnale 'dalla cache' esiste apposta per rendere osservabile quel non-accadere.

Esegue il piano di loop di [[decision:004]]: passo 1 la cache con scadenza in linkcheck.py, passo 2 la regressione sull'intero perimetro. Un passo per commit, arresto sui trigger del contratto.

## Amendments (append-only)
- 2026-08-09 · [park:directional-choice] · Passo 1 a meta': la cache deve vivere da qualche parte e il piano non lo dice. Dentro la cartella controllata inquina il repository del manoscritto; fuori (home utente) rende l'esito non riproducibile fra macchine. Scelta direzionale: dispone il Senior.
- 2026-08-09 · [resume] · Il Senior dispone: la cache vive nella cartella controllata come .linkcheck-cache.json, documentata come file da ignorare in Git. La localita' dello strumento vale piu' della riproducibilita' fra macchine.
- 2026-08-09 · [new-feature] · ## Telemetria (loop)

- Passo 1 — verde al primo giro: la seconda esecuzione legge dalla cache, esito invariato. 1 commit.
- Passo 2 — verde: regressione 1/0/0 sull'intero perimetro. 1 commit.
- Budget: 2 commit usati su 3. Parcheggi: 1 (directional-choice sulla sede della cache, sciolto dal Senior alla ripresa).
