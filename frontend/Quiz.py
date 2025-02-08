import os
import random
import pandas as pd
from streamlit_js_eval import streamlit_js_eval
import streamlit as st

# Set page centered
st.set_page_config(layout="wide")

# Cache the questions
@st.cache_data
def retrieve_questions():
    dfs = []
    for element in os.listdir('frontend/data'):
        df = pd.read_csv('frontend/data/' + element)
        
        # Filtro corretto
        filter_mask = (df['0'] != 'NUMERO ORDINE') & (df['1'] != 'ESITO') & (df['1'] != 'QUESITO') & (df['1'] != 'ELIMINATO')
        
        # Filtra le righe e seleziona le colonne
        df = df[filter_mask][['1', '2', '3', '4', '5']].sample(15)
        
        # Aggiungi la colonna 'Titolo'
        df['Titolo'] = element.split('.')[0]
        
        # Rinomina le colonne
        df.columns = ['Quesito', 'Risposta 1', 'Risposta 2', 'Risposta 3', 'Risposta 4', 'Titolo']
        
        # Aggiungi il dataframe alla lista
        dfs.append(df)

    # Unisci tutti i DataFrame in uno solo
    questions = pd.concat(dfs)

    return questions

def main():
    st.title("Simulazione Test di Diritto")
    st.write("Benvenuta/o! Espandi le categorie sottostanti per rispondere alle domande.")
    
    col1, col2 = st.columns([9, 1])  # Configura la larghezza delle colonne
    with col2:
        if st.button("Refresh Quiz 🔄"):
            st.cache_data.clear()
            streamlit_js_eval(js_expressions="parent.window.location.reload()")

    st.divider()
    df = retrieve_questions().reset_index()

    # Salva le risposte mescolate nella sessione
    if 'shuffled_answers' not in st.session_state:
        st.session_state['shuffled_answers'] = {
            index: random.sample(
                [row['Risposta 1'], row['Risposta 2'], row['Risposta 3'], row['Risposta 4']],
                4
            )
            for index, row in df.iterrows()
        }

    # Organizza il DataFrame per categoria
    categories = df['Titolo'].unique()

    # Dizionario per salvare le risposte degli utenti
    user_answers = {}
    correct_answers_by_category = {category: 0 for category in categories}  # Per categoria
    total_questions_by_category = {category: 0 for category in categories}  # Totali per categoria

    # Loop attraverso le categorie
    for category in categories:
        with st.expander(f"📚 Categoria: {category}", expanded=False):
            category_df = df[df['Titolo'] == category]
            total_questions_by_category[category] = len(category_df)

            # Loop attraverso i quesiti di questa categoria
            for index, row in category_df.iterrows():
                st.write(f"{index+1}. {row['Quesito']}")
                
                # Usa le risposte mescolate dalla sessione
                answers = st.session_state['shuffled_answers'][index]

                # Aggiungi radio buttons per selezionare una risposta
                user_answers[f"question_{index}"] = st.radio(
                    "Seleziona una risposta:",
                    options=answers,
                    index=None,  # Nessuna risposta selezionata di default
                    key=f"question_{index}"
                )

    if st.button("✔️ Submit Risposte"):
        correct_answers_total = 0  # Totale risposte corrette
        total_questions = len(df)  # Numero totale di domande
        wrong_questions_by_category = {category: [] for category in categories}  # Domande sbagliate per categoria

        # Verifica le risposte
        for index, row in df.iterrows():
            selected_answer = st.session_state.get(f"question_{index}")
            if selected_answer == row['Risposta 1']:
                correct_answers_total += 1
                correct_answers_by_category[row['Titolo']] += 1
            else:
                # Aggiungi alla lista delle domande sbagliate
                wrong_questions_by_category[row['Titolo']].append({
                    'Domanda': row['Quesito'],
                    'Risposta Corretta': row['Risposta 1'],
                    'Risposta Fornita': selected_answer
                })

        # Mostra i risultati
        st.write(f"### ✅ Totale Risposte Corrette: {correct_answers_total}/{total_questions}")
        st.write("### 📊 Risultati per Categoria:")
        for category in categories:
            correct = correct_answers_by_category[category]
            total = total_questions_by_category[category]
            st.write(f"- **{category}**: {correct}/{total} corrette")

        # Mostra le domande sbagliate in un menu richiudibile
        st.write("### ❌ Domande Sbagliate:")
        for category in categories:
            wrong_questions = wrong_questions_by_category[category]
            if wrong_questions:
                expander_title = f"🔍 {category} (Domande Sbagliate)"
                with st.expander(expander_title, expanded=False):
                    for question in wrong_questions:
                        st.divider()
                        st.caption(f"**Domanda**: {question['Domanda']}")
                        st.write(f"**Risposta Fornita**: {question['Risposta Fornita']}")
                        st.write(f"**Risposta Corretta**: {question['Risposta Corretta']}")

if __name__ == "__main__":
    main()
