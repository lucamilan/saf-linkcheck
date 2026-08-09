# 005 · Ancore stile GitHub: slug dai titoli, accenti conservati, con regex della libreria standard

- **Status:** accepted
- **Date:** 2026-08-09

Il frammento #sezione di un link interno viene confrontato con le ancore derivate dai titoli ATX del file bersaglio, con l'algoritmo di GitHub: minuscole, punteggiatura rimossa, spazi in trattini, accenti conservati, duplicati con suffisso -1/-2. Perche': e' cio' che il renderer reale produce — un link che passa il check funziona anche li'; e resta implementabile con regex della libreria standard, estendendo l'approccio senza parser di [[decision:002]]. Limiti accettati e dichiarati: ancore HTML esplicite (<a id=...>) e frammenti nello stesso file fuori perimetro.

## Relations
- extends → [[decision:002]]
- delivered-by → [[iteration:005]]
