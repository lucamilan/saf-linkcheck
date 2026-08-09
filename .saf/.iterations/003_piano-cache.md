# 003 · Analisi: promozione di BL-002, cache degli esiti esterni

- **Status:** closed
- **Lane:** complex
- **Area:** scanner, report
- **Nature:** analysis
- **Date:** 2026-08-09
- **Outcome:** implemented
- **Lesson:** Un piano eseguibile in autonomia nasce da una analisi che confronta alternative, non da una lista di cose da fare: il contratto (budget e trigger) e' la parte che rende il loop arrestabile, i passi sono la parte facile.

Domanda: il controllo esterno introdotto nella iterazione 002 e' volatile (rete, HEAD imperfetto) e la fonte W3C registrata mostra che il decadimento dei link e' strutturale, non occasionale. Vale la pena promuovere BL-002 a lavoro eseguibile in loop? Alternative confrontate: (a) lasciare il controllo esterno cosi' com'e', volatile ma semplice; (b) cache degli esiti con scadenza, ripetibile e gentile verso i siti; (c) spostare il controllo esterno in un servizio separato, fuori perimetro per uno strumento a file singolo. Raccomandazione: (b), eseguita in loop autonomo con passi piccoli e oracoli meccanici.

## Amendments (append-only)
- 2026-08-09 · [analysis] · L'analisi consegna il piano di loop registrato in [[decision:004]], che promuove BL-002.
