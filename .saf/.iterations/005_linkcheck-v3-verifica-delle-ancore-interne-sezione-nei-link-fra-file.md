# 005 · linkcheck v3: verifica delle ancore interne (#sezione) nei link fra file

- **Status:** in-progress
- **Lane:** fast
- **Area:** scanner, report
- **Nature:** new-feature
- **Date:** 2026-08-09

Promozione di BL-001: il bersaglio di un link interno viene verificato anche come sezione, non solo come file. Le ancore vengono calcolate dai titoli del file bersaglio e confrontate col frammento; ancora mancante = nuovo tipo di errore nel report, exit code non-zero. Oracolo: suite di test (ancora valida passa, ancora mancante fallisce, link senza frammento invariati, regressione verde).
