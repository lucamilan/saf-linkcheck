# 004 · Cache con scadenza per gli esiti dei controlli esterni (piano di loop)

- **Status:** accepted
- **Date:** 2026-08-09

Il controllo dei link esterni resta opzionale ma diventa ripetibile: gli esiti vengono conservati in una cache con scadenza accanto alla cartella controllata, cosi' due esecuzioni ravvicinate non interrogano due volte la rete. Il perimetro senza --esterni non cambia. La decisione e' motivata dalla conoscenza distillata sul link rot e dai limiti dell'oracolo di rete emersi nella iterazione 002. Promuove BL-002.

## Piano (loop)

- **Contratto:** promuovere BL-002 — cache degli esiti dei controlli esterni · budget: 3 commit · trigger: oracle-failure-repeated, directional-choice
- 1. Cache con scadenza degli esiti esterni in linkcheck.py — oracolo: doppia esecuzione con --esterni su fixture-esterni (verde = la seconda stampa 'dalla cache' per ogni link esterno e l'esito non cambia)
- 2. Regressione sull'intero perimetro — oracolo: fixture rotta, fixture sana, fixture-esterni senza opzione (verde = exit 1, 0, 0 nell'ordine)

## Relations
- informed-by → [[knowledge:001]]
- delivered-by → [[iteration:003]]
