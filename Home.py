import streamlit as st
import pandas as pd

def main():
    st.title("Seleziona le colonne di interesse")

    # Aggiungi input utente per il caricamento del file CSV
    uploaded_file = st.file_uploader("Carica il file CSV", type=["csv"])

    if uploaded_file is not None:
        try:
            # Carica il file CSV in un DataFrame con gestione dell'errore di decodifica Unicode
            df = pd.read_csv(uploaded_file, encoding='utf-8', error_bad_lines=False)
        except UnicodeDecodeError:
            df = pd.read_csv(uploaded_file, encoding='ISO-8859-1', error_bad_lines=False)

        # Mostra l'elenco delle colonne presenti nel file CSV
        st.write("Colonne disponibili:")
        st.write(df.columns)

        # Aggiungi input utente per selezionare le colonne da visualizzare
        selected_columns = st.multiselect("Seleziona le colonne da visualizzare", df.columns)

        if len(selected_columns) > 0:
            # Filtra il DataFrame per mantenere solo le colonne selezionate
            df_selected = df[selected_columns]

            # Mostra il DataFrame con le colonne selezionate
            st.write("Dati delle colonne selezionate:")
            st.write(df_selected)
        else:
            st.warning("Seleziona almeno una colonna da visualizzare.")
    else:
        st.warning("Carica un file CSV per iniziare.")

if __name__ == '__main__':
    main()


