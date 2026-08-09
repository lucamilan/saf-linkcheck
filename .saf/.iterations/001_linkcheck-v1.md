# 001 · linkcheck v1: controllo dei link interni del manoscritto

- **Status:** closed
- **Lane:** fast
- **Area:** scanner, report
- **Nature:** new-feature
- **Date:** 2026-08-09
- **Lesson:** Una esclusione di perimetro va validata, non solo dichiarata: la fixture sana contiene apposta un link esterno, cosi' l'oracolo dimostra che l'esclusione funziona invece di darla per buona.

Scopo: primo strumento funzionante che percorre i file Markdown di una cartella, estrae i link e segnala quelli interni rotti (file di destinazione mancante). Perimetro v1: link relativi fra file; esclusi i link esterni HTTP. Oracolo di validazione: eseguito su una fixture con un link rotto noto, lo strumento lo elenca ed esce con codice 1; su una fixture sana esce con codice 0.
