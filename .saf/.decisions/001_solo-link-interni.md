# 001 · Solo link interni: i link HTTP esterni restano fuori perimetro

- **Status:** accepted
- **Date:** 2026-08-09

linkcheck valida soltanto i bersagli interni (percorsi relativi fra file). I link esterni si riconoscono dal prefisso (http, https, mailto) e si saltano. Perche': l'oracolo deve restare deterministico e lo strumento deve girare in CI senza rete; un controllo HTTP introduce esiti che dipendono dal momento (timeout, 429, DNS) e trasforma un controllo del manoscritto in un controllo della rete. Alternativa considerata e rinviata: verifica HTTP dietro opzione dedicata, con timeout e cache degli esiti.

## Relations
- delivered-by → [[iteration:001]]
