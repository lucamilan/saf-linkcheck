# 002 · linkcheck v2: controllo opzionale dei link esterni

- **Status:** closed
- **Lane:** fast
- **Area:** scanner, report
- **Nature:** new-feature
- **Date:** 2026-08-09
- **Lesson:** Una richiesta HEAD con timeout non e' un oracolo perfetto: alcuni siti rifiutano HEAD o rispondono a intermittenza. Il controllo esterno resta indicativo e opzionale; l'oracolo vero del manoscritto rimane il controllo interno deterministico.

Scopo: il Senior dispone di includere i link esterni nel controllo. L'inclusione avviene dietro l'opzione --esterni: il comportamento di default resta deterministico e senza rete. La verifica usa urllib della libreria standard, in coerenza con la decisione sulla assenza di dipendenze. Oracolo di validazione: su una fixture con un dominio esterno inesistente (.invalid) e uno raggiungibile, con --esterni lo strumento segnala solo il primo; senza --esterni esce con 0 come prima.
