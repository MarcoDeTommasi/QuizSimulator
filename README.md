# Simulazione Test di Diritto

Benvenuto/a nell'applicazione **Simulazione Test di Diritto**, un'app realizzata con **Streamlit** per generare e somministrare quiz personalizzati basati su categorie di domande di diritto. 

E' Disponibile un Depoly di questa app grazie a Streamlit Community al seguente url:
[Quiz Diritto](https://quizsimulator-test-001.streamlit.app/)

## Caratteristiche

- **Categorie personalizzate**: Le domande sono suddivise in categorie basate sui file CSV presenti nella cartella `data`.
- **Risposte mescolate casualmente**: Le opzioni di risposta sono mescolate in modo casuale per ogni domanda.
- **Riepilogo dettagliato**:
  - Totale delle risposte corrette.
  - Performance suddivisa per categoria.
  - Visualizzazione delle domande sbagliate con le risposte corrette e quelle fornite.
- **Refresh dinamico**: Genera un nuovo set di domande con il pulsante "Refresh Quiz 🔄".

---

## Installazione

Segui questi passaggi per eseguire l'applicazione in locale:

1. **Clona il repository**:
   ```bash
   git clone <URL_del_tuo_repository>
   cd <nome_cartella_repository>

2. **Crea un ambiente virtuale**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Su Windows: venv\Scripts\activate
3. **Installa le dipendenze**
    ```bash
    pip install -r requirements.txt
4. **Esegui l'app:**
    ```bash
    streamlit run Quiz.py

