# 003 · I link esterni entrano nel perimetro, dietro l'opzione --esterni

- **Status:** accepted
- **Date:** 2026-08-09

Il Senior dispone che i link esterni http e https vengano verificati, con una richiesta HEAD e timeout. L'inclusione e' opzionale: senza --esterni il comportamento resta quello di prima, deterministico e senza rete, cosi' la CI non eredita la flakiness della rete. La verifica usa urllib della libreria standard: la decisione sulla assenza di dipendenze resta valida e ha modellato il come. Questo supera la decisione che teneva i link esterni fuori perimetro: l'alternativa che quella decisione aveva rinviato viene realizzata.

## Relations
- supersedes → [[decision:001]]
- delivered-by → [[iteration:002]]
