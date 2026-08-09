# 005 · linkcheck v3: verifica delle ancore interne (#sezione) nei link fra file

- **Status:** closed
- **Lane:** fast
- **Area:** scanner, report
- **Nature:** new-feature
- **Date:** 2026-08-09
- **Lesson:** L'ancora e' un contratto col renderer, non col filesystem: la verifica vale solo se replica l'algoritmo che il lettore vedra' (GitHub), accenti compresi. Le fixture con accenti e titoli duplicati sono l'oracolo che tiene ferma questa fedelta'.

Promozione di BL-001: il bersaglio di un link interno viene verificato anche come sezione, non solo come file. Le ancore vengono calcolate dai titoli del file bersaglio e confrontate col frammento; ancora mancante = nuovo tipo di errore nel report, exit code non-zero. Oracolo: suite di test (ancora valida passa, ancora mancante fallisce, link senza frammento invariati, regressione verde).
