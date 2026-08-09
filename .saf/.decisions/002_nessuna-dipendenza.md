# 002 · Nessuna dipendenza: espressione regolare della libreria standard, non un parser Markdown

- **Status:** accepted
- **Date:** 2026-08-09

L'estrazione dei link usa una espressione regolare della libreria standard Python, riga per riga. Perche': lo strumento e' piccolo e deve restare installabile ovunque senza gestione di dipendenze; un parser Markdown completo porta piu' fedelta' ma anche un costo di manutenzione che il perimetro attuale non ripaga. Limite accettato e dichiarato: i link spezzati su piu' righe non vengono visti.

## Relations
- delivered-by → [[iteration:001]]
